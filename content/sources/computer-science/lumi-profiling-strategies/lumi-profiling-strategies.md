---
archive_policy: text-only
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-5138110b0629
  position:
    end: 647
    start: 487
    type: TextPositionSelector
  selector:
    exact: Sampling consists of taking regular snapshots of the application's call
      stack to create a statistical profile. This is a good option for low overhead
      profiling.
    prefix: 'mum user interaction.

      Sampling¶

      '
    suffix: '

      Tracing¶

      Tracing is a profiling'
    type: TextQuoteSelector
  snapshot_sha256: sha256:4b0f40d2346476f6ac9ccb01a5ccd85ffe6d936505057a4e1509581925eb4e0c
- evidence_id: evidence-4321897985b6
  position:
    end: 886
    start: 657
    type: TextPositionSelector
  selector:
    exact: Tracing is a profiling technique that captures specific program events,
      such as entering or exiting a function, every time they occur. This allows the
      collection of accurate profiling information about specific areas of the code.
    prefix: 'ow overhead profiling.

      Tracing¶

      '
    suffix: ''
    type: TextQuoteSelector
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