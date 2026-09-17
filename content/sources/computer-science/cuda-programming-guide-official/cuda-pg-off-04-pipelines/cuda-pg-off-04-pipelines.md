---
archive_policy: text-only
attachments:
- filename: cuda-pg-off-04-pipelines.html
  kind: document
  media_type: text/html
  role: original
  sha256: sha256:2046887e8611bef7c97fcd00d6527cf4a2e6f4ead9835116ca1993a9b1d6d2c8
confidentiality: public
domain: computer-science
extractor: trafilatura/2.2.0
id: cuda-pg-off-04-pipelines
media_type: text/html
origin: external
raw_ref:
  path: archive/raw/2046887e8611bef7c97fcd00d6527cf4a2e6f4ead9835116ca1993a9b1d6d2c8.html
  sha256: sha256:2046887e8611bef7c97fcd00d6527cf4a2e6f4ead9835116ca1993a9b1d6d2c8
read_status: retrieved
retrieval:
  acquisition: fetch
  resolved_url: https://docs.nvidia.com/cuda/cuda-programming-guide/04-special-topics/pipelines.html
  url: https://docs.nvidia.com/cuda/cuda-programming-guide/04-special-topics/pipelines.html
schema_version: source/v1
snapshot_sha256: sha256:9a7df655e8f4aa10bec981549d67b214f80011f42a7a349c1778fab83020bf78
source_type: doc
vault_id: public
---
4.11. Pipelines#
Pipelines, introduced in Advanced Synchronization Primitives, are a mechanism for staging work and coordinating multi-buffer producer–consumer patterns, commonly used to overlap compute with asynchronous data copies.
This section provides details on how to use pipelines mainly via the cuda::pipeline API (with pointers to primitives where applicable).
4.11.1. Initialization#
A cuda::pipeline can be created at different thread scopes. For a scope other than cuda::thread_scope_thread, a cuda::pipeline_shared_state<scope, count> object is required to coordinate the participating threads. This state encapsulates the finite resources that allow a pipeline to process up to count concurrent stages.
// Create a pipeline at thread scope
constexpr auto scope = cuda::thread_scope_thread;
cuda::pipeline<scope> pipeline = cuda::make_pipeline();
// Create a pipeline at block scope
constexpr auto scope = cuda::thread_scope_block;
constexpr auto stages_count = 2;
__shared__ cuda::pipeline_shared_state<scope, stages_count> shared_state;
auto pipeline = cuda::make_pipeline(group, &shared_state);
Pipelines can be either unified or partitioned. In a unified pipeline, all the participating threads are both producers and consumers. In a partitioned pipeline, each participating thread is either a producer or a consumer and its role cannot change during the lifetime of the pipeline object. A thread-local pipeline cannot be partitioned. To create a partitioned pipeline, we need to provide either the number of producers or the role of the thread to cuda::make_pipeline().
// Create a partitioned pipeline at block scope where only thread 0 is a producer
constexpr auto scope = cuda::thread_scope_block;
constexpr auto stages_count = 2;
__shared__ cuda::pipeline_shared_state<scope, stages_count> shared_state;
auto thread_role = (group.thread_rank() == 0) ? cuda::pipeline_role::producer : cuda::pipeline_role::consumer;
auto pipeline = cuda::make_pipeline(group, &shared_state, thread_role);
To support partitioning, a shared cuda::pipeline incurs additional overheads, including using a set of shared memory barriers per stage for synchronization. These are used even when the pipeline is unified and could use __syncthreads() instead. Thus, it is preferable to use thread-local pipelines which avoid these overheads when possible.
4.11.2. Submitting Work#
Committing work to a pipeline stage involves:
Collectively acquiring the pipeline head from a set of producer threads using pipeline.producer_acquire().
Submitting asynchronous operations, e.g., memcpy_async, to the pipeline head.
Collectively committing (advancing) the pipeline head using pipeline.producer_commit().
If all resources are in use, pipeline.producer_acquire() blocks producer threads until the resources of the next pipeline stage are released by consumer threads.
4.11.3. Consuming Work#
Consuming work from a previously committed stage involves:
Collectively waiting for the stage to complete, e.g., using pipeline.consumer_wait() to wait on the tail (oldest) stage, from a set of consumer threads.
Collectively releasing the stage using pipeline.consumer_release().
With cuda::pipeline<cuda:thread_scope_thread> one can also use the cuda::pipeline_consumer_wait_prior<N>() friend function to wait for all except the last N stages to complete, similar to __pipeline_wait_prior(N) in the primitives API.
4.11.4. Warp Entanglement#
The pipeline mechanism is shared among CUDA threads in the same warp. This sharing causes sequences of submitted operations to be entangled within a warp, which can impact performance under certain circumstances.
Commit. The commit operation is coalesced such that the pipeline’s sequence is incremented once for all converged threads that invoke the commit operation and their submitted operations are batched together. If the warp is fully converged, the sequence is incremented by one and all submitted operations will be batched in the same stage of the pipeline; if the warp is fully diverged, the sequence is incremented by 32 and all submitted operations will be spread to different stages.
- Let PB be the warp-shared pipeline’s actual sequence of operations. PB = {BP0, BP1, BP2, …, BPL}
- Let TB be a thread’s perceived sequence of operations, as if the sequence were only incremented by this thread’s invocation of the commit operation. TB = {BT0, BT1, BT2, …, BTL}
The pipeline::producer_commit() return value is from the thread’s perceived batch sequence.
- An index in a thread’s perceived sequence always aligns to an equal or larger index in the actual warp-shared sequence. The sequences are equal only when all commit operations are invoked from fully converged threads. BTn ≡ BPm wheren <= m
For example, when a warp is fully diverged:
- The warp-shared pipeline’s actual sequence would be: PB = {0, 1, 2, 3, ..., 31} (PL=31 ).
- The perceived sequence for each thread of this warp would be: 
  - Thread 0: TB = {0} (TL=0 )
  - Thread 1: TB = {0} (TL=0 )
  - …
  - Thread 31: TB = {0} (TL=0 )
Wait. A CUDA thread invokes pipeline::consumer_wait() or pipeline_consumer_wait_prior<N>() to wait for batches in the perceived sequence TB to complete. Note that pipeline::consumer_wait() is equivalent to pipeline_consumer_wait_prior<N>(), where N = PL.
The wait prior variants wait for batches in the actual sequence at least up to and including PL-N. Since TL <= PL, waiting for batch up to and including PL-N includes waiting for batch TL-N. Thus, when TL < PL, the thread will unintentionally wait for additional, more recent batches. In the extreme fully-diverged warp example above, each thread could wait for all 32 batches.
Note
It is recommended that commit invocations are by converged threads to not over-wait, by keeping threads’ perceived sequence of batches aligned with the actual sequence.
When code preceding these operations diverges threads, then the warp should be re-converged, via __syncwarp before invoking commit operations.
4.11.5. Early Exit#
When a thread that is participating in a pipeline must exit early, that thread must explicitly drop out of participation before exiting using cuda::pipeline::quit(). The remaining participating threads can proceed normally with subsequent operations.
4.11.6. Tracking Asynchronous Memory Operations#
The following example demonstrates how to collectively copy data from global to shared memory with asynchronous memory copies using a pipeline to keep track of the copy operations. Each thread uses its own pipeline to independently submit memory copies and then wait for them to complete and consume the data. For more details on asynchronous data copies, see Section 3.2.5.
4.11.7. Producer-Consumer Pattern using Pipelines#
In Section 4.10.7, we showed how a thread block can be spatially partitioned to implement a producer-consumer pattern using asynchronous barriers. With cuda::pipeline, this can be simplified using a single partitioned pipeline with one stage per data buffer instead of two asynchronous barriers per buffer.
In this example, we use half of the threads in the thread block as producers and the other half as consumers. As a first step, we need to create a cuda::pipeline object. Since we want some threads to be producers and some to be consumers, we need to use a partitioned pipeline with cuda::thread_scope_block. Partitioned pipelines require a cuda::pipeline_shared_state to coordinate the participating threads. We initialize the state for a 2-stage pipeline in thread-block scope and then call cuda::make_pipeline(). Next, producer threads fill the pipeline by submitting asynchronous copies from in to buffer. At this point all data copies are in-flight. Finally, in the main loop, we go over all of the batches of data and depending on whether a thread is a producer or consumer, we either submit another asynchronous copy for a future batch or consume the current batch.