---
archive_policy: text-only
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-d0a3c3a29431
  position:
    end: 25230
    start: 25162
    type: TextPositionSelector
  quote_sha256: sha256:2aa06f15fbbe847a704e252ddae01321375fcfb47f7d9b7530d0ffbefe018c8b
  selector:
    exact: Hazards occur when instructions interact with each other in pipeline
    prefix: 'uctions were

      repeated 10 times?

      '
    suffix: '

      • RAW Data Hazards: An instruct'
    type: TextQuoteSelector
  selector_sha256: sha256:ce73c78b9aa72aaacca96ad7602eec6a6ca89d0706846ae590f3216a50c223a2
  snapshot_sha256: sha256:d20d0a30b8a23a497534a6dc4acdb6c0b9a51b8685e97ddb440e73a747e638ed
- evidence_id: evidence-e8b610e81cbb
  position:
    end: 29150
    start: 29024
    type: TextPositionSelector
  quote_sha256: sha256:de25639808cc3bcd3a603db29f1570f44855fc3a0b0acca0209ceabfdb82f421
  selector:
    exact: 'RAW data hazards occur when one instruction depends on a data value

      produced by a preceding instruction still in the pipeline.'
    prefix: 'eline Hazards: RAW Data Hazards

      '
    suffix: ' We use archi-

      tectural dependen'
    type: TextQuoteSelector
  selector_sha256: sha256:728634782be403f0711e42cc2539491cb81bf747478c5a539a29e4729f4e1e26
  snapshot_sha256: sha256:d20d0a30b8a23a497534a6dc4acdb6c0b9a51b8685e97ddb440e73a747e638ed
- evidence_id: evidence-2ccbb906f313
  position:
    end: 25453
    start: 25327
    type: TextPositionSelector
  quote_sha256: sha256:f1a6b489db73158fbf6376704fb0dfde98c2c8a9c9755b833288ae7fc4bf4c94
  selector:
    exact: 'Control Hazards: Whether or not an instruction should be executed

      depends on a control decision made by an earlier instruction'
    prefix: 'ced by an earlier instruction

      • '
    suffix: '

      • Structural Hazards: An instru'
    type: TextQuoteSelector
  selector_sha256: sha256:ee567c604c9f3750fc95dc76caead93729b48fdb3168e99de8a71b75e8392e9c
  snapshot_sha256: sha256:d20d0a30b8a23a497534a6dc4acdb6c0b9a51b8685e97ddb440e73a747e638ed
- evidence_id: evidence-c69b9407150e
  position:
    end: 25573
    start: 25456
    type: TextPositionSelector
  quote_sha256: sha256:71dbc9b55c1a481eb72c0111a1ed29fd776b40152144593685ce7b14b951b215
  selector:
    exact: 'Structural Hazards: An instruction in the pipeline needs a resource

      being used by another instruction in the pipeline'
    prefix: 'ade by an earlier instruction

      • '
    suffix: '

      • WAW and WAR Name Hazards: An '
    type: TextQuoteSelector
  selector_sha256: sha256:15fd83ef04746e2b0e2f6fbf9437826a626879c8d39215a19d547d399cee2266
  snapshot_sha256: sha256:d20d0a30b8a23a497534a6dc4acdb6c0b9a51b8685e97ddb440e73a747e638ed
- evidence_id: evidence-6438b00733d1
  position:
    end: 25727
    start: 25576
    type: TextPositionSelector
  quote_sha256: sha256:d5feeb22f494422ee2b2fe8549175956b1130fefd283d1f68337f9c0e064ea07
  selector:
    exact: 'WAW and WAR Name Hazards: An instruction in the pipeline is

      writing a register that an earlier instruction in the pipeline is either

      writing or reading'
    prefix: 'r instruction in the pipeline

      • '
    suffix: '

      Stalling and squashing instruct'
    type: TextQuoteSelector
  selector_sha256: sha256:aa5e2436cf0cd0f8374a6a209e7e688a17253982eab29e040f184ab7528f3239
  snapshot_sha256: sha256:d20d0a30b8a23a497534a6dc4acdb6c0b9a51b8685e97ddb440e73a747e638ed
- evidence_id: evidence-c8f472b47898
  position:
    end: 29991
    start: 29847
    type: TextPositionSelector
  quote_sha256: sha256:f8e684f82b100790595f35eae8c0ed1efcf0d1799b027452edecd32c5484af9c
  selector:
    exact: 'Hardware Scheduling: Hardware dynamically schedules

      instructions to avoid RAW hazards, potentially allowing

      instructions to execute out of order'
    prefix: 'e scheduling for correctness)

      • '
    suffix: '

      • Hardware Stalling: Hardware i'
    type: TextQuoteSelector
  selector_sha256: sha256:b50dd27ab6c1e6c7d930e53851183cb148894eead320de5f35050da81a99b8a0
  snapshot_sha256: sha256:d20d0a30b8a23a497534a6dc4acdb6c0b9a51b8685e97ddb440e73a747e638ed
- evidence_id: evidence-122ba33565ec
  position:
    end: 39310
    start: 39073
    type: TextPositionSelector
  quote_sha256: sha256:5d6ae613e11d59fdfd688dc371ed270454d6490e93453b008296d109cc0ba4ff
  selector:
    exact: 'Hardware Speculation: Hardware guesses which way the control

      ﬂow will go and potentially fetches incorrect instructions; detects

      when there is a problem and re-executes instructions the instructions

      that are along the correct control ﬂow'
    prefix: 'execute

      based on a data value

      • '
    suffix: '

      • Software Hints: Programmer or'
    type: TextQuoteSelector
  selector_sha256: sha256:0fe3568dfa654cb77a84f8d19e9a048a47fecc095d4243fe49b16a08f4dede85
  snapshot_sha256: sha256:d20d0a30b8a23a497534a6dc4acdb6c0b9a51b8685e97ddb440e73a747e638ed
extractor: pypdf/6.16.2
id: cornell-processor-microarchitecture
media_type: application/pdf
origin: external
read_status: retrieved
retrieval:
  acquisition: fetch
  resolved_url: https://bpb-us-w2.wpmucdn.com/sites.coecis.cornell.edu/dist/4/81/files/2017/03/ece4750_handout3-2n31ilm.pdf
  url: https://ocw.ece.cornell.edu/files/2017/03/ece4750_handout3-2n31ilm.pdf
schema_version: source/v1
snapshot_sha256: sha256:d20d0a30b8a23a497534a6dc4acdb6c0b9a51b8685e97ddb440e73a747e638ed
source_type: doc
vault_id: public
---
ECE 4750 Computer Architecture, Fall 2015
T02 Fundamental Processor Microarchitecture
School of Electrical and Computer Engineering
Cornell University
revision: 2015-09-23-20-19
1 Processor Microarchitectural Design Patterns 3
1.1. Transactions and Steps . . . . . . . . . . . . . . . . . . . . . . . . . . 3
1.2. Microarchitecture: Control/Datapath Split . . . . . . . . . . . . . . 4
2 PARCv1 Single-Cycle Processor 5
2.1. High-Level Idea for Single-Cycle Processors . . . . . . . . . . . . . . 6
2.2. Single-Cycle Processor Datapath . . . . . . . . . . . . . . . . . . . . 7
2.3. Single-Cycle Processor Control Unit . . . . . . . . . . . . . . . . . . 12
2.4. Analyzing Performance . . . . . . . . . . . . . . . . . . . . . . . . . 12
3 PARCv1 FSM Processor 15
3.1. High-Level Idea for FSM Processors . . . . . . . . . . . . . . . . . . 16
3.2. FSM Processor Datapath . . . . . . . . . . . . . . . . . . . . . . . . . 16
3.3. FSM Processor Control Unit . . . . . . . . . . . . . . . . . . . . . . . 23
3.4. Analyzing Performance . . . . . . . . . . . . . . . . . . . . . . . . . 27
4 PARCv1 Pipelined Processor 29
4.1. High-Level Idea for Pipelined Processors . . . . . . . . . . . . . . . 30
4.2. Pipelined Processor Datapath and Control Unit . . . . . . . . . . . . 32
5 Pipeline Hazards: RAW Data Hazards 37
5.1. Expose in Instruction Set Architecture . . . . . . . . . . . . . . . . . 39
5.2. Hardware Stalling . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 40
5.3. Hardware Bypassing/Forwarding . . . . . . . . . . . . . . . . . . . 41
5.4. RAW Data Hazards Through Memory . . . . . . . . . . . . . . . . . 45
6 Pipeline Hazards: Control Hazards 46
6.1. Expose in Instruction Set Architecture . . . . . . . . . . . . . . . . . 48
6.2. Hardware Speculation . . . . . . . . . . . . . . . . . . . . . . . . . . 49
6.3. Interrupts and Exceptions . . . . . . . . . . . . . . . . . . . . . . . . 52
7 Pipeline Hazards: Structural Hazards 57
7.1. Expose in Instruction Set Architecture . . . . . . . . . . . . . . . . . 58
7.2. Hardware Stalling . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 58
7.3. Hardware Duplication . . . . . . . . . . . . . . . . . . . . . . . . . . 59
8 Pipeline Hazards: WAW and WAR Name Hazards 60
8.1. Software Renaming . . . . . . . . . . . . . . . . . . . . . . . . . . . . 61
8.2. Hardware Stalling . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 62
9 Summary of Processor Performance 62
10 Case Study: Transition from CISC to RISC 66
10.1. Example CISC: IBM 360/M30 . . . . . . . . . . . . . . . . . . . . . . 67
10.2. Example RISC: MIPS R2K . . . . . . . . . . . . . . . . . . . . . . . . 70
2
1. Processor Microarchitectural Design Patterns 2.0. Transactions and Steps
1. Processor Microarchitectural Design Patterns
Time
Program = Instructions
Program × Cycles
Instruction× Time
Cycles
• Instructions / program depends on source code, compiler, ISA
• Cycles / instruction (CPI) depends on ISA, microarchitecture
• Time / cycle depends upon microarchitecture and implementation
Microarchitecture CPI Cycle Time
Single-Cycle Processor 1 long
FSM Processor >1 short
Pipelined Processor ≈1 short
1.1. Transactions and Steps
• We can think of each instruction as a transaction
• Executing a transaction involves a sequence of steps
addu addiu mul lw sw j jal jr bne
Fetch Instruction         
Decode Instruction         
Read Registers       
Register Arithmetic      
Read Memory 
Write Memory 
Write Registers     
Update PC         
3
1. Processor Microarchitectural Design Patterns 1.2. Microarchitecture: Control/Datapath Split
1.2. Microarchitecture: Control/Datapath Split
Control Signals Status Signals
Control Unit
Datapath
imem
req_val
imem
req
imem
resp
dmem
req_val
dmem
req
dmem
resp
Memory
4
2. PARCv1 Single-Cycle Processor 2.1. High-Level Idea for Single-Cycle Processors
2. PARCv1 Single-Cycle Processor
Time
Program = Instructions
Program × Cycles
Instruction× Time
Cycles
• Instructions / program depends on source code, compiler, ISA
• Cycles / instruction (CPI) depends on ISA, microarchitecture
• Time / cycle depends upon microarchitecture and implementation
Microarchitecture CPI Cycle Time
Single-Cycle Processor 1 long
FSM Processor >1 short
Pipelined Processor ≈1 short
Technology Constraints
• Assume technology where
logic is not too expensive, so
we do not need to overly
minimize the number of
registers and combinational
logic
• Assume multi-ported register
ﬁle with a reasonable number
of ports is feasible
• Assume a dual-ported
combinational memory
Control Status
Control Unit
Datapath
<1 cycle
combinational
Memory
regfile
imem
req
imem
resp
dmem
req
dmem
resp
5
2. PARCv1 Single-Cycle Processor 2.1. High-Level Idea for Single-Cycle Processors
2.1. High-Level Idea for Single-Cycle Processors
addu addiu mul lw sw j jal jr bne
Fetch Instruction         
Decode Instruction         
Read Registers       
Register Arithmetic      
Read Memory 
Write Memory 
Write Registers     
Update PC         
Fetch
Inst
lw
Decode
Inst
Reg
Arith
Read
Mem
Write
Reg
Read
Reg
Update
PC
Fetch
Inst
addu
Decode
Inst
Reg
Arith
Write
Reg
Read
Reg
Update
PC
Fetch
Inst
Decode
Inst
Update
PC
j
Single-Cycle
6
2. PARCv1 Single-Cycle Processor 2.2. Single-Cycle Processor Datapath
2.2. Single-Cycle Processor Datapath
Implementing ADDU Instruction
pc regfile
(read) regfile
(write)
rf
_wen
rf
_waddr
Implementing ADDIU Instruction
pc regfile
(read) regfile
(write)
rf
_wen
rf
_waddr
7
2. PARCv1 Single-Cycle Processor 2.2. Single-Cycle Processor Datapath
Implementing ADDU and ADDIU Instructions
pc regfile
(read) regfile
(write)
rf
_wen
rf
_waddr
alu
ir[20:16]
ir[25:21]
+4
imemreq.
addr
To control unit
pc_plus4
imemresp.
data
op1
_sel
sext
ir[15:0]
Adding the MUL Instruction
pc regfile
(read) regfile
(write)
rf
_wen
rf
_waddr
alu
ir[20:16]
ir[25:21]
+4
imemreq.
addr
To control unit
pc_plus4
imemresp.
data
op1
_sel
sext
ir[15:0]
mul
wb_sel
8
2. PARCv1 Single-Cycle Processor 2.2. Single-Cycle Processor Datapath
Adding the LW and SW Instructions
pc regfile
(read) regfile
(write)
rf
_wen
rf
_waddr
alu
ir[20:16]
ir[25:21]
+4
imemreq.
addr
To control unit
pc_plus4
imemresp.
data
op1
_sel
sext
ir[15:0]
mul
wb_sel
dmemresp.
data
dmemreq.
addr
Adding the J Instruction
pc regfile
(read) regfile
(write)
rf
_wen
rf
_waddr
alu
ir[20:16]
ir[25:21]
+4
imemreq.
addr
To control unit
pc_plus4
imemresp.
data
op1
_sel
sext
ir[15:0]
mul
wb_sel
dmemresp.
data
dmemreq.
addr
dmemreq.
data
ir[25:0]
j_tgen
j_targ
pc_sel
9
2. PARCv1 Single-Cycle Processor 2.2. Single-Cycle Processor Datapath
Adding the JAL and JR Instructions
pc regfile
(read) regfile
(write)
rf
_wen
rf
_waddr
alu
ir[20:16]
ir[25:21]
+4
imemreq.
addr
To control unit
pc_plus4
imemresp.
data
op1
_sel
sext
ir[15:0]
mul
wb_sel
dmemresp.
data
dmemreq.
addr
dmemreq.
data
ir[25:0]
j_tgen
j_targ
pc_sel
alu_func
Adding the BNE Instruction
pc regfile
(read) regfile
(write)
rf
_wen
rf
_waddr
alu
ir[20:16]
ir[25:21]
+4
imemreq.
addr
To control unit
pc_plus4
imemresp.
data
op1
_sel
sext
ir[15:0]
mul
wb_sel
dmemresp.
data
dmemreq.
addr
dmemreq.
data
ir[25:0]
j_tgen
j_targ
pc_sel
alu_func
jr
ir[15:0]
br_tgen
eq
br_targ
10
2. PARCv1 Single-Cycle Processor 2.2. Single-Cycle Processor Datapath
Adding a New Auto-Incrementing Load Instruction
Draw on the datapath diagram what paths we need to use as well as
any new paths we will need to add in order to implement the following
auto-incrementing load instruction.
lw.ai rt, offset(rs)
R[rt]← M[ R[rs] + sext(offset) ]; R[rs]← R[rs] + 4
pc regfile
(read) regfile
(write)
rf
_wen
rf
_waddr
alu
ir[20:16]
ir[25:21]
+4
imemreq.
addr
To control unit
pc_plus4
imemresp.
data
op1
_sel
sext
ir[15:0]
mul
wb_sel
dmemresp.
data
dmemreq.
addr
dmemreq.
data
ir[25:0]
j_tgen
j_targ
pc_sel
alu_func
jr
ir[15:0]
br_tgen
eq
br_targ
11
2. PARCv1 Single-Cycle Processor 2.3. Single-Cycle Processor Control Unit
2.3. Single-Cycle Processor Control Unit
imem dmem
pc op1 alu wb rf rf req req
inst sel sel func sel waddr wen val val
addu pc+4 rf + alu rd 1 1 0
addiu
mul pc+4 rf × mul rd 1 1 0
lw pc+4 sext + mem rt 1 1 1
sw
j j_targ – – – – 0 1 0
jal
jr jr – – – – 0 1 0
bne
lw.ai
2.4. Analyzing Performance
Time
Program = Instructions
Program × Cycles
Instruction× Time
Cycles
• Instructions / program depends on source code, compiler, ISA
• Cycles / instruction (CPI) depends on ISA, microarchitecture
• Time / cycle depends upon microarchitecture and implementation
12
2. PARCv1 Single-Cycle Processor 2.4. Analyzing Performance
Estimating cycle time
There are many paths through the design that start at a state element
and end at a state element. The “critical path” is the longest path across
all of these paths. We can usually use a simple ﬁrst-order static timing
estimate to estimate the cycle time (i.e., the clock period and thus also
the clock frequency).
pc regfile
(read) regfile
(write)
rf
_wen
rf
_waddr
alu
ir[20:16]
ir[25:21]
+4
imemreq.
addr
To control unit
pc_plus4
imemresp.
data
op1
_sel
sext
ir[15:0]
mul
wb_sel
dmemresp.
data
dmemreq.
addr
dmemreq.
data
ir[25:0]
j_tgen
j_targ
pc_sel
alu_func
jr
ir[15:0]
br_tgen
eq
br_targ
• register read = 1τ
• register write = 1τ
• regﬁle read = 10τ
• regﬁle write = 10τ
• memory read = 20τ
• memory write = 20τ
• +4 unit = 4τ
• sext unit = 1τ
• br_tgen = 8τ
• j_tgen = 1τ
• mux = 3τ
• multiplier = 20τ
• alu = 10τ
13
2. PARCv1 Single-Cycle Processor 2.4. Analyzing Performance
Estimating execution time
Using our ﬁrst-order equation for processor performance, how long in
nanoseconds will it take to execute the vector-vector add example as-
suming n is 64?
loop:
lw r12, 0(r4)
lw r13, 0(r5)
addu r14, r12, r13
sw r14, 0(r6)
addiu r4, r4, 4
addiu r5, r5, 4
addiu r6, r6, 4
addiu r7, r7, -1
bne r7, r0, loop
jr r31
Using our ﬁrst-order equation for processor performance, how long in
nanoseconds will it take to execute the mystery program assuming n is
64 and that we ﬁnd a match on the last element.
addiu r12, r0, 0
loop:
lw r13, 0(r4)
bne r13, r6, foo
addiu r2, r12, 0
jr r31
foo:
addiu r4, r4, 4
addiu r12, r12, 1
bne r12, r5, loop
addiu r2, r0, -1
jr r31
14
3. PARCv1 FSM Processor 3.1. High-Level Idea for FSM Processors
3. PARCv1 FSM Processor
Time
Program = Instructions
Program × Cycles
Instruction× Time
Cycles
• Instructions / program depends on source code, compiler, ISA
• Cycles / instruction (CPI) depends on ISA, microarchitecture
• Time / cycle depends upon microarchitecture and implementation
Microarchitecture CPI Cycle Time
Single-Cycle Processor 1 long
FSM Processor >1 short
Pipelined Processor ≈1 short
Technology Constraints
• Assume legacy technology
where logic is expensive, so
we want to minimize the
number of registers and
combinational logic
• Assume an (unrealistic)
combinational memory
• Assume multi-ported register
ﬁles and memories are too
expensive, these structures
can only have a single
read/write port
Control Status
Control Unit
Datapath
<1 cycle
combinational
Memory
regfile
mem
req
mem
resp
15
3. PARCv1 FSM Processor 3.1. High-Level Idea for FSM Processors
3.1. High-Level Idea for FSM Processors
addu addiu mul lw sw j jal jr bne
Fetch Instruction         
Decode Instruction         
Read Registers       
Register Arithmetic      
Read Memory 
Write Memory 
Write Registers     
Update PC         
Fetch
Inst
lw
Decode
Inst
Reg
Arith
Read
Mem
Write
Reg
Read
Reg
Update
PC
Fetch
Inst
addu
Decode
Inst
Reg
Arith
Write
Reg
Read
Reg
Update
PC
Fetch
Inst
Decode
Inst
Update
PC
j
Single-Cycle
j
Fetch
Inst
lw
Decode
Inst
Reg
Arith
Read
Mem
Write
Reg
Read
Reg
Update
PC
Fetch
Inst
addu
Decode
Inst
Reg
Arith
Write
Reg
Read
Reg
Update
PC
Fetch
Inst
Decode
Inst
Update
PC
FSM
3.2. FSM Processor Datapath
Implementing an FSM datapath requires thinking about the required
FSM states, but we will defer discussion of how to implement the control
logic to the next section.
16
3. PARCv1 FSM Processor 3.2. FSM Processor Datapath
Implementing Fetch Sequence
PC IR
ir_enpc_en
Datapath Bus
pc_
bus_en
A
a_en
+4
alu_
bus_en
memresp.
data
memreq.
addr
RD
rd_
bus_en
To control unit
F0
F1
F2
(pseudo-control-signal syntax)
17
3. PARCv1 FSM Processor 3.2. FSM Processor Datapath
Implementing ADDU Instruction
PC IR
ir_enpc_en
Datapath Bus
pc_
bus_en
A
a_en
+4
alu_
bus_en
memresp.
data
memreq.
addr
RD
rd_
bus_en
To control unit
B
b_en
RF
rf_wen
rf_
bus_en
alu_
func
alu func
alu
rf_addr
_sel
rs
rt
rd
A + 4 +4:
A + B +:
F0
F1
F2
A0
A1
A2
(pseudo-control-signal syntax)
addu rd, rs, rt
18
3. PARCv1 FSM Processor 3.2. FSM Processor Datapath
Full Datapath for PARCv1 FSM Processor
PC IR
ir_enpc_en
Datapath Bus
pc_
bus_en
A
a_en
+4
alu_
bus_en
memresp.
data
memreq.
addr
RD
rd_
bus_en
To control unit
B
b_en
RF
rf_wen
rf_
bus_en
alu_
func
alu func
alu
rf_addr
_sel
rs
rt
rd
A + 4 +4:
A + B +:
sext
imm
iau_
bus_en
>>
b_sel
>>C
c_sel
c_en
0
A +? B +?:
memreq.
data
WD
wd_en
iau_
func
jt: { A[31:28], B[27:0] }
iau func
iau
A == B cmp:
sext(IR[15:0]) si: 
IR[25:0] << 2 ts:
31
alu_
bus_en
eq
sext(IR[15:0]) << 2 sis:
F0
F1
F2
A0
A1
A2
AI0
AI1
AI2
M0
M1
M2
M34
M3
L0
L1
L2
L3
S0
S1
S2
S3
J0
J1
JA0
JA1
JA2
JR0 B0
B1
B2
B3
B4
ADDIU Pseudo-Control-Signal
Fragment
addiu rd, rs, imm
19
3. PARCv1 FSM Processor 3.2. FSM Processor Datapath
MUL Instruction
mul rd, rs, rt
M0: A← RF[r0]
M1: B← RF[rs]
M2: C← RF[rt]
M3: A← A +? B;
B← B << 1; C← C >> 1
M4: A← A +? B;
B← B << 1; C← C >> 1
...
M35: RF[rd]← A +? B; goto F0
LW Instruction
lw rt, offset(rs)
L0: A← RF[rs]
L1: B← sext(offset)
L2: memreq.addr← A + B
L3: RF[rt]← RD; goto F0
SW Instruction
sw rt, offset(rs)
S0: WD← RF[rt]
S1: A← RF[rs]
S2: B← sext(imm)
S3: memreq.addr← A + B; goto F0
J Instruction
j targ
J0: B← targ << 2
J1: PC← A jt B; goto F0
JAL Instruction
jal targ
JA0: RF[31]← PC
JA1: B← targ << 2
JA2: PC← A jt B; goto F0
JR Instruction
jr rs
JR0: PC← RF[rs]; goto F0
BNE Instruction
bne rs, rt, offset
B0: A← RF[rs]
B1: B← RF[rt]
B2: A← sext(offset) << 2;
if A == B goto F0
B3: B← PC
B4: PC← A + B; goto F0
20
3. PARCv1 FSM Processor 3.2. FSM Processor Datapath
Adding a Complex Instruction
FSM processors simplify adding complex instructions. New instructions
usually do not require datapath modiﬁcations, only additional states.
addu.mm rd, rs, rt
M[ R[rd] ]← M[ R[rs] ] + M[ R[rt] ]
PC IR
ir_enpc_en
Datapath Bus
pc_
bus_en
A
a_en
+4
alu_
bus_en
memresp.
data
memreq.
addr
RD
rd_
bus_en
To control unit
B
b_en
RF
rf_wen
rf_
bus_en
alu_
func
alu func
alu
rf_addr
_sel
rs
rt
rd
A + 4 +4:
A + B +:
sext
imm
iau_
bus_en
>>
b_sel
>>C
c_sel
c_en
0
A +? B +?:
memreq.
data
WD
wd_en
iau_
func
jt: { A[31:28], B[27:0] }
iau func
iau
A == B cmp:
sext(IR[15:0]) si: 
IR[25:0] << 2 ts:
31
alu_
bus_en
eq
sext(IR[15:0]) << 2 sis:
21
3. PARCv1 FSM Processor 3.2. FSM Processor Datapath
Adding a New Auto-Incrementing Load Instruction
Implement the following auto-incrementing load instruction using
pseudo-control-signal syntax. Modify the datapath if necessary.
lw.ai rt, offset(rs)
R[rt]← M[ R[rs] + sext(offset) ]; R[rs]← R[rs] + 4
PC IR
ir_enpc_en
Datapath Bus
pc_
bus_en
A
a_en
+4
alu_
bus_en
memresp.
data
memreq.
addr
RD
rd_
bus_en
To control unit
B
b_en
RF
rf_wen
rf_
bus_en
alu_
func
alu func
alu
rf_addr
_sel
rs
rt
rd
A + 4 +4:
A + B +:
sext
imm
iau_
bus_en
>>
b_sel
>>C
c_sel
c_en
0
A +? B +?:
memreq.
data
WD
wd_en
iau_
func
jt: { A[31:28], B[27:0] }
iau func
iau
A == B cmp:
sext(IR[15:0]) si: 
IR[25:0] << 2 ts:
31
alu_
bus_en
eq
sext(IR[15:0]) << 2 sis:
22
3. PARCv1 FSM Processor 3.3. FSM Processor Control Unit
3.3. FSM Processor Control Unit
F0
F1
F2
A0
A1
A2
AI0
AI1
AI2
M0
M1
M2
M34
M3
L0
L1
L2
L3
S0
S1
S2
S3
J0
J1
JA0
JA1
JA2
JR0 B0
B1
B2
B3
B4
We will study three techniques
for implementing FSM control
units:
• Hardwired control units are
high-performance, but
inﬂexible
• Horizontal µcoding
increases ﬂexibility, requires
large control store
• Vertical µcoding is an
intermediate design point
Hardwired FSM
State
Control
Signal
Logic
State
Transition
Logic
Control Signals
(24)
Status Signals
(1)
23
3. PARCv1 FSM Processor 3.3. FSM Processor Control Unit
Control signal output table for hardwired control unit
PC IR
ir_enpc_en
Datapath Bus
pc_
bus_en
A
a_en
+4
alu_
bus_en
memresp.
data
memreq.
addr
RD
rd_
bus_en
To control unit
B
b_en
RF
rf_wen
rf_
bus_en
alu_
func
alu func
alu
rf_addr
_sel
rs
rt
rd
A + 4 +4:
A + B +:
sext
imm
iau_
bus_en
>>
b_sel
>>C
c_sel
c_en
0
A +? B +?:
memreq.
data
WD
wd_en
iau_
func
jt: { A[31:28], B[27:0] }
iau func
iau
A == B cmp:
sext(IR[15:0]) si: 
IR[25:0] << 2 ts:
31
alu_
bus_en
eq
sext(IR[15:0]) << 2 sis:
F0: memreq.addr← PC; A← PC
F1: IR← RD
F2: PC← A + 4; A← A + 4; goto inst
A0: A← RF[rs]
A1: B← RF[rt]
A2: RF[rd]← A + B; goto F0
Bus Enables Register Enables Mux Func RF MReq
state pc iau alu rf rd pc ir a b c wd b c iau alu sel wen val op
F0 1 0 0 0 0 0 0 1 0 0 0 – – – – – 0 1 r
F1 0 0 0 0 1 0 1 0 0 0 0 – – – – – 0 0 –
F2 0 0 1 0 0 1 0 1 0 0 0 – – – +4 – 0 0 –
A0
A1
A2
24
3. PARCv1 FSM Processor 3.3. FSM Processor Control Unit
Vertically Microcoded FSM
uPC
Control
Signals
Next
State
+1
decoderopcode
F0
eq
Next State Encoding
n : increment uPC by one
d : dispatch based on opcode
f  : goto state F0
b : goto state F0 if A == B
Control Signals (24)
bus
en
mux
sel
Status Signals
(1)
• Use memory array (called the control store) instead of random logic
to encode both the control signal logic and the state transition logic
• Enables a more systematic approach to implementing complex
multi-cycle instructions
• Microcoding can produce good performance if accessing the control
store is much faster than accessing main memory
• Read-only control stores might be replaceable enabling in-ﬁeld
updates, while read-write control stores can simplify diagnostics
and microcode patches
25
3. PARCv1 FSM Processor 3.3. FSM Processor Control Unit
Control signal store for microcoded control unit
PC IR
ir_enpc_en
Datapath Bus
pc_
bus_en
A
a_en
+4
alu_
bus_en
memresp.
data
memreq.
addr
RD
rd_
bus_en
To control unit
B
b_en
RF
rf_wen
rf_
bus_en
alu_
func
alu func
alu
rf_addr
_sel
rs
rt
rd
A + 4 +4:
A + B +:
sext
imm
iau_
bus_en
>>
b_sel
>>C
c_sel
c_en
0
A +? B +?:
memreq.
data
WD
wd_en
iau_
func
jt: { A[31:28], B[27:0] }
iau func
iau
A == B cmp:
sext(IR[15:0]) si: 
IR[25:0] << 2 ts:
31
alu_
bus_en
eq
sext(IR[15:0]) << 2 sis:
B0: A← RF[rs]
B1: B← RF[rt]
B2: A← sext(offset) << 2; if A == B goto F0
B3: B← PC
B4: PC← A + B; goto F0
Bus Enables Register Enables Mux Func RF MReq
state pc iau alu rf rd pc ir a b c wd b c iau alu sel wen val op next
B0 0 0 0 1 0 0 0 1 0 0 0 – – – – rs 0 0 –
B1 0 0 0 1 0 0 0 0 1 0 0 b – – – rt 0 0 –
B2 0 1 0 0 0 0 0 1 0 0 0 – – sis cmp – 0 0 –
B3 1 0 0 0 0 0 0 0 1 0 0 b – – – – 0 0 –
B4 0 0 1 0 0 1 0 0 0 0 0 – – – + – 0 0 –
26
3. PARCv1 FSM Processor 3.4. Analyzing Performance
3.4. Analyzing Performance
Time
Program = Instructions
Program × Cycles
Instruction× Time
Cycles
Estimating cycle time
PC IR
ir_enpc_en
Datapath Bus
pc_
bus_en
A
a_en
+4
alu_
bus_en
memresp.
data
memreq.
addr
RD
rd_
bus_en
To control unit
B
b_en
RF
rf_wen
rf_
bus_en
alu_
func
alu func
alu
rf_addr
_sel
rs
rt
rd
A + 4 +4:
A + B +:
sext
imm
iau_
bus_en
>>
b_sel
>>C
c_sel
c_en
0
A +? B +?:
memreq.
data
WD
wd_en
iau_
func
jt: { A[31:28], B[27:0] }
iau func
iau
A == B cmp:
sext(IR[15:0]) si: 
IR[25:0] << 2 ts:
31
alu_
bus_en
eq
sext(IR[15:0]) << 2 sis:
• register read/write = 1τ
• regﬁle read/write = 10τ
• mem read/write = 20τ
• iau unit = 1τ
• mux = 3τ
• alu = 10τ
• 1b shifter = 1τ
• tri-state buf = 1τ
27
3. PARCv1 FSM Processor 3.4. Analyzing Performance
Estimating execution time
Using our ﬁrst-order equation for processor performance, how long in
nanoseconds will it take to execute the vector-vector add example as-
suming n is 64?
loop:
lw r12, 0(r4)
lw r13, 0(r5)
addu r14, r12, r13
sw r14, 0(r6)
addiu r4, r4, 4
addiu r5, r5, 4
addiu r6, r6, 4
addiu r7, r7, -1
bne r7, r0, loop
jr r31
Using our ﬁrst-order equation for processor performance, how long in
nanoseconds will it take to execute the mystery program assuming n is
64 and that we ﬁnd a match on the last element.
addiu r12, r0, 0
loop:
lw r13, 0(r4)
bne r13, r6, foo
addiu r2, r12, 0
jr r31
foo:
addiu r4, r4, 4
addiu r12, r12, 1
bne r12, r5, loop
addiu r2, r0, -1
jr r31
28
4. PARCv1 Pipelined Processor 4.1. High-Level Idea for Pipelined Processors
4. PARCv1 Pipelined Processor
Time
Program = Instructions
Program × Cycles
Instruction× Time
Cycles
• Instructions / program depends on source code, compiler, ISA
• Cycles / instruction (CPI) depends on ISA, microarchitecture
• Time / cycle depends upon microarchitecture and implementation
Microarchitecture CPI Cycle Time
Single-Cycle Processor 1 long
FSM Processor >1 short
Pipelined Processor ≈1 short
Technology Constraints
• Assume modern technology
where logic is cheap and fast
(e.g., fast integer ALU)
• Assume multi-ported register
ﬁles with a reasonable
number of ports are feasible
• Assume small amount of very
fast memory (caches) backed
by large, slower memory
Control Status
Control Unit
Datapath
<1 cycle
combinational
Memory
regfile
imem
req
imem
resp
dmem
req
dmem
resp
29
4. PARCv1 Pipelined Processor 4.1. High-Level Idea for Pipelined Processors
4.1. High-Level Idea for Pipelined Processors
• Anne, Brian, Cathy, and Dave each have one load of clothes
• Washing, drying, folding, and storing each take 30 minutes
7pm 8pm 9pm 10pm 11pm 12am 1am 2am 3am
Anne's
Load
Ben's
Load
Cathy's
Load
Dave's
Load
Pipelined Laundry with Slow Dryers
Anne's
Load
7pm 8pm 9pm
Ben's
Load
Cathy's
Load
Dave's
Load
7pm 8pm 9pm 10pm 11pm
Anne's
Load
Ben's
Load
Cathy's
Load
Dave's
Load
Fixed Time-Slot Laundry
Pipelined Laundry
10pm 12am
Pipelining lessons
• Multiple transactions operate simultaneously using different resources
• Pipelining does not help the transaction latency
• Pipelining does help the transaction throughput
• Potential speedup is proportional to the number of pipeline stages
• Potential speedup is limited by the slowest pipeline stage
• Potential speedup is reduced by time to ﬁll the pipeline
30
4. PARCv1 Pipelined Processor 4.1. High-Level Idea for Pipelined Processors
Applying pipelining to processors
addu addiu mul lw sw j jal jr bne
Fetch Instruction         
Decode Instruction         
Read Registers       
Register Arithmetic      
Read Memory 
Write Memory 
Write Registers     
Update PC         
Fetch
Inst
lw
Decode
Inst
Reg
Arith
Read
Mem
Write
Reg
Read
Reg
Update
PC
Fetch
Inst
addu
Decode
Inst
Reg
Arith
Write
Reg
Read
Reg
Update
PC
Fetch
Inst
Decode
Inst
Update
PC
j
Single-Cycle
j
Fetch
Inst
lw
Decode
Inst
Reg
Arith
Read
Mem
Write
Reg
Read
Reg
Update
PC
Fetch
Inst
addu
Decode
Inst
Reg
Arith
Write
Reg
Read
Reg
Update
PC
Fetch
Inst
Decode
Inst
Update
PC
FSM
Fetch
Inst
lw
Decode
Inst
Reg
Arith
Read
Mem
Write
Reg
Read
Reg
Update
PC
Fetch
Inst
Decode
Inst
Reg
Arith
Write
Reg
Read
Reg
Update
PC
Fetch
Inst
Decode
Inst
Update
PC
addu
j
Pipelined
31
4. PARCv1 Pipelined Processor 4.2. Pipelined Processor Datapath and Control Unit
4.2. Pipelined Processor Datapath and Control Unit
• Incrementally develop an unpipelined datapath
• Keep data ﬂowing from left to right
• Position control signal table early in the diagram
• Divided datapath/control into stages by inserting pipeline registers
• Keep the pipeline stages roughly balanced
• Forward arrows should avoid “skipping” pipeline registers
• Backward arrows will need careful consideration
pc_plus4
sext
op1
_sel_D
ir[15:0]
mul
result_sel_X
ir[25:0]
j_tgen
j_targ
alu_
fn_X
jr
ir[15:0]
br_tgen
eq_X
br_targ
wb_sel_M
pc_F
+4
regfile
(read)ir[20:16]
ir[25:21]
alu
regfile
(write)
rf
_wen_W
rf
_waddr_W
regfile
(write)
Control Signal
Table
pc
_sel_F
imemreq.
addr
imemresp.
data
dmemreq.
addr
dmemreq.
data
dmemresp.
data
imemreq.
addr
imemresp.
data
dmemreq.
addr
dmemreq.
data
dmemresp.
data
F D X M W
F D X M W
F D X M W
addiu r1, r2, 1
addiu r3, r4, 1
addiu r5, r6, 1
32
4. PARCv1 Pipelined Processor 4.2. Pipelined Processor Datapath and Control Unit
Adding a new auto-incrementing load instruction
Draw on the above datapath diagram what paths we need to use as well
as any new paths we will need to add in order to implement the follow-
ing auto-incrementing load instruction.
lw.ai rt, imm(rs)
R[rt]← M[ R[rs] + sext(imm) ]; R[rs]← R[rs] + 4
pc_plus4
sext
op1
_sel_D
ir[15:0]
mul
result_sel_X
ir[25:0]
j_tgen
j_targ
alu_
fn_X
jr
ir[15:0]
br_tgen
eq_X
br_targ
wb_sel_M
pc_F
+4
regfile
(read)ir[20:16]
ir[25:21]
alu
regfile
(write)
rf
_wen_W
rf
_waddr_W
regfile
(write)
Control Signal
Table
pc
_sel_F
imemreq.
addr
imemresp.
data
dmemreq.
addr
dmemreq.
data
dmemresp.
data
ir_FD
op0_DX
result
_XM
F Stage D Stage X Stage M Stage W Stage
cs_DX cs_XM cs_MW
sd_XM
result
_XM
result
_MW
sd_DX
btarg_DX
op0_DX
op1_DX
pc_F
pc_plus4
_FDalways
pc_plus4
val_DX val_XM val_MWval_FD
val_F
Control
Logic
Control
Logic
Control
Logic
33
4. PARCv1 Pipelined Processor 4.2. Pipelined Processor Datapath and Control Unit
Pipeline diagrams
addiu r1, r2, 1
addiu r3, r4, 1
addiu r5, r6, 1
What would be the total execution time if these three instructions were
repeated 10 times?
Hazards occur when instructions interact with each other in pipeline
• RAW Data Hazards: An instruction depends on a data value
produced by an earlier instruction
• Control Hazards: Whether or not an instruction should be executed
depends on a control decision made by an earlier instruction
• Structural Hazards: An instruction in the pipeline needs a resource
being used by another instruction in the pipeline
• WAW and WAR Name Hazards: An instruction in the pipeline is
writing a register that an earlier instruction in the pipeline is either
writing or reading
Stalling and squashing instructions
• Stalling: An instruction originates a stall due to a hazard, causing all
instructions earlier in the pipeline to also stall. When the hazard is
resolved, the instruction no longer needs to stall and the pipeline
starts ﬂowing again.
• Squashing: An instruction originates a squash due to a hazard, and
squashes all previous instructions in the pipeline (but not itself). We
restart the pipeline to begin executing a new instruction sequence.
34
4. PARCv1 Pipelined Processor 4.2. Pipelined Processor Datapath and Control Unit
Control logic with no stalling and no squashing
Stage A
Datapath
Logic
Stage B
Datapath
Logic
Stage C
Datapath
Logic
Stage A
Control
Logic
Stage B
Control
Logic
Stage C
Control
Logic
always_ff @( posedge clk )
if ( reset )
val_B <= 0
else
val_B <= next_val_A
next_val_B = val_B
Control logic with stalling and no squashing
Stage A
Control
Logic
Stage A
Datapath
Logic
Stage B
Control
Logic
Stage C
Control
Logic
Stage B
Datapath
Logic
Stage C
Datapath
Logic
control, ostall signals
reg_en_B
val_B
next_
val_B
reg_en_B = !stall_B
always_ff @( posedge clk )
if ( reset )
val_B <= 0
else if ( reg_en_B )
val_B <= next_val_A
ostall_B = val_B && ( ostall_hazard1_B || ostall_hazard2_B )
stall_B = val_B && ( ostall_B || ostall_C || ... )
next_val_B = val_B && !stall_B
ostall_B Originating stall due to hazards detected in B stage.
stall_B Should we actually stall B stage? Factors in ostalls due to hazards
and ostalls from later pipeline stages.
next_val_B Only send transaction to next stage if transaction in B stage is valid
and we are not stalling B stage.
35
4. PARCv1 Pipelined Processor 4.2. Pipelined Processor Datapath and Control Unit
Control logic with stalling and squashing
Stage A
Control
Logic
Stage A
Datapath
Logic
Stage B
Control
Logic
Stage C
Control
Logic
Stage B
Datapath
Logic
Stage C
Datapath
Logic
control, ostall signals
reg_en_B
val_B
next_
val_B
control, ostall, osquash signals
reg_en_B = !stall_B
always_ff @( posedge clk )
if ( reset )
val_B <= 0
else if ( reg_en_B )
val_B <= next_val_A
squash_B = val_B && ( osquash_C || ... )
ostall_B = val_B && !squash_B && ( ostall_hazard1_B || ostall_hazard2_B )
stall_B = val_B && !squash_B && ( ostall_B || ostall_C || ... )
osquash_B = val_B && !squash_B && !stall_B && ( osquash_hazard1_B || ... )
next_val_B = val_B && !stall_B && !squash_B
squash_B Should we squash B stage? Factors in the originating squashes
from later pipeline stages. An originating squash from B stage
means to squash all stages earlier than B, so osquash_B is not
factored into squash_B.
ostall_B A squash takes priority, since a squashed transaction is invalid and
thus it should not originate a stall.
stall_B A squash takes priority, since a squashed transaction is invalid and
thus it should not actually stall.
osquash_B Originating squash due to hazards detected in B stage. A squash
takes priority, since a squashed transaction is invalid and thus it
should not originate a squash. A stall also takes priority, since a
stalling transactions should not originate a squash.
next_val_B Only send transaction to next stage if transaction in B stage is valid
and we are not stalling or squashing B stage.
36
5. Pipeline Hazards: RAW Data Hazards
5. Pipeline Hazards: RAW Data Hazards
RAW data hazards occur when one instruction depends on a data value
produced by a preceding instruction still in the pipeline. We use archi-
tectural dependency arrows to illustrate RAW dependencies in assembly
code sequences.
addiu r1, r2, 1
addiu r3, r1, 1
addiu r4, r3, 1
Using pipeline diagrams to illustrate RAW hazards
We use microarchitectural dependency arrows to illustrate RAW hazards
on pipeline diagrams.
F D X M W
F D X M W
F D X M W
addiu r1, r2, 1
addiu r3, r1, 1
addiu r4, r3, 1
addiu r1, r2, 1
addiu r3, r1, 1
addiu r4, r3, 1
37
5. Pipeline Hazards: RAW Data Hazards
Approaches to resolving data hazards
• Expose in Instruction Set Architecture: Expose data hazards in ISA
forcing compiler to explicitly avoid scheduling instructions that
would create hazards (i.e., software scheduling for correctness)
• Hardware Scheduling: Hardware dynamically schedules
instructions to avoid RAW hazards, potentially allowing
instructions to execute out of order
• Hardware Stalling: Hardware includes control logic that freezes
later instructions until earlier instruction has ﬁnished producing
data value; software scheduling can still be used to avoid stalling
(i.e., software scheduling for performance)
• Hardware Bypassing/Forwarding: Hardware allows values to be
sent from an earlier instruction to a later instruction before the
earlier instruction has left the pipeline (sometimes called forwarding)
• Hardware Speculation: Hardware guesses that there is no hazard
and allows later instructions to potentially read invalid data; detects
when there is a problem, squashes and then re-executes instructions
that operated on invalid data
38
5. Pipeline Hazards: RAW Data Hazards 5.1. Expose in Instruction Set Architecture
5.1. Expose in Instruction Set Architecture
Insert nops to delay read of earlier
write. These nops count as real
instructions increasing
instructions per program.
addiu r1, r2, 1
nop
nop
nop
addiu r3, r1, 1
nop
nop
nop
addiu r4, r3, 1
Insert independent instructions to
delay read of earlier write, and
only use nops if there is not
enough useful work
addiu r1, r2, 1
addiu r6, r7, 1
addiu r8, r9, 1
nop
addiu r3, r1, 1
nop
nop
nop
addiu r4, r3, 1
Pipeline diagram showing software scheduling for RAW data hazards
addiu r1, r2, 1
addiu r6, r7, 1
addiu r8, r9, 1
nop
addiu r3, r1, 1
nop
nop
nop
addiu r4, r3, 1
Note: If hazard is exposed in ISA, software scheduling is required for
correctness! A scheduling mistake can cause undeﬁned behavior.
39
5. Pipeline Hazards: RAW Data Hazards 5.2. Hardware Stalling
5.2. Hardware Stalling
Hardware includes control logic that freezes later instructions (in front
of pipeline) until earlier instruction (in back of pipeline) has ﬁnished
producing data value.
Pipeline diagram showing hardware stalling for RAW data hazards
addiu r1, r2, 1
addiu r3, r1, 1
addiu r4, r3, 1
Note: Software scheduling is not required for correctness, but can
improve performance! Programmer or compiler schedules independent
instructions to reduce the number of cycles spent stalling.
Modiﬁcations to datapath/control to support hardware stalling
pc_plus4
sext
op1
_sel_D
ir[15:0]
mul
result_sel_X
ir[25:0]
j_tgen
j_targ
alu_
fn_X
jr
ir[15:0]
br_tgen
eq_X
br_targ
wb_sel_M
pc_F
+4
regfile
(read)ir[20:16]
ir[25:21]
alu
regfile
(write)
rf
_wen_W
rf
_waddr_W
regfile
(write)
Control Signal
Table
pc
_sel_F
imemreq.
addr
imemresp.
data
dmemreq.
addr
dmemreq.
data
dmemresp.
data
ir_FD
op0_DX
result
_XM
F Stage D Stage X Stage M Stage W Stage
cs_DX cs_XM cs_MW
sd_XM
result
_XM
result
_MW
sd_DX
btarg_DX
op0_DX
op1_DX
pc_F
pc_plus4
_FDalways
pc_plus4
val_DX val_XM val_MWval_FD
val_F
Control
Logic
Control
Logic
Control
Logic
imemreq.
addr
imemresp.
data
dmemreq.
addr
dmemreq.
data
dmemresp.
data
reg_
en_Dreg_
en_F
CSig Table
Stall Logic
40
5. Pipeline Hazards: RAW Data Hazards 5.3. Hardware Bypassing/Forwarding
Deriving the stall signal
addu addiu mul lw sw j jal jr bne
rs_en
rt_en
rf_wen
rf_waddr
ostall_waddr_X_rs_D =
val_D && rs_en_D && val_X && rf_wen_X
&& (inst_rs_D == rf_waddr_X) && (rf_waddr_X != 0)
ostall_waddr_M_rs_D =
val_D && rs_en_D && val_M && rf_wen_M
&& (inst_rs_D == rf_waddr_M) && (rf_waddr_M != 0)
ostall_waddr_W_rs_D =
val_D && rs_en_D && val_W && rf_wen_W
&& (inst_rs_D == rf_waddr_W) && (rf_waddr_W != 0)
... similar for ostall signals for rt source register ...
ostall_D = val_D
&& ( ostall_waddr_X_rs_D || ostall_waddr_X_rt_D
|| ostall_waddr_M_rs_D || ostall_waddr_M_rt_D
|| ostall_waddr_W_rs_D || ostall_waddr_W_rt_D )
5.3. Hardware Bypassing/Forwarding
Hardware allows values to be sent from an earlier instruction (in back
of pipeline) to a later instruction (in front of pipeline) before the earlier
instruction has left the pipeline. Sometimes called “forwarding”.
41
5. Pipeline Hazards: RAW Data Hazards 5.3. Hardware Bypassing/Forwarding
Pipeline diagram showing hardware bypassing for RAW data hazards
addiu r1, r2, 1
addiu r3, r1, 1
addiu r4, r3, 1
Adding single bypass path to support limited hardware bypassing
pc_plus4
sext
op1
_sel_D
ir[15:0]
mul
result_sel_X
ir[25:0]
j_tgen
j_targ
alu_
fn_X
jr
ir[15:0]
br_tgen
eq_X
br_targ
wb_sel_M
pc_F
+4
regfile
(read)ir[20:16]
ir[25:21]
alu
regfile
(write)
rf
_wen_W
rf
_waddr_W
regfile
(write)
Control Signal
Table
pc
_sel_F
imemreq.
addr
imemresp.
data
dmemreq.
addr
dmemreq.
data
dmemresp.
data
ir_FD
op0_DX
result
_XM
F Stage D Stage X Stage M Stage W Stage
cs_DX cs_XM cs_MW
sd_XM
result
_XM
result
_MW
sd_DX
btarg_DX
op0_DX
op1_DX
pc_F
pc_plus4
_FDalways
pc_plus4
val_DX val_XM val_MWval_FD
val_F
Control
Logic
Control
Logic
Control
Logic
reg_
en_Dreg_
en_F
CSig Table
Stall Logic
CSig Table
Stall & Bypass
Logic
bypass_from_X
op0_byp
_sel_D
Deriving the bypass and stall signals
ostall_waddr_X_rs_D = 0
bypass_waddr_X_rs_D = val_D && rs_en_D && val_X && rf_wen_X
&& (inst_rs_D == rf_waddr_X) && (rf_waddr_X != 0)
42
5. Pipeline Hazards: RAW Data Hazards 5.3. Hardware Bypassing/Forwarding
Pipeline diagram showing multiple hardware bypass paths
addiu r2, r10, 1
addiu r2, r11, 1
addiu r1, r2, 1
addiu r3, r4, 1
addiu r5, r3, 1
addu r6, r1, r3
sw r5, 0(r1)
jr r6
Adding all bypass path to support full hardware bypassing
pc_plus4
sext
op1
_sel_D
ir[15:0]
mul
result_sel_X
ir[25:0]
j_tgen
j_targ
alu_
fn_X
jr
ir[15:0]
br_tgen
eq_X
br_targ
wb_sel_M
pc_F
+4
regfile
(read)ir[20:16]
ir[25:21]
alu
regfile
(write)
rf
_wen_W
rf
_waddr_W
regfile
(write)
Control Signal
Table
pc
_sel_F
imemreq.
addr
imemresp.
data
dmemreq.
addr
dmemreq.
data
dmemresp.
data
ir_FD
op0_DX
result
_XM
F Stage D Stage X Stage M Stage W Stage
cs_DX cs_XM cs_MW
sd_XM
result
_XM
result
_MW
sd_DX
btarg_DX
op0_DX
op1_DX
pc_F
pc_plus4
_FDalways
pc_plus4
val_DX val_XM val_MWval_FD
val_F
Control
Logic
Control
Logic
Control
Logic
reg_
en_Dreg_
en_F
CSig Table
Stall Logic
CSig Table
Stall & Bypass
Logic
bypass_from_X
op0_byp
_sel_D
bypass_from_M
bypass_from_W
op1_
byp_
sel_D
43
5. Pipeline Hazards: RAW Data Hazards 5.3. Hardware Bypassing/Forwarding
Handling load-use RAW dependencies
ALU-use latency is only one cycle, but load-use latency is two cycles.
lw r1, 0(r2)
addiu r3, r1, 1
lw r1, 0(r2)
addiu r3, r1, 1
ostall_load_use_X_rs_D =
val_D && rs_en_D && val_X && rf_wen_X
&& (inst_rs_D == rf_waddr_X) && (rf_waddr_X != 0)
&& (op_X == lw)
ostall_load_use_X_rt_D =
val_D && rt_en_D && val_X && rf_wen_X
&& (inst_rt_D == rf_waddr_X) && (rf_waddr_X != 0)
&& (op_X == lw)
ostall_D =
val_D && ( ostall_load_use_X_rs_D || ostall_load_use_X_rt_D )
bypass_waddr_X_rs_D =
val_D && rs_en_D && val_X && rf_wen_X
&& (inst_rs_D == rf_waddr_X) && (rf_waddr_X != 0)
&& (op_X != lw)
bypass_waddr_X_rt_D =
val_D && rt_en_D && val_X && rf_wen_X
&& (inst_rt_D == rf_waddr_X) && (rf_waddr_X != 0)
&& (op_X != lw)
44
5. Pipeline Hazards: RAW Data Hazards 5.4. RAW Data Hazards Through Memory
Pipeline diagram for simple assembly sequence
Draw a pipeline diagram illustrating how the following assembly
sequence would execute on a fully bypassed pipelined PARCv1
processor. Include microarchitectural dependency arrows to illustrate
how data is transferred along various bypass paths.
lw r1, 0(r2)
lw r3, 0(r4)
addu r5, r1, r3
sw r5, 0(r6)
addiu r2, r2, 4
addiu r4, r4, 4
addiu r6, r6, 4
addiu r7, r7, -1
bne r7, r0, loop
5.4. RAW Data Hazards Through Memory
So far we have only studied RAW data hazards through registers, but
we must also carefully consider RAW data hazards through memory.
sw r1, 0(r2)
lw r3, 0(r4) # RAW dependency occurs if R[r2] == R[r4]
sw r1, 0(r2)
lw r3, 0(r4)
45
6. Pipeline Hazards: Control Hazards
6. Pipeline Hazards: Control Hazards
Control hazards occur when whether or not an instruction should be
executed depends on a control decision made by an earlier instruction
We use architectural dependency arrows to illustrate control
dependencies in assembly code sequences.
Static Instr Sequence
addiu r1, r0, 1
j foo
opA
opB
foo: addiu r2, r3, 1
bne r0, r1, bar
opC
opD
opE
bar: addiu r4, r5, 1
Dynamic Instr Sequence
addiu r1, r0, 1
j foo
addiu r2, r3, 1
bne r0, r1, bar
addiu r4, r5, 1
Using pipeline diagrams to illustrate control hazards
We use microarchitectural dependency arrows to illustrate control
hazards on pipeline diagrams.
addiu r1, r0, 1
j foo
addiu r2, r3, 1
bne r0, r1, bar
addiu r4, r5, 1
46
6. Pipeline Hazards: Control Hazards 6.1. Expose in Instruction Set Architecture
The jump resolution latency and branch resolution latency are the
number of cycles we need to delay the fetch of the next instruction in
order to avoid any kind of control hazard. Jump resolution latency is
two cycles, and branch resolution latency is three cycles.
addiu r1, r0, 1
j foo
addiu r2, r3, 1
bne r0, r1, bar
addiu r4, r5, 1
Approaches to resolving control hazards
• Expose in Instruction Set Architecture: Expose control hazards in
ISA forcing compiler to explicitly avoid scheduling instructions that
would create hazards (i.e., software scheduling for correctness)
• Software Predication: Programmer or compiler converts control
ﬂow into data ﬂow by using instructions that conditionally execute
based on a data value
• Hardware Speculation: Hardware guesses which way the control
ﬂow will go and potentially fetches incorrect instructions; detects
when there is a problem and re-executes instructions the instructions
that are along the correct control ﬂow
• Software Hints: Programmer or compiler provides hints about
whether a conditional branch will be taken or not taken, and
hardware can use these hints for more efﬁcient hardware speculation
47
6. Pipeline Hazards: Control Hazards 6.1. Expose in Instruction Set Architecture
6.1. Expose in Instruction Set Architecture
Expose branch delay slots as part of the instruction set. Branch delay
slots are instructions that follow a jump or branch and are always
executed regardless of whether a jump or branch is taken or not taken.
Compiler tries to insert useful instructions, otherwise inserts nops.
addiu r1, r0, 1
j foo
nop
opA
opB
foo: addiu r2, r3, 1
bne r0, r1, bar
nop
nop
opC
opD
opE
bar: addiu r4, r5, 1
Assume we modify the PARCv1
instruction set to specify that J,
JAL, and JR instructions have a
single-instruction branch delay
slot (i.e., one instruction after a J,
JAL, and JR is always executed)
and the BNE instruction has a
two-instruction branch delay slot
(i.e., two instructions after a BNE
are always executed).
Pipeline diagram showing using branch delay slots for control hazards
addiu r1, r0, 1
j foo
nop
addiu r2, r3, 1
bne r0, r1, bar
nop
nop
addiu r4, r5, 1
48
6. Pipeline Hazards: Control Hazards 6.2. Hardware Speculation
6.2. Hardware Speculation
Hardware guesses which way the control ﬂow will go and potentially
fetches incorrect instructions; detects when there is a problem and
re-executes instructions the instructions that are along the correct
control ﬂow. For now, we will only consider a simple branch prediction
scheme where the hardware always predicts not taken.
Pipeline diagram when branch is not taken
addiu r1, r0, 1
j foo
opA
addiu r2, r3, 1
bne r0, r1, bar
opC
opD
Pipeline diagram when branch is taken
addiu r1, r0, 1
j foo
opA
addiu r2, r3, 1
bne r0, r1, bar
opC
opD
addiu r4, r5, 1
49
6. Pipeline Hazards: Control Hazards 6.2. Hardware Speculation
Modiﬁcations to datapath/control to support hardware speculation
pc_plus4
sext
op1
_sel_D
ir[15:0]
mul
result_sel_X
ir[25:0]
j_tgen
j_targ
alu_
fn_X
jr
ir[15:0]
br_tgen
eq_X
br_targ
wb_sel_M
pc_F
+4
regfile
(read)ir[20:16]
ir[25:21]
alu
regfile
(write)
rf
_wen_W
rf
_waddr_W
regfile
(write)
Control Signal
Table
pc
_sel_F
imemreq.
addr
imemresp.
data
dmemreq.
addr
dmemreq.
data
dmemresp.
data
ir_FD
op0_DX
result
_XM
F Stage D Stage X Stage M Stage W Stage
cs_DX cs_XM cs_MW
sd_XM
result
_XM
result
_MW
sd_DX
btarg_DX
op0_DX
op1_DX
pc_F
pc_plus4
_FDalways
pc_plus4
val_DX val_XM val_MWval_FD
val_F
Control
Logic
Control
Logic
Control
Logic
reg_
en_Dreg_
en_F
CSig Table
Stall Logic
CSig Table
Stall & Bypass
Logic
bypass_from_X
op0_byp
_sel_D
bypass_from_M
bypass_from_W
op1_
byp_
sel_D
pc
_sel_F
CSig Table
Stall, Bypass, &
Squash Logic
Deriving the squash signals
osquash_j_D = (op_D == j) || (op_D == jal) || (op_D == jr)
osquash_br_X = br_taken_X
Our generic stall/squash scheme gives priority to squashes over stalls.
A squashed instruction is invalid, so it should not stall the pipeline.
squash_D = val_D && osquash_X
ostall_D = val_D && !squash_D && ( ostall_hazard1_D || ... )
stall_D = val_D && !squash_D && ostall_D
osquash_D = val_D && !squash_D && !stall_D && osquash_j_D
Important: PC select logic must give priority to older instructions
(i.e., prioritize branches over jumps)! Good quiz question?
50
6. Pipeline Hazards: Control Hazards 6.2. Hardware Speculation
Pipeline diagram for simple assembly sequence
Draw a pipeline diagram illustrating how the following assembly
sequence would execute on a fully bypassed pipelined PARCv1
processor that uses hardware speculation which always predicts
not-taken. Unlike the “standard” PARCv1 processor, you should also
assume that we add a single-instruction branch delay slot to the
instruction set. So this processor will partially expose the control
hazard in the instruction, but also use hardware speculation. Include
microarchitectural dependency arrows to illustrate both data and
control ﬂow.
addiu r1, r2, 1
bne r0, r3, foo # assume R[rs] != 0
addiu r4, r5, 1 # instruction is in branch delay slot
addiu r6, r7, 1
...
foo:
addu r8, r1, r4
addiu r9, r1, 1
51
6. Pipeline Hazards: Control Hazards 6.3. Interrupts and Exceptions
6.3. Interrupts and Exceptions
Interrupts and exceptions alter the normal control ﬂow of the program.
They are caused by an external or internal event that needs to be
processed by the system, and these events are usually unexpected or
rare from the program’s point of view.
• Asynchronous Interrupts
– Input/output device needs to be serviced
– Timer has expired
– Power distruption or hardware failure
• Synchronous Exceptions
– Undeﬁned opcode, privileged instruction
– Arithmetic overﬂow, ﬂoating-point exception
– Misaligned memory access for instruction fetch or data access
– Memory protection violation
– Virtual memory page faults
– System calls (traps) to jump into the operating system kernel
Interrupts and Exception Semantics
• Interrupts are asynchronous with respect to the program, so the
microarchitecture can decide when to service the interrupt
• Exceptions are synchronous with respect to the program, so they
must be handled immediately
52
6. Pipeline Hazards: Control Hazards 6.3. Interrupts and Exceptions
• To handle an interrupt or exception the hardware/software must:
– Stop program at current instruction ( I), ensure previous insts ﬁnished
– Save cause of interrupt or exception in privileged arch state
– Save the PC of the instruction I in a special register (EPC)
– Switch to privileged mode
– Set the PC to the address of either the interrupt or the exception handler
– Disable interrupts
– Save the user architectural state
– Check the type of interrupt or exception
– Handle the interrupt or exception
– Enable interrupts
– Switch to user mode
– Set the PC to EPC if I should be restarted
– Potentially set PC to EPC+4 if we should skip I
Handling a misaligned data address and syscall exceptions
Static Instr Sequence
addiu r1, r0, 0x2001
lw r2, 0(r1)
syscall
opB
opC
...
exception_hander:
opD # disable interrupts
opE # save user registers
opF # check exception type
opG # handle exception
opH # enable interrupts
addiu EPC, EPC, 4
eret
Dynamic Instr Sequence
addiu r1, r0, 0x2001
lw r2, 0(r1) (excep)
opD
opE
opF
opG
opH
addiu EPC, EPC, 4
eret
syscall (excep)
opD
opE
opF
53
6. Pipeline Hazards: Control Hazards 6.3. Interrupts and Exceptions
Interrupts and Exceptions in a PARCv4? Pipelined Processor
F D X M W
Inst Address
Exceptions
Illegal
Instruction
Arithmetic
Overflow
Data Address
Exceptions
• How should we handle a single instruction which generates
multiple exceptions in different stages as it goes down the pipeline?
– Exceptions in earlier pipeline stages override later exceptions for a given
instruction
• How should we handle multiple instructions generating exceptions
in different stages at the same or different times?
– We always want the execution to appear as if we have completely
executed one instruction before going onto the next instruction
– So we want to process the exception corresponding to the earliest
instruction in program order ﬁrst
– Hold exception ﬂags in pipeline until commit point
– Commit point is after all exceptions could be generated but before any
architectural state has been updated
– To handle an exception at the commit point: update cause and EPC,
squash all stages before the commit point, and set PC to exception handler
• How and where to handle external asynchronous interrupts?
– Inject asynchronous interrupts at the commit point
– Asynchronous interrupts will then naturally override exceptions caused
by instructions earlier in the pipeline
54
6. Pipeline Hazards: Control Hazards 6.3. Interrupts and Exceptions
Modiﬁcations to datapath/control to support exceptions
pc_plus4
sext
op1
_sel_D
ir[15:0]
mul
result_sel_X
ir[25:0]
j_tgen
j_targ
alu_
fn_X
jr
ir[15:0]
br_tgen
eq_X
br_targ
wb_sel_M
pc_F
+4
regfile
(read)ir[20:16]
ir[25:21]
alu
regfile
(write)
rf
_wen_W
rf
_waddr_W
regfile
(write)
Control Signal
Table
imemreq.
addr
imemresp.
data
dmemreq.
addr
dmemreq.
data
dmemresp.
data
ir_FD
op0_DX
result
_XM
F Stage D Stage X Stage M Stage W Stage
cs_DX cs_XM cs_MW
sd_XM
result
_XM
result
_MW
sd_DX
btarg_DX
op0_DX
op1_DX
pc_F
pc_plus4
_FD
val_DX val_XM val_MWval_FD
val_F
Control
Logic
Control
Logic
Control
Logic
xcept_XMxcept_DXxcept_FD
Exception
Handling Logic
xcept
handler
reg_
en_Dreg_
en_F
CSig Table
Stall Logic
CSig Table
Stall & Bypass
Logic
bypass_from_X
op0_byp
_sel_D
bypass_from_M
bypass_from_W
op1_
byp_
sel_D
pc_sel_F
CSig Table
Stall, Bypass, &
Squash Logic
Deriving the squash signals
osquash_j_D = (op_D == j) || (op_D == jal) || (op_D == jr)
osquash_br_X = br_taken_X
osquash_xcept_M = exception_M
Control logic needs to redirect the front end of the pipeline just like for a
jump or branch. Again, squashes take priority over stalls, and PC select
logic must give priority to older instructions (i.e., priortize exceptions,
over branches, over jumps)!
55
6. Pipeline Hazards: Control Hazards 6.3. Interrupts and Exceptions
Pipeline diagram of exception handling
addiu r1, r0, 0x2001
lw r2, 0(r1) # assume causes misaligned address exception
syscall # causes a syscall exception
opB
opC
...
exception_hander:
opD # disable interrupts
opE # save user registers
opF # check exception type
opG # handle exception
opH # enable interrupts
addiu EPC, EPC, 4
eret
56
7. Pipeline Hazards: Structural Hazards 7.1. Expose in Instruction Set Architecture
7. Pipeline Hazards: Structural Hazards
Structural hazards occur when an instruction in the pipeline needs a
resource being used by another instruction in the pipeline. The PARCv1
processor pipeline is speciﬁcally designed to avoid any structural
hazards.
Let’s introduce a structural hazard by allowing ADDU, ADDIU, MUL,
and JAL instructions to write to the register ﬁle in the M stage instead of
waiting until the W stage. We would need to add another writeback
mux in the W stage and carefully handle bypassing.
Using pipeline diagrams to illustrate structural hazards
We use structural dependency arrows to illustrate structural hazards.
addiu r1, r2, 1
addiu r3, r4, 1
lw r5, 0(r6)
addiu r7, r8, 1
Approaches to resolving structural hazards
• Expose in Instruction Set Architecture: Expose structural hazards in
ISA forcing compiler to explicitly avoid scheduling instructions that
would create hazards (i.e., software scheduling for correctness)
• Hardware Stalling: Hardware includes control logic that freezes
later instructions until earlier instruction has ﬁnished using the
shared resource; software scheduling can still be used to avoid
stalling (i.e., software scheduling for performance)
• Hardware Duplication: Add more hardware so that each instruction
can access separate resources at the same time
57
7. Pipeline Hazards: Structural Hazards 7.1. Expose in Instruction Set Architecture
7.1. Expose in Instruction Set Architecture
Insert independent instructions or nops to delay an ADDU, ADDIU,
MUL, or JAL instructions if they follow a LW instruction.
Pipeline diagram showing software scheduling for structural hazards
addiu r1, r2, 1
addiu r3, r4, 1
lw r5, 0(r6)
nop
addiu r7, r8, 1
7.2. Hardware Stalling
Hardware includes control logic that freezes an ADDU, ADDIU, MUL,
or JAL instruction if a LW instruction is ahead in the pipeline.
Pipeline diagram showing hardware stalling for structural hazards
addiu r1, r2, 1
addiu r3, r4, 1
lw r5, 0(r6)
addiu r7, r8, 1
Deriving the stall signal
ostall_wport_hazard_D = val_D && rf_wen_D && val_X && (op_X == lw)
Stall far before the structural hazard actually occurs, because we know
exactly how instructions move down the pipeline. Also possible to use
dynamic arbitration in the back-end of the pipeline.
58
7. Pipeline Hazards: Structural Hazards 7.3. Hardware Duplication
7.3. Hardware Duplication
Add a second write port so that an ADDU, ADDIU, MUL, or JAL
instruction can writeback to the register ﬁle at the same time as a LW.
pc_plus4
sext
op1
_sel_D
ir[15:0]
mul
result_sel_X
ir[25:0]
j_tgen
j_targ
alu_
fn_X
jr
ir[15:0]
br_tgen
eq_X
br_targ
wb_sel_M
pc_F
+4
regfile
(read)ir[20:16]
ir[25:21]
alu
regfile
(write)
rf
_wen_W
rf
_waddr_W
regfile
(write)
Control Signal
Table
pc
_sel_F
imemreq.
addr
imemresp.
data
dmemreq.
addr
dmemreq.
data
dmemresp.
data
ir_FD
op0_DX
result
_XM
F Stage D Stage X Stage M Stage W Stage
cs_DX cs_XM cs_MW
sd_XM
result
_XM
result
_MW
sd_DX
btarg_DX
op0_DX
op1_DX
pc_F
pc_plus4
_FDalways
pc_plus4
val_DX val_XM val_MWval_FD
val_F
Control
Logic
Control
Logic
Control
Logic
reg_
en_Dreg_
en_F
CSig Table
Stall Logic
CSig Table
Stall & Bypass
Logic
bypass_from_X
op0_byp
_sel_D
bypass_from_M
bypass_from_W
op1_
byp_
sel_D
pc
_sel_F
CSig Table
Stall, Bypass, &
Squash Logic
rf
_wen1_W
rf
_waddr1_W
Does allowing early writeback help performance in the ﬁrst place?
addiu r1, r2, 1
addiu r3, r1, 1
addiu r4, r3, 1
addiu r5, r4, 1
addiu r6, r5, 1
addiu r7, r6, 1
59
8. Pipeline Hazards: WAW and WAR Name Hazards
8. Pipeline Hazards: WAW and WAR Name Hazards
WAW dependencies occur when an instruction overwrites a register
than an earlier instruction has already written. WAR dependencies
occur when an instruction writes a register than an earlier instruction
needs to read. We use architectural dependency arrows to illustrate
WAW and WAR dependencies in assembly code sequences.
mul r1, r2, r3
addiu r4, r6, 1
addiu r1, r5, 1
WAW name hazards occur when an instruction in the pipeline writes a
register before an earlier instruction (in back of the pipeline) has had a
chance to write that same register.
WAR name hazards occur when an instruction in the pipeline writes a
register before an earlier instuction (in back of pipeline) has had a
chance to read that same register.
The PARCv1 processor pipeline is speciﬁcally designed to avoid any
WAW or WAR name hazards. Instructions always write the registerﬁle
in-order in the same stage, and instructions always read registers in the
front of the pipeline and write registers in the back of the pipeline.
Let’s introduce a WAW name hazard by using an iterative variable
latency multiplier, and allowing other instructions to continue
executing while the multiplier is working.
60
8. Pipeline Hazards: WAW and WAR Name Hazards 8.1. Software Renaming
Using pipeline diagrams to illustrate WAW name hazards
We use microarchitectural dependency arrows to illustrate WAW
hazards on pipeline diagrams.
mul r1, r2, r3
addiu r4, r6, 1
addiu r1, r5, 1
Approaches to resolving structural hazards
• Software Renaming: Programmer or compiler changes the register
names to avoid creating name hazards
• Hardware Renaming: Hardware dynamically changes the register
names to avoid creating name hazards
• Hardware Stalling: Hardware includes control logic that freezes
later instructions until earlier instruction has ﬁnished either writing
or reading the problematic register name
8.1. Software Renaming
As long as we have enough architectural registers, renaming registers in
software is easy. WAW and WAR dependencies occur because we have
a ﬁnite number of architectural registers.
mul r1, r2, r3
addiu r4, r6, 1
addiu r7, r5, 1
61
9. Summary of Processor Performance 8.2. Hardware Stalling
8.2. Hardware Stalling
Simplest approach is to add stall logic in the decode stage similar to
what the approach used to resolve other hazards.
mul r1, r2, r3
addiu r4, r6, 1
addiu r1, r5, 1
Deriving the stall signal
ostall_struct_hazard_D = val_D && (op_D == MUL) && !imul_rdy_D
ostall_waw_hazard_D =
val_D && rf_wen_D && val_Z && rf_wen_Z
&& (rf_waddr_D == rf_waddr_Z) && (rf_waddr_Z != 0)
9. Summary of Processor Performance
Time
Program = Instructions
Program × Cycles
Instruction× Time
Cycles
Results for vector-vector add example
Microarchitecture Inst CPI Cycle Time Exec Time
Single-Cycle Processor 576 1.0 74 τ 43 kτ
FSM Processor 576 6.5 40 τ 150 kτ
Pipelined Processor 576
62
9. Summary of Processor Performance
Estimating cycle time for pipelined processor
pc_plus4
sext
op1
_sel_D
ir[15:0]
mul
result_sel_X
ir[25:0]
j_tgen
j_targ
alu_
fn_X
jr
ir[15:0]
br_tgen
eq_X
br_targ
wb_sel_M
pc_F
+4
regfile
(read)ir[20:16]
ir[25:21]
alu
regfile
(write)
rf
_wen_W
rf
_waddr_W
regfile
(write)
Control Signal
Table
pc
_sel_F
imemreq.
addr
imemresp.
data
dmemreq.
addr
dmemreq.
data
dmemresp.
data
ir_FD
op0_DX
result
_XM
F Stage D Stage X Stage M Stage W Stage
cs_DX cs_XM cs_MW
sd_XM
result
_XM
result
_MW
sd_DX
btarg_DX
op0_DX
op1_DX
pc_F
pc_plus4
_FDalways
pc_plus4
val_DX val_XM val_MWval_FD
val_F
Control
Logic
Control
Logic
Control
Logic
reg_
en_Dreg_
en_F
CSig Table
Stall Logic
CSig Table
Stall & Bypass
Logic
bypass_from_X
op0_byp
_sel_D
bypass_from_M
bypass_from_W
op1_
byp_
sel_D
pc
_sel_F
CSig Table
Stall, Bypass, &
Squash Logic
• register read = 1τ
• register write = 1τ
• regﬁle read = 10τ
• regﬁle write = 10τ
• memory read = 20τ
• memory write = 20τ
• +4 unit = 4τ
• sext unit = 1τ
• br_tgen = 8τ
• j_tgen = 1τ
• mux = 3τ
• multiplier = 20τ
• alu = 10τ
63
9. Summary of Processor Performance
Estimating execution time
Using our ﬁrst-order equation for processor performance, how long in τ
will it take to execute the vvadd example assuming n is 64?
loop:
lw r12, 0(r4)
lw r13, 0(r5)
addu r14, r12, r13
sw r14, 0(r6)
addiu r4, r4, 4
addiu r5, r5, 4
addiu r6, r6, 4
addiu r7, r7, -1
bne r7, r0, loop
jr r31
lw
lw
addu
sw
addiu
addiu
addiu
addiu
bne
opA
opB
lw
64
9. Summary of Processor Performance
Using our ﬁrst-order equation for processor performance, how long in τ
will it take to execute the mystery program assuming n is 64 and that
we ﬁnd a match on the last element.
addiu r12, r0, 0
loop:
lw r13, 0(r4)
bne r13, r6, foo
addiu r2, r12, 0
jr r31
foo:
addiu r4, r4, 4
addiu r12, r12, 1
bne r12, r5, loop
addiu r2, r0, -1
jr r31
65
10. Case Study: Transition from CISC to RISC
10. Case Study: Transition from CISC to RISC
• Microcoding thrived in the 1970’s
– ROMs signiﬁcantly faster than DRAMs
– For complex instruction sets, microcode was cheaper and simpler
– New instructions supported without modifying datapath
– Fixing bugs in controller is easier
– ISA compatibility across models relatively straight-forward
— Maurice Wilkes, 1954
66
10. Case Study: Transition from CISC to RISC 10.1. Example CISC: IBM 360/M30
10.1. Example CISC: IBM 360/M30
M30 M40 M50 M65
Datapath width (bits) 8 16 32 64
µinst width (bits) 50 52 85 87
µcode size (1K µinsts) 4 4 2.75 2.75
µstore technology CCROS TCROS BCROS BCROS
µstore cycle (ns) 750 625 500 200
Memory cycle (ns) 1500 2500 2000 750
Rental fee ($K/month) 4 7 15 35
TROS = transformer read-only storage (magnetic storage)
BCROS = balanced capacitor read-only storage (capacitive storage)
CCROS = card capacitor read-only storage (metal punch cards, replace in ﬁeld)
Only the fastest models (75,95) were hardwired
IBM 360/M30 microprogram for register-register logical OR
OR
Fetch first byte
of operands
Instruction Fetch
Writeback Result
Prepare for Next Byte
67
10. Case Study: Transition from CISC to RISC 10.1. Example CISC: IBM 360/M30
IBM 360/M30 microprogram for register-register binary ADD
Analyzing Microcoded Machines
• John Cocke and group at IBM
– Working on a simple pipelined processor, 801, and advanced compilers
– Ported experimental PL8 compiler to IBM 370, and only used simple
register-register and load/store instructions similar to 801
– Code ran faster than other existing compilers that used all 370
instructions! (up to 6 MIPS, whereas 2 MIPS considered good before)
• Joel Emer and Douglas Clark at DEC
– Measured VAX-11/780 using external hardware
– Found it was actually a 0.5 MIPS machine, not a 1 MIPS machine
– 20% of VAX instrs = 60% of µcode, but only 0.2% of the dynamic execution
• VAX 8800, high-end VAX in 1984
– Control store: 16K×147b RAM, Uniﬁed Cache: 64K×8b RAM
– 4.5× more microstore RAM than cache RAM!
68
10. Case Study: Transition from CISC to RISC 10.1. Example CISC: IBM 360/M30
From CISC to RISC
• Key changes in technology constraints
– Logic, RAM, ROM all implemented with MOS transistors
– RAM ≈ same speed as ROM
• Use fast RAM to build fast instruction cache of user-visible
instructions, not ﬁxed hardware microfragments
– Change contents of fast instruction memory to ﬁt what app needs
• Use simple ISA to enable hardwired pipelined implementation
– Most compiled code only used a few of CISC instructions
– Simpler encoding allowed pipelined implementations
– Load/Store Reg-Reg ISA as opposed to Mem-Mem ISA
• Further beneﬁt with integration
– Early 1980’s→ ﬁt 32-bit datapath, small caches on single chip
– No chip crossing in common case allows faster operation
μPC
ROM for
μInst
Small
Decoder
User PC
RAM for
Instr Cache 
"Larger"
Decoder
Vertical μCode
Controller
RISC
Controller
69
10. Case Study: Transition from CISC to RISC 10.2. Example RISC: MIPS R2K
10.2. Example RISC: MIPS R2K
• MIPS R2K is one of the ﬁrst popular
pipelined RISC processors
• MIPS R2K implements the MIPS I
instruction set
• MIPS = Microprocessor without
Interlocked Pipeline Stages
MIPSI
MIPSII
MIPSIII
MIPSIV
MIPS64
MIPS32
MIPS16
• MIPS I used software scheduling to avoid some RAW hazards by
including a single-instruction load-use delay slot
• MIPS I used software scheduling to avoid some control hazards by
including a single-instruction branch delay slot
One-Instr Branch Delay Slot
addiu r1, r2, 1
j foo
addiu r3, r4, 1 # BDS
...
foo:
addiu r5, r6, 1
bne r7, r8, bar
addiu r9, r10, 1 # BDS
...
bar:
Present in all MIPS instruction
sets; not possible to depricate and
still enable legacy code to execute
on new microarchitectures
One-Instr Load-Use Delay Slot
lw r1, 0(r2)
lw r3, 0(r4)
addiu r2, r2, 4 # LDS
addu r5, r1, r3
Deprecated in MIPS II instruction
set; legacy code can still execute
on new microarchitectures, but
code using the MIPS II instruction
set can rely in hardware stalling
70
10. Case Study: Transition from CISC to RISC 10.2. Example RISC: MIPS R2K
MIPS R2K Microarchitecture
The pipelined datapath and control
were located on a single die. Cache
control and memory management unit
were also integrated on-die, but the
actual tag and data storage for the
cache was located off-chip.
Control Unit Datapath
I$ Controller D$ Controller
I$ (4-32KB) D$ (4-32KB)
Used two-phase clocking to enable ﬁve pipeline stages to ﬁt into four
clock cycles. This avoided the need for explicit bypassing from the W
stage to the end of the D stage.
1.2 The MIPS Five-Stage Pipeline 5
Instruction 1
Instruction 2
Instruction 3
RDIF ALU WB
RD ALU MEM WB
Time
Instruction sequence
IF
from 
I-cache
MEM 
from
D-cache
RD 
from
register
file
WB
to 
register
file
ALU
IF
MEM
FIGURE 1.2 MIPS ﬁve-stage pipeline.
fetch data from the cache; a cache miss is a relatively rare event and we can just
stop the CPU when it happens (though cleverer CPUs ﬁnd more useful things
to do).
The MIPS architecture was planned with separate instruction and data
caches, so it can fetch an instruction and read or write a memory variable simul-
taneously.
CISC architectures have caches too, but they’re most often afterthoughts,
ﬁtted in as a feature of the memory system. A RISC architecture makes more
sense if you regard the caches as very much part of the CPU and tied ﬁrmly into
the pipeline.
1.2 The MIPS Five-Stage Pipeline
The MIPS architecture is made for pipelining, and Figure 1.2 is close to the
earliest MIPS CPUs and typical of many. So long as the CPU runs from the
cache, the execution of every MIPS instruction is divided into ﬁve phases, called
pipestages, with each pipestage taking a ﬁxed amount of time. The ﬁxed amount
of time is usually a processor clock cycle (though some actions take only half
a clock, so the MIPS ﬁve-stage pipeline actually occupies only four clock
cycles).
All instructions are rigidly deﬁned so they can follow the same sequence
of pipestages, even where the instruction does nothing at some stage. The net
result is that, so long as it keeps hitting the cache, the CPU starts an instruction
every clock cycle.
Two-phase clocking enabled a single-cycle branch resolution latency
since register read, branch address generation, and branch comparison
can ﬁt in a single cycle.
1.5 MIPS Compared with CISC Architectures 27
IF
IF RD ALU MEM WB
WBMEMALURDIF
RD MEM WBBranch
instruction
Branch
delay
Branch
target
Branch
address
FIGURE 1.3 The pipeline and branch delays.
on a MIPS CPU without using some registers). For a program running
in any system that takes interrupts or traps, the values of these registers
may change at any time, so you’d better not use them.
1.5.4 Programmer-Visible Pipeline Effects
So far, this has all been what you might expect from a simpliﬁed CPU. However,
making the instruction set pipeline friendly has some stranger effects as well,
and to understand them we’re going to draw some pictures.
Delayed branches:T h ep i p e l i n es t r u c t u r eo ft h eM I P SC P U( F i g u r e1 . 3 )
means that when a jump/branch instruction reaches the execute phase
and a new program counter is generated, the instruction after the jump
will already have been started. Rather than discard this potentially useful
work, the architecture dictates that the instruction after a branch must
always be executed before the instruction at the target of the branch. The
instruction position following any branch is called the branch delay slot.
If nothing special was done by the hardware, the decision to branch or
not, together with the branch target address, would emerge at the end
of the ALU pipestage—by which time, as Figure 1.3 shows, you’re too
late to present an address for an instruction in even the next-but-one
pipeline slot.
But branches are important enough to justify special treatment, and you
can see from Figure 1.3 that a special path is provided through the ALU to
make the branch address available half a clock cycle early. T ogether with
the odd half-clock-cycle shift of the instruction fetch stage, that means
that the branch target can be fetched in time to become the next but one,
71
10. Case Study: Transition from CISC to RISC 10.2. Example RISC: MIPS R2K
MIPS R2K VLSI Design
Process: 2 µm, two metal layers
Clock Frequency: 8–15 MHz
Size: 110K transistors, 80 mm2
72
10. Case Study: Transition from CISC to RISC 10.2. Example RISC: MIPS R2K
Ratio of
MIPS
to
VAX
-- H&P, Appendix J, from Bhandarkar and Clark, 1991
Performance Ratio
Instructions Excuted Ratio
CPI Ratio
4.0
3.5
3.0
2.5
2.0
1.5
1.0
0.5
0.0
spice matrix nasa7 fpppp tomcatv doduc
espresso eqntott
li
2x more instr
6x lower CPI
2-4x higher perf
CISC/RISC Convergence
byoLinleyoGwennap
NotCtoCbeCleftCoutCinCtheCmoveCtoCthe
nextCgenerationCofCRISoRCMIPSCTech4
nologiesCuMTI.CunveiledCtheCdesignCof
theCRzppppRCalsoCknownCasCTUfC6sCthe
spiritualCsuccessorCtoCtheCREpppRCthe
newCdesignCwillCbeCtheCbasisCofChigh4end
MIPSCprocessorsCforCsomeCtimeRCatCleastCuntilCz55ﬂfCay
swappingCsuperpipeliningCforCanCaggressivelyCout4of4
orderCsuperscalarCdesignRCtheCRzppppChasCtheCpotential
toCdeliverChighCperformanceCthroughoutCthatCperiodf
TheCnewCprocessorCusesCdeepCqueuesCdecoupleCthe
instructionCfetchClogicCfromCtheCexecutionCunitsfCInstruc4
tionsCthatCareCreadyCtoCexecuteCcanCjumpCaheadCofCthose
waitingCforCoperandsRCincreasingCtheCutilizationCofCtheCex4
ecutionCunitsfCThisCtechniqueRCknownCasCout4of4orderCex4
ecutionRChasCbeenCusedCinCPowerPoCprocessorsCforCsome
timeC(see 081402.PDF )RCbutCtheCnewCMIPSCdesignCisCthe
mostCaggressiveCimplementationCyetRCallowingCmoreCin4
structionsCtoCbeCqueuedCthanCanyCofCitsCcompetitorsf
TakingCadvantageCofCitsCexperienceCwithCtheC,pp4
MHzCREEppRCMTICwasCableCtoCstreamlineCtheCdesignCand
expectsCitCtoCrunCatCaChighCclockCratefCSpeakingCatCthe
MicroprocessorCborumRCMTI’sCohrisCRowenCsaidCthatCthe
ﬁrstCRzppppCprocessorsCwillCreachCaCspeedCofC,ppCMHzR
Up2CfasterCthanCtheCPowerPoCe,pfC6tCthisCspeedRCheCex4
pectsCperformanceCinCexcessCofC8ppCSP7oint5,CandCepp
SP7ofp5,RCchallengingCHigital’sC,zzeECforCtheCperfor4
manceCleadfCHueCtoCscheduleCslipsRChoweverRCtheCRzpppp
hasCnotCyetCtapedCout(CweCdoCnotCexpectCvolumeCship4
mentsCuntilCEQ5URCbyCwhichCtimeCHigitalCmayCenhance
theCperformanceCofCitsCprocessorf
SpeculativeC7xecutionCaeyondCaranches
TheCfrontCendCofCtheCprocessorCisCresponsibleCfor
maintainingCaCcontinuousCﬂowCofCinstructionsCintoCthe
queuesRCdespiteCproblemsCcausedCbyCbranchesCandCcache
missesfC6sCbigureCzCshowsRCtheCchipCusesCaCtwo4wayCset4
associativeCinstructionCcacheCofC8,KfCLikeCotherChighly
superscalarCdesignsRCtheCRzppppCpredecodesCinstructions
asCtheyCareCloadedCintoCthisCcacheRCwhichCholdsCfourCextra
bitsCperCinstructionfCTheseCbitsCreduce
theCtimeCneededCtoCdetermineCtheCap4
propriateCqueueCforCeachCinstructionf
TheCprocessorCfetchesCfourCinstruc4
tionsCperCcycleCfromCtheCcacheCandCde4
codesCthemfCIfCaCbranchCisCdiscoveredRCit
isCimmediatelyCpredicted(CifCitCisCpre4
dictedCtakenRCtheCtargetCaddressCisCsent
toCtheCinstructionCcacheRCredirectingCthe
fetchCstreamfCaecauseCofCtheConeCcycle
neededCtoCdecodeCtheCbranchRCtaken
branchesCcreateCaC“bubble”CinCtheCfetch
stream(CtheCdeepCqueuesRChoweverRCgen4
erallyCpreventCthisCbubbleCfromCdelay4
ingCtheCexecutionCpipelinef
TheCsequentialCinstructionsCthat
areCloadedCduringCthisCextraCcycleCare
notCdiscardedCbutCareCsavedCinCaC“re4
sume”CcachefCIfCtheCbranchCisClaterCde4
terminedCtoChaveCbeenCmispredictedRCthe
sequentialCinstructionsCareCreloaded
fromCtheCresumeCcacheRCreducingCthe
mispredictedCbranchCpenaltyCbyCone
cyclefCTheCresumeCcacheChasCfourCentries
ofCfourCinstructionsCeachRCallowingCspec4
ulativeCexecutionCbeyondCfourCbranchesf
TheCRzppppCdesignCusesCtheCstan4
dardCtwo4bitCSmithCmethodCtoCpredict
M I C R O P R O C E S S O R  R E P O R T
MIPSoR10000oUsesoDecoupledoArchitecture VolfCFRCNofCzERCOctoberC,ERCz55E ©o1994oMicroDesignoResources
MIPSCRzppppCUsesCHecoupledC6rchitecture
High4PerformanceCooreCWillCHriveCMIPSCHigh47ndCforCYears
1 9 9 4
FORUMMICROPROCESSOR
Figure 1. The R10000 uses deep instruction queues to decouple the instruction fetch logic
from the ﬁve function units.
Instruction Cache
32K, two-way associative
PC
Unit
Predecode
Unit
ITLB
8 entry
Decode, Map,
Dispatch
Active
List
Map
Table
Main TLB
64 entries
ALU1
Data Cache
32K, two-way associative
FP
Adder
4 instr
4 instr
4 instr
Memory
Queue
16 entries
Integer
Queue
16 entries
FP
Queue
16 entries
ALU2 FP
Mult÷!
FP
÷
"
virtual
addr
phys addr
64
Data
SRAM
128
512K
-16M
Avalanche Bus (64 bit addr/data)
L2 Cache Interface
128
System Interface
Tag
SRAM
BHT
512 x 2
Resume
Cache
Address
Adder
Integer Registers
64 ! 64 bits
FP Registers
64 ! 64 bits
MIPS R10K uses sophisticated
out-of-order engine; branch
delay slot not useful
– Gwennap, MPR, 1994
Intel Nehalem frontend breaks x86 CISC
into smaller RISC-like µops; µcode engine
handles rarely used complex instr
– Kanter, Real World Technologies, 2009
73
10. Case Study: Transition from CISC to RISC 10.2. Example RISC: MIPS R2K
Microprogamming Today
• Microprogramming is far from extinct
• Played a crucial role in microprocessors of the 1980s
(DEC VAX, Motorola 68K series, Intel 386/486)
• Microprogramming plays assisting role in many modern processors
(AMD Phenom, Intel Nehalem, Intel Atom, IBM Z196)
– 761 Z196 instructions executed with hardwired control
– 219 Z196 “complex” instructions always executed with microcode
– 24 Z196 instructions conditionally executed with microcode
• Patchable microcode common for post-fabrication bug ﬁxes (Intel
processors load µcode patches at bootup)
74