---
archive_policy: text-only
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-63df9b6249a9
  position:
    end: 428
    start: 318
    type: TextPositionSelector
  quote_sha256: sha256:c54cae406baa2b9e25974220e0964b97c631928249522918b541221271e83b2b
  selector:
    exact: A structural hazard happens when two or more instructions need the same
      part of CPU (e.g., an execution unit).
    prefix: 'ultiple ways this may happen:

      - '
    suffix: '

      - A data hazard happens when yo'
    type: TextQuoteSelector
  selector_sha256: sha256:c3a2e00f72deba651c69d8c8278706887c898d1900253de97c697da221b89f8b
  snapshot_sha256: sha256:19f40970c4f6d592dd9039469d0ea0409ef8fd47e546443f10ddc03db4968640
- evidence_id: evidence-e4655e64d9dc
  position:
    end: 529
    start: 431
    type: TextPositionSelector
  quote_sha256: sha256:d5d9fe52f4e290b51fef9cc3324a6e558c756a12794c1c459d7472e655b6cff0
  selector:
    exact: A data hazard happens when you have to wait for an operand to be computed
      from some previous step.
    prefix: 'PU (e.g., an execution unit).

      - '
    suffix: '

      - A control hazard happens when'
    type: TextQuoteSelector
  selector_sha256: sha256:e6dc80195248ca8fd1a44bfeac30301990a8a2b1ccb9847ca98cd72abfc7b274
  snapshot_sha256: sha256:19f40970c4f6d592dd9039469d0ea0409ef8fd47e546443f10ddc03db4968640
- evidence_id: evidence-e33552e7453f
  position:
    end: 623
    start: 532
    type: TextPositionSelector
  quote_sha256: sha256:56fb6e8e077190b02bd1845469b390ceddab22d78ceef070f08287ba46862962
  selector:
    exact: A control hazard happens when a CPU can’t tell which instructions it needs
      to execute next.
    prefix: 'uted from some previous step.

      - '
    suffix: '

      The only way to resolve a hazar'
    type: TextQuoteSelector
  selector_sha256: sha256:2352d4df364d1d03e18f6de875f8f82403f97945490830bb8c648251354e5d22
  snapshot_sha256: sha256:19f40970c4f6d592dd9039469d0ea0409ef8fd47e546443f10ddc03db4968640
extractor: trafilatura/2.2.0
id: pipeline-hazards
media_type: text/html
origin: external
read_status: retrieved
retrieval:
  acquisition: fetch
  resolved_url: https://en.algorithmica.org/hpc/pipelining/hazards/
  url: https://en.algorithmica.org/hpc/pipelining/hazards/
schema_version: source/v1
snapshot_sha256: sha256:19f40970c4f6d592dd9039469d0ea0409ef8fd47e546443f10ddc03db4968640
source_type: doc
vault_id: public
---
Pipelining lets you hide the latencies of instructions by running them concurrently, but also creates some potential obstacles of its own — characteristically called pipeline hazards, that is, situations when the next instruction cannot execute on the following clock cycle.
There are multiple ways this may happen:
- A structural hazard happens when two or more instructions need the same part of CPU (e.g., an execution unit).
- A data hazard happens when you have to wait for an operand to be computed from some previous step.
- A control hazard happens when a CPU can’t tell which instructions it needs to execute next.
The only way to resolve a hazard is to have a pipeline stall: stop the progress of all previous steps until the cause of congestion is gone. This creates bubbles in the pipeline — analogous with air bubbles in fluid pipes — a time-propagating condition when execution units are idling and no useful work is done.
Different hazards have different penalties:
- In structural hazards, you have to wait (usually one more cycle) until the execution unit is ready. They are fundamental bottlenecks on performance and can’t be avoided — you have to engineer around them.
- In data hazards, you have to wait for the required data to be computed (the latency of the critical path). Data hazards are solved by restructuring computations so that the critical path is shorter.
- In control hazards, you generally have to flush the entire pipeline and start over, wasting a whole 15-20 cycles. They are solved by either removing branches completely, or making them predictable so that the CPU can effectively speculate on what is going to be executed next.
As they have very different impacts on performance, we are going to go in the reversed order and start with the more grave ones.