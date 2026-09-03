---
archive_policy: text-only
confidentiality: public
domain: computer-science
extractor: pypdf/6.16.2
id: ddca-lecture10-microarchitecture
media_type: application/pdf
origin: external
read_status: retrieved
retrieval:
  acquisition: fetch
  resolved_url: https://safari.ethz.ch/ddca/spring2026/lib/exe/fetch.php?media=onur-ddca-2026-lecture10-microarchitecture-fundamentals-design-afterlecture.pdf
  url: https://safari.ethz.ch/ddca/spring2026/lib/exe/fetch.php?media=onur-ddca-2026-lecture10-microarchitecture-fundamentals-design-afterlecture.pdf
schema_version: source/v1
snapshot_sha256: sha256:7a51de5468966c624784ff15ccdc9453f7ee8b3bbb3b4f6144e6e5967937e2a8
source_type: doc
vault_id: public
---
Digital Design & Computer Arch.
Lecture 10: Microarchitecture 
Fundamentals & Design
Dr. Mohammad Sadrosadati
Prof. Onur Mutlu
ETH Zürich
Spring 2026
20 March 2026
Agenda for Today & Next Few Lectures
 Instruction Set Architectures (ISA): LC-3 and MIPS
 Assembly programming: LC-3 and MIPS
 Microarchitecture (principles & single-cycle uarch)
 Multi-cycle microarchitecture
 Pipelining
 Issues in Pipelining: 
 Control & Data Dependence Handling 
 State Maintenance and Recovery
 Out-of-Order Execution
2
Micro-architecture
SW/HW Interface
Program/Language
Algorithm
Problem
Logic
Devices
System Software
Electrons
Readings
 This week
 Introduction to microarchitecture and single-cycle 
microarchitecture
 H&H, Chapter 7.1-7.3
 P&P, Appendices A and C
 Multi-cycle microarchitecture
 H&H, Chapter 7.4
 P&P, Appendices A and C
 Next week
 Pipelining
 H&H, Chapter 7.5
 Pipelining Issues
 H&H, Chapter 7.7, 7.8.1-7.8.3
3
Recall: Microarchitecture
 Implementation of the ISA under specific design constraints 
and goals
 Anything done in hardware without exposure to software
 Pipelining
 In-order versus out-of-order instruction execution
 Memory access scheduling policy
 Speculative execution
 Superscalar processing (multiple instruction issue?)
 Clock gating
 Caching? Levels, size, associativity, replacement policy
 Prefetching?
 Voltage/frequency scaling?
 Error correction?
4
Implementing the ISA: 
Microarchitecture Basics
Now That We Know What an ISA Is…
 How do we implement it?
 i.e., how do we design a system that obeys the 
hardware/software interface?
 Aside: “System” can be solely hardware or a combination of 
hardware and software
 Recall the “Translation of ISAs” 
 An ISA can be converted (by software or hardware) into an 
implementation ISA
 We will assume “completely hardware” implementation for 
most lectures
6
How Does a Machine Process Instructions? 
 What does processing an instruction mean?
 We will assume the von Neumann model (for now)
AS = Architectural (programmer visible) state before an 
instruction is processed
Process instruction
AS’ = Architectural (programmer visible) state after an 
instruction is processed
 Processing an instruction: Transforming AS to AS’ according 
to the ISA specification of the instruction
7
Recall: von Neumann Model/Architecture
Stored program
Sequential instruction processing
8
Recall: Programmer Visible (Architectural) State
9
M[0]
M[1]
M[2]
M[3]
M[4]
M[N-1]
Memory
array of storage locations
indexed by an address
Program Counter
memory address
of the current (or next) instruction
Registers
- given special names in the ISA
(as opposed to addresses)
- general vs. special purpose
Instructions (and programs) specify how to transform
the values of programmer visible state
The “Process Instruction” Step
 ISA specifies abstractly what AS’ should be, given an 
instruction and AS
 It defines an abstract finite state machine where
 State = programmer-visible state 
 Next-state logic = instruction execution specification
 From ISA point of view, there are no “intermediate states” 
between AS and AS’ during instruction execution
 One state transition per instruction
 Microarchitecture implements how AS is transformed to AS’
 There are many choices in implementation 
 We can have programmer-invisible state to optimize the speed of 
instruction execution: multiple state transitions per instruction
 Choice 1: AS  AS’ (transform AS to AS’ in a single clock cycle)
 Choice 2: AS  AS+MS1  AS+MS2  AS+MS3  AS’ (take multiple 
clock cycles to transform AS to AS’)
10
A Very Basic Instruction Processing Engine
 Each instruction takes a single clock cycle to execute
 Only combinational logic is used to implement instruction 
execution 
 No intermediate, programmer-invisible state updates
AS = Architectural (programmer visible) state 
at the beginning of a clock cycle
Process instruction in one clock cycle
AS’ = Architectural (programmer visible) state 
at the end of a clock cycle
11
A Very Basic Instruction Processing Engine
 Single-cycle machine
 What is the clock cycle time determined by?
 What is the critical path (i.e., longest delay path) of the 
combinational logic determined by?
12
AS’ ASSequential
Logic 
(State)
Combinational
Logic
AS: Architectural State
Single-cycle vs. Multi-cycle Machines
 Single-cycle machines
 Each instruction takes a single clock cycle
 All state updates made at the end of an instruction’s execution
 Big disadvantage: The slowest instruction determines cycle time 
long clock cycle time
 Multi-cycle machines 
 Instruction processing broken into multiple cycles/stages
 State updates can be made during an instruction’s execution
 Architectural state updates made at the end of an instruction’s 
execution
 Advantage over single-cycle: The slowest “stage” determines cycle time
 Both single-cycle and multi-cycle machines literally follow the 
von Neumann model at the microarchitecture level
13
Instruction Processing “Cycle”
 Instructions are processed under the direction of a “control 
unit” step by step. 
 Instruction cycle: Sequence of steps to process an instruction
 Fundamentally, there are six steps:
 Fetch
 Decode
 Evaluate Address
 Fetch Operands
 Execute
 Store Result
 Not all instructions require all six steps (see P&P Ch. 4)
14
Recall: The Instruction Processing “Cycle”
 FETCH
 DECODE
 EVALUATE ADDRESS
 FETCH OPERANDS
 EXECUTE
 STORE RESULT
15
Instruction Processing “Cycle” vs. Machine Clock Cycle
 Single-cycle machine: 
 All six phases of the instruction processing cycle take a single 
machine clock cycle to complete
 Multi-cycle machine: 
 All six phases of the instruction processing cycle can take 
multiple machine clock cycles to complete
 In fact, each phase can take multiple clock cycles to complete
16
Instruction Processing Viewed Another Way
 Instructions transform Data (AS) to Data’ (AS’)
 This transformation is done by functional units 
 Units that “operate” on data
 These units need to be told what to do to the data
 An instruction processing engine consists of two components
 Datapath: Consists of hardware elements that deal with and 
transform data signals
 functional units that operate on data
 hardware structures (e.g., wires, muxes, decoders, tri-state bufs) 
that enable the flow of data into the functional units and registers
 storage units that store data (e.g., registers)
 Control logic: Consists of hardware elements that determine 
control signals, i.e., signals that specify what the datapath
elements should do to the data
17
Recall: LC-3: A von Neumann Machine
18
Scanned by CamScanner
Control signals
Data
ALU: 2 inputs, 1 output
Memory Data 
Register
Memory Address
Register 16-bit 
addressable
Keyboard
KBDR (data), KBSR (status)
Monitor
DDR (data), DSR (status)
8 General Purpose 
Registers (GPR)
Finite State Machine 
(for Generating Control Signals)
Instruction 
Register
Program 
Counter
ALU operation
GateALU
Clock
Control 
Unit 
FSM
Single-cycle vs. Multi-cycle: Control & Data
 Single-cycle machine:
 Control signals are generated in the same clock cycle as the 
one during which data signals are operated on
 Everything related to an instruction happens in one clock cycle 
(serialized processing)
 Multi-cycle machine:
 Control signals needed in the next cycle can be generated in 
the current cycle
 Latency of control processing can be overlapped with latency 
of datapath operation (more parallelism)
 See P&P Appendix C for more (microprogrammed multi-
cycle microarchitecture)
19
Many Ways of Datapath and Control Design
 There are many ways of designing the datapath and control 
logic
 Example ways
 Single-cycle, multi-cycle, pipelined, out-of-order datapath & 
control
 Single-bus vs. multi-bus datapaths
 Hardwired/combinational vs. microcoded/microprogrammed 
control
 Control signals generated by combinational logic versus
 Control signals stored in a memory structure
 Control signals and structure depend on the datapath design
20
Flash-Forward: Performance Analysis
 Execution time of a single instruction
 {CPI}  x  {clock cycle time} 
 Execution time of an entire program
 Sum over all instructions [{CPI}  x  {clock cycle time}]
 {# of instructions}  x  {Average CPI}  x  {clock cycle time}
 Single-cycle microarchitecture performance 
 CPI = 1
 Clock cycle time = long
 Multi-cycle microarchitecture performance
 CPI = different for each instruction
 Average CPI  hopefully small
 Clock cycle time = short
21
In multi-cycle, we have 
two degrees of freedom
to optimize independently
CPI: Cycles Per Instruction
A Single-Cycle Microarchitecture
From the Ground Up
Remember…
 Single-cycle machine
23
ASSequential
Logic 
(State)
Combinational
Logic
AS’ 
AS: Architectural State
Let’s Start with the State Elements (MIPS)
 Data and control inputs
24
PC
Instruction
memory
Instruction
address
Instruction
a. Instruction memory b. Program counter
Add Sum
c. Adder
PC
Instruction
memory
Instruction
address
Instruction
a. Instruction memory b. Program counter
Add Sum
c. Adder
16 32Sign
extend
b. Sign-extension unit
MemRead
MemWrite
Data
memory
Write
data
Read
data
a. Data memory unit
Address
ALU control
RegWrite
Registers
Write
register
Read
data 1
Read
data 2
Read
register 1
Read
register 2
Write
data
ALU
result
ALU
Data
Data
Register
numbers
a. Registers b. ALU
Zero
5
5
5 3
**Based on original figure from [P&H CO&D, COPYRIGHT 2004 Elsevier. ALL RIGHTS RESERVED.] We will use this notation in lectures
Recall: A Memory Array (4 locations X 3 bits)
25
Di[2] Di[1] Di[0]
D[2] D[1] D[0]
Addr[1:0]
WE
Address Decoder
Multiplexer
MIPS State Elements
CLK
A RD
Instruction
Memory
A1
A3
WD3
RD2
RD1WE3
A2
CLK
Register
File
A RD
Data
Memory
WD
WEPCPC'
CLK
32 32
32 32
32
32
32 32
32
32
5
5
5
 Program counter: 
32-bit register 
 Instruction memory: 
Takes input 32-bit address A and reads the 32-bit data (i.e., instruction) 
from that address to the read data output RD
 Register file: 
The 32-element, 32-bit register file has 2 read ports and 1 write port
 Data memory: 
If the write enable, WE, is 1, it writes 32-bit data WD into memory location 
at 32-bit address A on the rising edge of the clock. 
If the write enable is 0, it reads 32-bit data from address A onto RD.
The H&H book uses this notation (H&H Chapter 7.3)
For Now, We Will Assume
 Ultra-fast (i.e., single-cycle) memory and register file
 Combinational read
 output of the read data port is a combinational function of the 
memory contents and the corresponding input address
 Synchronous write
 target location is updated at the positive edge clock transition 
when the write enable signal is asserted
 Cannot affect read output in-between positive clock edges
 Single-cycle memory
 Contrast this with memory that tells when the data is ready
 i.e., Ready signal: indicating the read or write is done
 See P&P Appendix C (LC3-b) for multi-cycle memory
27
Instruction Processing
 5 generic steps 
 Instruction fetch (IF)
 Instruction decode and register operand fetch (ID/RF)
 Execute/Evaluate memory address (EX/AG)
 Memory operand fetch (MEM)
 Store/writeback result (WB) 
28
Registers
Register #
Data
Register #
Data
memory
Address
Data
Register #
PC Instruction ALU
Instruction
memory
Address
IF
ID/RF EX/AG
MEM
WB
**Based on original figure from [P&H CO&D, COPYRIGHT 2004 Elsevier. ALL RIGHTS RESERVED.]
We Need to Provide the 
Datapath & Control Logic 
to Execute All ISA Instructions
What Is To Come: Single-Cycle MIPS Processor
Shift
left 2
PC
Instruction
memory
Read
address
Instruction
[31– 0]
Data
memory
Read
data
Write
data
Registers
Write
register
Write
data
Read
data 1
Read
data 2
Read
register 1
Read
register 2
Instruction [15– 11]
Instruction [20– 16]
Instruction [25– 21]
Add
ALU
result
Zero
Instruction [5– 0]
MemtoReg
ALUOp
MemWrite
RegWrite
MemRead
Branch
Jump
RegDst
ALUSrc
Instruction [31– 26]
4
M
u
x
Instruction [25– 0] Jump address [31– 0]
PC+4 [31– 28]
Sign
extend
16 32Instruction [15– 0]
1
M
u
x
1
0
M
u
x
0
1
M
u
x
0
1
ALU
control
Control
Add ALU
result
M
u
x
0
1 0
ALU
Shift
left 226 28
Address
PCSrc2=Br Taken
PCSrc1=Jump
ALU operation
bcond
**Based on original figure from [P&H CO&D, COPYRIGHT 2004 Elsevier. 
ALL RIGHTS RESERVED.] JAL, JR, JALR omitted
Another Complete Single-Cycle Processor
SignImm
CLK
A RD
Instruction
Memory
+
4
A1
A3
WD3
RD2
RD1WE3
A2
CLK
Sign Extend
Register
File
0
1
0
1
A RD
Data
Memory
WD
WE
0
1
PC0
1
PC' Instr
25:21
20:16
15:0
5:0
SrcB
20:16
15:11
<<2
+
ALUResult ReadData
WriteData
SrcA
PCPlus4
PCBranch
WriteReg 4:0
Result
31:26
RegDst
Branch
MemWrite
MemtoReg
ALUSrc
RegWrite
Op
Funct
Control
Unit
Zero
PCSrc
CLK
ALUControl2:0
ALU
31Single-cycle processor. Harris and Harris, Chapter 7.3.
Single-Cycle Datapath for
Arithmetic and Logical Instructions
 R-type: 3 register operands
 Semantics
R-Type ALU Instructions
33
add $s0, $s1, $s2       #$s0=rd, $s1=rs, $s2=rt
MIPS assembly (e.g., register-register signed addition)
Machine Encoding
if MEM[PC] == add rd rs rt
GPR[rd]  GPR[rs] + GPR[rt] 
PC  PC + 4
0 rs rt rd 0 add (32)
6 bits 5 bits 5 bits 5 bits 5 bits 6 bits
R-Type
(R-Type) ALU Datapath
34
PC
Instruction
memory
Read
address
Instruction
4
Add
Instruction
Registers
Write
register
Read
data 1
Read
data 2
Read
register 1
Read
register 2
Write
data
ALU
result
ALU
Zero
RegWrite
ALU operation3
1
15:11
20:16
25:21
**Based on original figure from [P&H CO&D, COPYRIGHT 2004 Elsevier. ALL RIGHTS RESERVED.]
if MEM[PC] == ADD rd rs rt
GPR[rd]  GPR[rs] + GPR[rt] 
PC  PC + 4
Combinational
state update logic
IF ID EX MEM WB
**Based on original figure from [P&H CO&D, COPYRIGHT 2004 Elsevier. ALL RIGHTS RESERVED.]
 ALU operation (F2:0) comes from the control logic
Example: ALU Design
+2
0
1
A B
Cout
Y
3
0
1
F2
F1:0
[N-1] S
NN
N
N
N NNN
N
2
Zero
Extend

 I-type: 2 register operands and 1 immediate
 Semantics
I-Type ALU Instructions
36
addi (0) rs rt immediate
addi $s0, $s1, 5           #$s0=rt, $s1=rs
MIPS assembly (e.g., register-immediate signed addition)
Machine Encoding
if MEM[PC] == addi rs rt immediate
PC  PC + 4
GPR[rt]  GPR[rs] + sign-extend(immediate) 
I-Type
5 bits 5 bits6 bits 16 bits
Datapath for R- and I-Type ALU Insts.
PC
Instruction
memory
Read
address
Instruction
4
Add
Instruction
16 32
RegistersWrite
register
Read
data 1
Read
data 2
Read
register 1
Read
register 2
Data
memoryWrite
data
Read
data
Write
data
Sign
extend
ALU
result
Zero
ALU
Address
MemRead
MemWrite
RegWrite
ALU operation3
1 ALUSrc
isItype
RegDest
isItype
15:11
20:16
25:21
**Based on original figure from [P&H CO&D, COPYRIGHT 2004 Elsevier. ALL RIGHTS RESERVED.]
if MEM[PC] == ADDI rt rs immediate
GPR[rt]  GPR[rs] + sign-extend (immediate) 
PC  PC + 4
Combinational
state update logic
IF ID EX MEM WB
n
 ADD assembly and machine code 
Recall: ADD with one Literal in LC-3
38
ADD R1, R4, #-2
LC-3 assembly
Field Values
Machine Code
1 1 4 1 -2
OP DR SR imm5
0 0 0 1 0 0 1 1 0 0 1 1 1 1 1 0
OP DR SR imm5
15 12 11 9 8 6 05 4
Register file
SR
DR
From 
FSM
Instruction register
Sign-
extend
Single-Cycle Datapath for
Data Movement Instructions
 Load 4-byte word
 Semantics
Load Instructions
40
lw (35) base rt offset
op rs=base rt imm=offset
lw $s3, 8($s0)             #$s0=rs, $s3=rt
MIPS assembly
Machine Encoding
I-Type
15 0162021252631
if MEM[PC] == lw rt offset16 (base)
PC  PC + 4
address = sign-extend(offset) + GPR(base)
GPR[rt]  MEM[address] 
LW Datapath
PC
Instruction
memory
Read
address
Instruction
4
Add
Instruction
16 32
RegistersWrite
register
Read
data 1
Read
data 2
Read
register 1
Read
register 2
Data
memoryWrite
data
Read
data
Write
data
Sign
extend
ALU
result
Zero
ALU
Address
MemRead
MemWrite
RegWrite
ALU operation3
ALUSrc
if MEM[PC]==LW rt offset16 (base) 
address = sign-extend(offset) + GPR[base]
GPR[rt]  MEM[address] 
PC  PC + 4
Combinational
state update logic
IF ID EX MEM WB
16 32Sign
extend
b. Sign-extension unit
MemRead
MemWrite
Data
memory
Write
data
Read
data
a. Data memory unit
Address
1
add
isItype
RegDest
isItype
1
0
n
Store Instructions
 Store 4-byte word
 Semantics
42
sw $s3, 8($s0)             #$s0=rs, $s3=rt
MIPS assembly
sw (43) base rt offset
op rs=base rt imm=offset
Machine Encoding
if Mem[PC] == sw rt offset16 (base)
PC  PC + 4
address = sign-extend(offset) + GPR(base)
MEM[address]  GPR[rt]
I-Type
15 0162021252631
SW Datapath
PC
Instruction
memory
Read
address
Instruction
4
Add
Instruction
16 32
RegistersWrite
register
Read
data 1
Read
data 2
Read
register 1
Read
register 2
Data
memoryWrite
data
Read
data
Write
data
Sign
extend
ALU
result
Zero
ALU
Address
MemRead
MemWrite
RegWrite
ALU operation3
if MEM[PC]==SW rt offset16 (base) 
address = sign-extend(offset) + GPR[base]
MEM[address]  GPR[rt] 
PC  PC + 4
Combinational
state update logic
IF ID EX MEM WB
16 32Sign
extend
b. Sign-extension unit
MemRead
MemWrite
Data
memory
Write
data
Read
data
a. Data memory unit
Address
0
add
ALUSrc
isItype
RegDest
isItype
0
1
n
Load-Store Datapath
44
PC
Instruction
memory
Read
address
Instruction
4
Add
Instruction
16 32
RegistersWrite
register
Read
data 1
Read
data 2
Read
register 1
Read
register 2
Data
memoryWrite
data
Read
data
Write
data
Sign
extend
ALU
result
Zero
ALU
Address
MemRead
MemWrite
RegWrite
ALU operation3
!isStore
add isStore
isLoad
ALUSrc
isItype
RegDest
isItype
**Based on original figure from [P&H CO&D, COPYRIGHT 
2004 Elsevier. ALL RIGHTS RESERVED.]
Datapath for Non-Control-Flow Insts.
45
PC
Instruction
memory
Read
address
Instruction
4
Add
Instruction
16 32
RegistersWrite
register
Read
data 1
Read
data 2
Read
register 1
Read
register 2
Data
memoryWrite
data
Read
data
Write
data
Sign
extend
ALU
result
Zero
ALU
Address
MemRead
MemWrite
RegWrite
ALU operation3
!isStore
isStore
isLoad
ALUSrc
isItype
MemtoReg
isLoad
RegDest
isItype
**Based on original figure from [P&H CO&D, COPYRIGHT 2004 Elsevier. ALL RIGHTS RESERVED.]
Single-Cycle Datapath for
Control Flow Instructions
Jump Instruction
 Unconditional branch or jump
 2 = opcode
 immediate (target) = target address
 Semantics
if MEM[PC]== j immediate26
target = { PC ✝[31:28], immediate26, 2’b00 }
PC  target
47
j (2) immediate
6 bits 26 bits
j target
J-Type
✝This is the incremented PC
Unconditional Jump Datapath
PC
Instruction
memory
Read
address
Instruction
4
Add
Instruction
16 32
RegistersWrite
register
Read
data 1
Read
data 2
Read
register 1
Read
register 2
Data
memoryWrite
data
Read
data
Write
data
Sign
extend
ALU
result
Zero
ALU
Address
MemRead
MemWrite
RegWrite
ALU operation3
ALUSrc
concat
PCSrc
isJ
What about JR, JAL, JALR?
?
**Based on original figure from [P&H CO&D, COPYRIGHT 
2004 Elsevier. ALL RIGHTS RESERVED.]
0
X 0
0
X
if MEM[PC]==J immediate26
PC = { PC ✝[31:28], immediate26, 2’b00 }
Do no harm
in datapath parts 
not involved
with jump
Is this correct?
Other Jumps in MIPS
 jr: jump register
Semantics
if MEM[PC]== jr rs
PC  GPR(rs)
 jal: jump and link (function calls)
Semantics
if MEM[PC]== jal immediate26
$ra  PC + 4
target = { PC ✝[31:28], immediate26, 2’b00 }
PC  target
 jalr: jump and link register
Semantics
if MEM[PC]== jalr rs
$ra  PC + 4
PC  GPR(rs)
49✝This is the incremented PC
Aside: MIPS Cheat Sheet
 https://safari.ethz.ch/digitaltechnik/spring2023/lib/exe/fetc
h.php?media=mips_reference_data.pdf
 On the course website
50

Conditional Branch Instructions
 beq (Branch if Equal)
 Semantics (assuming no branch delay slot)
if MEM[PC] == beq rs rt immediate16
target = PC✝+ sign-extend(immediate) x 4 
if GPR[rs]==GPR[rt] then PC  target
else PC  PC + 4
 Variations: beq, bne, blez, bgtz
51
beq (4) rs rt immediate=offset
6 bits 5 bits 5 bits 16 bits
beq $s0, $s1, offset #$s0=rs,$s1=rt
✝This is the incremented PC
I-Type
Conditional Branch Datapath (for you to finish)
16 32Sign
extend
ZeroALU
Sum
Shift
left 2
To branch
control logic
Branch target
PC + 4 from instruction datapath
Instruction
Add
Registers
Write
register
Read
data 1
Read
data 2
Read
register 1
Read
register 2
Write
data
RegWrite
ALU operation3
PC
Instruction
memory
Read
address
Instruction
4
Add
PCSrc
concat
0
sub
Foreshadowing: How to uphold the delayed branch semantics?
bcond
**Based on original figure from [P&H CO&D, COPYRIGHT 2004 Elsevier. ALL RIGHTS RESERVED.]
watch out
Putting It All Together
Shift
left 2
PC
Instruction
memory
Read
address
Instruction
[31– 0]
Data
memory
Read
data
Write
data
Registers
Write
register
Write
data
Read
data 1
Read
data 2
Read
register 1
Read
register 2
Instruction [15– 11]
Instruction [20– 16]
Instruction [25– 21]
Add
ALU
result
Zero
Instruction [5– 0]
MemtoReg
ALUOp
MemWrite
RegWrite
MemRead
Branch
Jump
RegDst
ALUSrc
Instruction [31– 26]
4
M
u
x
Instruction [25– 0] Jump address [31– 0]
PC+4 [31– 28]
Sign
extend
16 32Instruction [15– 0]
1
M
u
x
1
0
M
u
x
0
1
M
u
x
0
1
ALU
control
Control
Add ALU
result
M
u
x
0
1 0
ALU
Shift
left 226 28
Address
PCSrc2=Br Taken
PCSrc1=Jump
ALU operation
bcond
**Based on original figure from [P&H CO&D, COPYRIGHT 2004 Elsevier. 
ALL RIGHTS RESERVED.] JAL, JR, JALR omitted
Single-Cycle Control Logic
Single-Cycle Hardwired Control
 As combinational function of Inst=MEM[PC]
 Consider
 All R-type and I-type ALU instructions
 lw and sw
 beq, bne, blez, bgtz
 j, jr, jal, jalr omitted
55
0 rs rt rd shamt funct
6 bits 5 bits 5 bits 5 bits 5 bits 6 bits
R-Type
15 0162021252631 11 10 6 5
opcode rs rt immediate I-Type
15 0162021252631
6 bits 5 bits 5 bits 16 bits
opcode immediate
6 bits 26 bits
J-Type
0252631
Generate Control Signals (in Orange Color)
Shift
left 2
PC
Instruction
memory
Read
address
Instruction
[31– 0]
Data
memory
Read
data
Write
data
Registers
Write
register
Write
data
Read
data 1
Read
data 2
Read
register 1
Read
register 2
Instruction [15– 11]
Instruction [20– 16]
Instruction [25– 21]
Add
ALU
result
Zero
Instruction [5– 0]
MemtoReg
ALUOp
MemWrite
RegWrite
MemRead
Branch
Jump
RegDst
ALUSrc
Instruction [31– 26]
4
M
u
x
Instruction [25– 0] Jump address [31– 0]
PC+4 [31– 28]
Sign
extend
16 32Instruction [15– 0]
1
M
u
x
1
0
M
u
x
0
1
M
u
x
0
1
ALU
control
Control
Add ALU
result
M
u
x
0
1 0
ALU
Shift
left 226 28
Address
PCSrc2=Br Taken
PCSrc1=Jump
ALU operation
bcond
**Based on original figure from [P&H CO&D, COPYRIGHT 2004 Elsevier. 
ALL RIGHTS RESERVED.] JAL, JR, JALR omitted
Single-Bit Control Signals (I)
When De-asserted When asserted Equation
RegDst
GPR write select 
according to rt, i.e., 
inst[20:16]
GPR write select 
according to rd, i.e., 
inst[15:11]
opcode==0
ALUSrc
2nd ALU input from      
2nd GPR read port
2nd ALU input from  
sign-extended 16-bit 
immediate
(opcode!=0) &&
(opcode!=BEQ) &&
(opcode!=BNE)
MemtoReg Steer ALU result            
to GPR write port
Steer memory output    
to GPR write port
opcode==LW
RegWrite
GPR write disabled GPR write enabled (opcode!=SW) &&
(opcode!=Bxx) &&
(opcode!=J) &&
(opcode!=JR))
JAL and JALR require additional RegDst and MemtoReg options 
Single-Bit Control Signals (II)
When De-asserted When asserted Equation
MemRead Memory read disabled Memory read port 
returns load value
opcode==LW
MemWrite Memory write disabled Memory write enabled opcode==SW
PCSrc1
According to PCSrc2 next PC is based on 26-
bit immediate jump 
target
(opcode==J) ||
(opcode==JAL)
PCSrc2
next PC = PC + 4 next PC is based on     
16-bit immediate 
branch target
(opcode==Bxx) &&
“bcond is satisfied”
JR and JALR require additional PCSrc options 
R-Type ALU
Shift
left 2
PC
Instruction
memory
Read
address
Instruction
[31– 0]
Data
memory
Read
data
Write
data
Registers
Write
register
Write
data
Read
data 1
Read
data 2
Read
register 1
Read
register 2
Instruction [15– 11]
Instruction [20– 16]
Instruction [25– 21]
Add
ALU
result
Zero
Instruction [5– 0]
MemtoReg
ALUOp
MemWrite
RegWrite
MemRead
Branch
Jump
RegDst
ALUSrc
Instruction [31– 26]
4
M
u
x
Instruction [25– 0] Jump address [31– 0]
PC+4 [31– 28]
Sign
extend
16 32Instruction [15– 0]
1
M
u
x
1
0
M
u
x
0
1
M
u
x
0
1
ALU
control
Control
Add ALU
result
M
u
x
0
1 0
ALU
Shift
left 226 28
Address
PCSrc2=Br Taken
PCSrc1=Jump
ALU operation
bcond
**Based on original figure from [P&H CO&D, COPYRIGHT 
2004 Elsevier. ALL RIGHTS RESERVED.]
1 0
0funct
I-Type ALU
Shift
left 2
PC
Instruction
memory
Read
address
Instruction
[31– 0]
Data
memory
Read
data
Write
data
Registers
Write
register
Write
data
Read
data 1
Read
data 2
Read
register 1
Read
register 2
Instruction [15– 11]
Instruction [20– 16]
Instruction [25– 21]
Add
ALU
result
Zero
Instruction [5– 0]
MemtoReg
ALUOp
MemWrite
RegWrite
MemRead
Branch
Jump
RegDst
ALUSrc
Instruction [31– 26]
4
M
u
x
Instruction [25– 0] Jump address [31– 0]
PC+4 [31– 28]
Sign
extend
16 32Instruction [15– 0]
1
M
u
x
1
0
M
u
x
0
1
M
u
x
0
1
ALU
control
Control
Add ALU
result
M
u
x
0
1 0
ALU
Shift
left 226 28
Address
PCSrc2=Br Taken
PCSrc1=Jump
ALU operation
1 0
0
bcond
**Based on original figure from [P&H CO&D, COPYRIGHT 2004 
Elsevier. ALL RIGHTS RESERVED.]
opcode
LW
Shift
left 2
PC
Instruction
memory
Read
address
Instruction
[31– 0]
Data
memory
Read
data
Write
data
Registers
Write
register
Write
data
Read
data 1
Read
data 2
Read
register 1
Read
register 2
Instruction [15– 11]
Instruction [20– 16]
Instruction [25– 21]
Add
ALU
result
Zero
Instruction [5– 0]
MemtoReg
ALUOp
MemWrite
RegWrite
MemRead
Branch
Jump
RegDst
ALUSrc
Instruction [31– 26]
4
M
u
x
Instruction [25– 0] Jump address [31– 0]
PC+4 [31– 28]
Sign
extend
16 32Instruction [15– 0]
1
M
u
x
1
0
M
u
x
0
1
M
u
x
0
1
ALU
control
Control
Add ALU
result
M
u
x
0
1 0
ALU
Shift
left 226 28
Address
PCSrc2=Br Taken
PCSrc1=Jump
ALU operation
1 0
1
bcond
**Based on original figure from [P&H CO&D, COPYRIGHT 2004 
Elsevier. ALL RIGHTS RESERVED.]
Add
SW
Shift
left 2
PC
Instruction
memory
Read
address
Instruction
[31– 0]
Data
memory
Read
data
Write
data
Registers
Write
register
Write
data
Read
data 1
Read
data 2
Read
register 1
Read
register 2
Instruction [15– 11]
Instruction [20– 16]
Instruction [25– 21]
Add
ALU
result
Zero
Instruction [5– 0]
MemtoReg
ALUOp
MemWrite
RegWrite
MemRead
Branch
Jump
RegDst
ALUSrc
Instruction [31– 26]
4
M
u
x
Instruction [25– 0] Jump address [31– 0]
PC+4 [31– 28]
Sign
extend
16 32Instruction [15– 0]
1
M
u
x
1
0
M
u
x
0
1
M
u
x
0
1
ALU
control
Control
Add ALU
result
M
u
x
0
1 0
ALU
Shift
left 226 28
Address
PCSrc2=Br Taken
PCSrc1=Jump
ALU operation
0 1
0
XX
bcond
**Based on original figure from [P&H CO&D, COPYRIGHT 2004 
Elsevier. ALL RIGHTS RESERVED.]
Add
Branch (Not Taken)
Shift
left 2
PC
Instruction
memory
Read
address
Instruction
[31– 0]
Data
memory
Read
data
Write
data
Registers
Write
register
Write
data
Read
data 1
Read
data 2
Read
register 1
Read
register 2
Instruction [15– 11]
Instruction [20– 16]
Instruction [25– 21]
Add
ALU
result
Zero
Instruction [5– 0]
MemtoReg
ALUOp
MemWrite
RegWrite
MemRead
Branch
Jump
RegDst
ALUSrc
Instruction [31– 26]
4
M
u
x
Instruction [25– 0] Jump address [31– 0]
PC+4 [31– 28]
Sign
extend
16 32Instruction [15– 0]
1
M
u
x
1
0
M
u
x
0
1
M
u
x
0
1
ALU
control
Control
Add ALU
result
M
u
x
0
1 0
ALU
Shift
left 226 28
Address
PCSrc2=Br Taken
PCSrc1=Jump
ALU operation
0 0
0
XX
bcond
**Based on original figure from [P&H CO&D, COPYRIGHT 2004 
Elsevier. ALL RIGHTS RESERVED.]
bcond
Some control signals are dependent
on the processing of data
Branch (Taken)
Shift
left 2
PC
Instruction
memory
Read
address
Instruction
[31– 0]
Data
memory
Read
data
Write
data
Registers
Write
register
Write
data
Read
data 1
Read
data 2
Read
register 1
Read
register 2
Instruction [15– 11]
Instruction [20– 16]
Instruction [25– 21]
Add
ALU
result
Zero
Instruction [5– 0]
MemtoReg
ALUOp
MemWrite
RegWrite
MemRead
Branch
Jump
RegDst
ALUSrc
Instruction [31– 26]
4
M
u
x
Instruction [25– 0] Jump address [31– 0]
PC+4 [31– 28]
Sign
extend
16 32Instruction [15– 0]
1
M
u
x
1
0
M
u
x
0
1
M
u
x
0
1
ALU
control
Control
Add ALU
result
M
u
x
0
1 0
ALU
Shift
left 226 28
Address
PCSrc2=Br Taken
PCSrc1=Jump
ALU operation
0 0
0
XX
bcond
**Based on original figure from [P&H CO&D, COPYRIGHT 
2004 Elsevier. ALL RIGHTS RESERVED.]
bcond
Some control signals are dependent
on the processing of data
Jump
Shift
left 2
PC
Instruction
memory
Read
address
Instruction
[31– 0]
Data
memory
Read
data
Write
data
Registers
Write
register
Write
data
Read
data 1
Read
data 2
Read
register 1
Read
register 2
Instruction [15– 11]
Instruction [20– 16]
Instruction [25– 21]
Add
ALU
result
Zero
Instruction [5– 0]
MemtoReg
ALUOp
MemWrite
RegWrite
MemRead
Branch
Jump
RegDst
ALUSrc
Instruction [31– 26]
4
M
u
x
Instruction [25– 0] Jump address [31– 0]
PC+4 [31– 28]
Sign
extend
16 32Instruction [15– 0]
1
M
u
x
1
0
M
u
x
0
1
M
u
x
0
1
ALU
control
Control
Add ALU
result
M
u
x
0
1 0
ALU
Shift
left 226 28
Address
PCSrc2=Br Taken
PCSrc1=Jump
ALU operation
0 0
0
XX
X
X
bcond
**Based on original figure from [P&H CO&D, COPYRIGHT 
2004 Elsevier. ALL RIGHTS RESERVED.]
X
What is in That Control Box?
 Combinational Logic  Hardwired Control
 Idea: Control signals generated combinationally based on bits 
in instruction encoding
 Sequential Logic  Sequential Control
 Idea: A memory structure contains the control signals 
associated with an instruction
 Called Control Store
 Both types of control structure can be used in single-cycle 
processors
 Choice depends on latency of each structure + how much on 
the critical path control signal generation is, etc. 
66
Review: Complete Single-Cycle Processor
Shift
left 2
PC
Instruction
memory
Read
address
Instruction
[31– 0]
Data
memory
Read
data
Write
data
Registers
Write
register
Write
data
Read
data 1
Read
data 2
Read
register 1
Read
register 2
Instruction [15– 11]
Instruction [20– 16]
Instruction [25– 21]
Add
ALU
result
Zero
Instruction [5– 0]
MemtoReg
ALUOp
MemWrite
RegWrite
MemRead
Branch
Jump
RegDst
ALUSrc
Instruction [31– 26]
4
M
u
x
Instruction [25– 0] Jump address [31– 0]
PC+4 [31– 28]
Sign
extend
16 32Instruction [15– 0]
1
M
u
x
1
0
M
u
x
0
1
M
u
x
0
1
ALU
control
Control
Add ALU
result
M
u
x
0
1 0
ALU
Shift
left 226 28
Address
PCSrc2=Br Taken
PCSrc1=Jump
ALU operation
bcond
**Based on original figure from [P&H CO&D, COPYRIGHT 2004 Elsevier. 
ALL RIGHTS RESERVED.] JAL, JR, JALR omitted
Another Single-Cycle 
MIPS Processor (from H&H)
See backup slides to reinforce the concepts we have covered. 
They are to complement your reading:
H&H, Chapter 7.1-7.3, 7.6
Another Complete Single-Cycle Processor
SignImm
CLK
A RD
Instruction
Memory
+
4
A1
A3
WD3
RD2
RD1WE3
A2
CLK
Sign Extend
Register
File
0
1
0
1
A RD
Data
Memory
WD
WE
0
1
PC0
1
PC' Instr
25:21
20:16
15:0
5:0
SrcB
20:16
15:11
<<2
+
ALUResult ReadData
WriteData
SrcA
PCPlus4
PCBranch
WriteReg 4:0
Result
31:26
RegDst
Branch
MemWrite
MemtoReg
ALUSrc
RegWrite
Op
Funct
Control
Unit
Zero
PCSrc
CLK
ALUControl2:0
ALU
69Single-cycle processor. Harris and Harris, Chapter 7.3.
Carnegie Mellon
70
Example: Single-Cycle Datapath: lw fetch
 STEP 1: Fetch instruction
CLK
A RD
Instruction
Memory
A1
A3
WD3
RD2
RD1WE3
A2
CLK
Register
File
A RD
Data
Memory
WD
WEPCPC' Instr
CLK
lw $s3, 1($0)          # read memory word 1 into $s3
op rs rt imm
6 bits 5 bits 5 bits 16 bits
I-Type
Carnegie Mellon
71
Single-Cycle Datapath: lw register read
 STEP 2: Read source operands from register file
Instr
CLK
A RD
Instruction
Memory
A1
A3
WD3
RD2
RD1WE3
A2
CLK
Register
File
A RD
Data
Memory
WD
WE
PCPC'
25:21
CLK
lw $s3, 1($0)          # read memory word 1 into $s3
op rs rt imm
6 bits 5 bits 5 bits 16 bits
I-Type
Carnegie Mellon
72
Single-Cycle Datapath: lw immediate
 STEP 3: Sign-extend the immediate
SignImm
CLK
A RD
Instruction
Memory
A1
A3
WD3
RD2
RD1WE3
A2
CLK
Sign Extend
Register
File
A RD
Data
Memory
WD
WE
PCPC' Instr
25:21
15:0
CLK
lw $s3, 1($0)          # read memory word 1 into $s3
op rs rt imm
6 bits 5 bits 5 bits 16 bits
I-Type
Carnegie Mellon
73
Single-Cycle Datapath: lw address
 STEP 4: Compute the memory address
SignImm
CLK
A RD
Instruction
Memory
A1
A3
WD3
RD2
RD1WE3
A2
CLK
Sign Extend
Register
File
A RD
Data
Memory
WD
WE
PCPC' Instr
25:21
15:0
SrcB
ALUResult
SrcA Zero
CLK
ALUControl2:0
ALU
010
lw $s3, 1($0)          # read memory word 1 into $s3
op rs rt imm
6 bits 5 bits 5 bits 16 bits
I-Type
Carnegie Mellon
74
Single-Cycle Datapath: lw memory read
 STEP 5: Read from memory and write back to register file
A1
A3
WD3
RD2
RD1WE3
A2
SignImm
CLK
A RD
Instruction
Memory
CLK
Sign Extend
Register
File
A RD
Data
Memory
WD
WE
PCPC' Instr
25:21
15:0
SrcB20:16
ALUResult ReadData
SrcA
RegWrite
Zero
CLK
ALUControl2:0
ALU
0101
lw $s3, 1($0)          # read memory word 1 into $s3
op rs rt imm
6 bits 5 bits 5 bits 16 bits
I-Type
Carnegie Mellon
75
Single-Cycle Datapath: lw PC increment
 STEP 6: Determine address of next instruction
SignImm
CLK
A RD
Instruction
Memory
+
4
A1
A3
WD3
RD2
RD1WE3
A2
CLK
Sign Extend
Register
File
A RD
Data
Memory
WD
WE
PCPC' Instr
25:21
15:0
SrcB
20:16
ALUResult ReadData
SrcA
PCPlus4
Result
RegWrite
Zero
CLK
ALUControl2:0
ALU
0101
lw $s3, 1($0)          # read memory word 1 into $s3
op rs rt imm
6 bits 5 bits 5 bits 16 bits
I-Type
 Control signals are generated by the decoder in control unit
Similarly, We Need to Design the Control Unit
Instruction Op5:0 RegWrite RegDst AluSrc Branch MemWrite MemtoReg ALUOp1:0 Jump
R-type 000000 1 1 0 0 0 0 10 0
lw 100011 1 0 1 0 0 1 00 0
sw 101011 0 X 1 0 1 X 00 0
beq 000100 0 X 0 1 0 X 01 0
addi 001000 1 0 1 0 0 0 00 0
j 000010 0 X X X 0 X XX 1
76Single-cycle processor. Harris and Harris, Chapter 7.3.
Another Complete Single-Cycle Processor (H&H)
SignImm
CLK
A RD
Instruction
Memory
+
4
A1
A3
WD3
RD2
RD1WE3
A2
CLK
Sign Extend
Register
File
0
1
0
1
A RD
Data
Memory
WD
WE
0
1
PC0
1
PC' Instr
25:21
20:16
15:0
5:0
SrcB
20:16
15:11
<<2
+
ALUResult ReadData
WriteData
SrcA
PCPlus4
PCBranch
WriteReg 4:0
Result
31:26
RegDst
Branch
MemWrite
MemtoReg
ALUSrc
RegWrite
Op
Funct
Control
Unit
Zero
PCSrc
CLK
ALUControl2:0
ALU
77
Your Reading Assignment
 Please go over and internalize the Lecture Slides & 
Backup Slides
 Please do your readings from the H&H Book
 H&H, Chapter 7.1-7.3, 7.6
78
Single-Cycle Uarch I (We Developed in Lectures)
Shift
left 2
PC
Instruction
memory
Read
address
Instruction
[31– 0]
Data
memory
Read
data
Write
data
Registers
Write
register
Write
data
Read
data 1
Read
data 2
Read
register 1
Read
register 2
Instruction [15– 11]
Instruction [20– 16]
Instruction [25– 21]
Add
ALU
result
Zero
Instruction [5– 0]
MemtoReg
ALUOp
MemWrite
RegWrite
MemRead
Branch
Jump
RegDst
ALUSrc
Instruction [31– 26]
4
M
u
x
Instruction [25– 0] Jump address [31– 0]
PC+4 [31– 28]
Sign
extend
16 32Instruction [15– 0]
1
M
u
x
1
0
M
u
x
0
1
M
u
x
0
1
ALU
control
Control
Add ALU
result
M
u
x
0
1 0
ALU
Shift
left 226 28
Address
PCSrc2=Br Taken
PCSrc1=Jump
ALU operation
bcond
**Based on original figure from [P&H CO&D, COPYRIGHT 2004 Elsevier. 
ALL RIGHTS RESERVED.] JAL, JR, JALR omitted
Single-Cycle Uarch II (In Your Readings)
SignImm
CLK
A RD
Instruction
Memory
+
4
A1
A3
WD3
RD2
RD1WE3
A2
CLK
Sign Extend
Register
File
0
1
0
1
A RD
Data
Memory
WD
WE
0
1
PC0
1
PC' Instr
25:21
20:16
15:0
5:0
SrcB
20:16
15:11
<<2
+
ALUResult ReadData
WriteData
SrcA
PCPlus4
PCBranch
WriteReg 4:0
Result
31:26
RegDst
Branch
MemWrite
MemtoReg
ALUSrc
RegWrite
Op
Funct
Control
Unit
Zero
PCSrc
CLK
ALUControl2:0
ALU
80Single-cycle processor. Harris and Harris, Chapter 7.3.
Evaluating the Single-Cycle 
Microarchitecture
81
A Single-Cycle Microarchitecture
 Is this a good idea/design?
 When is this a good design?
 When is this a bad design?
 How can we design a better microarchitecture?
82
Performance Analysis Basics
Recall: Performance Analysis Basics
 Execution time of a single instruction
 {CPI}  x  {clock cycle time} 
 CPI: Number of cycles it takes to execute an instruction
 Execution time of an entire program
 Sum over all instructions [{CPI}  x  {clock cycle time}]
 {# of instructions}  x  {Average CPI}  x  {clock cycle time}
84
Carnegie Mellon
85
Processor Performance
 How fast is my program?
 Every program consists of a series of instructions
 Each instruction needs to be executed
Carnegie Mellon
86
Processor Performance
 How fast is my program?
 Every program consists of a series of instructions
 Each instruction needs to be executed
 How fast are my instructions?
 Instructions are realized on the hardware
 Each instruction can take one or more clock cycles to complete
 Cycles per Instruction = CPI
Carnegie Mellon
87
Processor Performance
 How fast is my program?
 Every program consists of a series of instructions
 Each instruction needs to be executed
 How fast are my instructions?
 Instructions are realized on the hardware
 Each instruction can take one or more clock cycles to complete
 Cycles per Instruction = CPI
 How long is one clock cycle?
 The critical path determines how much time one cycle requires = 
clock period
 1/clock period = clock frequency = how many clock cycles are in 
each second
Carnegie Mellon
88
Processor Performance
 As a general formula
 Our program consists of executing N instructions
 Our processor needs CPI cycles (on average) for each instruction
 The clock frequency of the processor is f 
 the clock period is therefore T=1/f
Carnegie Mellon
89
Processor Performance
 As a general formula
 Our program consists of executing N instructions
 Our processor needs CPI cycles (on average) for each instruction
 The clock frequency of the processor is f 
 the clock period is therefore T=1/f
 Our program executes in 
N x CPI x (1/f) = 
N x CPI x T seconds
Performance Analysis of 
Our Single-Cycle Design
A Single-Cycle Microarchitecture: Analysis
 Every instruction takes 1 cycle to execute
 CPI (Cycles per instruction) is strictly 1
 How long each instruction takes is determined by how long 
the slowest instruction takes to execute
 Even though many instructions do not need that long to 
execute
 Clock cycle time of the microarchitecture is determined by 
how long it takes to complete the slowest instruction
 Critical path of the design is determined by the processing 
time of the slowest instruction
91
What is the Slowest Instruction to Process?
 Let’s go back to the basics
 All six phases of the instruction processing cycle take a single 
machine clock cycle to complete
 Fetch
 Decode
 Evaluate Address
 Fetch Operands
 Execute
 Store Result
 Does every instruction take the same time (latency) to 
complete?
92
1. Instruction fetch (IF)
2. Instruction decode and 
register operand fetch (ID/RF)
3. Execute/Evaluate memory address (EX/AG)
4. Memory operand fetch (MEM)
5. Store/writeback result (WB) 
Let’s Find the Critical Path
Shift
left 2
PC
Instruction
memory
Read
address
Instruction
[31– 0]
Data
memory
Read
data
Write
data
Registers
Write
register
Write
data
Read
data 1
Read
data 2
Read
register 1
Read
register 2
Instruction [15– 11]
Instruction [20– 16]
Instruction [25– 21]
Add
ALU
result
Zero
Instruction [5– 0]
MemtoReg
ALUOp
MemWrite
RegWrite
MemRead
Branch
Jump
RegDst
ALUSrc
Instruction [31– 26]
4
M
u
x
Instruction [25– 0] Jump address [31– 0]
PC+4 [31– 28]
Sign
extend
16 32Instruction [15– 0]
1
M
u
x
1
0
M
u
x
0
1
M
u
x
0
1
ALU
control
Control
Add ALU
result
M
u
x
0
1 0
ALU
Shift
left 226 28
Address
PCSrc2=Br Taken
PCSrc1=Jump
ALU operation
bcond
[Based on original figure from P&H CO&D, COPYRIGHT 2004 
Elsevier. ALL RIGHTS RESERVED.]
steps IF ID EX MEM WB
Delay
resources mem RF ALU mem RF
R-type 200 50 100 50 400
I-type 200 50 100 50 400
LW 200 50 100 200 50 600
SW 200 50 100 200 550
Branch 200 50 100 350
Jump 200 200
Example Single-Cycle Datapath Analysis
 Assume (for the design in the previous slide)
 memory units (read or write): 200 ps
 ALU and adders: 100 ps
 register file (read or write): 50 ps
 other logic or wire delay: 0 ps
Let’s Find the Critical Path
Shift
left 2
PC
Instruction
memory
Read
address
Instruction
[31– 0]
Data
memory
Read
data
Write
data
Registers
Write
register
Write
data
Read
data 1
Read
data 2
Read
register 1
Read
register 2
Instruction [15– 11]
Instruction [20– 16]
Instruction [25– 21]
Add
ALU
result
Zero
Instruction [5– 0]
MemtoReg
ALUOp
MemWrite
RegWrite
MemRead
Branch
Jump
RegDst
ALUSrc
Instruction [31– 26]
4
M
u
x
Instruction [25– 0] Jump address [31– 0]
PC+4 [31– 28]
Sign
extend
16 32Instruction [15– 0]
1
M
u
x
1
0
M
u
x
0
1
M
u
x
0
1
ALU
control
Control
Add ALU
result
M
u
x
0
1 0
ALU
Shift
left 226 28
Address
PCSrc2=Br Taken
PCSrc1=Jump
ALU operation
bcond
[Based on original figure from P&H CO&D, COPYRIGHT 2004 
Elsevier. ALL RIGHTS RESERVED.]
R-Type and I-Type ALU
Shift
left 2
PC
Instruction
memory
Read
address
Instruction
[31– 0]
Data
memory
Read
data
Write
data
Registers
Write
register
Write
data
Read
data 1
Read
data 2
Read
register 1
Read
register 2
Instruction [15– 11]
Instruction [20– 16]
Instruction [25– 21]
Add
ALU
result
Zero
Instruction [5– 0]
MemtoReg
ALUOp
MemWrite
RegWrite
MemRead
Branch
Jump
RegDst
ALUSrc
Instruction [31– 26]
4
M
u
x
Instruction [25– 0] Jump address [31– 0]
PC+4 [31– 28]
Sign
extend
16 32Instruction [15– 0]
1
M
u
x
1
0
M
u
x
0
1
M
u
x
0
1
ALU
control
Control
Add ALU
result
M
u
x
0
1 0
ALU
Shift
left 226 28
Address
PCSrc2=Br Taken
PCSrc1=Jump
ALU operation
bcond
[Based on original figure from P&H CO&D, COPYRIGHT 
2004 Elsevier. ALL RIGHTS RESERVED.]
200ps 250ps
350ps400ps
100ps
100ps
LW
Shift
left 2
PC
Instruction
memory
Read
address
Instruction
[31– 0]
Data
memory
Read
data
Write
data
Registers
Write
register
Write
data
Read
data 1
Read
data 2
Read
register 1
Read
register 2
Instruction [15– 11]
Instruction [20– 16]
Instruction [25– 21]
Add
ALU
result
Zero
Instruction [5– 0]
MemtoReg
ALUOp
MemWrite
RegWrite
MemRead
Branch
Jump
RegDst
ALUSrc
Instruction [31– 26]
4
M
u
x
Instruction [25– 0] Jump address [31– 0]
PC+4 [31– 28]
Sign
extend
16 32Instruction [15– 0]
1
M
u
x
1
0
M
u
x
0
1
M
u
x
0
1
ALU
control
Control
Add ALU
result
M
u
x
0
1 0
ALU
Shift
left 226 28
Address
PCSrc2=Br Taken
PCSrc1=Jump
ALU operation
bcond
[Based on original figure from P&H CO&D, COPYRIGHT 
2004 Elsevier. ALL RIGHTS RESERVED.]
200ps 250ps
350ps600ps
100ps
100ps
550ps
SW
Shift
left 2
PC
Instruction
memory
Read
address
Instruction
[31– 0]
Data
memory
Read
data
Write
data
Registers
Write
register
Write
data
Read
data 1
Read
data 2
Read
register 1
Read
register 2
Instruction [15– 11]
Instruction [20– 16]
Instruction [25– 21]
Add
ALU
result
Zero
Instruction [5– 0]
MemtoReg
ALUOp
MemWrite
RegWrite
MemRead
Branch
Jump
RegDst
ALUSrc
Instruction [31– 26]
4
M
u
x
Instruction [25– 0] Jump address [31– 0]
PC+4 [31– 28]
Sign
extend
16 32Instruction [15– 0]
1
M
u
x
1
0
M
u
x
0
1
M
u
x
0
1
ALU
control
Control
Add ALU
result
M
u
x
0
1 0
ALU
Shift
left 226 28
Address
PCSrc2=Br Taken
PCSrc1=Jump
ALU operation
bcond
[Based on original figure from P&H CO&D, COPYRIGHT 
2004 Elsevier. ALL RIGHTS RESERVED.]
200ps 250ps
350ps
100ps
100ps
550ps
Branch Taken
Shift
left 2
PC
Instruction
memory
Read
address
Instruction
[31– 0]
Data
memory
Read
data
Write
data
Registers
Write
register
Write
data
Read
data 1
Read
data 2
Read
register 1
Read
register 2
Instruction [15– 11]
Instruction [20– 16]
Instruction [25– 21]
Add
ALU
result
Zero
Instruction [5– 0]
MemtoReg
ALUOp
MemWrite
RegWrite
MemRead
Branch
Jump
RegDst
ALUSrc
Instruction [31– 26]
4
M
u
x
Instruction [25– 0] Jump address [31– 0]
PC+4 [31– 28]
Sign
extend
16 32Instruction [15– 0]
1
M
u
x
1
0
M
u
x
0
1
M
u
x
0
1
ALU
control
Control
Add ALU
result
M
u
x
0
1 0
ALU
Shift
left 226 28
Address
PCSrc2=Br Taken
PCSrc1=Jump
ALU operation
bcond
[Based on original figure from P&H CO&D, COPYRIGHT 
2004 Elsevier. ALL RIGHTS RESERVED.]
200ps 250ps
350ps
100ps
350ps
200ps
Jump
Shift
left 2
PC
Instruction
memory
Read
address
Instruction
[31– 0]
Data
memory
Read
data
Write
data
Registers
Write
register
Write
data
Read
data 1
Read
data 2
Read
register 1
Read
register 2
Instruction [15– 11]
Instruction [20– 16]
Instruction [25– 21]
Add
ALU
result
Zero
Instruction [5– 0]
MemtoReg
ALUOp
MemWrite
RegWrite
MemRead
Branch
Jump
RegDst
ALUSrc
Instruction [31– 26]
4
M
u
x
Instruction [25– 0] Jump address [31– 0]
PC+4 [31– 28]
Sign
extend
16 32Instruction [15– 0]
1
M
u
x
1
0
M
u
x
0
1
M
u
x
0
1
ALU
control
Control
Add ALU
result
M
u
x
0
1 0
ALU
Shift
left 226 28
Address
PCSrc2=Br Taken
PCSrc1=Jump
ALU operation
bcond
[Based on original figure from P&H CO&D, COPYRIGHT 
2004 Elsevier. ALL RIGHTS RESERVED.]
200ps
100ps
200ps
steps IF ID EX MEM WB
Delay
resources mem RF ALU mem RF
R-type 200 50 100 50 400
I-type 200 50 100 50 400
LW 200 50 100 200 50 600
SW 200 50 100 200 550
Branch 200 50 100 350
Jump 200 200
Example Single-Cycle Datapath Analysis
 Assume (for the design in the previous slide)
 memory units (read or write): 200 ps
 ALU and adders: 100 ps
 register file (read or write): 50 ps
 other logic or wire delay: 0 ps
What About Control Logic?
 How does that affect the critical path?
 Food for thought for you:
 Can control logic be on the critical path?
 Historical example:
 CDC 5600: control store access took too long…
102
We Covered Until Here in Lecture
103
Digital Design & Computer Arch.
Lecture 10: Microarchitecture 
Fundamentals & Design
Dr. Mohammad Sadrosadati
Prof. Onur Mutlu
ETH Zürich
Spring 2026
20 March 2026
Further Slides for Your Own Study
(May Be Covered in Future Lectures)
105
What is Really the Slowest Instruction to Process?
 Real world: Memory is slow (not magic)
 What if memory sometimes takes 150ns to access?
 Does it make sense to have a simple register to register 
add or jump to take {150ns + all else to perform a memory 
operation}?
 And, what if you need to access memory more than once to 
process an instruction?
 Which instructions require this?
106
Single Cycle uArch: Complexity
 Contrived 
 All instructions run as slow as the slowest instruction
 Inefficient
 All instructions run as slow as the slowest instruction
 Must provide worst-case combinational resources in parallel as required by 
any instruction
 Need to replicate a resource if it is needed more than once by an 
instruction during different parts of the instruction processing cycle
 Not necessarily the simplest way to implement an ISA
 Tough for complex instructions, e.g., REP MOVS (x86) or INDEX (VAX)
 Not easy to optimize/improve performance
 Optimizing the common case (frequent instructions) does not work 
 Need to optimize the worst case all the time
107
(Micro)architecture Design Principles
 Critical path design
 Find and decrease the maximum combinational logic delay
 Break a path into multiple cycles if it takes too long
 Bread and butter (common case) design
 Spend time and resources on where it matters most
 i.e., improve what the machine is really designed to do
 Common case vs. uncommon case 
 Balanced design
 Balance instruction/data flow through hardware components
 Design to eliminate bottlenecks: balance the hardware for the 
work
108
Single-Cycle Design vs. Design Principles
 Critical path design
 Bread and butter (common case) design
 Balanced design
How does a single-cycle microarchitecture fare 
with respect to these principles?
109
Aside: System Design Principles
 When designing computer systems/architectures, it is 
important to follow good principles
 Actually, this is true for any system design
 Real architectures, buildings, bridges, train stations, …
 Good consumer products
 Security & safety-critical systems
 Decision making systems
 …
 Remember: “principled design” from our second lecture
 Frank Lloyd Wright: “architecture […] based upon principle, 
and not upon precedent”
110
Aside: Principled Architecture
 “architecture […] based upon principle, and not upon 
precedent”
111
This
112

That
113

Recall: Takeaways
 It all starts from the basic building blocks and design 
principles
 And, knowledge of how to use, apply, enhance them
 Underlying technology might change (e.g., steel vs. wood)
 but methods of taking advantage of technology bear resemblance
 methods used for design depend on the principles employed
114
Aside: System Design Principles
 We will continue to cover key principles in this course
 Here are some references where you can learn more
 Yale Patt, “Requirements, Bottlenecks, and Good Fortune: Agents for 
Microprocessor Evolution,” Proc. of IEEE, 2001. (Levels of 
transformation, design point, etc)
 Mike Flynn, “Very High-Speed Computing Systems,” Proc. of IEEE, 
1966. (Flynn’s Bottleneck  Balanced design)
 Gene M. Amdahl, "Validity of the single processor approach to achieving 
large scale computing capabilities," AFIPS Conference, April 1967. 
(Amdahl’s Law  Common-case design)
 Butler W. Lampson, “Hints for Computer System Design,” ACM 
Operating Systems Review, 1983.
115
A Key System Design Principle 
 Keep it simple
 “Everything should be made as simple as possible,           
but no simpler.”
 Albert Einstein (paraphrased) 
 And, keep it low cost: “An engineer is a person who can   
do for a dime what any fool can do for a dollar.”
 For more, see:
 Butler W. Lampson, “Hints for Computer System Design,” ACM 
Operating Systems Review, 1983, updated 2021.
 https://arxiv.org/pdf/2011.02455
116

Can We Do Better?
117
Multi-Cycle Microarchitectures
118
Multi-Cycle Microarchitectures
 Goal: Let each instruction take (close to) only as much time 
it really needs
 Idea
 Determine clock cycle time independently of instruction 
processing time
 Each instruction takes as many clock cycles as it needs to take
 Multiple state transitions per instruction
 The states followed by each instruction is different
119
Recall: The “Process Instruction” Step
 ISA specifies abstractly what AS’ should be, given an 
instruction and AS
 It defines an abstract finite state machine where
 State = programmer-visible state 
 Next-state logic = instruction execution specification
 From ISA point of view, there are no “intermediate states” 
between AS and AS’ during instruction execution
 One state transition per instruction
 Microarchitecture implements how AS is transformed to AS’
 There are many choices in implementation 
 We can have programmer-invisible state to optimize the speed of 
instruction execution: multiple state transitions per instruction
 Choice 1: AS  AS’ (transform AS to AS’ in a single clock cycle)
 Choice 2: AS  AS+MS1  AS+MS2  AS+MS3  AS’ (take multiple 
clock cycles to transform AS to AS’)
120
Multi-Cycle Microarchitecture
AS = Architectural (programmer visible) state 
at the beginning of an instruction
Step 1: Process part of instruction in one clock cycle
Step 2: Process part of instruction in the next clock cycle
…
AS’ = Architectural (programmer visible) state 
at the end of a clock cycle
121
Recall: Control of the Instruction Cycle
 State 1
 The FSM asserts GatePC and 
LD.MAR
 It selects input (+1) in PCMUX and 
asserts LD.PC
 State 2
 MDR is loaded with the instruction
 State 3
 The FSM asserts GateMDR and 
LD.IR
 State 4
 The FSM goes to next state 
depending on opcode
 State 63
 JMP loads register into PC
 Full state diagram in Patt&Pattel, 
Appendix C
122
This is an FSM Controlling a Multi-Cycle LC-3 Microarchitecture
Recall: Full State Machine for LC-3b
123
https://safari.ethz.ch/digitaltechnik/spring2022/lib/exe/fetch.php?media=pp-appendixc.pdf
Full FSM Controlling 
a Multi-Cycle LC-3b 
Microarchitecture
Execute 
Phase
Decode Phase
Fetch Phase
Recall: LC-3 Multi-Cycle Implementation
124
Scanned by CamScanner
Control signals
Data
ALU: 2 inputs, 1 output
Memory Data 
Register
Memory Address
Register 16-bit 
addressable
Keyboard
KBDR (data), KBSR (status)
Monitor
DDR (data), DSR (status)
8 General Purpose 
Registers (GPR)
Finite State Machine 
(for Generating Control Signals)
Instruction 
Register
Program 
Counter
ALU operation
GateALU
Clock
Control 
Unit 
FSM
Benefits of Multi-Cycle Design
 Critical path design
 Can keep reducing the critical path independently of the worst-
case processing time of any instruction
 Bread and butter (common case) design
 Can optimize the number of states it takes to execute “important” 
instructions that make up much of the execution time
 Balanced design
 No need to provide more capability or resources than really 
needed 
 An instruction that needs resource X multiple times does not require 
multiple X’s to be implemented
 Leads to more efficient hardware: Can reuse hardware components 
needed multiple times for an instruction
125
Downsides of Multi-Cycle Design
 Need to store the intermediate results at the end of each 
clock cycle
 Hardware overhead for microarchitectural registers
 Register setup/hold overhead (i.e., sequencing overhead) is 
paid multiple times for an instruction
 Limited concurrency
 Only a small part of the machine is used at any point in time 
126
Multi-Cycle LC-3 Data Path
127
Processing 
Unit
Extra registers 
not needed in a 
single-cycle 
design
Remember: Performance Analysis
 Execution time of a single instruction
 {CPI}  x  {clock cycle time} 
 Execution time of an entire program
 Sum over all instructions [{CPI}  x  {clock cycle time}]
 {# of instructions}  x  {Average CPI}  x  {clock cycle time}
 Single-cycle microarchitecture performance 
 CPI = 1
 Clock cycle time = long
 Multi-cycle microarchitecture performance
 CPI = different for each instruction
 Average CPI  hopefully small
 Clock cycle time = short
128
In multi-cycle, we have 
two degrees of freedom
to optimize independently
CPI: Cycles Per Instruction