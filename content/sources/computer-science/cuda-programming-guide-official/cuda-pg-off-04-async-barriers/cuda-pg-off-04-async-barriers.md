---
archive_policy: text-only
attachments:
- filename: cuda-pg-off-04-async-barriers.html
  kind: document
  media_type: text/html
  role: original
  sha256: sha256:79181f295d62e0494afe349ede85d6668d8b4933b70751746b1fb473a8b3eaa3
confidentiality: public
domain: computer-science
extractor: trafilatura/2.2.0
id: cuda-pg-off-04-async-barriers
media_type: text/html
origin: external
raw_ref:
  path: archive/raw/79181f295d62e0494afe349ede85d6668d8b4933b70751746b1fb473a8b3eaa3.html
  sha256: sha256:79181f295d62e0494afe349ede85d6668d8b4933b70751746b1fb473a8b3eaa3
read_status: retrieved
retrieval:
  acquisition: fetch
  resolved_url: https://docs.nvidia.com/cuda/cuda-programming-guide/04-special-topics/async-barriers.html
  url: https://docs.nvidia.com/cuda/cuda-programming-guide/04-special-topics/async-barriers.html
schema_version: source/v1
snapshot_sha256: sha256:0e183638c9d094073f587afc15e078211ea344d5e8e0e1633ed3019d4456ef26
source_type: doc
vault_id: public
---
4.10. Asynchronous Barriers#
Asynchronous barriers, introduced in Advanced Synchronization Primitives, extend CUDA synchronization beyond __syncthreads() and __syncwarp(), enabling fine-grained, non-blocking coordination and better overlap of communication and computation.
This section provides details on how to use asynchronous barriers mainly via the cuda::barrier API (with pointers to cuda::ptx and primitives where applicable).
4.10.1. Initialization#
Initialization must happen before any thread begins participating in a barrier.
Before any thread can participate in a barrier, the barrier must be initialized using the cuda::barrier::init() friend function. This must happen before any thread arrives on the barrier. This poses a bootstrapping challenge in that threads must synchronize before participating in the barrier, but threads are creating a barrier in order to synchronize. In this example, threads that will participate are part of a cooperative group and use block.sync() to bootstrap initialization. Since a whole thread block is participating in the barrier, __syncthreads() could also be used.
The second parameter of init() is the expected arrival count, i.e., the number of times bar.arrive() will be called by participating threads before a participating thread is unblocked from its call to bar.wait(std::move(token)). In this and the previous examples, the barrier is initialized with the number of threads in the thread block i.e., cooperative_groups::this_thread_block().size(), so that all threads within the thread block can participate in the barrier.
Asynchronous barriers are flexible in specifying how threads participate (split arrive/wait) and which threads participate. In contrast, this_thread_block.sync() or __syncthreads() is applicable to the whole thread-block and __syncwarp(mask) to a specified subset of a warp. Nonetheless, if the intention of the user is to synchronize a full thread block or a full warp, we recommend using __syncthreads() and __syncwarp() respectively for better performance.
4.10.2. A Barrier’s Phase: Arrival, Countdown, Completion, and Reset#
An asynchronous barrier counts down from the expected arrival count to zero as participating threads call bar.arrive(). When the countdown reaches zero, the barrier is complete for the current phase. When the last call to bar.arrive() causes the countdown to reach zero, the countdown is automatically and atomically reset. The reset assigns the countdown to the expected arrival count, and moves the barrier to the next phase.
A token object of class cuda::barrier::arrival_token, as returned from token=bar.arrive(), is associated with the current phase of the barrier. A call to bar.wait(std::move(token)) blocks the calling thread while the barrier is in the current phase, i.e., while the phase associated with the token matches the phase of the barrier. If the phase is advanced (because the countdown reaches zero) before the call to bar.wait(std::move(token)) then the thread does not block; if the phase is advanced while the thread is blocked in bar.wait(std::move(token)), the thread is unblocked.
It is essential to know when a reset could or could not occur, especially in non-trivial arrive/wait synchronization patterns.
- A thread’s calls to token=bar.arrive() andbar.wait(std::move(token)) must be sequenced such thattoken=bar.arrive() occurs during the barrier’s current phase, andbar.wait(std::move(token)) occurs during the same or next phase.
- A thread’s call to bar.arrive() must occur when the barrier’s counter is non-zero. After barrier initialization, if a thread’s call tobar.arrive() causes the countdown to reach zero then a call tobar.wait(std::move(token)) must happen before the barrier can be reused for a subsequent call tobar.arrive() .
- bar.wait() must only be called using atoken object of the current phase or the immediately preceding phase. For any other values of thetoken object, the behavior is undefined.
For simple arrive/wait synchronization patterns, compliance with these usage rules is straightforward.
4.10.2.1. Warp Entanglement#
Warp-divergence affects the number of times an arrive on operation updates the barrier. If the invoking warp is fully converged, then the barrier is updated once. If the invoking warp is fully diverged, then 32 individual updates are applied to the barrier.
Note
It is recommended that arrive-on(bar) invocations are used by converged threads to minimize updates to the barrier object. When code preceding these operations diverges threads, then the warp should be re-converged, via __syncwarp before invoking arrive-on operations.
4.10.3. Explicit Phase Tracking#
An asynchronous barrier can have multiple phases depending on how many times it is used to synchronize threads and memory operations. Instead of using tokens to track barrier phase flips, we can directly track a phase using the mbarrier_try_wait_parity() family of functions available through the cuda::ptx and primitives APIs.
In its simplest form, the cuda::ptx::mbarrier_try_wait_parity(uint64_t* bar, const uint32_t& phaseParity) function waits for a phase with a particular parity. The phaseParity operand is the integer parity of either the current phase or the immediately preceding phase of the barrier object. An even phase has integer parity 0 and an odd phase has integer parity 1. When we initialize a barrier, its phase has parity 0. So the valid values of phaseParity are 0 and 1. Explicit phase tracking can be useful when tracking asynchronous memory operations, as it allows only a single thread to arrive on the barrier and set the transaction count, while other threads only wait for a parity-based phase flip. This can be more efficient than having all threads arrive on the barrier and use tokens. This functionality is only available for shared-memory barriers at thread-block and cluster scope.
4.10.4. Early Exit#
When a thread that is participating in a sequence of synchronizations must exit early from that sequence, that thread must explicitly drop out of participation before exiting. The remaining participating threads can proceed normally with subsequent arrive and wait operations.
The bar.arrive_and_drop() operation arrives on the barrier to fulfill the participating thread’s obligation to arrive in the current phase, and then decrements the expected arrival count for the next phase so that this thread is no longer expected to arrive on the barrier.
4.10.5. Completion Function#
The cuda::barrier API supports an optional completion function. A CompletionFunction of cuda::barrier<Scope, CompletionFunction> is executed once per phase, after the last thread arrives and before any thread is unblocked from the wait. Memory operations performed by the threads that arrived at the barrier during the phase are visible to the thread executing the CompletionFunction, and all memory operations performed within the CompletionFunction are visible to all threads waiting at the barrier once they are unblocked from the wait.
4.10.6. Tracking Asynchronous Memory Operations#
Asynchronous barriers can be used to track asynchronous memory copies. When an asynchronous copy operation is bound to a barrier, the copy operation automatically increments the expected count of the current barrier phase upon initiation and decrements it upon completion. This mechanism ensures that the barrier’s wait() operation will block until all associated asynchronous memory copies have completed, providing a convenient way to synchronize multiple concurrent memory operations.
Starting with compute capability 9.0, asynchronous barriers in shared memory with thread-block or cluster scope can explicitly track asynchronous memory operations. We refer to these barriers as asynchronous transaction barriers. In addition to the expected arrival count, a barrier object can accept a transaction count, which can be used for tracking the completion of asynchronous transactions. The transaction count tracks the number of asynchronous transactions that are outstanding and yet to be complete, in units specified by the asynchronous memory operation (typically bytes). The transaction count to be tracked by the current phase can be set on arrival with cuda::device::barrier_arrive_tx() or directly with cuda::device::barrier_expect_tx(). When a barrier uses a transaction count, it blocks threads at the wait operation until all the producer threads have performed an arrive and the sum of all the transaction counts reaches an expected value.
In this example, the cuda::device::barrier_arrive_tx() operation constructs an arrival token object associated with the phase synchronization point for the current phase. Then, decrements the arrival count by 1 and increments the expected transaction count by 0. Since the transaction count update is 0, the barrier is not tracking any transactions. The subsequent section on Using the Tensor Memory Accelerator (TMA) includes examples of tracking asynchronous memory operations.
4.10.7. Producer-Consumer Pattern Using Barriers#
A thread block can be spatially partitioned to allow different threads to perform independent operations. This is most commonly done by assigning threads from different warps within the thread block to specific tasks. This technique is referred to as warp specialization.
This section shows an example of spatial partitioning in a producer-consumer pattern, where one subset of threads produces data that is concurrently consumed by the other (disjoint) subset of threads. A producer-consumer spatial partitioning pattern requires two one-sided synchronizations to manage a data buffer between the producer and consumer.
Producer threads wait for consumer threads to signal that the buffer is ready to be filled; however, consumer threads do not wait for this signal. Consumer threads wait for producer threads to signal that the buffer is filled; however, producer threads do not wait for this signal. For full producer/consumer concurrency this pattern has (at least) double buffering where each buffer requires two barriers.
In this example, the first warp is specialized as the producer and the remaining warps are specialized as consumers. All producer and consumer threads participate (call bar.arrive() or bar.arrive_and_wait()) in each of the four barriers so the expected arrival counts are equal to block.size().
A producer thread waits for the consumer threads to signal that the shared memory buffer can be filled. In order to wait for a barrier, a producer thread must first arrive on that ready[i%2].arrive() to get a token and then ready[i%2].wait(token) with that token. For simplicity, ready[i%2].arrive_and_wait() combines these operations.
bar.arrive_and_wait();
/* is equivalent to */
bar.wait(bar.arrive());
Producer threads compute and fill the ready buffer, they then signal that the buffer is filled by arriving on the filled barrier, filled[i%2].arrive(). A producer thread does not wait at this point, instead it waits until the next iteration’s buffer (double buffering) is ready to be filled.
A consumer thread begins by signaling that both buffers are ready to be filled. A consumer thread does not wait at this point, instead it waits for this iteration’s buffer to be filled, filled[i%2].arrive_and_wait(). After the consumer threads consume the buffer they signal that the buffer is ready to be filled again, ready[i%2].arrive(), and then wait for the next iteration’s buffer to be filled.