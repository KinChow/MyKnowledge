---
archive_policy: text-only
attachments:
- filename: cornell-out-of-order-execution.pdf
  kind: document
  media_type: application/pdf
  role: original
  sha256: sha256:db3761d4c16e4b0339a01a365ab1e8b95b15fb76642bb4bccecfaefa02fff364
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-ebf68b3329f2
  position:
    end: 10682
    start: 10554
    type: TextPositionSelector
  quote_sha256: sha256:b4377a61443aa68c136b280d68453c76d1a6c3b3926dccf9696f30609e51f5a2
  selector:
    exact: "- Reorder buffer (ROB)\n  - allocated in-order in D stage\n  - updated
      out-of-order in W stage\n  - deallocated in-order in C stage"
    prefix: 'uture regfile, working regfile)

      '
    suffix: '

      - WAW hazards are possible, whi'
    type: TextQuoteSelector
  selector_sha256: sha256:f0de03666926938af85afab1d5978379d7c6f52379a771dcfa53663cbcde653a
  snapshot_sha256: sha256:d3695f04addc8b3cbd864b1cf1b23dcbc32869cdf3982b3d39968ed191870463
- evidence_id: evidence-09b58cd6677b
  position:
    end: 11147
    start: 11099
    type: TextPositionSelector
  quote_sha256: sha256:aecdfb18b186f44e2757738430246b8f03e15b0a37a030cb0b85546d8e0d31d0
  selector:
    exact: '- new instructions allocated ROB entries at tail'
    prefix: "lemented with circular buffer\n  "
    suffix: "\n  - instructions update pending"
    type: TextQuoteSelector
  selector_sha256: sha256:f30157ad791e0d5ad9d3e2b4d9169698a05d2dc5628a9931c2d01022ccc38816
  snapshot_sha256: sha256:d3695f04addc8b3cbd864b1cf1b23dcbc32869cdf3982b3d39968ed191870463
- evidence_id: evidence-38824228f5d4
  position:
    end: 11255
    start: 11199
    type: TextPositionSelector
  quote_sha256: sha256:7231413ca66b9b732559d1cb9e626411b2a3f9251cdb82812492030e7d8456a7
  selector:
    exact: '- commit stage waits for pending bit of head to be clear'
    prefix: "date pending bit out-of-order\n  "
    suffix: '


      #### **Example Execution Diagr'
    type: TextQuoteSelector
  selector_sha256: sha256:267d02c6d48419b077f4c784f8abc8570c494c8ae3e8edd04e12af6b2bd5aa09
  snapshot_sha256: sha256:d3695f04addc8b3cbd864b1cf1b23dcbc32869cdf3982b3d39968ed191870463
extractor: marker/2.0.0
id: cornell-out-of-order-execution
media_type: application/pdf
origin: external
raw_ref:
  path: archive/raw/db3761d4c16e4b0339a01a365ab1e8b95b15fb76642bb4bccecfaefa02fff364.pdf
  sha256: sha256:db3761d4c16e4b0339a01a365ab1e8b95b15fb76642bb4bccecfaefa02fff364
read_status: retrieved
retrieval:
  acquisition: fetch
  resolved_url: https://bpb-us-w2.wpmucdn.com/sites.coecis.cornell.edu/dist/4/81/files/2017/03/ece4750_handout11-1rshc7n.pdf
  url: https://ocw.ece.cornell.edu/files/2017/03/ece4750_handout11-1rshc7n.pdf
schema_version: source/v1
snapshot_sha256: sha256:d3695f04addc8b3cbd864b1cf1b23dcbc32869cdf3982b3d39968ed191870463
source_type: doc
vault_id: public
---
# **ECE 4750 Computer Architecture, Fall 2015 T10 Advanced Processors: Out-of-Order Execution**

School of Electrical and Computer Engineering Cornell University

revision: 2015-11-04-13-46

**1 Incremental Approach to Exploring OOO Execution 2 2 I3L: IO Front-End/Issue/Completion, Late Commit 3 3 I2OE: IO Front-End/Issue, OOO Completion, Early Commit 5 4 I2OL: IO Front-End/Issue, OOO Completion, Late Commit 9 5 IO2E: IO Front-End, OOO Issue/Completion, Early Commit 14 6 IO2L: IO Front-End, OOO Issue/Completion, Late Commit 20**

## **1. Incremental Approach to Exploring OOO Execution**

- Gradually work through five different microarchitectures
- For each microarchitecture
  - overall pipeline structure
  - required hardware data-structures
  - example instruction sequence executing on microarchitecture
  - handling precise exceptions
- Several simplifications
  - all designs are single issue
  - assume code sequence never includes WAW or WAR dependencies
  - only support addu, addiu, mul

| Front-End | or           | Writeback | or         | Data              |
|-----------|--------------|-----------|------------|-------------------|
|           | Fetch/Decode | Issue     | Completion | Commit Structures |
| I3L       | io           | io        | io         | late              |
| I2OE      | io           | io        | ooo        | early SB          |
| I2OL      | io           | io        | ooo        | late SB, ROB      |
| IO2E      | io           | ooo       | ooo        | early SB, IQ      |
| IO2L      | io           | ooo       | ooo        | late SB, IQ, ROB  |

a: mul r1, r2, r3 b: addiu r11, r10, 1 c: mul r5, r1, r4 d: mul r7, r5, r6 e: addiu r12, r11, 1 f: addiu r13, r12, 1 g: addiu r14, r12, 2

## **2. IO Front-End/Issue/Completion, Late Commit**

| Front-End | or           | Writeback | or         | Data              |
|-----------|--------------|-----------|------------|-------------------|
|           | Fetch/Decode | Issue     | Completion | Commit Structures |
| I3L       | io           | io        | io         | late              |
| I2OE      | io           | io        | ooo        | early SB          |
| I2OL      | io           | io        | ooo        | late SB, ROB      |
| IO2E      | io           | ooo       | ooo        | early SB, IQ      |
| IO2L      | io           | ooo       | ooo        | late SB, IQ, ROB  |

The following is the basic in-order single-issue pipeline.

F D X M W

Split X/M stages into two functional units. Still single issue, so not strictly necessary but a nice incremental design step.

F <sup>1</sup> D X0 M0 M1 <sup>1</sup> <sup>1</sup> W X1

What if we want to incorporate a four-cycle pipelined integer multiplier? Key Idea: Extend all pipelines to equal length.

F <sup>1</sup> D X0 M0 M1 <sup>1</sup> X1 X2 <sup>1</sup> W M2 X3 M3 Y0 Y1 Y2 Y3

#### **Cannonical I3L Pipeline**

![](_page_3_Diagram_2.jpeg)

- To avoid increasing CPI, need full bypassing which can be expensive
- Add new issue stage which
  - reads architectural register file
  - performs hazard checking and includes bypass muxing
  - "issues" instruction to appropriate functional unit
- Include just X-pipe and Y-pipe since we are only focusing on addu, addiu, and mul instructions

#### **Example Execution Diagrams**

| a | : mul   | r1,  | r2, r3 |                                                   |
|---|---------|------|--------|---------------------------------------------------|
| b | : addiu | r11, | r10,   | 1                                                 |
| c | : mul   | r5,  | r1, r4 |                                                   |
| d | : mul   | r7,  | r5,    | r6                                                |
| e | : addiu | r12, | r11,   | 1                                                 |
| f | : addiu | r13, | r12,   | 1                                                 |
| g | : addiu | r14, | r12,   | 2                                                 |
|   |         |      |        | 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 |

## **3. IO Front-End/Issue, OOO Completion, Early Commit**

| Front-End | or           | Writeback | or         | Data              |
|-----------|--------------|-----------|------------|-------------------|
|           | Fetch/Decode | Issue     | Completion | Commit Structures |
| I3L       | io           | io        | io         | late              |
| I2OE      | io           | io        | ooo        | early SB          |
| I2OL      | io           | io        | ooo        | late SB, ROB      |
| IO2E      | io           | ooo       | ooo        | early SB, IQ      |
| IO2L      | io           | ooo       | ooo        | late SB, IQ, ROB  |

### **Cannonical I2OE Pipeline**

![](_page_4_Diagram_4.jpeg)

- Remove "dummy" pipeline stages
- Fewer bypass paths, significantly reduces hardware complexity
  - I3L has six bypass paths
  - I2OE has three bypass paths
  - Bypass from end of Y3, end of X, and W to end of I
- Scoreboard is used to centralize structural/data hazard detection
- WAW hazards are possible, which we ignore in this topic
- WAR hazards are not possible
- NOTE: Fewer stages does not necessarily mean better performance!

#### **Data Structure: Scoreboard**

- Indexed by functional unit
  - **V**: valid bit
  - **rdest**: destination reg specifier
  - Entries shift to right every cycle
- Structural hazards: addu and addiu check col 2 valid bit to ensure no structural hazard on WB port
- RAW hazards: I stage compares current instruction source reg specifiers with every valid entry in SB
  - match in col 2–4 = stall I
  - match in col 0–1 = bypass into I
  - no match = read ARF
- Large number of comparisons make accessing SB expensive
- Indexed by reg specifier
  - **P**: pending bit
  - **FU**: functional unit
  - **WA**: when available?
  - WA bits shift to right every cycle
- Structural hazards: addu and addiu check no bits are set in col 2 to ensure no structural hazard on WB port
- I stage compares checks pending bit for each source register specifier
  - pending bit set = check WA to see if stall or bypass (FU says where to bypass from)
  - pending bit clear = read ARF
- Can use SB to stall to prevent WAW hazards

#### **Example Execution Diagrams**

| a | : mul   | r1,  | r2, r3 |                                                   |
|---|---------|------|--------|---------------------------------------------------|
| b | : addiu | r11, | r10,   | 1                                                 |
| c | : mul   | r5,  | r1, r4 |                                                   |
| d | : mul   | r7,  | r5,    | r6                                                |
| e | : addiu | r12, | r11,   | 1                                                 |
| f | : addiu | r13, | r12,   | 1                                                 |
| g | : addiu | r14, | r12,   | 2                                                 |
|   |         |      |        | 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 |

| a | : mul   | r1,  | r2, r3 |                                                   |
|---|---------|------|--------|---------------------------------------------------|
| b | : addiu | r11, | r10,   | 1                                                 |
| c | : mul   | r5,  | r1, r4 |                                                   |
| d | : mul   | r7,  | r5,    | r6                                                |
| e | : addiu | r12, | r11,   | 1                                                 |
| f | : addiu | r13, | r12,   | 1                                                 |
| g | : addiu | r14, | r12,   | 2                                                 |
|   |         |      |        | 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 |

#### **Handling Precise Exceptions**

Early commit requires the commit point to be in the decode stage. What if instruction d causes an exception?

| a | : mul   | r1,  | r2, r3 |                                                   |
|---|---------|------|--------|---------------------------------------------------|
| b | : addiu | r11, | r10,   | 1                                                 |
| c | : mul   | r5,  | r1, r4 |                                                   |
| d | : mul   | r7,  | r5,    | r6                                                |
| e | : addiu | r12, | r11,   | 1                                                 |
| f | : addiu | r13, | r12,   | 1                                                 |
| g | : addiu | r14, | r12,   | 2                                                 |
|   |         |      |        | 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 |

| a | : mul   | r1,  | r2, r3 |                                                   |
|---|---------|------|--------|---------------------------------------------------|
| b | : addiu | r11, | r10,   | 1                                                 |
| c | : mul   | r5,  | r1, r4 |                                                   |
| d | : mul   | r7,  | r5,    | r6                                                |
| e | : addiu | r12, | r11,   | 1                                                 |
| f | : addiu | r13, | r12,   | 1                                                 |
| g | : addiu | r14, | r12,   | 2                                                 |
|   |         |      |        | 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 |

Not usually possible to detect all exceptions in the front-end, which motivates our interest in supporting late commit at the end of the pipeline.

## **4. IO Front-End/Issue, OOO Completion, Late Commit**

| Front-End | or           | Writeback | or         | Data              |
|-----------|--------------|-----------|------------|-------------------|
|           | Fetch/Decode | Issue     | Completion | Commit Structures |
| I3L       | io           | io        | io         | late              |
| I2OE      | io           | io        | ooo        | early SB          |
| I2OL      | io           | io        | ooo        | late SB, ROB      |
| IO2E      | io           | ooo       | ooo        | early SB, IQ      |
| IO2L      | io           | ooo       | ooo        | late SB, IQ, ROB  |

### **Cannonical I2OL Pipeline**

![](_page_8_Diagram_4.jpeg)

- Add extra C stage for commit at end of pipeline
- Still use scoreboard to centeralize structural/data hazard detection
- Add physical regfile (PRF) and reorder buffer (ROB) between W/C
- PRF keeps uncommited results (a.k.a. future regfile, working regfile)
- Reorder buffer (ROB)
  - allocated in-order in D stage
  - updated out-of-order in W stage
  - deallocated in-order in C stage
- WAW hazards are possible, which we ignore in this topic
- WAR hazards are not possible

#### **Data Structure: Reorder Buffer**

- ROB fields
  - **V**: valid bit (is this entry valid?)
  - **P**: pending bit (instruction in flight targeting this entry)
  - **V**: valid bit (is the dest reg specifier valid?)
  - **rdest**: destination reg specifier
- ROB managed like a queue, implemented with circular buffer
  - new instructions allocated ROB entries at tail
  - instructions update pending bit out-of-order
  - commit stage waits for pending bit of head to be clear

#### **Example Execution Diagrams**

| a | : mul   | r1,  | r2, r3 |                                                   |
|---|---------|------|--------|---------------------------------------------------|
| b | : addiu | r11, | r10,   | 1                                                 |
| c | : mul   | r5,  | r1, r4 |                                                   |
| d | : mul   | r7,  | r5,    | r6                                                |
| e | : addiu | r12, | r11,   | 1                                                 |
| f | : addiu | r13, | r12,   | 1                                                 |
| g | : addiu | r14, | r12,   | 2                                                 |
|   |         |      |        | 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 |

We can use a table to compactly illustrate how the ROB works.

### **Handling Precise Exceptions**

Late commit means exceptions are handled in the C stage at the end of the pipeline. What if instruction a causes an exception?

| a | : mul   | r1,  | r2, r3 |                                                   |
|---|---------|------|--------|---------------------------------------------------|
| b | : addiu | r11, | r10,   | 1                                                 |
| c | : mul   | r5,  | r1, r4 |                                                   |
| d | : mul   | r7,  | r5,    | r6                                                |
| e | : addiu | r12, | r11,   | 1                                                 |
| f | : addiu | r13, | r12,   | 1                                                 |
| g | : addiu | r14, | r12,   | 2                                                 |
|   |         |      |        | 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 |

| a | : mul   | r1,  | r2, r3 |                                                   |
|---|---------|------|--------|---------------------------------------------------|
| b | : addiu | r11, | r10,   | 1                                                 |
| c | : mul   | r5,  | r1, r4 |                                                   |
| d | : mul   | r7,  | r5,    | r6                                                |
| e | : addiu | r12, | r11,   | 1                                                 |
| f | : addiu | r13, | r12,   | 1                                                 |
| g | : addiu | r14, | r12,   | 2                                                 |
|   |         |      |        | 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 |

Need to copy values from ARF to PRF on an exception before redirecting the front of the pipeline to the exception handler. This copy may take multiple cycles. Also possible to include additional bits in I stage to indicate wether the most recent version of every given architectural register is in the ARF or PRF.

## **5. IO Front-End, OOO Issue/Completion, Early Commit**

| Front-End | or           | Writeback | or         | Data              |
|-----------|--------------|-----------|------------|-------------------|
|           | Fetch/Decode | Issue     | Completion | Commit Structures |
| I3L       | io           | io        | io         | late              |
| I2OE      | io           | io        | ooo        | early SB          |
| I2OL      | io           | io        | ooo        | late SB, ROB      |
| IO2E      | io           | ooo       | ooo        | early SB, IQ      |
| IO2L      | io           | ooo       | ooo        | late SB, IQ, ROB  |

#### **Cannonical IO2E Pipeline**

![](_page_13_Diagram_4.jpeg)

- Still use scoreboard to centeralize structural/data hazard detection
- Add issue queue (IQ) between D and I stages
  - allocated in-order in D stage
  - updated out-of-order in W stage
  - deallocated out-of-order in I stage
- Do not necessarily want to wait for W stage to update IQ; we will need to assume *aggressive bypassing* which requires combinational communication between last stage of functional unit and I stage
- WAW hazards are possible, which we ignore in this topic
- WAR hazards are possible, which we ignore in this topic

#### **Data Structure: Issue Queue**

- IQ fields
  - **V**: valid bit (is this entry valid?)
  - **op**: instruction opcode
  - **imm** immediate value
  - **V**: valid bit (is the dest/src reg specifier valid?)
  - **P**: pending bit (is the src data ready?)
  - **rdest/rsrc**: destination/source reg specifiers
- IQ managed like a queue, implemented with circular buffer
  - new instructions allocated IQ entries at tail
  - instructions leave IQ out-of-order when ready
- Wakeup Logic: An instruction needs to update pending bits of dependent instructions when that instruction is in W stage (actually need to do this earlier to enable aggressive bypassing)
- Select Logic: Determine which instructions are ready to be issued, and then select which one to actually issue. Usually issue oldest ready instruction.

inst\_ready = ( !val\_src0 || !p\_src0 ) && ( !val\_src1 || !p\_src1 ) && no structural hazards

#### **Example Execution Diagrams**

| a | : mul   | r1,  | r2, r3 |                                                   |
|---|---------|------|--------|---------------------------------------------------|
| b | : addiu | r11, | r10,   | 1                                                 |
| c | : mul   | r5,  | r1, r4 |                                                   |
| d | : mul   | r7,  | r5,    | r6                                                |
| e | : addiu | r12, | r11,   | 1                                                 |
| f | : addiu | r13, | r12,   | 1                                                 |
| g | : addiu | r14, | r12,   | 2                                                 |
|   |         |      |        | 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 |

**Issue Queue**

We can use a table to compactly illustrate how the IQ works.

#### **Handling Precise Exceptions**

Early commit requires the commit point to be in the decode stage. What if instruction e causes an exception?

| a | : mul   | r1,  | r2, r3 |                                                   |
|---|---------|------|--------|---------------------------------------------------|
| b | : addiu | r11, | r10,   | 1                                                 |
| c | : mul   | r5,  | r1, r4 |                                                   |
| d | : mul   | r7,  | r5,    | r6                                                |
| e | : addiu | r12, | r11,   | 1                                                 |
| f | : addiu | r13, | r12,   | 1                                                 |
| g | : addiu | r14, | r12,   | 2                                                 |
|   |         |      |        | 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 |

| a | : mul   | r1,  | r2, r3 |                                                   |
|---|---------|------|--------|---------------------------------------------------|
| b | : addiu | r11, | r10,   | 1                                                 |
| c | : mul   | r5,  | r1, r4 |                                                   |
| d | : mul   | r7,  | r5,    | r6                                                |
| e | : addiu | r12, | r11,   | 1                                                 |
| f | : addiu | r13, | r12,   | 1                                                 |
| g | : addiu | r14, | r12,   | 2                                                 |
|   |         |      |        | 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 |

#### **Performance Benefit of OOO Execution**

Does IO2E improve performance compared to I2OE? Let's assume all instructions are in issue queue.

| a | : mul   | r1,  | r2, r3 |                                                   |
|---|---------|------|--------|---------------------------------------------------|
| b | : addiu | r11, | r10,   | 1                                                 |
| c | : mul   | r5,  | r1, r4 |                                                   |
| d | : mul   | r7,  | r5,    | r6                                                |
| e | : addiu | r12, | r11,   | 1                                                 |
| f | : addiu | r13, | r12,   | 1                                                 |
| g | : addiu | r14, | r12,   | 2                                                 |
|   |         |      |        | 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 |

| a | : mul   | r1,  | r2, r3 |                                                   |
|---|---------|------|--------|---------------------------------------------------|
| b | : addiu | r11, | r10,   | 1                                                 |
| c | : mul   | r5,  | r1, r4 |                                                   |
| d | : mul   | r7,  | r5,    | r6                                                |
| e | : addiu | r12, | r11,   | 1                                                 |
| f | : addiu | r13, | r12,   | 1                                                 |
| g | : addiu | r14, | r12,   | 2                                                 |
|   |         |      |        | 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 |

#### **Centeralized vs. Distributed IQs**

IQs can either be centeralized or distributed across functional units. Distributed IQs are sometimes called reservation stations. This can naturally enable superscalar execution.

![](_page_18_Diagram_3.jpeg)

## **6. IO Front-End, OOO Issue/Completion, Late Commit**

| Front-End | or           | Writeback | or         | Data              |
|-----------|--------------|-----------|------------|-------------------|
|           | Fetch/Decode | Issue     | Completion | Commit Structures |
| I3L       | io           | io        | io         | late              |
| I2OE      | io           | io        | ooo        | early SB          |
| I2OL      | io           | io        | ooo        | late SB, ROB      |
| IO2E      | io           | ooo       | ooo        | early SB, IQ      |
| IO2L      | io           | ooo       | ooo        | late SB, IQ, ROB  |

#### **Cannonical IO2L Pipeline**

F <sup>1</sup> D

X

Y0 Y1 Y2 Y3

I <sup>1</sup>

1 1

| ARF | write                        |
|-----|------------------------------|
| IQ  | alloc                        |
|     | write read/dealloc           |
| SB  | read/write                   |
| PRF | read write read read/dealloc |
| ROB | alloc                        |

IQ

1

PRF

ARF

W C 1 1

ROB

- Use scoreboard to centeralize structural/data hazard detection
- Use IQ to enable out-of-order issue, ROB to enable late commit
- Overall organization:
  - In-order fetc/decode (front-end of pipeline)
  - Out-of-order issue/completion (middle of pipeline)
  - In-order commit (back-end of pipeline)
- WAW hazards are possible, which we ignore in this topic
- WAR hazards are possible, which we ignore in this topic

#### **Example Execution Diagrams**

| a | : mul   | r1,  | r2, r3 |                                                   |
|---|---------|------|--------|---------------------------------------------------|
| b | : addiu | r11, | r10,   | 1                                                 |
| c | : mul   | r5,  | r1, r4 |                                                   |
| d | : mul   | r7,  | r5,    | r6                                                |
| e | : addiu | r12, | r11,   | 1                                                 |
| f | : addiu | r13, | r12,   | 1                                                 |
| g | : addiu | r14, | r12,   | 2                                                 |
|   |         |      |        | 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 |

| a | : mul   | r1,  | r2, r3 |                                                   |
|---|---------|------|--------|---------------------------------------------------|
| b | : addiu | r11, | r10,   | 1                                                 |
| c | : mul   | r5,  | r1, r4 |                                                   |
| d | : mul   | r7,  | r5,    | r6                                                |
| e | : addiu | r12, | r11,   | 1                                                 |
| f | : addiu | r13, | r12,   | 1                                                 |
| g | : addiu | r14, | r12,   | 2                                                 |
|   |         |      |        | 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 |

#### **Handling Precise Exceptions**

Late commit means exceptions are handled in the C stage at the end of the pipeline. What if instruction a causes an exception?

| a | : mul   | r1,  | r2, r3 |                                                   |
|---|---------|------|--------|---------------------------------------------------|
| b | : addiu | r11, | r10,   | 1                                                 |
| c | : mul   | r5,  | r1, r4 |                                                   |
| d | : mul   | r7,  | r5,    | r6                                                |
| e | : addiu | r12, | r11,   | 1                                                 |
| f | : addiu | r13, | r12,   | 1                                                 |
| g | : addiu | r14, | r12,   | 2                                                 |
|   |         |      |        | 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 |

| a | : mul   | r1,  | r2, r3 |                                                   |
|---|---------|------|--------|---------------------------------------------------|
| b | : addiu | r11, | r10,   | 1                                                 |
| c | : mul   | r5,  | r1, r4 |                                                   |
| d | : mul   | r7,  | r5,    | r6                                                |
| e | : addiu | r12, | r11,   | 1                                                 |
| f | : addiu | r13, | r12,   | 1                                                 |
| g | : addiu | r14, | r12,   | 2                                                 |
|   |         |      |        | 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 |

#### **Out-of-Order Dual-Issue Processor**

Assume we can fetch, decode, issue, writeback, and commit two instructions per cycle.

| a | : mul   | r1,  | r2, r3 |                                                   |
|---|---------|------|--------|---------------------------------------------------|
| b | : addiu | r11, | r10,   | 1                                                 |
| c | : mul   | r5,  | r1, r4 |                                                   |
| d | : mul   | r7,  | r5,    | r6                                                |
| e | : addiu | r12, | r11,   | 1                                                 |
| f | : addiu | r13, | r12,   | 1                                                 |
| g | : addiu | r14, | r12,   | 2                                                 |
|   |         |      |        | 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 |

| a | : mul   | r1,  | r2, r3 |                                                   |
|---|---------|------|--------|---------------------------------------------------|
| b | : addiu | r11, | r10,   | 1                                                 |
| c | : mul   | r5,  | r1, r4 |                                                   |
| d | : mul   | r7,  | r5,    | r6                                                |
| e | : addiu | r12, | r11,   | 1                                                 |
| f | : addiu | r13, | r12,   | 1                                                 |
| g | : addiu | r14, | r12,   | 2                                                 |
|   |         |      |        | 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 |