---
archive_policy: text-only
attachments:
- filename: cornell-superscalar-execution.pdf
  kind: document
  media_type: application/pdf
  role: original
  sha256: sha256:c0504e599b8e6bc70cbaa096f1931f5a2014f3a7c7b2947d94137e263b837375
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-098639dc3686
  position:
    end: 1113
    start: 1011
    type: TextPositionSelector
  quote_sha256: sha256:e22e4e64897bb147d313330d22eab43b5cfd58ba8fd9519e3dabb045b3a40675
  selector:
    exact: '- Superscalar processors enable CPI < 1 (i.e., IPC > 1) by executing multiple
      instructions in parallel'
    prefix: 'ndamentally limited to CPI >= 1

      '
    suffix: '

      - Can have both in-order and ou'
    type: TextQuoteSelector
  selector_sha256: sha256:e1f0dbdf871822995a12c6c18aa629621d2c37eaeb03b42332107ae8b62d8b0e
  snapshot_sha256: sha256:114cc1cb712199990c95a187ed34798a42f3c6876bca89cbac9c269ab07e639c
- evidence_id: evidence-e9edfbabf635
  position:
    end: 1219
    start: 1114
    type: TextPositionSelector
  quote_sha256: sha256:755c67e88d55bfaae93d206ca5524d1bf0b532c3979c25204eb5ff45d8c779d3
  selector:
    exact: '- Can have both in-order and out-of-order superscalar processors, but
      we will start by exploring in-order'
    prefix: 'ltiple instructions in parallel

      '
    suffix: '


      ![](_page_1_Diagram_3.jpeg)


      -'
    type: TextQuoteSelector
  selector_sha256: sha256:4d1ba41b6c0eb0e30ab6561192b88767701e2f148efa40595dfb1cc5dd324eaa
  snapshot_sha256: sha256:114cc1cb712199990c95a187ed34798a42f3c6876bca89cbac9c269ab07e639c
extractor: marker/2.0.0
id: cornell-superscalar-execution
media_type: application/pdf
origin: external
raw_ref:
  path: archive/raw/c0504e599b8e6bc70cbaa096f1931f5a2014f3a7c7b2947d94137e263b837375.pdf
  sha256: sha256:c0504e599b8e6bc70cbaa096f1931f5a2014f3a7c7b2947d94137e263b837375
read_status: retrieved
retrieval:
  acquisition: fetch
  resolved_url: https://bpb-us-w2.wpmucdn.com/sites.coecis.cornell.edu/dist/4/81/files/2017/03/ece4750_handout10-21jbv7m.pdf
  url: https://ocw.ece.cornell.edu/files/2017/03/ece4750_handout10-21jbv7m.pdf
schema_version: source/v1
snapshot_sha256: sha256:114cc1cb712199990c95a187ed34798a42f3c6876bca89cbac9c269ab07e639c
source_type: doc
vault_id: public
---
# **ECE 4750 Computer Architecture, Fall 2015 T09 Advaced Processors: Superscalar Execution**

School of Electrical and Computer Engineering Cornell University

revision: 2015-11-02-00-30

| 1 | In-Order  | Dual-Issue  |             | Superscalar    | PARCv1 Processor | 2  |
|---|-----------|-------------|-------------|----------------|------------------|----|
| 2 |           | Superscalar | Pipeline    | Hazards        |                  | 4  |
|   | 2.1.      | RAW Hazards |             |                |                  | 4  |
|   | 2.2.      | Control     | Hazards     |                |                  | 6  |
|   | 2.3.      | Structural  | Hazards     |                |                  | 10 |
|   | 2.4.      | WAW and     | WAR         | Name Hazards   |                  | 10 |
| 3 | Analyzing |             | Performance | of Superscalar | Processors       | 11 |

# **1. In-Order Dual-Issue Superscalar PARCv1 Processor**

- Processors studied so far are fundamentally limited to CPI >= 1
- Superscalar processors enable CPI < 1 (i.e., IPC > 1) by executing multiple instructions in parallel
- Can have both in-order and out-of-order superscalar processors, but we will start by exploring in-order

![](_page_1_Diagram_3.jpeg)

- Continue to assume combinational memories
- F Stage : fetch two instructions at once
- D Stage : 4 read ports, decode 2 inst, "issue" inst to correct pipe
- X/M Stage : separate into A and B pipes (see next page)
- W Stage : 2 write ports

More abstract way to illustrate same dual-issue superscalar pipeline

![](_page_2_Diagram_3.jpeg)

Different instructions use the A-pipe and/or the B-pipe

|        | addu addiu | mul | lw | sw | j jal | jr bne |
|--------|------------|-----|----|----|-------|--------|
| A-Pipe | ✓ ✓        | ✓   |    |    | ✓ ✓   | ✓ ✓    |
| B-Pipe | ✓ ✓        |     | ✓  | ✓  | ✓ ✓   | ✓      |

Example pipeline diagram for dual-issue superscalar processor

| addiu | r1,  | r2,    | 1   |
|-------|------|--------|-----|
| addiu | r3,  | r4,    | 1   |
| addiu | r5,  | r6,    | 1   |
| mul   | r7,  | r8, r9 |     |
| mul   | r10, | r11,   | r12 |
| addiu | r13, | r14,   | 1   |

- Multiple instructions in stages F, D, W allowed because superscalar processor has duplicated hardware to avoid structural hazards
- Fetch Block group of instructions fetched as unit
- Swizzle instructions "swapped" from natural fetch position to appropriate execution pipe

# **2. Superscalar Pipeline Hazards**

Seems so easy, but why is pipelining hard?

- RAW Hazards
- Control Hazards
- Structural Hazards
- WAR/WAR Name Hazards

# **2.1. RAW Hazards**

Let's first assume we only use stalling to resolve RAW hazards

| addiu | r1, | r2, | 1  |
|-------|-----|-----|----|
| addiu | r3, | r4, | 1  |
| addu  | r5, | r1, | r3 |
| addiu | r6, | r5, | 1  |
| addiu | r7, | r8, | 1  |
| addiu | r9, | r8, | 1  |

| addiu | r1, | r2, | 1  |
|-------|-----|-----|----|
| addiu | r3, | r4, | 1  |
| addu  | r5, | r1, | r3 |
| addiu | r6, | r5, | 1  |
| addiu | r7, | r8, | 1  |
| addiu | r9, | r8, | 1  |

A fully-bypassed superscalar processor is possible, but expensive

![](_page_3_Diagram_10.jpeg)

Revisit previous assembly sequence with full bypassing

| addiu | r1, | r2, | 1  |
|-------|-----|-----|----|
| addiu | r3, | r4, | 1  |
| addu  | r5, | r1, | r3 |
| addiu | r6, | r5, | 1  |
| addiu | r7, | r8, | 1  |
| addiu | r9, | r8, | 1  |

| addiu | r1, | r2, | 1  |
|-------|-----|-----|----|
| addiu | r3, | r4, | 1  |
| addu  | r5, | r1, | r3 |
| addiu | r6, | r5, | 1  |
| addiu | r7, | r8, | 1  |
| addiu | r9, | r8, | 1  |

Activity: Draw a pipeline diagram for following instruction sequence. Include all microarchitectural dependency arrows.

| addiu | r1, | r2,   | 1 |
|-------|-----|-------|---|
| lw    | r3, | 0(r4) |   |
| lw    | r5, | 0(r3) |   |
| addiu | r6, | r7,   | 1 |
| addiu | r8, | r5,   | 1 |
| addiu | r9, | r8,   | 1 |

| addiu | r1, | r2,   | 1 |
|-------|-----|-------|---|
| lw    | r3, | 0(r4) |   |
| lw    | r5, | 0(r3) |   |
| addiu | r6, | r7,   | 1 |
| addiu | r8, | r5,   | 1 |
| addiu | r9, | r8,   | 1 |

# **2.2. Control Hazards**

Consider following two static instruction sequences.

 0x1000 addiu r1, r2, 1 0x1004 j foo ... foo: 0x2000 addiu r3, r4, 1 0x2004 addiu r5, r6, 1 # assume R[r1] != R[r2] 0x1000 bne r1, r2, foo ... foo: 0x2000 addiu r3, r4, 1 0x2004 addiu r5, r6, 1

Pipeline diagram for left sequence. Jumps are resolved in D stage.

Pipeline diagram for right sequence. Branches are resolved in A0 stage.

### **Unaligned fetch blocks**

Consider the following static instruction sequence

 0x000 opA 0x004 opB 0x008 opC 0x00c j 0x100

 ... 0x100 opD 0x104 j 0x204

 ... 0x204 opE 0x208 j 0x30c

 ... 0x30c opF 0x310 opG 0x314 opH

Layout of fetch blocks in instruction cache. Numbers indicate which instructions belong to which fetch block.

- Unaligned fetch blocks within a cache line are challenging
- Unaligned fetch blocks across cache lines are very challenging

### **Aligned fetch blocks**

Only fetch aligned fetch blocks, possibly discarding first instruction. Reconsider the same static instruction sequence

 0x000 opA 0x004 opB 0x008 opC 0x00c j 0x100

 ... 0x100 opD 0x104 j 0x204

 ... 0x204 opE 0x208 j 0x30c

 ... 0x30c opF 0x310 opG 0x314 opH

Layout of fetch blocks in instruction cache. Numbers indicate which instructions belong to which fetch block.

#### **Supporting precise exceptions**

Consider following instruction sequence. Assume commit point is in the A1/B1 stage and the xxx instruction causes an illegal instruction exception originating in the D stage.

 addu r1, r2, r3 xxx # causes illegal instruction exception addiu r4, r5, 1 addiu r6, r7, 1 ... exception\_handler: opX opY opZ

![](_page_8_Picture_5.jpeg)

What if addu caused an arithmetic overflow exception?

# **2.3. Structural Hazards**

Structural hazards *are not* possible in the canonical single-issue PARCv1 pipeline, but structural hazards *are* possible in the canonical dual-issue PARCv1 pipeline if two instructions in the same fetch block want to use the same pipe.

# **2.4. WAW and WAR Name Hazards**

WAW name hazards *are not* possible in the canonical single-issue PARCv1 pipeline, but WAW name hazards *are* possible in the canonical dual-issue PARCv1 pipeline if two instructions in the same fetch block write the same register.

WAR name hazards *are not* possible in the canonical single-issue PARCv1 pipeline. Are WAR name hazards possible in the canonical dual-issue PARCv1 pipeline?

# **3. Analyzing Performance of Superscalar Processors**

Consider the classic vector-vector add loop over arrays with 64 elements. This loop has a CPI of 1.33 on the canonical single-issue PARCv1 processor. What is the CPI on the canonical dual-issue PARCv1 processor?

loop: lw r12, 0(r4) lw r13, 0(r5) addu r14, r12, r13 sw r14, 0(r6) addiu r4, r4, 4 addiu r5, r5, 4 addiu r6, r6, 4 addiu r7, r7, -1 bne r7, r0, loop jr r31