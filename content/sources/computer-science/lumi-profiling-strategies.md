---
archive_policy: text-only
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-9ce34a48845e
  position:
    end: 791
    start: 657
    type: TextPositionSelector
  quote_sha256: sha256:c3061f7bd62f9dd7f65d73509a1f137fb07c2b0ee89b12677aada15c97ff5d8a
  selector:
    exact: Tracing is a profiling technique that captures specific program events,
      such as entering or exiting a function, every time they occur.
    prefix: 'ow overhead profiling.

      Tracing¶

      '
    suffix: ' This allows the collection of a'
    type: TextQuoteSelector
  selector_sha256: sha256:931ab5905cadb22b066fb0e302598d89b00876366e6f188db364ebc41b5447c7
  snapshot_sha256: sha256:4b0f40d2346476f6ac9ccb01a5ccd85ffe6d936505057a4e1509581925eb4e0c
- evidence_id: evidence-685c7e0035da
  position:
    end: 597
    start: 487
    type: TextPositionSelector
  quote_sha256: sha256:8dd27dabfdbd035b59ebea9ba12ce55837ceecfecde75727f6b04dc918c36934
  selector:
    exact: Sampling consists of taking regular snapshots of the application's call
      stack to create a statistical profile.
    prefix: 'mum user interaction.

      Sampling¶

      '
    suffix: ' This is a good option for low o'
    type: TextQuoteSelector
  selector_sha256: sha256:e4fa74c0aa1da4f304dfd2a886de0e81eaaab801b793d4da4017794abdb094fc
  snapshot_sha256: sha256:4b0f40d2346476f6ac9ccb01a5ccd85ffe6d936505057a4e1509581925eb4e0c
extractor: trafilatura/2.2.0
id: lumi-profiling-strategies
media_type: text/html
origin: external
read_status: retrieved
retrieval:
  acquisition: fetch
  resolved_url: https://docs.lumi-supercomputer.eu/development/profiling/strategies/
  url: https://docs.lumi-supercomputer.eu/development/profiling/strategies
schema_version: source/v1
snapshot_sha256: sha256:4b0f40d2346476f6ac9ccb01a5ccd85ffe6d936505057a4e1509581925eb4e0c
source_type: doc
vault_id: public
---
Performance analysis strategies¶
Profiling reveals performance issues and informs you about where your application spends most of its time. Once you have identified bottlenecks, you then focus your efforts on investigating those parts and improve them.
Quick profiling¶
For a quick profiling, you can use the perftools-lite tool, a simplified and
easy-to-use version of CrayPat that provides basic performance analysis
information automatically, with minimum user interaction.
Sampling¶
Sampling consists of taking regular snapshots of the application's call stack to create a statistical profile. This is a good option for low overhead profiling.
Tracing¶
Tracing is a profiling technique that captures specific program events, such as entering or exiting a function, every time they occur. This allows the collection of accurate profiling information about specific areas of the code.