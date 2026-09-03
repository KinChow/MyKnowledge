---
archive_policy: text-only
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-8cbf47f4bcdd
  position:
    end: 6945
    start: 6891
    type: TextPositionSelector
  quote_sha256: sha256:4944b50ca3c651d30a717c7f8ab98a495a7b37a23848b282b77dc630cf3a46b8
  selector:
    exact: commit stage waits for pending bit of head to be clear
    prefix: 'date pending bit out-of-order

      – '
    suffix: '

      10

      4. I2OL: IO Front-End/Issue,'
    type: TextQuoteSelector
  selector_sha256: sha256:b89db283f7e1625b6c26addd91c6c2b07e5e2caca0e014640989c7a2ea545845
  snapshot_sha256: sha256:1629f08faf835ed3d7a9f85ee11e3122ad8693b8dd0a6a32acdc2b6c9eb5c643
- evidence_id: evidence-0a67e6c41e7b
  position:
    end: 6841
    start: 6795
    type: TextPositionSelector
  quote_sha256: sha256:1bfc6c0c13a45e2e8b64531c25bc3d166f67a061fac1e587bf547e4a7d8a04bd
  selector:
    exact: new instructions allocated ROB entries at tail
    prefix: 'lemented with circular buffer

      – '
    suffix: '

      – instructions update pending b'
    type: TextQuoteSelector
  selector_sha256: sha256:af88c0faff5a998f90be4a53b6881af1f809adc7b176fe83c869885a18caeb6d
  snapshot_sha256: sha256:1629f08faf835ed3d7a9f85ee11e3122ad8693b8dd0a6a32acdc2b6c9eb5c643
- evidence_id: evidence-1554a03bd9f6
  position:
    end: 6358
    start: 6238
    type: TextPositionSelector
  quote_sha256: sha256:5aedd1fcf4fc70f07eae578687dbed5db8a7dcfd931995fbc87bedc8c8098f67
  selector:
    exact: 'Reorder buffer (ROB)

      – allocated in-order in D stage

      – updated out-of-order in W stage

      – deallocated in-order in C stage'
    prefix: 'uture regﬁle, working regﬁle)

      • '
    suffix: '

      • WAW hazards are possible, whi'
    type: TextQuoteSelector
  selector_sha256: sha256:9c7a616dcb77b99394b17338a39c9f5836dad6d9fba7abbf8a13ff275aaf98b1
  snapshot_sha256: sha256:1629f08faf835ed3d7a9f85ee11e3122ad8693b8dd0a6a32acdc2b6c9eb5c643
extractor: pypdf/6.16.2
id: cornell-out-of-order-execution
media_type: application/pdf
origin: external
read_status: retrieved
retrieval:
  acquisition: fetch
  resolved_url: https://bpb-us-w2.wpmucdn.com/sites.coecis.cornell.edu/dist/4/81/files/2017/03/ece4750_handout11-1rshc7n.pdf
  url: https://ocw.ece.cornell.edu/files/2017/03/ece4750_handout11-1rshc7n.pdf
schema_version: source/v1
snapshot_sha256: sha256:1629f08faf835ed3d7a9f85ee11e3122ad8693b8dd0a6a32acdc2b6c9eb5c643
source_type: doc
vault_id: public
---
ECE 4750 Computer Architecture, Fall 2015
T10 Advanced Processors:
Out-of-Order Execution
School of Electrical and Computer Engineering
Cornell University
revision: 2015-11-04-13-46
1 Incremental Approach to Exploring OOO Execution 2
2 I3L: IO Front-End/Issue/Completion, Late Commit 3
3 I2OE: IO Front-End/Issue, OOO Completion, Early Commit 5
4 I2OL: IO Front-End/Issue, OOO Completion, Late Commit 9
5 IO2E: IO Front-End, OOO Issue/Completion, Early Commit 14
6 IO2L: IO Front-End, OOO Issue/Completion, Late Commit 20
1
1. Incremental Approach to Exploring OOO Execution
1. Incremental Approach to Exploring OOO Execution
• Gradually work through ﬁve different microarchitectures
• For each microarchitecture
– overall pipeline structure
– required hardware data-structures
– example instruction sequence executing on microarchitecture
– handling precise exceptions
• Several simpliﬁcations
– all designs are single issue
– assume code sequence never includes WAW or WAR dependencies
– only support addu, addiu, mul
Front-End or Writeback or Data
Fetch/Decode Issue Completion Commit Structures
I3L io io io late
I2OE io io ooo early SB
I2OL io io ooo late SB, ROB
IO2E io ooo ooo early SB, IQ
IO2L io ooo ooo late SB, IQ, ROB
a: mul r1, r2, r3
b: addiu r11, r10, 1
c: mul r5, r1, r4
d: mul r7, r5, r6
e: addiu r12, r11, 1
f: addiu r13, r12, 1
g: addiu r14, r12, 2
2
2. I3L: IO Front-End/Issue/Completion, Late Commit
2. IO Front-End/Issue/Completion, Late Commit
Front-End or Writeback or Data
Fetch/Decode Issue Completion Commit Structures
I3L io io io late
I2OE io io ooo early SB
I2OL io io ooo late SB, ROB
IO2E io ooo ooo early SB, IQ
IO2L io ooo ooo late SB, IQ, ROB
The following is the basic in-order single-issue pipeline.
F D X WM
Split X/M stages into two functional units. Still single issue, so not strictly
necessary but a nice incremental design step.
F D1
X0
M0 M1
1 W1
X1
What if we want to incorporate a four-cycle pipelined integer multiplier?
Key Idea: Extend all pipelines to equal length.
F D1 X0
M0 M1
1 W1X1 X2
M2
X3
M3
Y0 Y1 Y2 Y3
3
2. I3L: IO Front-End/Issue/Completion, Late Commit
Cannonical I3L Pipeline
F D1
X0
1 W1
Y0 Y1 Y2 Y3
ARF
ARFread
I 1
write
X1 X2 X3
• To avoid increasing CPI, need full bypassing which can be expensive
• Add new issue stage which
– reads architectural register ﬁle
– performs hazard checking and includes bypass muxing
– “issues” instruction to appropriate functional unit
• Include just X-pipe and Y-pipe since we are only focusing on
addu, addiu, and mul instructions
Example Execution Diagrams
a : mul r1, r2, r3
b : addiu r11, r10, 1
c : mul r5, r1, r4
d : mul r7, r5, r6
e : addiu r12, r11, 1
f : addiu r13, r12, 1
g : addiu r14, r12, 2
0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19
4
3. I2OE: IO Front-End/Issue, OOO Completion, Early Commit
3. IO Front-End/Issue, OOO Completion, Early Commit
Front-End or Writeback or Data
Fetch/Decode Issue Completion Commit Structures
I3L io io io late
I2OE io io ooo early SB
I2OL io io ooo late SB, ROB
IO2E io ooo ooo early SB, IQ
IO2L io ooo ooo late SB, IQ, ROB
Cannonical I2OE Pipeline
F D1
X
1 W1
Y0 Y1 Y2 Y3
ARF
ARFread
I 1
write
SB
SBread/write
• Remove “dummy” pipeline stages
• Fewer bypass paths, signiﬁcantly reduces hardware complexity
– I3L has six bypass paths
– I2OE has three bypass paths
– Bypass from end of Y3, end of X, and W to end of I
• Scoreboard is used to centralize structural/data hazard detection
• WAW hazards are possible, which we ignore in this topic
• WAR hazards are not possible
• NOTE: Fewer stages does not necessarily mean better performance!
5
3. I2OE: IO Front-End/Issue, OOO Completion, Early Commit
Data Structure: Scoreboard
• Indexed by functional unit
– V: valid bit
– rdest: destination reg speciﬁer
– Entries shift to right every cycle
• Structural hazards: addu and
addiu check col 2 valid bit to
ensure no structural hazard on
WB port
• RAW hazards: I stage compares
current instruction source reg
speciﬁers with every valid
entry in SB
– match in col 2–4 = stall I
– match in col 0–1 = bypass into I
– no match = read ARF
• Large number of comparisons
make accessing SB expensive
• Indexed by reg speciﬁer
– P: pending bit
– FU: functional unit
– WA: when available?
– WA bits shift to right every cycle
• Structural hazards: addu and
addiu check no bits are set in
col 2 to ensure no structural
hazard on WB port
• I stage compares checks
pending bit for each source
register speciﬁer
– pending bit set = check WA to
see if stall or bypass (FU says
where to bypass from)
– pending bit clear = read ARF
• Can use SB to stall to prevent
WAW hazards
6
3. I2OE: IO Front-End/Issue, OOO Completion, Early Commit
Example Execution Diagrams
a : mul r1, r2, r3
b : addiu r11, r10, 1
c : mul r5, r1, r4
d : mul r7, r5, r6
e : addiu r12, r11, 1
f : addiu r13, r12, 1
g : addiu r14, r12, 2
0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19
WA Entry
cycle D I r1 r5 r7 r11 r12 r13 r14
0
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
7
3. I2OE: IO Front-End/Issue, OOO Completion, Early Commit
Handling Precise Exceptions
Early commit requires the commit point to be in the decode stage.
What if instruction d causes an exception?
a : mul r1, r2, r3
b : addiu r11, r10, 1
c : mul r5, r1, r4
d : mul r7, r5, r6
e : addiu r12, r11, 1
f : addiu r13, r12, 1
g : addiu r14, r12, 2
0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19
Not usually possible to detect all exceptions in the front-end, which
motivates our interest in supporting late commit at the end of the
pipeline.
8
4. I2OL: IO Front-End/Issue, OOO Completion, Late Commit
4. IO Front-End/Issue, OOO Completion, Late Commit
Front-End or Writeback or Data
Fetch/Decode Issue Completion Commit Structures
I3L io io io late
I2OE io io ooo early SB
I2OL io io ooo late SB, ROB
IO2E io ooo ooo early SB, IQ
IO2L io ooo ooo late SB, IQ, ROB
Cannonical I2OL Pipeline
F D1
X
1
Y0 Y1 Y2 Y3
PRF
ARF
I 1
write
SB ARF
W C1 1
SBread/write
PRFread write
ROB writealloc read/dealloc
ROB
1
read
• Add extra C stage for commit at end of pipeline
• Still use scoreboard to centeralize structural/data hazard detection
• Add physical regﬁle (PRF) and reorder buffer (ROB) between W/C
• PRF keeps uncommited results (a.k.a. future regﬁle, working regﬁle)
• Reorder buffer (ROB)
– allocated in-order in D stage
– updated out-of-order in W stage
– deallocated in-order in C stage
• WAW hazards are possible, which we ignore in this topic
• WAR hazards are not possible
9
4. I2OL: IO Front-End/Issue, OOO Completion, Late Commit
Data Structure: Reorder Buffer
• ROB ﬁelds
– V: valid bit (is this entry valid?)
– P: pending bit (instruction in ﬂight targeting this entry)
– V: valid bit (is the dest reg speciﬁer valid?)
– rdest: destination reg speciﬁer
• ROB managed like a queue, implemented with circular buffer
– new instructions allocated ROB entries at tail
– instructions update pending bit out-of-order
– commit stage waits for pending bit of head to be clear
10
4. I2OL: IO Front-End/Issue, OOO Completion, Late Commit
Example Execution Diagrams
a : mul r1, r2, r3
b : addiu r11, r10, 1
c : mul r5, r1, r4
d : mul r7, r5, r6
e : addiu r12, r11, 1
f : addiu r13, r12, 1
g : addiu r14, r12, 2
0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19
v
Reorder Buffer
p0
p1
p2
p3
p4
p5
p6
rdest
Physical Register File
r1
r2
r3
r4
r5
r6
r7
r31
...
r8
r9
r10
...
r1
r2
r3
r4
r5
r6
r7
r31
...
r8
r9
r10
...
Architectural Register File
r11
r12
r13
r14
r11
r12
r13
r14
1
2
3
4
21
1
2
3
4
21
p
11
4. I2OL: IO Front-End/Issue, OOO Completion, Late Commit
We can use a table to compactly illustrate how the ROB works.
ROB Entry
cycle D I 0 1 2 3
0
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
12
4. I2OL: IO Front-End/Issue, OOO Completion, Late Commit
Handling Precise Exceptions
Late commit means exceptions are handled in the C stage at the end of
the pipeline. What if instruction a causes an exception?
a : mul r1, r2, r3
b : addiu r11, r10, 1
c : mul r5, r1, r4
d : mul r7, r5, r6
e : addiu r12, r11, 1
f : addiu r13, r12, 1
g : addiu r14, r12, 2
0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19
Need to copy values from ARF to PRF on an exception before
redirecting the front of the pipeline to the exception handler. This copy
may take multiple cycles. Also possible to include additional bits in I
stage to indicate wether the most recent version of every given
architectural register is in the ARF or PRF.
13
5. IO2E: IO Front-End, OOO Issue/Completion, Early Commit
5. IO Front-End, OOO Issue/Completion, Early Commit
Front-End or Writeback or Data
Fetch/Decode Issue Completion Commit Structures
I3L io io io late
I2OE io io ooo early SB
I2OL io io ooo late SB, ROB
IO2E io ooo ooo early SB, IQ
IO2L io ooo ooo late SB, IQ, ROB
Cannonical IO2E Pipeline
F D1
X
Y0 Y1 Y2 Y3
ARF
I 1
SB
W1 1
SBread/write
ARF read write
IQ writealloc
IQ
read/dealloc
1
• Still use scoreboard to centeralize structural/data hazard detection
• Add issue queue (IQ) between D and I stages
– allocated in-order in D stage
– updated out-of-order in W stage
– deallocated out-of-order in I stage
• Do not necessarily want to wait for W stage to update IQ; we will
need to assume aggressive bypassing which requires combinational
communication between last stage of functional unit and I stage
• WAW hazards are possible, which we ignore in this topic
• WAR hazards are possible, which we ignore in this topic
14
5. IO2E: IO Front-End, OOO Issue/Completion, Early Commit
Data Structure: Issue Queue
• IQ ﬁelds
– V: valid bit (is this entry valid?)
– op: instruction opcode
– imm immediate value
– V: valid bit (is the dest/src reg speciﬁer valid?)
– P: pending bit (is the src data ready?)
– rdest/rsrc: destination/source reg speciﬁers
• IQ managed like a queue, implemented with circular buffer
– new instructions allocated IQ entries at tail
– instructions leave IQ out-of-order when ready
• Wakeup Logic: An instruction needs to update pending bits of
dependent instructions when that instruction is in W stage (actually
need to do this earlier to enable aggressive bypassing)
• Select Logic: Determine which instructions are ready to be issued,
and then select which one to actually issue. Usually issue oldest
ready instruction.
inst_ready = ( !val_src0 || !p_src0 )
&& ( !val_src1 || !p_src1 )
&& no structural hazards
15
5. IO2E: IO Front-End, OOO Issue/Completion, Early Commit
Example Execution Diagrams
a : mul r1, r2, r3
b : addiu r11, r10, 1
c : mul r5, r1, r4
d : mul r7, r5, r6
e : addiu r12, r11, 1
f : addiu r13, r12, 1
g : addiu r14, r12, 2
0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19
op imm v v v p p rdest rsrc0 rsrc1
Issue Queue
r1
r2
r3
r4
r5
r6
r7
r31
...
r8
r9
r10
...
r11
r12
r13
r14
1
2
3
4
21
Architectural Register File
16
5. IO2E: IO Front-End, OOO Issue/Completion, Early Commit
We can use a table to compactly illustrate how the IQ works.
IQ Entry
cycle D I 0 1 2
0
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
17
5. IO2E: IO Front-End, OOO Issue/Completion, Early Commit
Handling Precise Exceptions
Early commit requires the commit point to be in the decode stage.
What if instruction e causes an exception?
a : mul r1, r2, r3
b : addiu r11, r10, 1
c : mul r5, r1, r4
d : mul r7, r5, r6
e : addiu r12, r11, 1
f : addiu r13, r12, 1
g : addiu r14, r12, 2
0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19
Performance Beneﬁt of OOO Execution
Does IO2E improve performance compared to I2OE? Let’s assume all
instructions are in issue queue.
a : mul r1, r2, r3
b : addiu r11, r10, 1
c : mul r5, r1, r4
d : mul r7, r5, r6
e : addiu r12, r11, 1
f : addiu r13, r12, 1
g : addiu r14, r12, 2
0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19
18
5. IO2E: IO Front-End, OOO Issue/Completion, Early Commit
Centeralized vs. Distributed IQs
IQs can either be centeralized or distributed across functional units.
Distributed IQs are sometimes called reservation stations. This can
naturally enable superscalar execution.
F D1
X
Y0 Y1 Y2 Y3Iy 1
W1
1
IQy
1
Ix1 1IQx
19
6. IO2L: IO Front-End, OOO Issue/Completion, Late Commit
6. IO Front-End, OOO Issue/Completion, Late Commit
Front-End or Writeback or Data
Fetch/Decode Issue Completion Commit Structures
I3L io io io late
I2OE io io ooo early SB
I2OL io io ooo late SB, ROB
IO2E io ooo ooo early SB, IQ
IO2L io ooo ooo late SB, IQ, ROB
Cannonical IO2L Pipeline
F D1
X
Y0 Y1 Y2 Y3
I 1
SB
1 1
IQalloc
IQ
read/dealloc
1
PRF
write
ARF
W C1 1
write
write read/dealloc
ROB
ARF
SBread/write
PRF read
ROBalloc
read
• Use scoreboard to centeralize structural/data hazard detection
• Use IQ to enable out-of-order issue, ROB to enable late commit
• Overall organization:
– In-order fetc/decode (front-end of pipeline)
– Out-of-order issue/completion (middle of pipeline)
– In-order commit (back-end of pipeline)
• WAW hazards are possible, which we ignore in this topic
• WAR hazards are possible, which we ignore in this topic
20
6. IO2L: IO Front-End, OOO Issue/Completion, Late Commit
Example Execution Diagrams
a : mul r1, r2, r3
b : addiu r11, r10, 1
c : mul r5, r1, r4
d : mul r7, r5, r6
e : addiu r12, r11, 1
f : addiu r13, r12, 1
g : addiu r14, r12, 2
0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19
Handling Precise Exceptions
Late commit means exceptions are handled in the C stage at the end of
the pipeline. What if instruction a causes an exception?
a : mul r1, r2, r3
b : addiu r11, r10, 1
c : mul r5, r1, r4
d : mul r7, r5, r6
e : addiu r12, r11, 1
f : addiu r13, r12, 1
g : addiu r14, r12, 2
0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19
21
6. IO2L: IO Front-End, OOO Issue/Completion, Late Commit
Out-of-Order Dual-Issue Processor
Assume we can fetch, decode, issue, writeback, and commit two
instructions per cycle.
a : mul r1, r2, r3
b : addiu r11, r10, 1
c : mul r5, r1, r4
d : mul r7, r5, r6
e : addiu r12, r11, 1
f : addiu r13, r12, 1
g : addiu r14, r12, 2
0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19
22