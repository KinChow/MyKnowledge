---
archive_policy: text-only
attachments:
- filename: cortex-a76-deep-dive.html
  kind: document
  media_type: text/html
  role: original
  sha256: sha256:a84a55da6bded7231f8043c0c2c9bad6dcd1c899b2086b054275f4410ff8adc9
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-0b9e4d4f5b0c
  position:
    end: 2629
    start: 2518
    type: TextPositionSelector
  quote_sha256: sha256:428a35c161ea43a694f971c6e7187aa3be78b113d14271d3e87e8540f056828b
  selector:
    exact: moves over to a 4-instruction/cycle decode path rising to eight 16-bit
      instructions, up from three with the A75
    prefix: 'e pipeline.

      The Cortex-A76 also '
    suffix: ' and 2 with the A73. This means '
    type: TextQuoteSelector
  selector_sha256: sha256:e77851deaef25b484228b32c79abc2cc62394b679a39e9547aff6cfd3e2acda6
  snapshot_sha256: sha256:c9cd27101cb5da7a657a4deb4b8f3206c2d2ec030d1be9c853182ad0a2160cf9
- evidence_id: evidence-620cb82ae63b
  position:
    end: 3575
    start: 3505
    type: TextPositionSelector
  quote_sha256: sha256:b03f2e8f46dbb7e684bf437af4a7085a3dbafbe314eb8fc4a94a8d4beb7d2358
  selector:
    exact: the same 64KB, 4-way set associative L1 cache and 256-512KB private L2
    prefix: ' improvements here too.

      There’s '
    suffix: ' as before, but the decoupled ad'
    type: TextQuoteSelector
  selector_sha256: sha256:464f5bdf7cc58356da2c70f3781939b647cf8a75481c893482664cfe74c0564b
  snapshot_sha256: sha256:c9cd27101cb5da7a657a4deb4b8f3206c2d2ec030d1be9c853182ad0a2160cf9
- evidence_id: evidence-5649ac82db63
  position:
    end: 1684
    start: 1519
    type: TextPositionSelector
  quote_sha256: sha256:db6dbf5e12694c1fe8cf25e700559b04789cc839a1c8b7d93d01b1d2bbaef1a8
  selector:
    exact: paired up with two SIMD NEON execution pipelines, only one of which can
      handle floating-point divide and multiply-accumulate instructions. Both of these
      dual 128-bit
    prefix: 'st in Arm’s benchmarks.

      This is '
    suffix: ' pipes offer twice the bandwidth'
    type: TextQuoteSelector
  selector_sha256: sha256:be8189966814ccccc8f3f018f66fad1e0b0726ebe0603fc9ed98c1c7571b8e10
  snapshot_sha256: sha256:c9cd27101cb5da7a657a4deb4b8f3206c2d2ec030d1be9c853182ad0a2160cf9
extractor: trafilatura/2.2.0
id: cortex-a76-deep-dive
media_type: text/html
origin: external
raw_ref:
  path: archive/raw/a84a55da6bded7231f8043c0c2c9bad6dcd1c899b2086b054275f4410ff8adc9.html
  sha256: sha256:a84a55da6bded7231f8043c0c2c9bad6dcd1c899b2086b054275f4410ff8adc9
read_status: retrieved
retrieval:
  acquisition: fetch
  resolved_url: https://www.androidauthority.com/cortex-a76-deep-dive-870896/
  url: https://www.androidauthority.com/cortex-a76-deep-dive-870896/
schema_version: source/v1
snapshot_sha256: sha256:c9cd27101cb5da7a657a4deb4b8f3206c2d2ec030d1be9c853182ad0a2160cf9
source_type: doc
vault_id: public
---
Arm Cortex-A76 CPU deep dive
May 31, 2018 — 3:41 PM ET
Despite the minor change in digits to Arm’s latest CPU moniker, the latest processor design is a significant release for the company powering Android smartphones everywhere. The Cortex-A76 is a ground-up microarchitecture redesign which emphasizes improving peak performance and, perhaps more importantly, sustaining it in compact form factors. According to Arm this is just the first in a series of CPUs that will build off the A76 to push performance to new heights.
Arm’s Cortex-A76 is still compatible with existing processors, as well as the company’s DynamIQ CPU cluster technology. However, the micro-architecture redesign provides a 35 percent performance improvement over the Cortex-A75 on average, along with 40 percent improved power efficiency. The biggest wins are for floating point and machine learning math tasks, so let’s dive deeper into the new design to see what’s been changed.
Keep the core well fed
If there’s a general theme to understanding the changes with the Cortex-A76 it’s to “go wider,” boosting the CPU’s throughput to keep the more powerful execution core well fed with things to do.
In the execution core, the Cortex-A76 boasts two simple arithmetic locus units (ALUs) for basic math and bit-shifting, one multi-cycle integer and combined simple ALU to perform multiplication, and a branch unit. The Cortex-A75 just had one basic ALU and one ALU/MAC, which helps explain the integer performance boost in Arm’s benchmarks.
This is paired up with two SIMD NEON execution pipelines, only one of which can handle floating-point divide and multiply-accumulate instructions. Both of these dual 128-bit pipes offer twice the bandwidth of Arm’s prior CPUs for its single instruction multiple data extensions. Half-precision FP16 support remains from the A75, and this also has big benefits for boosting low precision INT8 dot product extensions, which are becoming increasingly popular in machine learning applications.
Another major change in the A76 is the new branch predictor, which is now decoupled from the instruction fetch. The branch predictor runs at twice the speed of the fetch at 32 versus 16 bytes per cycle. The main reason to do this is to expose lots of memory level parallelism — in other words, the potential to handle multiple memory operations seemingly at once. This is particularly handy for dealing with cache and TLB misses and helps to remove cycles where nothing happens from the pipeline.
The Cortex-A76 also moves over to a 4-instruction/cycle decode path rising to eight 16-bit instructions, up from three with the A75 and 2 with the A73. This means that the CPU core can now dispatch up to eight µops/cycle, instead of six with the A75 and four with the A73. Combined with eight issue queues, one of each of the execution units, and a 128-entry instruction window, Arm is further enhancing the processor’s ability to execute instructions out of order to boost the instructions per cycle (IPC) performance.
Going wider early in the design ensures high instruction throughput, which will keep the high-performance math units further down the pipe well fed, even during a cache miss. This is what’s helping Arm boost the IPC and math performance metrics, but it comes with a hit to area and energy.
Lower latency to memory
None of these fetch and execution improvements would be much good if the processor was bottlenecked by memory reads and writes, so Arm’s made improvements here too.
There’s the same 64KB, 4-way set associative L1 cache and 256-512KB private L2 as before, but the decoupled address generation and cache-lookup pipelines have received double the bandwidth. Memory level parallelism is a key target here as well, as the memory management unit can handle 68 in-flight loads, 72 in-flight stores, and 20 outstanding non-prefetch misses. The whole cache hierarchy has been optimized for latency too. It only takes four cycles to access the L1 cache, nine cycles to L2, and 31 cycles to go out to the L3 cache. The bottom line is memory access is faster, which will help to speed up execution.
The Cortex-A76 offers improved single core throughput, lower latency memory access, and sustained performance.
Speaking of the L3 cache, there’s support for up to 4MB of memory in the second generation DynamIQ shared unit. This huge memory pool will most likely be reserved for laptop class products through, as doubling the cache only produces roughly a 5 percent performance uplift. Smartphone products will likely cap out at a maximum of 2MB, owing to the lower performance point and tighter restrictions on silicon area and cost.
Achieving laptop-class performance (TLDR)
The Cortex-A76 is also the first CPU starting to transition away from 32-bit support. The A76 still supports Aarch32 but just at the lowest privilege application level (EL0). Meanwhile, Aarch64 is supported throughout, up to EL3 — from the OS through to low-level firmware. At some point in the future, it’s possible that Arm will transition over to solely 64-bit, but this will depend heavily on the ecosystem in question.
If all that seems like gobbledygook, here are the key things to understand. Generally speaking, a processor’s speed is dictated by how much it can do in a clock cycle. Being able to do two additions instead of one is better, so Arm added an extra math unit and increased the performance of its floating point (complex) math units.
The problem with this approach is you need to keep the execution units doing something or they waste power and silicon space, so you have to be able to issue more instructions to the units and faster than before. This produces further problems, such as increasing the likelihood that data isn’t where the processor thought it would be (cache miss), which stalls the whole system. Therefore you need to focus on better branch prediction and prefetching, as well as faster access to cache memory. Finally, all of this costs more silicon and power, so you have to optimize to keep those aspects under control, too.
Arm has focused on all of these aspects with the Cortex-A76, which is why there’s been such a big redesign, rather than just a small tweak to the A75. Combine all these IPC performance improvements with the expected move down to 7nm, and we’re looking at a notable 35 percent typical performance improvement over the already impressive Cortex-A75. The A76 does all this using only around half the power too, by running at a lower frequency to hit the same performance target.
The Cortex-A76 is Arm’s major play for higher performance computing with scalable use cases, ranging from mobile all the way up to laptops (and beyond) — all while supporting the power efficiency targets that have made the company so successful thus far. We’ll likely see the first chipsets sporting the A76 make their way into products in early 2019.