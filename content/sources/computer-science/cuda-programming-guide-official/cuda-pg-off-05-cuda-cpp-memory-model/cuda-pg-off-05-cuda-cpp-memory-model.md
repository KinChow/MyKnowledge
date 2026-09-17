---
archive_policy: text-only
attachments:
- filename: cuda-pg-off-05-cuda-cpp-memory-model.html
  kind: document
  media_type: text/html
  role: original
  sha256: sha256:1787e8fd42032ecbeb36441364db57dd6379eee5f459e188221163ab2e984d86
confidentiality: public
domain: computer-science
extractor: trafilatura/2.2.0
id: cuda-pg-off-05-cuda-cpp-memory-model
media_type: text/html
origin: external
raw_ref:
  path: archive/raw/1787e8fd42032ecbeb36441364db57dd6379eee5f459e188221163ab2e984d86.html
  sha256: sha256:1787e8fd42032ecbeb36441364db57dd6379eee5f459e188221163ab2e984d86
read_status: retrieved
retrieval:
  acquisition: fetch
  resolved_url: https://docs.nvidia.com/cuda/cuda-programming-guide/05-appendices/cuda-cpp-memory-model.html
  url: https://docs.nvidia.com/cuda/cuda-programming-guide/05-appendices/cuda-cpp-memory-model.html
schema_version: source/v1
snapshot_sha256: sha256:d8115cbcd91cc0fb873792148e1aaaecda91221f52f55b032d44db8d8af7f879
source_type: doc
vault_id: public
---
5.7. CUDA C++ Memory Model#
Standard C++ presents a view that the cost to synchronize threads is uniform and low.
CUDA C++ is different: the cost to synchronize threads grows as threads are further apart. It is low across threads within a block, but high across arbitrary threads in the system running on multiple GPUs and CPUs.
To account for non-uniform thread synchronization costs that are not always low, CUDA C++ extends the standard C++
memory model and concurrency facilities in the cuda:: namespace with thread scopes, retaining the syntax and
semantics of standard C++ by default.
5.7.1. Thread Scopes#
A thread scope specifies the kind of threads that can synchronize with each other using a synchronization primitive such as cuda::atomic or cuda::barrier.
namespace cuda {
enum thread_scope {
  thread_scope_system,
  thread_scope_device,
  thread_scope_block,
  thread_scope_thread
};
}  // namespace cuda
5.7.1.1. Scope Relationships#
- Each program thread is related to each other program thread by one or more thread scope relations:
  - Each thread in the system is related to each other thread in the system by the system thread scope: cuda::thread_scope_system .
  - Each GPU thread is related to each other GPU thread in the same CUDA device and within the same memory synchronization domain by the device thread scope: cuda::thread_scope_device .
  - Each GPU thread is related to each other GPU thread in the same CUDA thread block by the block thread scope: cuda::thread_scope_block .
  - Each thread is related to itself by the thread thread scope: cuda::thread_scope_thread .
5.7.2. Synchronization primitives#
Types in namespaces std:: and cuda::std:: have the same behavior as corresponding types in namespace cuda::
when instantiated with a scope of cuda::thread_scope_system.
5.7.3. Atomicity#
An atomic operation is atomic at the scope it specifies if:
- it specifies a scope other than cuda::thread_scope_system , or
- the scope is cuda::thread_scope_system and:
  - it affects an object in system allocated memory and pageableMemoryAccess is 1 [0,1],  or
  - it affects an object in managed memory and concurrentManagedAccess is 1 [1], or
  - it affects an object in mapped memory and hostNativeAtomicSupported is 1 , or
  - it is a load or store that affects a naturally-aligned object of sizes 1 ,2 ,4 ,8 , or16 bytes on mapped memory [2], or
  - it affects an object in GPU memory, only GPU threads access it, and 
    - cudaDeviceGetP2PAttribute (&val, cudaDevP2PAttrNativeAtomicSupported, srcDev, dstDev) between each accessingsrcDev and the GPU where the object resides,dstDev , is1 [1], or
    - only GPU threads from a single GPU concurrently access it.
Note
- [0] If PageableMemoryAccessUsesHostPagetables is 0 then atomic operations to memory mapped file orhugetlbfs allocations are not atomic.
- [1] System-scope tensor reduction operations are only atomic at system-scope in these cases if hostNativeAtomicSupported is 1 .
System-scope tensor reduction operations include PTX{multimem.}cp.reduce.async.bulk.tensor.relaxed.sys instruction families and APIs that expose them like, e.g.,cuda::ptx::cp_reduce_async_bulk_tensor .
- [2] If hostNativeAtomicSupported is 0 , atomic load or store operations at system scope that affect a
naturally-aligned 16-byte wide object in system allocated memory or mapped memory require system
support. NVIDIA is not aware of any system that lacks this support and there is no CUDA API query available to
detect such systems.
For more information on system allocated memory, managed memory, mapped memory, CPU memory, and GPU memory, see the relevant sections of this guide.
5.7.4. Data Races#
Modify intro.races paragraph 21 of ISO/IEC IS 14882 (the C++ Standard) as follows:
The execution of a program contains a data race if it contains two potentially concurrent conflicting actions, at least one of which is not atomic at a scope that includes the thread that performed the other operation, and neither happens before the other, except for the special case for signal handlers described below. Any such data race results in undefined behavior. […]
Modify thread.barrier.class paragraph 4 of ISO/IEC IS 14882 (the C++ Standard) as follows
4. Concurrent invocations of the member functions of barrier, other than its destructor, do not introduce data
races as if they were atomic operations. […]
Modify thread.latch.class paragraph 2 of ISO/IEC IS 14882 (the C++ Standard) as follows:
2. Concurrent invocations of the member functions of latch, other than its destructor, do not introduce data
races as if they were atomic operations. […]
Modify thread.sema.cnt paragraph 3 of ISO/IEC IS 14882 (the C++ Standard) as follows:
3. Concurrent invocations of the member functions of counting_semaphore, other than its destructor, do not
introduce data races as if they were atomic operations.
Modify thread.stoptoken.intro paragraph 5 of ISO/IEC IS 14882 (the C++ Standard) as follows:
Calls to the functions request_stop, stop_requested, and stop_possible do not introduce data
races as if they were atomic operations. […]
Modify atomics.fences paragraph 2 through 4 of ISO/IEC IS 14882 (the C++ Standard) as follows:
A release fence A synchronizes with an acquire fence B if there exist atomic operations X and Y, both operating on some atomic object M, such that A is sequenced before X, X modifies M, Y is sequenced before B, and Y reads the value written by X or a value written by any side effect in the hypothetical release sequence X would head if it were a release operation, and each operation (A, B, X, and Y) specifies a scope that includes the thread that performed each other operation.
A release fence A synchronizes with an atomic operation B that performs an acquire operation on an atomic object M if there exists an atomic operation X such that A is sequenced before X, X modifies M, and B reads the value written by X or a value written by any side effect in the hypothetical release sequence X would head if it were a release operation, and each operation (A, B, and X) specifies a scope that includes the thread that performed each other operation.
An atomic operation A that is a release operation on an atomic object M synchronizes with an acquire fence B if there exists some atomic operation X on M such that X is sequenced before B and reads the value written by A or a value written by any side effect in the release sequence headed by A, and each operation (A, B, and X) specifies a scope that includes the thread that performed each other operation.
5.7.5. Example: Message Passing#
The following example passes a message stored to the x variable by a
thread in block 0 to a thread in block 1 via the flag f:
In the following variation of the previous example, two threads
concurrently access the f object without synchronization, which
leads to a data race, and exhibits undefined behavior:
While the memory operations on f - the store and the loads - are
atomic, the scope of the store operation is “block scope”. Since the
store is performed by Thread 0 of Block 0, it only includes all other
threads of Block 0. However, the thread doing the loads is in Block 1,
i.e., it is not in a scope included by the store operation performed in
Block 0, causing the store and the load to not be “atomic”, and
introducing a data-race.
For more examples see the PTX memory consistency model litmus tests.