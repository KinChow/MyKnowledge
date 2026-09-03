---
archive_policy: text-only
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-878e7e0d7d13
  position:
    end: 122
    start: 28
    type: TextPositionSelector
  quote_sha256: sha256:410802f5f80f301c859e0bfbf8bbe9b84de6e432e14853d399afa161e1ea5a97
  selector:
    exact: 'LLVM has two vectorizers: The Loop Vectorizer, which operates on Loops,
      and the SLP Vectorizer'
    prefix: 'Auto-Vectorization in LLVM#

      '
    suffix: . These vectorizers focus on dif
    type: TextQuoteSelector
  selector_sha256: sha256:3a882fe29c2d1f94501ecbc19b83fdcafffa7919a1e81a4f161aa3ca86019e79
  snapshot_sha256: sha256:15bcdf01d39fc1f96f34f376b39642709ee6e2d06596424645a3aba001766aa1
- evidence_id: evidence-41839e947a4e
  position:
    end: 300
    start: 218
    type: TextPositionSelector
  quote_sha256: sha256:0f8207cc8675d49e29bac218fd3c7a72ba616378a12fe392110aafc50701b834
  selector:
    exact: The SLP vectorizer merges multiple scalars that are found in the code into
      vectors
    prefix: 's and use different techniques. '
    suffix: ' while the Loop Vectorizer widen'
    type: TextQuoteSelector
  selector_sha256: sha256:a4aa8b00ffb2d3e9cd70bb9710078ae7de55594658e5ea63da55e0ca1f573e6c
  snapshot_sha256: sha256:15bcdf01d39fc1f96f34f376b39642709ee6e2d06596424645a3aba001766aa1
- evidence_id: evidence-b37af9d946eb
  position:
    end: 996
    start: 900
    type: TextPositionSelector
  quote_sha256: sha256:41bb1e046b357bdcd20ec4a063a6cecf0ad0f03644bc9e2aa9a62f0d8aaaf904
  selector:
    exact: Users can control the vectorization SIMD width using the command line flag
      “-force-vector-width”
    prefix: ' ‘opt’ support the flags below.

      '
    suffix: '.

      $ clang  -mllvm -force-vector-'
    type: TextQuoteSelector
  selector_sha256: sha256:0d295febf581c44a754006fbd5b3fd5def932f8d1a7242cf22ed43fe955882da
  snapshot_sha256: sha256:15bcdf01d39fc1f96f34f376b39642709ee6e2d06596424645a3aba001766aa1
- evidence_id: evidence-f6d60969c183
  position:
    end: 474
    start: 403
    type: TextPositionSelector
  quote_sha256: sha256:24506c67d8ad870681cdc59fa321b6fada8188b9a8cb68c72ccc53b6e863191b
  selector:
    exact: Both the Loop Vectorizer and the SLP Vectorizer are enabled by default.
    prefix: 'ultiple consecutive iterations.

      '
    suffix: '

      The Loop Vectorizer#

      Usage#

      The'
    type: TextQuoteSelector
  selector_sha256: sha256:3c1aaf68853e4abdac882f2775c1668c77bb5bd99555a35cbc0c4639254c5412
  snapshot_sha256: sha256:15bcdf01d39fc1f96f34f376b39642709ee6e2d06596424645a3aba001766aa1
- evidence_id: evidence-acbdf3a5d0f7
  position:
    end: 611
    start: 503
    type: TextPositionSelector
  quote_sha256: sha256:e7afb4b9920fc22535a2607b3d0225fbead2850609bb492f47f4b1b145187ef6
  selector:
    exact: 'The Loop Vectorizer is enabled by default, but it can be disabled through
      clang using the command line flag:'
    prefix: 'lt.

      The Loop Vectorizer#

      Usage#

      '
    suffix: '

      $ clang ... -fno-vectorize  fil'
    type: TextQuoteSelector
  selector_sha256: sha256:1a9ab7e4f9909f0cc9dbbe8c89550747848c0767f96e6e1b39149b117ff1274b
  snapshot_sha256: sha256:15bcdf01d39fc1f96f34f376b39642709ee6e2d06596424645a3aba001766aa1
- evidence_id: evidence-0b6bd80cc315
  position:
    end: 1178
    start: 1088
    type: TextPositionSelector
  quote_sha256: sha256:aa5817a6e539aed1f3cdf0d87e40b381178f6b13d5ec1e2e1817a5b0e491b9e7
  selector:
    exact: Users can control the unroll factor using the command line flag “-force-vector-interleave”
    prefix: 'orize -force-vector-width=8 ...

      '
    suffix: '

      $ clang  -mllvm -force-vector-i'
    type: TextQuoteSelector
  selector_sha256: sha256:7a1328e9b5b98319d63ccddfd2c27c426990316572b140f70bc46eb6fd524311
  snapshot_sha256: sha256:15bcdf01d39fc1f96f34f376b39642709ee6e2d06596424645a3aba001766aa1
- evidence_id: evidence-fa72e0bfaddc
  position:
    end: 1460
    start: 1308
    type: TextPositionSelector
  quote_sha256: sha256:839be9c97daf469682fd41ba817cf73b741cfba0694496a7f22ddf6c493cbf61
  selector:
    exact: 'The #pragma clang loop directive allows loop vectorization hints to be

      specified for the subsequent for, while, do-while, or c++11 range-based for

      loop.'
    prefix: '..

      Pragma loop hint directives#

      '
    suffix: ' The directive allows vectorizat'
    type: TextQuoteSelector
  selector_sha256: sha256:18661e95b663485f7d33e680448252d9f464e990b962686ef1cf5c08ad61b204
  snapshot_sha256: sha256:15bcdf01d39fc1f96f34f376b39642709ee6e2d06596424645a3aba001766aa1
- evidence_id: evidence-03d1de17ae44
  position:
    end: 2436
    start: 2363
    type: TextPositionSelector
  quote_sha256: sha256:5f295b0a12b7eb66c4d414e765cc90929c76e14e890951f693ceaef1be8f0926
  selector:
    exact: -Rpass=loop-vectorize identifies loops that were successfully vectorized.
    prefix: 'tion remarks are enabled using:

      '
    suffix: '

      -Rpass-missed=loop-vectorize id'
    type: TextQuoteSelector
  selector_sha256: sha256:541452fe111971b40d5ddf3f8bd68ef75509a9735f64f955e99ebb7f5562f2a8
  snapshot_sha256: sha256:15bcdf01d39fc1f96f34f376b39642709ee6e2d06596424645a3aba001766aa1
- evidence_id: evidence-fdd7b1718c11
  position:
    end: 2508
    start: 2437
    type: TextPositionSelector
  quote_sha256: sha256:e9a2b2d488fa023996fc15e33d5df20cf8dcdfbf22733018b2fd4cc7545407db
  selector:
    exact: -Rpass-missed=loop-vectorize identifies loops that failed vectorization
    prefix: 't were successfully vectorized.

      '
    suffix: ' and

      indicates if vectorization '
    type: TextQuoteSelector
  selector_sha256: sha256:26ac2c8e4e28f917d09fed9df402b2d4423fbdcc1ce9b6af6ea0dfc1d4687b2c
  snapshot_sha256: sha256:15bcdf01d39fc1f96f34f376b39642709ee6e2d06596424645a3aba001766aa1
- evidence_id: evidence-83cd6b02e7df
  position:
    end: 3780
    start: 3718
    type: TextPositionSelector
  quote_sha256: sha256:646eabc6c7e2fdcf604bfafb73745949e315f46f04c37cf2f349316f3f2233d8
  selector:
    exact: The Loop Vectorizer supports loops with an unknown trip count.
    prefix: '

      Loops with unknown trip count#

      '
    suffix: '

      In the loop below, the iteratio'
    type: TextQuoteSelector
  selector_sha256: sha256:136422d614a4eb726271472ada1a4bf8b380d5b94c9546c5064544705be1e511
  snapshot_sha256: sha256:15bcdf01d39fc1f96f34f376b39642709ee6e2d06596424645a3aba001766aa1
- evidence_id: evidence-97b92953540f
  position:
    end: 8090
    start: 8030
    type: TextPositionSelector
  quote_sha256: sha256:293f99eb325e61189511a0fc732178fbfd6c81b82ae2f634dca066ef4dd7f30c
  selector:
    exact: The Loop Vectorizer can vectorize programs with mixed types.
    prefix: '.

      Vectorization of Mixed Types#

      '
    suffix: ' The Vectorizer cost model can e'
    type: TextQuoteSelector
  selector_sha256: sha256:6d22df9ed92e1532a2aebe8e09bfac6a0c5b51e4510bc668f24a56831bf6a19a
  snapshot_sha256: sha256:15bcdf01d39fc1f96f34f376b39642709ee6e2d06596424645a3aba001766aa1
- evidence_id: evidence-f6ff3239ca00
  position:
    end: 8876
    start: 8817
    type: TextPositionSelector
  quote_sha256: sha256:09cab6a2046fa2492daadc98f39d9941ae139a191c569fa6d952fdbf8d426cfe
  selector:
    exact: The Loop Vectorizer can vectorize intrinsic math functions.
    prefix: 'ectorization of function calls#

      '
    suffix: ' See the table below for a list '
    type: TextQuoteSelector
  selector_sha256: sha256:e2970bd5caeda7bb0747ae28e99fc619f39d8abe813b41d9bb588b39da9e3fef
  snapshot_sha256: sha256:15bcdf01d39fc1f96f34f376b39642709ee6e2d06596424645a3aba001766aa1
- evidence_id: evidence-eca4e264cf4d
  position:
    end: 9885
    start: 9704
    type: TextPositionSelector
  quote_sha256: sha256:95fb9b1a74f7ef6f9c6c7f648163127f86d4a193c1049d18b945043c131fe818
  selector:
    exact: 'Using clang, this is handled by the “-fveclib” command line option with
      one of the following vector libraries: “Accelerate,libmvec,MASSV,SVML,SLEEF,Darwin_libsystem_m,ArmPL,AMDLIBM”'
    prefix: 'entation of that math function. '
    suffix: '

      $ clang ... -fno-math-errno -fv'
    type: TextQuoteSelector
  selector_sha256: sha256:614e5176c176cdc834ddc9cbd279d6b725b0bc1ffd2de23e3e6e65df4986cd89
  snapshot_sha256: sha256:15bcdf01d39fc1f96f34f376b39642709ee6e2d06596424645a3aba001766aa1
- evidence_id: evidence-dc8a5899f4a1
  position:
    end: 10252
    start: 10141
    type: TextPositionSelector
  quote_sha256: sha256:8f71092c88edbf0570a8308e4d9ef6efeedada416d6617a9efe5991f16e27b83
  selector:
    exact: The Loop Vectorizer increases the instruction level parallelism (ILP) by
      performing partial-unrolling of loops.
    prefix: 'he entire width of the machine. '
    suffix: '

      In the example below the entire'
    type: TextQuoteSelector
  selector_sha256: sha256:34b31a255f473cf6c84e7fae333f56700a4e765c1312e8e953e8a50448d447c7
  snapshot_sha256: sha256:15bcdf01d39fc1f96f34f376b39642709ee6e2d06596424645a3aba001766aa1
- evidence_id: evidence-b73fecc37bed
  position:
    end: 14192
    start: 14085
    type: TextPositionSelector
  quote_sha256: sha256:851d1bb8c8a8282cb00ba0c288e9769531ad89b599ed35350a57a37ac67e6cf9
  selector:
    exact: 'The SLP Vectorizer is enabled by default, but it can be disabled through
      clang using the command line flag:'
    prefix: 'h of scalars to combine.

      Usage#

      '
    suffix: '

      $ clang -fno-slp-vectorize file'
    type: TextQuoteSelector
  selector_sha256: sha256:587079b78e6d14566d2824ef4d5763c475139deb310e8f68c237aff23b1da87d
  snapshot_sha256: sha256:15bcdf01d39fc1f96f34f376b39642709ee6e2d06596424645a3aba001766aa1
- evidence_id: evidence-1e8de6a08cea
  position:
    end: 13536
    start: 13397
    type: TextPositionSelector
  quote_sha256: sha256:9518acdfb5d6af47f30f0124246dd61f2fd20532685a99abe24c69e78f169de2
  selector:
    exact: The goal of SLP vectorization (a.k.a. superword-level parallelism) is to
      combine similar independent instructions into vector instructions.
    prefix: 'r.

      The SLP Vectorizer#

      Details#

      '
    suffix: ' Memory accesses, arithmetic ope'
    type: TextQuoteSelector
  selector_sha256: sha256:b8ab7d949f8fd050ec4b2fedebfb245a151b3de14bb864819ac8cb780f253715
  snapshot_sha256: sha256:15bcdf01d39fc1f96f34f376b39642709ee6e2d06596424645a3aba001766aa1
- evidence_id: evidence-0faa375b91ea
  position:
    end: 2646
    start: 2555
    type: TextPositionSelector
  quote_sha256: sha256:7c894f9050e8304e789f70b5ac15aca1117a52c8262e7f8497673dfae05cc85a
  selector:
    exact: '-Rpass-analysis=loop-vectorize identifies the statements that caused

      vectorization to fail.'
    prefix: 'if vectorization was specified.

      '
    suffix: ' If in addition -fsave-optimizat'
    type: TextQuoteSelector
  selector_sha256: sha256:5a63f29bbfe3a695aadbfe38862144c276c1ddd21a7e5337c481a43b8be28dfe
  snapshot_sha256: sha256:15bcdf01d39fc1f96f34f376b39642709ee6e2d06596424645a3aba001766aa1
extractor: trafilatura/2.2.0
id: llvm-auto-vectorization
media_type: text/html
origin: external
read_status: retrieved
retrieval:
  acquisition: fetch
  resolved_url: https://llvm.org/docs/Vectorizers.html
  url: https://llvm.org/docs/Vectorizers.html
schema_version: source/v1
snapshot_sha256: sha256:15bcdf01d39fc1f96f34f376b39642709ee6e2d06596424645a3aba001766aa1
source_type: doc
vault_id: public
---
Auto-Vectorization in LLVM#
LLVM has two vectorizers: The Loop Vectorizer, which operates on Loops, and the SLP Vectorizer. These vectorizers focus on different optimization opportunities and use different techniques. The SLP vectorizer merges multiple scalars that are found in the code into vectors while the Loop Vectorizer widens instructions in loops to operate on multiple consecutive iterations.
Both the Loop Vectorizer and the SLP Vectorizer are enabled by default.
The Loop Vectorizer#
Usage#
The Loop Vectorizer is enabled by default, but it can be disabled through clang using the command line flag:
$ clang ... -fno-vectorize  file.c
Command line flags#
The loop vectorizer uses a cost model to decide on the optimal vectorization factor and unroll factor. However, users of the vectorizer can force the vectorizer to use specific values. Both ‘clang’ and ‘opt’ support the flags below.
Users can control the vectorization SIMD width using the command line flag “-force-vector-width”.
$ clang  -mllvm -force-vector-width=8 ...
$ opt -loop-vectorize -force-vector-width=8 ...
Users can control the unroll factor using the command line flag “-force-vector-interleave”
$ clang  -mllvm -force-vector-interleave=2 ...
$ opt -loop-vectorize -force-vector-interleave=2 ...
Pragma loop hint directives#
The #pragma clang loop directive allows loop vectorization hints to be
specified for the subsequent for, while, do-while, or c++11 range-based for
loop. The directive allows vectorization and interleaving to be enabled or
disabled. Vector width as well as interleave count can also be manually
specified. The following example explicitly enables vectorization and
interleaving:
#pragma clang loop vectorize(enable) interleave(enable)
while(...) {
  ...
}
The following example implicitly enables vectorization and interleaving by specifying a vector width and interleaving count:
#pragma clang loop vectorize_width(2) interleave_count(2)
for(...) {
  ...
}
See the Clang language extensions for details.
Diagnostics#
Many loops cannot be vectorized including loops with complicated control flow, unvectorizable types, and unvectorizable calls. The loop vectorizer generates optimization remarks which can be queried using command line options to identify and diagnose loops that are skipped by the loop-vectorizer.
Optimization remarks are enabled using:
-Rpass=loop-vectorize identifies loops that were successfully vectorized.
-Rpass-missed=loop-vectorize identifies loops that failed vectorization and
indicates if vectorization was specified.
-Rpass-analysis=loop-vectorize identifies the statements that caused
vectorization to fail. If in addition -fsave-optimization-record is
provided, multiple causes of vectorization failure may be listed (this behavior
might change in the future).
Consider the following loop:
#pragma clang loop vectorize(enable)
for (int i = 0; i < Length; i++) {
  switch(A[i]) {
  case 0: A[i] = i*2; break;
  case 1: A[i] = i;   break;
  default: A[i] = 0;
  }
}
The command line -Rpass-missed=loop-vectorize prints the remark:
no_switch.cpp:4:5: remark: loop not vectorized: vectorization is explicitly enabled [-Rpass-missed=loop-vectorize]
And the command line -Rpass-analysis=loop-vectorize indicates that the
switch statement cannot be vectorized.
no_switch.cpp:4:5: remark: loop not vectorized: loop contains a switch statement [-Rpass-analysis=loop-vectorize]
  switch(A[i]) {
  ^
To ensure line and column numbers are produced include the command line options
-gline-tables-only and -gcolumn-info. See the Clang user manual
for details
Features#
The LLVM Loop Vectorizer has a number of features that allow it to vectorize complex loops.
Loops with unknown trip count#
The Loop Vectorizer supports loops with an unknown trip count.
In the loop below, the iteration start and finish points are unknown,
and the Loop Vectorizer has a mechanism to vectorize loops that do not start
at zero. In this example, ‘n’ may not be a multiple of the vector width, and
the vectorizer has to execute the last few iterations as scalar code. Keeping
a scalar copy of the loop increases the code size.
void bar(float *A, float* B, float K, int start, int end) {
  for (int i = start; i < end; ++i)
    A[i] *= B[i] + K;
}
Runtime Checks of Pointers#
In the example below, if the pointers A and B point to consecutive addresses, then it is illegal to vectorize the code because some elements of A will be written before they are read from array B.
Some programmers use the ‘restrict’ keyword to notify the compiler that the pointers are disjointed, but in our example, the Loop Vectorizer has no way of knowing that the pointers A and B are unique. The Loop Vectorizer handles this loop by placing code that checks, at runtime, if the arrays A and B point to disjointed memory locations. If arrays A and B overlap, then the scalar version of the loop is executed.
void bar(float *A, float* B, float K, int n) {
  for (int i = 0; i < n; ++i)
    A[i] *= B[i] + K;
}
Reductions#
In this example the sum variable is used by consecutive iterations of
the loop. Normally, this would prevent vectorization, but the vectorizer can
detect that ‘sum’ is a reduction variable. The variable ‘sum’ becomes a vector
of integers, and at the end of the loop the elements of the array are added
together to create the correct result. We support a number of different
reduction operations, such as addition, multiplication, XOR, AND and OR.
int foo(int *A, int n) {
  unsigned sum = 0;
  for (int i = 0; i < n; ++i)
    sum += A[i] + 5;
  return sum;
}
Fully vectorizing reductions requires reordering operations, which is problematic for floating-point arithmetic because it is not associative; therefore results may depend on the evaluation order.
Changing floating-point results is implicitly prohibited by the C and C++
standards, therefore LLVM supports vectorizing floating point reductions only
when at least the -fassociative-math -fno-signed-zeros -fno-trapping-math
subset of -ffast-math is used on most targets. On some targets, such as
AArch64 and RISC-V, LLVM can generate ordered reductions that preserve the
exact result, enabling limited, standards-compliant vectorization. However,
ordered reductions are typically less efficient than traditionally vectorized
reductions, therefore enabling floating-point reordering may still result in
more performant reductions on these targets.
Inductions#
In this example the value of the induction variable i is saved into an
array. The Loop Vectorizer knows to vectorize induction variables.
void bar(float *A, int n) {
  for (int i = 0; i < n; ++i)
    A[i] = i;
}
If Conversion#
The Loop Vectorizer is able to “flatten” the IF statement in the code and generate a single stream of instructions. The Loop Vectorizer supports any control flow in the innermost loop. The innermost loop may contain complex nesting of IFs, ELSEs and even GOTOs.
int foo(int *A, int *B, int n) {
  unsigned sum = 0;
  for (int i = 0; i < n; ++i)
    if (A[i] > B[i])
      sum += A[i] + 5;
  return sum;
}
Pointer Induction Variables#
This example uses the “accumulate” function of the standard c++ library. This loop uses C++ iterators, which are pointers, and not integer indices. The Loop Vectorizer detects pointer induction variables and can vectorize this loop. This feature is important because many C++ programs use iterators.
int baz(int *A, int n) {
  return std::accumulate(A, A + n, 0);
}
Reverse Iterators#
The Loop Vectorizer can vectorize loops that count backwards.
void foo(int *A, int n) {
  for (int i = n; i > 0; --i)
    A[i] +=1;
}
Scatter / Gather#
The Loop Vectorizer can vectorize code that becomes a sequence of scalar instructions that scatter/gathers memory.
void foo(int * A, int * B, int n) {
  for (intptr_t i = 0; i < n; ++i)
      A[i] += B[i * 4];
}
In many situations the cost model will inform LLVM that this is not beneficial and LLVM will only vectorize such code if forced with “-mllvm -force-vector-width=#”.
Vectorization of Mixed Types#
The Loop Vectorizer can vectorize programs with mixed types. The Vectorizer cost model can estimate the cost of the type conversion and decide if vectorization is profitable.
void foo(int *A, char *B, int n) {
  for (int i = 0; i < n; ++i)
    A[i] += 4 * B[i];
}
Global Structures Alias Analysis#
Access to global structures can also be vectorized, with alias analysis being used to make sure accesses don’t alias. Run-time checks can also be added on pointer access to structure members.
Many variations are supported, but some that rely on undefined behaviour being ignored (as other compilers do) are still being left un-vectorized.
struct { int A[100], K, B[100]; } Foo;
void foo() {
  for (int i = 0; i < 100; ++i)
    Foo.A[i] = Foo.B[i] + 100;
}
Vectorization of function calls#
The Loop Vectorizer can vectorize intrinsic math functions. See the table below for a list of these functions.
Note that the optimizer may not be able to vectorize math library functions that correspond to these intrinsics if the library calls access external state such as “errno”. To allow better optimization of C/C++ math library functions, use “-fno-math-errno”.
The loop vectorizer knows about special instructions on the target and will vectorize a loop containing a function call that maps to the instructions. For example, the loop below will be vectorized on Intel x86 if the SSE4.1 roundps instruction is available.
void foo(float *f) {
  for (int i = 0; i != 1024; ++i)
    f[i] = floorf(f[i]);
}
Many of these math functions are only vectorizable if the file has been built with a specified target vector library that provides a vector implementation of that math function. Using clang, this is handled by the “-fveclib” command line option with one of the following vector libraries: “Accelerate,libmvec,MASSV,SVML,SLEEF,Darwin_libsystem_m,ArmPL,AMDLIBM”
$ clang ... -fno-math-errno -fveclib=libmvec file.c
Partial unrolling during vectorization#
Modern processors feature multiple execution units, and only programs that contain a high degree of parallelism can fully utilize the entire width of the machine. The Loop Vectorizer increases the instruction level parallelism (ILP) by performing partial-unrolling of loops.
In the example below the entire array is accumulated into the variable ‘sum’. This is inefficient because only a single execution port can be used by the processor. By unrolling the code the Loop Vectorizer allows two or more execution ports to be used simultaneously.
int foo(int *A, int n) {
  unsigned sum = 0;
  for (int i = 0; i < n; ++i)
      sum += A[i];
  return sum;
}
The Loop Vectorizer uses a cost model to decide when it is profitable to unroll loops. The decision to unroll the loop depends on the register pressure and the generated code size.
Epilogue Vectorization#
When vectorizing a loop, often a scalar remainder (epilogue) loop is necessary to execute tail iterations of the loop if the loop trip count is unknown or it does not evenly divide the vectorization and unroll factors. When the vectorization and unroll factors are large, it’s possible for loops with smaller trip counts to end up spending most of their time in the scalar (rather than the vector) code. In order to address this issue, the inner loop vectorizer is enhanced with a feature that allows it to vectorize epilogue loops with a vectorization and unroll factor combination that makes it more likely for small trip count loops to still execute in vectorized code. The diagram below shows the CFG for a typical epilogue vectorized loop with runtime checks. As illustrated the control flow is structured in a way that avoids duplicating the runtime pointer checks and optimizes the path length for loops that have very small trip counts.
Early Exit Vectorization#
When vectorizing a loop with a single early exit, the loop blocks following the
early exit are predicated and the vector loop will always exit via the latch.
The loop terminates with a single BranchOnTwoConds VPInstruction, which takes
both the early and latch exiting conditions. If the early exiting condition is
true, BranchOnTwoConds exits to an intermediate block (vector.early.exit
below). This intermediate block is responsible for calculating any exit values
of loop-defined variables that are used in the early exit block. If the latch
exiting condition is true, BranchOnTwoConds exits to the middle.block which
selects between the exit block and the scalar remainder loop. Otherwise
BranchOnTwoConds continues executing the loop by jumping back to the region
header.
BranchOnTwoConds is lowered to a chain of conditional branches exiting the vector loop after dissolving loop regions:
Performance#
This section shows the execution time of Clang on a simple benchmark: gcc-loops. This benchmarks is a collection of loops from the GCC autovectorization page by Dorit Nuzman.
The chart below compares GCC-4.7, ICC-13, and Clang-SVN with and without loop vectorization at -O3, tuned for “corei7-avx”, running on a Sandybridge iMac. The Y-axis shows the time in msec. Lower is better. The last column shows the geomean of all the kernels.
And Linpack-pc with the same configuration. Result is Mflops, higher is better.
Ongoing Development Directions#
- Vectorization Plan
- Modeling the process and upgrading the infrastructure of LLVM’s Loop Vectorizer.
The SLP Vectorizer#
Details#
The goal of SLP vectorization (a.k.a. superword-level parallelism) is to combine similar independent instructions into vector instructions. Memory accesses, arithmetic operations, comparison operations, PHI-nodes, can all be vectorized using this technique.
For example, the following function performs very similar operations on its inputs (a1, b1) and (a2, b2). The basic-block vectorizer may combine these into vector operations.
void foo(int a1, int a2, int b1, int b2, int *A) {
  A[0] = a1*(a1 + b1);
  A[1] = a2*(a2 + b2);
  A[2] = a1*(a1 + b1);
  A[3] = a2*(a2 + b2);
}
The SLP-vectorizer processes the code bottom-up, across basic blocks, in search of scalars to combine.
Usage#
The SLP Vectorizer is enabled by default, but it can be disabled through clang using the command line flag:
$ clang -fno-slp-vectorize file.c
The Sandbox Vectorizer#
The Sandbox Vectorizer is an experimental framework for building modular vectorization pipelines on top of Sandbox IR, with a focus on ease of testing and ease of development.