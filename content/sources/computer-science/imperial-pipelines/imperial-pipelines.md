---
archive_policy: text-only
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-8b1491c048e8
  position:
    end: 8510
    start: 8418
    type: TextPositionSelector
  quote_sha256: sha256:f2d5dbccdc595fb720005b84c965d3cc868a685d1fc4ebd247c7854e3c7da130
  selector:
    exact: 'Pipelining doesn’t help latency of single instruction

      it helps throughput of entire workload'
    prefix: ' Cycle 4 Cycle 6 Cycle 7Cycle 5

      '
    suffix: '

      Pipeline rate limited by slowes'
    type: TextQuoteSelector
  selector_sha256: sha256:3a70a35e86e29ae70f21d37adba3173128d3a4b23c121b85ad30d4d73d192378
  snapshot_sha256: sha256:920997cc0ff95a10290da564f0e70ce0664f8b390d282c9d83ec2f038e57f0af
- evidence_id: evidence-aecc626b591d
  position:
    end: 8558
    start: 8511
    type: TextPositionSelector
  quote_sha256: sha256:0398625d89e1d88fb0a103e5e539ae7cc6fc7f235ff6269253276d042bf2bb09
  selector:
    exact: Pipeline rate limited by slowest pipeline stage
    prefix: 's throughput of entire workload

      '
    suffix: '

      Potential speedup = Number pipe'
    type: TextQuoteSelector
  selector_sha256: sha256:4c34096f29399860511ff49f27a9395718061499ab429d2f86d44b2a532e11b6
  snapshot_sha256: sha256:920997cc0ff95a10290da564f0e70ce0664f8b390d282c9d83ec2f038e57f0af
- evidence_id: evidence-33ccb50e3697
  position:
    end: 8031
    start: 7968
    type: TextPositionSelector
  quote_sha256: sha256:c071190d89f04556e9e73b6ddf650a2174f33e0d72f11a755be72432b679ca18
  selector:
    exact: At cycle 5 the pipeline is fully-occupied – all stages are busy
    prefix: 'Instr 2

      Instr 3

      Instr 4

      Instr 5

      '
    suffix: '

      IF is fetching Instr 5

      ID is de'
    type: TextQuoteSelector
  selector_sha256: sha256:0499ca338f78bb1da7d22ce972cca422d75f172d1da7469a0c381c108af16a2d
  snapshot_sha256: sha256:920997cc0ff95a10290da564f0e70ce0664f8b390d282c9d83ec2f038e57f0af
extractor: pypdf/6.16.2
id: imperial-pipelines
media_type: application/pdf
origin: external
read_status: retrieved
retrieval:
  acquisition: fetch
  resolved_url: https://www.doc.ic.ac.uk/~phjk/AdvancedCompArchitecture/Lectures/pdfs/Ch01-part2-Pipelines.pdf
  url: https://www.doc.ic.ac.uk/~phjk/AdvancedCompArchitecture/Lectures/pdfs/Ch01-part2-Pipelines.pdf
schema_version: source/v1
snapshot_sha256: sha256:920997cc0ff95a10290da564f0e70ce0664f8b390d282c9d83ec2f038e57f0af
source_type: doc
vault_id: public
---
October 2025
Paul H J Kelly
These lecture notes are partly based on the course text, Hennessy and 
Patterson’s Computer Architecture, a quantitative approach (6th ed), and on 
the lecture slides of David Patterson’s Berkeley course (CS252)
COMP60001/COMP70086
Advanced Computer Architecture
Chapter 1.2
Pipelining: a quick review of introductory computer 
architecture
Objective: bring everyone up to speed, and also establish some key ideas 
that will come up later in the course in more complicated contexts
Course materials online on 
https://scientia.doc.ic.ac.uk/2526/modules/60001/materials and 
https://www.doc.ic.ac.uk/~phjk/AdvancedCompArchitecture/aca20/ 
Pre-requisites
• This is a second-to-third-level computer architecture course
– We aim to get from what you’d learn in DoC’s first year up to 
understanding the design, and design alternatives, in current 
commercially-available processors
– It’s a stretch but my job is to help!
• You can take this course provided you’re prepared to catch 
up if necessary
– I will introduce all the key ideas, but if they are new to you, 
you will need to do some homework!
• We are keen to help you succeed – and I count on you to ask 
questions – both live and on EdStem
• This lecture introduces pipelining – we’re looking for the 
issues in simple designs that help us understand the more 
complicated designs that are coming up
Example: MIPS
Op
31 26 01516202125
Rs1 Rd immediate
Op
31 26 025
Op
31 26 01516202125
Rs1 Rs2
target
Rd Opx
Register-Register
561011
Register-Immediate
Op
31 26 01516202125
Rs1 Rs2/Opx immediate
Branch
Jump / Call
Eg:  ADD R8,R6,R4 // R8 ← R6+R4 ;   PC ← PC+4
 LW R2, 100(R3) // R2 ← Memory[R3+100] ; PC ← PC+4
 SW R5, 100(R6) // Memory[R6+100] ← R5 ; PC ← PC+4
 ADDI R4, R5, 50 // R4 ← R5+signExtend(50) ; PC ← PC+4
 BEQ R5, R7, 25 // if R5=R7 then PC ← PC+4+25*4 else PC ← PC+4
 J 200000 // PC ← 200000*4
Opcode specifies how 
other fields will be 
interpreted
5-bit register specifier at 
fixed field so access can 
start immediately 
Example: MIPS
Op
31 26 01516202125
Rs1 Rd immediate
Op
31 26 025
Op
31 26 01516202125
Rs1 Rs2
target
Rd Opx
Register-Register
561011
Register-Immediate
Op
31 26 01516202125
Rs1 Rs2/Opx immediate
Branch
Jump / Call
Eg:  ADD R8,R6,R4 // R8 ← R6+R4 ;   PC ← PC+4
 LW R2, 100(R3) // R2 ← Memory[R2+100] ; PC ← PC+4
 SW R5, 100(R6) // Memory[R6+100] ← R5 ; PC ← PC+4
 ADDI R4, R5, 50 // R4 ← R5+signExtend(50) ; PC ← PC+4
 BEQ R5, R7, 25 // if R5=R7 then PC ← PC+4+25*4 else PC ← PC+4
 J 200000 // PC ← 200000*4
Opcode specifies how 
other fields will be 
interpreted
5-bit register specifier at 
fixed field so access can 
start immediately 
ADD R8,R6,R4  // R8 ← R6+R4
LW R2, 100(R3) // R2 ← Memory[R3+100] 
SW R5, 100(R6) // Memory[R6+100] ← R5 
ADDI R4, R5, 50 // R4 ← R5+signExtend(50) 
;
BEQ R5, R7, 25 // if R5=R7 
  // then PC ← PC+4+25*4 
  // else PC ← PC+4
J 200000 // PC ← 200000*4
Example: MIPS
Op
31 26 01516202125
Rs1 Rd immediate
Op
31 26 025
Op
31 26 01516202125
Rs1 Rs2
target
Rd Opx
Register-Register
561011
Register-Immediate
Op
31 26 01516202125
Rs1 Rs2/Opx immediate
Branch
Jump / Call
Eg:  ADD R8,R6,R4 // R8 ← R6+R4 ;   PC ← PC+4
 LW R2, 100(R3) // R2 ← Memory[R3+100] ; PC ← PC+4
 SW R5, 100(R6) // Memory[R6+100] ← R5 ; PC ← PC+4
 ADDI R4, R5, 50 // R4 ← R5+signExtend(50) ; PC ← PC+4
 BEQ R5, R7, 25 // if R5=R7 then PC ← PC+4+25*4 else PC ← PC+4
 J 200000 // PC ← 200000*4
Opcode specifies how 
other fields will be 
interpreted
5-bit register specifier at 
fixed field so access can 
start immediately 
Q: How many 
registers can we 
address?
Q: What is the largest 
signed immediate 
operand for “ADD 
R1,R2,X”?
Q: What range of 
addresses can a 
conditional branch 
jump to?

A machine to execute these instructions
• To execute this instruction set we need a machine that fetches them and 
does what each instruction says
• A “universal” computing device – a simple digital circuit that, with the right 
code, can compute anything
• Something like:
Instr = Mem[PC]; PC+=4;
rs1 = Reg[Instr.rs1]; 
rs2 = Reg[Instr.rs2]; 
imm = SignExtend(Instr.imm); 
Operand1 = if(Instr.op==BRANCH) then PC else rs1;
Operand2 = if(immediateOperand(Instr.op)) then imm else rs2;
res = ALU(Instr.op, Operand1, Operand2);
switch(Instr.op) {
case BRANCH:
  if (rs1==0) then PC=PC+imm*4; continue;
case STORE:
  Mem[res] = rs1; continue;
case LOAD:
  lmd = Mem[res];
} 
Reg[Instr.rd] = if (Instr.op==LOAD) then lmd else res;  
5 Steps of MIPS Datapath
Memory
Access
Write
Back
Instruction
Fetch
Instr. Decode
Reg. Fetch
Execute
Addr. Calc
L
M
D
ALU
MUX
Memory
Reg File
MUXMUX
Data
Memory
MUX
Sign
Extend
4
Adder
Zero?
Next SEQ PC
Address
Next PC
WB Data
Inst
RD
RS1
RS2
Imm
Figure 3.1, Page 130, CA:AQA 2e

5 Steps of MIPS Datapath
Memory
Access
Write
Back
Instruction
Fetch
Instr. Decode
Reg. Fetch
Execute
Addr. Calc
L
M
D
ALU
MUX
Memory
Reg File
MUXMUX
Data
Memory
MUX
Sign
Extend
4
Adder
Zero?
Next SEQ PC
Address
Next PC
WB Data
Inst
RD
RS1
RS2
Imm
Figure 3.1, Page 130, CA:AQA 2e
Memory
Access
Write
Back
Instruction
Fetch
Instr. Decode
Reg. Fetch
Execute
Addr. Calc
ALU
Memory
Reg File
MUXMUX
Data
Memory
MUX
Sign
Extend
Zero?
IF/ID
ID/EX
MEM/WB
EX/MEM
4
Adder Next SEQ PC Next SEQ PC
RD RD RD
WB Data
Next PCAddress RS1
RS2
Imm
MUX
Figure 3.4, Page 134 , CA:AQA 2e
5-stage MIPS pipeline with pipeline buffers
Memory
Access
Write
Back
Instruction
Fetch
Instr. Decode
Reg. Fetch
Execute
Addr. Calc
ALU
Memory
Reg File
MUXMUX
Data
Memory
MUX
Sign
Extend
Zero?
IF/ID
ID/EX
MEM/WB
EX/MEM
4
Adder Next SEQ PC Next SEQ PC
RD RD RD
WB Data
Next PCAddress RS1
RS2
Imm
MUX
Figure 3.4, Page 134 , CA:AQA 2e
5-stage MIPS pipeline with pipeline buffers
Decode
Opcode
•  Data stationary control
– Control signals are needed to configure the MUXes, ALU, read/write
– Carried with the corresponding instruction along the pipeline 
Time (clock cycles)
Figure 3.3, Page 133 , CA:AQA 2e
Cycle 1 Cycle 2 Cycle 3 Cycle 4 Cycle 6 Cycle 7Cycle 5
Reg
ALU DMemIfetch Reg
Reg
ALU DMemIfetch Reg
Reg
ALU DMemIfetch Reg
Reg
ALU DMemIfetch Reg
Reg
ALU DMemIfetch Reg
Cycle 8 Cycle 9
Instr 1
Instr 2
Instr 3
Instr 4
Instr 5
Time (clock cycles)
Figure 3.3, Page 133 , CA:AQA 2e
Cycle 1 Cycle 2 Cycle 3 Cycle 4 Cycle 6 Cycle 7Cycle 5
Reg
ALU DMemIfetch Reg
Reg
ALU DMemIfetch Reg
Reg
ALU DMemIfetch Reg
Reg
ALU DMemIfetch Reg
Reg
ALU DMemIfetch Reg
Cycle 8 Cycle 9
Instr 1
Instr 2
Instr 3
Instr 4
Instr 5
At each cycle we fetch a new instruction
And pass the preceding instruction to the next stage of the 
pipeline
Time (clock cycles)
Figure 3.3, Page 133 , CA:AQA 2e
Cycle 1 Cycle 2 Cycle 3 Cycle 4 Cycle 6 Cycle 7Cycle 5
Reg
ALU DMemIfetch Reg
Reg
ALU DMemIfetch Reg
Reg
ALU DMemIfetch Reg
Reg
ALU DMemIfetch Reg
Reg
ALU DMemIfetch Reg
Cycle 8 Cycle 9
Instr 1
Instr 2
Instr 3
Instr 4
Instr 5
At each cycle we fetch a new instruction
And pass the preceding instruction to the next stage of the 
pipeline
Time (clock cycles)
Figure 3.3, Page 133 , CA:AQA 2e
Cycle 1 Cycle 2 Cycle 3 Cycle 4 Cycle 6 Cycle 7Cycle 5
Reg
ALU DMemIfetch Reg
Reg
ALU DMemIfetch Reg
Reg
ALU DMemIfetch Reg
Reg
ALU DMemIfetch Reg
Reg
ALU DMemIfetch Reg
Cycle 8 Cycle 9
Instr 1
Instr 2
Instr 3
Instr 4
Instr 5
At each cycle we fetch a new instruction
And pass the preceding instruction to the next stage of the 
pipeline
Time (clock cycles)
Figure 3.3, Page 133 , CA:AQA 2e
Cycle 1 Cycle 2 Cycle 3 Cycle 4 Cycle 6 Cycle 7Cycle 5
Reg
ALU DMemIfetch Reg
Reg
ALU DMemIfetch Reg
Reg
ALU DMemIfetch Reg
Reg
ALU DMemIfetch Reg
Reg
ALU DMemIfetch Reg
Cycle 8 Cycle 9
Instr 1
Instr 2
Instr 3
Instr 4
Instr 5
At each cycle we fetch a new instruction
And pass the preceding instruction to the next stage of the 
pipeline
Time (clock cycles)
Figure 3.3, Page 133 , CA:AQA 2e
Cycle 1 Cycle 2 Cycle 3 Cycle 4 Cycle 6 Cycle 7Cycle 5
Reg
ALU DMemIfetch Reg
Reg
ALU DMemIfetch Reg
Reg
ALU DMemIfetch Reg
Reg
ALU DMemIfetch Reg
Reg
ALU DMemIfetch Reg
Cycle 8 Cycle 9
Instr 1
Instr 2
Instr 3
Instr 4
Instr 5
At cycle 5 the pipeline is fully-occupied – all stages are busy
IF is fetching Instr 5
ID is decoding Instr 4
EX is executing Instr 3
MEM is handling Instr 2 if it is a load or store
WB is writing the register results from Instr 1 back
Pipelining:
facts of life
I
n
s
t
r.
O
r
d
e
r
Time (clock cycles)
Reg
ALU DMemIfetch Reg
Reg
ALU DMemIfetch Reg
Reg
ALU DMemIfetch Reg
Reg
ALU DMemIfetch Reg
Cycle 1 Cycle 2 Cycle 3 Cycle 4 Cycle 6 Cycle 7Cycle 5
Pipelining doesn’t help latency of single instruction
it helps throughput of entire workload
Pipeline rate limited by slowest pipeline stage
Potential speedup = Number pipe stages
Unbalanced lengths of pipe stages reduces speedup
Time to “fill” pipeline and time to “drain” it reduces speedup
Speedup comes from parallelism - for free – no new hardware
Many pipelines are more complex - Pentium 4 “Netburst” has 31 stages.
It’s Not That Easy 
• Limits to pipelining: Hazards prevent next 
instruction from executing during its 
designated clock cycle
– Structural hazards: the hardware cannot support 
this combination of instructions 
– Data hazards: Instruction depends on result of a 
prior instruction still in the pipeline 
– Control hazards: Caused by delay between the 
fetching of instructions and decisions about 
changes in control flow (branches and jumps).
Structural Hazard: example – one RAM port
I
n
s
t
r.
O
r
d
e
r
Time (clock cycles)
Load
Instr 1
Instr 2
Instr 3
Instr 4
Reg
ALU DMemIfetch Reg
Reg
ALU DMemIfetch Reg
Reg
ALU DMemIfetch Reg
Reg
ALU DMemIfetch Reg
Cycle 1 Cycle 2 Cycle 3 Cycle 4 Cycle 6 Cycle 7Cycle 5
Reg
ALU DMemIfetch Reg
Figure 3.6, Page 142 , CA:AQA 2e
• Eg if there is only one memory for both instructions and data
• Two different stages may need access at same time
• Example: IBM/Sony/Toshiba Cell processor’s “SPE” cores
– The microarchitecture of the synergistic processor for a cell processor (IEEE J. Solid-State Circuits (V41(1) , Jan 2006)
I
n
s
t
r.
O
r
d
e
r
Time (clock cycles)
Load
Instr 1
Instr 2
Stall
Instr 3
Reg
ALU DMemIfetch Reg
Reg
ALU DMemIfetch Reg
Reg
ALU DMemIfetch Reg
Cycle 1 Cycle 2 Cycle 3 Cycle 4 Cycle 6 Cycle 7Cycle 5
Reg
ALU DMemIfetch Reg
Figure 3.7, Page 143 , CA:AQA 2e
• Instr 3 cannot be loaded in cycle 4
• ID stage has nothing to do in cycle 5
• EX stage has nothing to do in cycle 6, etc.  “Bubble” propagates
Structural Hazard: example – one RAM port
Reg
ALU DMemIfetch Reg
I
n
s
t
r.
O
r
d
e
r
Time (clock cycles)
Load
Instr 1
Instr 2
Stall
Instr 3
Reg
ALU DMemIfetch Reg
Reg
ALU DMemIfetch Reg
Reg
ALU DMemIfetch Reg
Cycle 1 Cycle 2 Cycle 3 Cycle 4 Cycle 6 Cycle 7Cycle 5
Reg
ALU DMemIfetch Reg
Bubble Bubble Bubble BubbleBubble
Figure 3.7, Page 143 , CA:AQA 2e
• Instr 3 cannot be loaded in cycle 4
• ID stage has nothing to do in cycle 5
• EX stage has nothing to do in cycle 6, etc.  “Bubble” propagates
Structural Hazard: example – one RAM port
I
n
s
t
r.
O
r
d
e
r
add r1,r2,r3
sub r4,r1,r3
and r6,r1,r7
or   r8,r1,r9
xor r10,r1,r11
Reg
ALU DMemIfetch Reg
Reg
ALU DMemIfetch Reg
Reg
ALU DMemIfetch Reg
Reg
ALU DMemIfetch Reg
Reg
ALU DMemIfetch Reg
Data Hazard on R1
Time (clock cycles)
IF ID/RF EX MEM WB
Figure 3.9, page 147 , CA:AQA 2e
Time (clock cycles)
Forwarding to Avoid Data Hazard
Figure 3.10, Page 149 , CA:AQA 2e
I
n
s
t
r.
O
r
d
e
r
add r1,r2,r3
sub r4,r1,r3
and r6,r1,r7
or   r8,r1,r9
xor r10,r1,r11
Reg
ALU DMemIfetch Reg
Reg
ALU DMemIfetch Reg
Reg
ALU DMemIfetch Reg
Reg
ALU DMemIfetch Reg
Reg
ALU DMemIfetch Reg
HW Change for Forwarding
Figure 3.20, Page 161, CA:AQA 2e
MEM/WB
ID/EX
EX/MEM 
Data
Memory
ALU
muxmux
Registers
NextPC
Immediate
mux
Add forwarding (“bypass”) paths
Add multiplexors to select where ALU operand should come from
Determine mux control in ID stage
If source register is the target of an instrn that will not WB in time
Time (clock cycles)
I
n
s
t
r.
O
r
d
e
r
add r1, r0, 100
sub r4,r1,r6
and r6,r4,r7
or   r8,r6,r9
Forwarding builds the data flow graph
Reg
ALU DMemIfetch Reg
Reg
ALU DMemIfetch Reg
Reg
ALU DMemIfetch Reg
Reg
ALU DMemIfetch Reg
Values are passed directly from the output of the ALU to the input
Via forwarding wires
That are dynamically configured by the instruction decoder/control
(This gets much more exciting when we have multiple ALUs and multiple-issue)
I
n
s
t
r.
O
r
d
e
r
add r1, r0, 100
sub r4,r1,r6
and r6,r4,r7
or   r8,r6,r9
Imagine a 
machine with 
more ALUs
Reg
ALU
DMemIfetch Reg
We would need a rather complicated 
forwarding network
It’s a bit more complicated if three different 
instructions are issued each cycle 
ALU ALU
Reg
ALU
DMemIfetch Reg
ALU ALU
Reg
ALU
DMemIfetch Reg
ALU ALU
Reg
ALU
DMemIfetch Reg
ALU ALU
Time (clock cycles)
I
n
s
t
r.
O
r
d
e
r
lw r1, 0(r2)
sub r4,r1,r6
and r6,r1,r7
or   r8,r1,r9
Data Hazard Even with Forwarding
Figure 3.12, Page 153 , CA:AQA 2e
Reg
ALU DMemIfetch Reg
Reg
ALU DMemIfetch Reg
Reg
ALU DMemIfetch Reg
Reg
ALU DMemIfetch Reg
Time (clock cycles)
or   r8,r1,r9
I
n
s
t
r.
O
r
d
e
r
lw r1, 0(r2)
sub r4,r1,r6
and r6,r1,r7
Reg
ALU DMemIfetch Reg
RegIfetch
ALU DMem RegBubble
Ifetch
ALU DMem RegBubble Reg
Ifetch
ALU DMemBubble Reg
EX stage waits in cycle 4 for operand
Following instruction (“and”) waits in ID stage 
Missed instruction issue opportunity…
Data Hazard Even with Forwarding
Figure 3.12, Page 153 , CA:AQA 2e
Try producing fast code for
  a = b + c;
  d = e – f;
assuming a, b, c, d ,e, and f in memory. 
Slow code:
  
Software Scheduling to Avoid Load Hazards
Fast code:
  LW Rb,b LW Rb,b
LW Rc,c LW Rc,c
STALL LW Re,e
ADD Ra,Rb,Rc ADD Ra,Rb,Rc
SW a,Ra
LW Re,e
LW Rf,f LW Rf,f
STALL SW a,Ra
SUB Rd,Re,Rf SUB Rd,Re,Rf
SW d,Rd SW d,Rd
10 cycles (2 stalls) 8 cycles (0 stalls)
Show the stalls 
explicitly
Control Hazard on Branches
10: beq r1,r3,36
14: and r2,r3,r5 
18: or  r6,r1,r7
22: add r8,r1,r9
36: xor r10,r1,r11
Reg
ALU DMemIfetch Reg
Reg
ALU DMemIfetch Reg
Reg
ALU DMemIfetch Reg
Reg
ALU DMemIfetch Reg
Reg
ALU DMemIfetch Reg
If we’re not smart we risk a three-cycle stall
Adder
IF/ID
Pipelined MIPS Datapath with early branch determination
Memory
Access
Write
Back
Instruction
Fetch
Instr. Decode
Reg. Fetch
Execute
Addr. Calc
ALU
Memory
Reg File
MUX
Data
Memory
MUX
Sign
Extend
Zero?
MEM/WB
EX/MEM
4
Adder
Next 
SEQ 
PC
RD RD RD
WB Data
Next PCAddress RS1
RS2
Imm
MUX
ID/EX
Figure 3.22, page 163, CA:AQA 2/e
• Add extra hardware to the decode stage, to determine branch direction and target earlier
• We still have a one-cycle delay – we just have to fetch and start executing the next instruction
• If the branch is actually taken, block the MEM and WB stages and fetch the right instruction
Eliminating hazards with multi-threading
• If we had no stalls we could finish one instruction 
every cycle
• If we had no hazards we could do without 
forwarding – and decode/control would be simpler 
too
Reg
ALU DMemIfetch Reg
PC0
PC1
Next
PC
Thread 0
regs
Thread 1
regs
IF maintains two Program Counters
Even cycle – fetch from PC0
Odd cycle – fetch from PC1
Thread 0 reads and writes thread-0 registers
No register-to-register hazards between adjacent 
pipeline stages
Example: 
PowerPC 
processing 
element (PPE) 
in the Cell 
Broadband 
Engine (Sony 
PlayStation 3)
(cf “C-Slowing”......)
So – how fast can this design go?
A simple 5-stage pipeline can run at 5-9GHz
Limited by critical path through slowest pipeline stage 
logic
Tradeoff: do more per cycle?  Or increase clock rate?
Or do more per cycle, in parallel…
At 3GHz, clock period is 330 picoseconds.
The time light takes to go about four inches
About 10 gate delays
for example, the Cell BE is designed for 11 FO4 (“fan-out=4”) 
gates per cycle:
www.fe.infn.it/~belletti/articles/ISSCC2005-cell.pdf
Pipeline latches etc account for 3-5 FO4 delays leaving only 
5-8 for actual work
How can we build a RAM that can implement our MEM stage in 5-
8 FO4 delays?
Summary
This course is about fetch-execute 
machines!
The fetch-decode-execute sequence is 
naturally pipelinable
Pipelining would be wonderful… but:
Control hazards
Data hazards
Structural hazards
Hazards can sometimes be handled by 
forwarding
Hazards sometimes cause stalls
Control hazards are just trouble! But there 
are things we can do!
Pipeline design affects the maximum 
clock rate 
We will see how all of these can be 
tackled with dynamically-scheduled 
“out-of-order” microarchitectures
Next: tutorial exercise 1 on the 
connection between the instruction 
set and the pipeline architecture
And then we’ll look at caches and the 
memory system
For next week
Watch Ch01-part3 on caches
•  Make sure you understand it - 
•  come with questions
Have a think about the Turing Tax 
discussion exercise – watch the video!
•    Come prepared to talk about it!
Watch Ch02-part1 on dynamic instruction 
scheduling 
•  Come with questions!
Feeding curiosity
Do you really need pipeline latches?
Perhaps we could compute with just the wavefront of the 
signal as it propagates through the combinational logic?
But what if the wires are not precisely matched in length?
See Wave-Pipelining: A Tutorial and Research Survey, Burleson 
et al 1998 
https://ieeexplore.ieee.org/abstract/document/711317
Do we really need a global clock?
Look up asynchronous circuit design
What’s the optimal number of pipeline stages?
Eg see Optimizing Pipelines for Power and Performance, 
Srinivasan et al MICRO 2002 
https://vlsiarch.eecs.harvard.edu/sites/hwpi.harvard.edu/files/
vlsiarch/files/micro2002-optpipeline.pdf?m=1651843040