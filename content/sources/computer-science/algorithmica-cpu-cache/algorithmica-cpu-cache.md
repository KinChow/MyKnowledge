---
archive_policy: text-only
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-9b7a55f92851
  position:
    end: 658
    start: 504
    type: TextPositionSelector
  quote_sha256: sha256:3b58861a370927569c3dbd0589eeb009ce579a4ff27bf52dc733967619f2bee9
  selector:
    exact: To perform more fine-grained optimization of in-memory algorithms, we have
      to start taking into account the many specific details of the CPU cache system.
    prefix: 'e operations become comparable.

      '
    suffix: ' And instead of studying loads o'
    type: TextQuoteSelector
  selector_sha256: sha256:fb25848e3625ed50a8c6c13a20468c2f4c1fbfdb7564885d5cc2ac9ea3451a93
  snapshot_sha256: sha256:d51a32369b41d5409972d53eac29ea4886c21f5783a95a707e058225d711ff8f
- evidence_id: evidence-44856c2dbd94
  position:
    end: 1704
    start: 1633
    type: TextPositionSelector
  quote_sha256: sha256:8364aa44b3c1b1cc5ffe7350bd4af4f9d20a24bd1caa8cb2bf1fe81ba5330b99
  selector:
    exact: Not all conclusions will generalize to every CPU platform in existence.
    prefix: ' the CPU on WikiChip and 7-CPU. '
    suffix: '

      Due to difficulties in preventi'
    type: TextQuoteSelector
  selector_sha256: sha256:29d1d7a5b28fa1278a102a0f3b29c9efccc11f44075da306829f4e399f465856
  snapshot_sha256: sha256:d51a32369b41d5409972d53eac29ea4886c21f5783a95a707e058225d711ff8f
extractor: trafilatura/2.2.0
id: algorithmica-cpu-cache
media_type: text/html
origin: external
read_status: retrieved
retrieval:
  acquisition: fetch
  resolved_url: https://en.algorithmica.org/hpc/cpu-cache/
  url: https://en.algorithmica.org/hpc/cpu-cache/
schema_version: source/v1
snapshot_sha256: sha256:d51a32369b41d5409972d53eac29ea4886c21f5783a95a707e058225d711ff8f
source_type: doc
vault_id: public
---
In the previous chapter, we studied computer memory from a theoretical standpoint, using the external memory model to estimate the performance of memory-bound algorithms.
While the external memory model is more or less accurate for computations involving HDDs and network storage, where cost of arithmetic operations on in-memory values is negligible compared to external I/O operations, it is too imprecise for lower levels in the cache hierarchy, where the costs of these operations become comparable.
To perform more fine-grained optimization of in-memory algorithms, we have to start taking into account the many specific details of the CPU cache system. And instead of studying loads of boring Intel documents with dry specs and theoretically achievable limits, we will estimate these parameters experimentally by running numerous small benchmark programs with access patterns that resemble the ones that often occur in practical code.
Experimental Setup
As before, I will be running all experiments on Ryzen 7 4700U, which is a “Zen 2” CPU with the following main cache-related specs:
- 8 physical cores (without hyper-threading) clocked at 2GHz (and 4.1GHz in boost mode — which we disable);
- 256K of 8-way set associative L1 data cache or 32K per core;
- 4M of 8-way set associative L2 cache or 512K per core;
- 8M of 16-way set associative L3 cache, shared between 8 cores;
- 16GB (2x8G) of DDR4 RAM @ 2667MHz.
You can compare it with your own hardware by running dmidecode -t cache or lshw -class memory on Linux or by installing CPU-Z on Windows. You can also find additional details about the CPU on WikiChip and 7-CPU. Not all conclusions will generalize to every CPU platform in existence.
Due to difficulties in preventing the compiler from optimizing away unused values, the code snippets in this article are slightly simplified for exposition purposes. Check the code repository if you want to reproduce them yourself.
Acknowledgements
This chapter is inspired by “Gallery of Processor Cache Effects” by Igor Ostrovsky and “What Every Programmer Should Know About Memory” by Ulrich Drepper, both of which can serve as good accompanying readings.