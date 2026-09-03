---
archive_policy: text-only
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-a821569e45dc
  position:
    end: 15832
    start: 15780
    type: TextPositionSelector
  quote_sha256: sha256:8a2ba8ca36b9e7865e59b3870a3fb107a07918e77de5503123e285b6b7c93923
  selector:
    exact: 'Microarchitecture: How the underlying implementation'
    prefix: 'es a dataflow execution order

      ◼ '
    suffix: " \nactually executes instructions"
    type: TextQuoteSelector
  selector_sha256: sha256:d2f6a304b3ae3e4a201c70048a13823d8801bab92b9b34a4b5290bec4a95da43
  snapshot_sha256: sha256:b7a50ab4c8641f3ddac6de555d42e559d9af0a09decb3455af36832519cca8d4
- evidence_id: evidence-b1430ecb4f5d
  position:
    end: 18560
    start: 18511
    type: TextPositionSelector
  quote_sha256: sha256:bc4fb1dc52086e41158872287d649173a4f5424d9427120a4151c211203159e5
  selector:
    exact: There can be many implementations of the same ISA
    prefix: "scuss this for many lectures \n◼ "
    suffix: '

      ❑ MIPS R2000, R3000, R4000, R60'
    type: TextQuoteSelector
  selector_sha256: sha256:6e12a03981137f4b28597acc8e6e3b6cdcf407296299591eb6c87ca65ede3bee
  snapshot_sha256: sha256:b7a50ab4c8641f3ddac6de555d42e559d9af0a09decb3455af36832519cca8d4
- evidence_id: evidence-934896f7d3b4
  position:
    end: 15864
    start: 15780
    type: TextPositionSelector
  quote_sha256: sha256:c6550235af532144c778c85098662d3d80d6b0066af8426a802749d96c6de87f
  selector:
    exact: "Microarchitecture: How the underlying implementation \nactually executes
      instructions"
    prefix: 'es a dataflow execution order

      ◼ '
    suffix: " \n❑ Microarchitecture can execut"
    type: TextQuoteSelector
  selector_sha256: sha256:512c15ab189cc945599645c5dc0e91ff9750519e0f96904a3398e9b8764d1bff
  snapshot_sha256: sha256:b7a50ab4c8641f3ddac6de555d42e559d9af0a09decb3455af36832519cca8d4
- evidence_id: evidence-0fcb148be49a
  position:
    end: 16036
    start: 15868
    type: TextPositionSelector
  quote_sha256: sha256:93fa0258ace39551fbb2a45a6ca95d41a859eb64f0392279ece394be651fd882
  selector:
    exact: "Microarchitecture can execute instructions in any order as long \nas it
      obeys the semantics specified by the ISA when making the \ninstruction results
      visible to software"
    prefix: "tually executes instructions \n❑ "
    suffix: '

      ◼ Programmer should see the ord'
    type: TextQuoteSelector
  selector_sha256: sha256:ffe5f5db653e8a68767955f3674cddc5e6d2f34de870ad2fd54f320a790c5708
  snapshot_sha256: sha256:b7a50ab4c8641f3ddac6de555d42e559d9af0a09decb3455af36832519cca8d4
extractor: pypdf/6.16.2
id: ddca-lecture9a-isa-microarchitecture
media_type: application/pdf
origin: external
read_status: retrieved
retrieval:
  acquisition: fetch
  resolved_url: https://safari.ethz.ch/ddca/spring2026/lib/exe/fetch.php?media=onur-ddca-2026-lecture9a-isa-microarchitecture-afterlecture.pdf
  url: https://safari.ethz.ch/ddca/spring2026/lib/exe/fetch.php?media=onur-ddca-2026-lecture9a-isa-microarchitecture-afterlecture.pdf
schema_version: source/v1
snapshot_sha256: sha256:b7a50ab4c8641f3ddac6de555d42e559d9af0a09decb3455af36832519cca8d4
source_type: doc
vault_id: public
---
Digital Design & Computer Arch.
Lecture 9a: ISA & Microarchitecture
Prof. Onur Mutlu
ETH Zürich
Spring 2026
19 March 2026
Extra Credit Assignment: Talk Analysis
◼ The Story of RowHammer, RowPress & Beyond
◼ Watch and analyze this short lecture (30 minutes)
❑ https://www.youtube.com/watch?v=U1EcqXlclKU (June 2024)
◼ Assignment – for 1% extra credit
❑ Write a good 1-page individualized summary (no AI use) 
◼ What are your key takeaways? What did you learn?
◼ What surprised you about the content presented? What excited you?
◼ What do you think solutions should be like? 
◼ Submit your summary to Moodle – deadline March 21
2

Agenda for Today & Next Few Lectures
◼ The von Neumann model
◼ LC-3: An example of von Neumann machine
◼ LC-3 and MIPS Instruction Set Architectures
◼ LC-3 and MIPS assembly and programming
◼ Introduction to microarchitecture and                         
single-cycle microarchitecture
◼ Multi-cycle microarchitecture
3
Micro-architecture
SW/HW Interface
Program/Language
Algorithm
Problem
Logic
Devices
System Software
Electrons
What Have We Been Learning?
◼ Basic elements of a computer & the von Neumann model
❑ LC-3: An example von Neumann machine
◼ Instruction Set Architectures: LC-3 and MIPS
❑ Operate instructions
❑ Data movement instructions
❑ Control instructions
◼ Instruction formats
◼ Addressing modes
4
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
◼ Last week
❑ Von Neumann Model, ISA, LC-3, and MIPS
◼ P&P, Chapters 4, 5 (we will follow these today & tomorrow)
◼ H&H, Chapter 6 (until 6.5)
◼ P&P, Appendices A and C (ISA and microarchitecture of LC -3)
◼ H&H, Appendix B (MIPS instructions)
❑ Programming
◼ P&P, Chapter 6 (we will follow this tomorrow)
❑ Recommended: H&H Chapter 5, especially 5.1, 5.2, 5.4, 5.5
◼ This week
❑ Introduction to microarchitecture and single-cycle microarchitecture
◼ H&H, Chapter 7.1-7.3
◼ P&P, Appendices A and C
❑ Multi-cycle microarchitecture
◼ H&H, Chapter 7.4
◼ P&P, Appendices A and C 
5
Instruction (Processing) Cycle
6
Recall: The Instruction (Processing) Cycle
❑ FETCH
❑ DECODE
❑ EVALUATE ADDRESS
❑ FETCH OPERANDS
❑ EXECUTE
❑ STORE RESULT
7
Recall: Control of the Instruction Cycle
◼ State 1
❑ The FSM asserts GatePC and 
LD.MAR
❑ It selects input (+1) in PCMUX and 
asserts LD.PC
◼ State 2
❑ MDR is loaded with the instruction
◼ State 3
❑ The FSM asserts GateMDR and 
LD.IR
◼ State 4
❑ The FSM goes to next state 
depending on opcode
◼ State 63
❑ JMP loads register into PC
◼ Full state diagram in Patt&Pattel, 
Appendix C
8
This is an FSM Controlling the LC-3 Processor
Recall: Full State Machine for LC-3b
9https://safari.ethz.ch/digitaltechnik/spring2022/lib/exe/fetch.php?media=pp-appendixc.pdf 
Decode Phase
Fetch Phase
Execute 
Phase
Recall: LC-3: A von Neumann Machine
10
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
LC-3 and MIPS 
Instruction Set Architectures
11
Instructions (Opcodes)
12
Data Types
13
Addressing Modes
14
Operate Instructions
15
Data Movement Instructions 
and Addressing Modes
16
Control Flow Instructions
17
Conditional Control Flow
(Conditional Branching)
18
There Is A Lot More to Cover on ISAs 
19https://www.youtube.com/onurmutlulectures 
Bigger Picture: 
Program Execution
20
Carnegie Mellon
21
How Do We Compile & Run an Application?
Assembly Code
High Level Code
Compiler
Object File
Assembler
Executable
Linker
Memory
Loader
Object Files
Library Files
H&H Chapter 6.6
Carnegie Mellon
22
What is Stored in Memory?
 Instructions (also called text)
 Data
▪ Global/static: allocated before program begins
▪ Dynamic: allocated within program
 How big is memory (in MIPS ISA)?
▪ At most 232 = 4 gigabytes (4 GB)
▪ From address 0x00000000 to 0xFFFFFFFF
H&H Chapter 6.6
Carnegie Mellon
23
The MIPS Memory Map
SegmentAddress
0xFFFFFFFC
0x80000000
0x7FFFFFFC
0x10010000
0x1000FFFC
0x10000000
0x0FFFFFFC
0x00400000
0x003FFFFC
0x00000000
Reserved
Stack
Heap
Static Data
Text
Reserved
Dynamic Data
H&H Chapter 6.6
Carnegie Mellon
24
Example Program: C Code
int f, g, y;  // global variables
int main(void) 
{
  f = 2;
  g = 3;
  y = sum(f, g);
  return y;
}
int sum(int a, int b) {
  return (a + b);
}
Carnegie Mellon
25
Example Program: Assembly Code
int f, g, y;  // global
int main(void) 
{
  f = 2;
  g = 3;
  y = sum(f, g);
  return y;
}
int sum(int a, int b) {
  return (a + b);
}
.data
f:
g:
y:
.text
main: addi $sp, $sp, -4 # stack
      sw   $ra, 0($sp)  # store $ra
      addi $a0, $0, 2   # $a0 = 2
      sw   $a0, f       # f = 2
      addi $a1, $0, 3   # $a1 = 3
      sw   $a1, g       # g = 3
      jal  sum          # call sum
      sw   $v0, y       # y = sum()
      lw   $ra, 0($sp)  # rest. $ra
      addi $sp, $sp, 4  # rest. $sp
      jr   $ra          # return
sum:  add  $v0, $a0, $a1 # $v0= a+b
      jr   $ra          # return
Carnegie Mellon
26
Example Program: Symbol Table
Symbol Address
f 0x10000000
g 0x10000004
y 0x10000008
main 0x00400000
sum 0x0040002C
Carnegie Mellon
27
Example Program: Executable
Executable file header Text Size Data Size
Text segment
Data segment
Address Instruction
Address Data
0x00400000
0x00400004
0x00400008
0x0040000C
0x00400010
0x00400014
0x00400018
0x0040001C
0x00400020
0x00400024
0x00400028
0x0040002C
0x00400030
addi $sp, $sp, -4
sw    $ra, 0 ($sp)
addi $a0, $0, 2
sw    $a0, 0x8000 ($gp)
addi $a1, $0, 3
sw    $a1, 0x8004 ($gp)
jal     0x0040002C
sw    $v0, 0x8008 ($gp)
lw     $ra, 0 ($sp)
addi $sp, $sp, -4
jr      $ra
add  $v0, $a0, $a1
jr      $ra
0x10000000
0x10000004
0x10000008
f
g
y
0xC (12 bytes)0x34 (52 bytes)
0x23BDFFFC
0xAFBF0000
0x20040002
0xAF848000
0x20050003
0xAF858004
0x0C10000B
0xAF828008
0x8FBF0000
0x23BD0004
0x03E00008
0x00851020
0x03E0008
H&H Chapter 6.6
Carnegie Mellon
28
Example Program: In Memory
y
g
f
0x03E00008
0x00851020
0x03E00008
0x23BD0004
0x8FBF0000
0xAF828008
0x0C10000B
0xAF858004
0x20050003
0xAF848000
0x20040002
0xAFBF0000
0x23BDFFFC
MemoryAddress
$sp = 0x7FFFFFFC0x7FFFFFFC
0x10010000
0x00400000
Stack
Heap
$gp = 0x10008000
PC = 0x00400000
0x10000000
Reserved
Reserved
H&H Chapter 6.6
Extra Lecture on Assembly Programming
29https://www.youtube.com/watch?v=Tqc3XRJB9js  

Extra Lecture on Assembly Programming
30
https://www.youtube.com/watch?v=Tqc3XRJB9js  
Some More on ISA Tradeoffs
31
Complex vs. Simple Instructions+Data Types
◼ Complex instruction: An instruction does a lot of work, e.g. 
many operations
❑ Insert in a doubly linked list
❑ Compute FFT
❑ String copy
❑ Matrix multiply
❑ … 
◼ Simple instruction: An instruction does little work -- it is a 
primitive using which complex operations can be built
❑ Add
❑ XOR
❑ Multiply
❑ …
32
Harder mapping of HLL to ISA
More work for software designer
Less work for hardware designer
Optimization burden on SW
Recall: Semantic Gap
◼ How close instructions & data types & addressing modes 
are to high-level language (HLL)
HLL
HW
Control 
Signals
HLL
HW
Control 
Signals
ISA with
Complex Inst
& Data Types
& Addressing Modes ISA with
Simple Inst
& Data Types
& Addressing Modes
Small Semantic Gap
Large Semantic Gap
Easier mapping of HLL to ISA
Less work for software designer
More work for hardware designer
Optimization burden on HW
How to Change the Semantic Gap Tradeoffs
◼ Translate from one ISA into a different “implementation” ISA
34
HLL
HW
Control 
Signals
Small Semantic Gap
Implementation ISA with
Simple Inst
& Data Types
& Addressing Modes
Software or Hardware Translator
ISA with
Complex Inst
& Data Types
& Addressing Modes
X86-64
ARM v8.4
An Example: Rosetta 2 Binary Translator
35
https://en.wikipedia.org/wiki/Rosetta_(software)#Rosetta_2 
An Example: Rosetta 2 Binary Translator
36
Source: https://www.anandtech.com/show/16252/mac-mini-apple-m1-tested 
Apple M1,
2021
Another Example: Intel and AMD Processors
37
HLL
HW
Control 
Signals
Small Semantic Gap
Implementation ISA with
Simple Inst
& Data Types
& Addressing Modes
Hardware Translator
ISA with
Complex Inst
& Data Types
& Addressing Modes
X86-64
Secret
Micro-operations
Another Example: Intel and AMD Processors
38Source: https://twitter.com/Locuza_/status/1454152714930331652 
Intel Alder Lake,
2021

Another Example: Intel and AMD Processors
39
https://wccftech.com/amd -ryzen-5000-zen-3-vermeer-undressed-high-res-die-shots-close-ups-pictured-detailed/
AMD Ryzen 5000, 2020
Core Count:
8 cores/16 threads
L1 Caches: 
32 KB per core
L2 Caches:
512 KB per core
L3 Cache:
32 MB shared
Another Example: NVIDIA Denver
40
HLL
HW
Control 
Signals
Small Semantic Gap
Implementation ISA with
Simple Inst
& Data Types
& Addressing Modes
Software Translator
ISA with
Complex Inst
& Data Types
& Addressing Modes
ARM ISA
Secret
Micro-operations
Another Example: NVIDIA Denver
41
https://www.anandtech.com /show/8701/the -google-nexus-9-review/4
https://www.toradex.com/computer-on-modules/apalis-arm-family/nvidia-tegra-k1
Transmeta: x86 to VLIW Translation
42
Klaiber, “The Technology Behind Crusoe Processors,” Transmeta White Paper 2000.
X86
Proprietary VLIW ISA
X86
https://www.wikiwand.com/en/Transmeta_Efficeon
Principle: Indirection
◼ “Any problem in computer science can be solved
with another level of indirection.”
❑ David Wheeler 
❑ Attributed in Butler Lampson’s “Principles for Computer 
Systems Design” https://arxiv.org/pdf/2011.02455 
◼ Tradeoffs can change and new opportunities become 
enabled once you add a level of indirection
◼ But indirection comes with extra complexity and latency
◼ We will see this again when we discuss Virtual Memory
43
ISA-level Tradeoffs: Number of Registers
◼ Affects:
❑ Number of bits used for encoding register address
❑ Number of values kept in fast storage (register file)
❑ (uarch) Size, access time, power consumption of register file
◼ Large number of registers:
+ Enables better register allocation (and optimizations) by 
compiler → fewer saves/restores
-- Larger instruction size
-- Larger register file size
◼ We already saw this tradeoff: LC-3 vs MIPS
44
There Is A Lot More to Cover on ISAs 
45https://www.youtube.com/onurmutlulectures 
There Is A Lot More to Cover on ISAs
46https://www.youtube.com/onurmutlulectures 

Detailed Lectures on ISAs & ISA Tradeoffs
◼ Computer Architecture, Spring 2015, Lecture 3
❑ ISA Tradeoffs (CMU, Spring 2015)
❑ https://www.youtube.com/watch?v=QKdiZSfwg-
g&list=PL5PHm2jkkXmi5CxxI7b3JCL1TWybTDtKq&index=3
◼ Computer Architecture, Spring 2015, Lecture 4
❑ ISA Tradeoffs & MIPS ISA (CMU, Spring 2015)
❑ https://www.youtube.com/watch?v=RBgeCCW5Hjs&list=PL5PHm2jkkXmi5CxxI7b3J
CL1TWybTDtKq&index=4
◼ Computer Architecture, Spring 2015, Lecture 2
❑ Fundamental Concepts and ISA (CMU, Spring 2015)
❑ https://www.youtube.com/watch?v=NpC39uS4K4o&list=PL5PHm2jkkXmi5CxxI7b3J
CL1TWybTDtKq&index=2 
47https://www.youtube.com/onurmutlulectures 
ISA Design and Tradeoffs:
More Critical Thinking
The Von Neumann Model/Architecture
Stored program
Sequential instruction processing
49
The von Neumann Model/Architecture
◼ Von Neumann model is also called stored program computer 
(instructions in memory). It has two key properties:
◼ Stored program
❑ Instructions stored in a linear memory array
❑ Memory is unified between instructions and data
◼ The interpretation of a stored value depends on the control signals
◼ Sequential instruction processing
50
When is a value interpreted as an instruction?
Recall: The Instruction Cycle
❑ FETCH
❑ DECODE
❑ EVALUATE ADDRESS
❑ FETCH OPERANDS
❑ EXECUTE
❑ STORE RESULT
51
Whether a value fetched from memory is interpreted as an instruction depends on 
when that value is fetched in the instruction processing cycle.
Interpret memory value as Instruction
Interpret memory value as Data
The von Neumann Model/Architecture
◼ Von Neumann model is also called stored program computer 
(instructions in memory). It has two key properties:
◼ Stored program
❑ Instructions stored in a linear memory array
❑ Memory is unified between instructions and data
◼ The interpretation of a stored value depends on the control signals
◼ Sequential instruction processing
❑ One instruction processed (fetched, executed, completed) at a time
❑ Program counter (instruction pointer) identifies the current instruction
❑ Program counter is advanced sequentially except for control transfer 
instructions
52
When is a value interpreted as an instruction?
The von Neumann Model/Architecture
◼ Recommended reading
❑ Burks, Goldstein, von Neumann, “Preliminary discussion of the 
logical design of an electronic computing instrument,” 1946.
◼ Important reading
❑ Patt and Patel book, Chapter 4, “The von Neumann Model”
◼ Stored program
◼ Sequential instruction processing
53
The Von Neumann Model (of a Computer)
54
CONTROL UNIT
PC or IP Inst Register
PROCESSING UNIT
ALU TEMP
MEMORY
Mem Addr Reg
Mem Data Reg
INPUT
Keyboard,
Mouse,
Disk…
OUTPUT
Monitor, 
Printer, 
Disk…
◼ Q: Is this the only way that a computer can process 
computer programs?
◼ A: No.
◼ Qualified Answer: No. But, it has been the dominant way 
❑ i.e., the dominant paradigm for computing
❑ for N decades
The Von Neumann Model (of a Computer)
55Let’s examine a completely different model for processing computer programs
The Dataflow Execution Model
of a Computer
The Dataflow Model (of a Computer)
◼ Von Neumann model: An instruction is fetched and 
executed in control flow order 
❑ As specified by the program counter (instruction pointer)
❑ Sequential unless explicit control flow instruction
◼ Dataflow model: An instruction is fetched and executed in 
data flow order
❑ i.e., when its operands are ready
❑ i.e., there is no program counter (instruction pointer)
❑ Instruction ordering specified by data flow dependence
◼ Each instruction specifies “who” should receive the result
◼ An instruction can “fire” whenever all operands are received
❑ Potentially many instructions can execute at the same time
◼ Inherently more parallel
57
Von Neumann vs. Dataflow
◼ Consider a Von Neumann program 
❑ What is the significance of the program order?
❑ What is the significance of the storage locations?
58
v = a + b;   
w = b * 2;
x = v - w
y = v + w
z = x * y
+ *2
- +
*
a b
z
Sequential
Dataflow
Which model is more natural to you as a programmer?
a, b are the only inputs
z is the only output
More on Dataflow
◼ In a dataflow machine, a program consists of dataflow 
nodes
❑ A dataflow node fires (fetched and executed) when all it 
inputs are ready
◼ i.e. when all inputs have tokens
◼ Dataflow node and its ISA representation
59

Example Dataflow Nodes
60

A Simple Example Dataflow Program
61
OUT
N is a 
non-negative
integer
N1
What is the
value of OUT?
Decrement
Multiply
ISA-level Tradeoff: Program Counter
◼ Do we want a Program Counter (PC or IP) in the ISA?
❑ Yes: Control-driven, sequential execution
◼ An instruction is executed when the PC points to it
◼ PC automatically changes sequentially (except for control flow 
instructions) → sequential
❑ No: Data-driven, parallel execution
◼ An instruction is executed when all its operand values are 
available → dataflow
◼ Tradeoffs: MANY high-level ones
❑ Ease of programming (for average programmers)?
❑ Ease of compilation?
❑ Performance: Extraction of parallelism?
❑ Hardware complexity?
62
ISA vs. Microarchitecture Level Tradeoff
◼ A similar tradeoff (control vs. data-driven execution) can be 
made at the microarchitecture level
◼ ISA: Specifies how the programmer sees the instructions to 
be executed
❑ Programmer sees a sequential, control-flow execution order vs.
❑ Programmer sees a dataflow execution order
◼ Microarchitecture: How the underlying implementation 
actually executes instructions 
❑ Microarchitecture can execute instructions in any order as long 
as it obeys the semantics specified by the ISA when making the 
instruction results visible to software
◼ Programmer should see the order specified by the ISA
63
Let’s Get Back to the von Neumann Model
◼ But, if you want to learn more about dataflow…
◼ Dennis and Misunas, “A preliminary architecture for a basic 
data-flow processor,” ISCA 1974.
◼ Gurd et al., “The Manchester prototype dataflow 
computer,” CACM 1985.
◼ Some Lecture Videos:
❑ http://www.youtube.com/watch?v=D2uue7izU2c
❑ http://www.ece.cmu.edu/~ece740/f13/lib/exe/fetch.php?medi
a=onur-740-fall13-module5.2.1-dataflow-part1.ppt 
64
Lecture Video on Dataflow Architectures
65
http://www.youtube.com/watch?v=D2uue7izU2c
The von Neumann Model
◼ All major instruction set architectures today use this model
❑ x86, ARM, MIPS, SPARC, Alpha, POWER, RISC-V, …
◼ Underneath (at the microarchitecture level), the execution 
model of almost all implementations (or, microarchitectures) 
is very different
❑ Pipelined instruction execution: Intel 80486 uarch
❑ Multiple instructions at a time: Intel Pentium uarch
❑ Out-of-order execution: Intel Pentium Pro uarch
❑ Separate instruction and data caches
◼ But, what happens underneath that is not consistent with 
the von Neumann model is not exposed to software
❑ Difference between ISA and microarchitecture
66
What is Computer Architecture?
◼ ISA+implementation definition: The science and art of 
designing, selecting, and interconnecting hardware 
components and designing the hardware/software interface 
to create a computing system that meets functional, 
performance, energy consumption, cost, and other specific 
goals. 
◼ Traditional (ISA-only) definition: “The term 
architecture is used here to describe the attributes of a 
system as seen by the programmer, i.e., the conceptual 
structure and functional behavior as distinct from the 
organization of the dataflow and controls, the logic design, 
and the physical implementation. ” 
 Gene Amdahl, IBM Journal of R&D, April 1964
67
ISA vs. Microarchitecture
◼ ISA
❑ Agreed upon interface between software 
and hardware
◼ SW/compiler assumes, HW promises
❑ What the software writer needs to know 
to write and debug system/user programs 
◼ Microarchitecture
❑ Specific implementation of an ISA
❑ Not visible to the software
◼ Microprocessor
❑ ISA, uarch, circuits
❑ “Architecture” = ISA + microarchitecture
68
Microarchitecture
ISA
Program
Algorithm
Problem
Circuits
Electrons
Microarchitecture
◼ A specific implementation of the ISA
◼ How do we implement the ISA?
❑ We will discuss this for many lectures 
◼ There can be many implementations of the same ISA
❑ MIPS R2000, R3000, R4000, R6000, R8000, R10000, …
❑ x86: Intel 80486, Pentium, Pentium Pro, Pentium 4, Kaby Lake, 
Coffee Lake, Comet Lake, Ice Lake, Golden Cove, Sapphire Rapids, 
…, AMD K5, K7, K9, Bulldozer, BobCat, Ryzen X, …
❑ POWER 4, 5, 6, 7, 8, 9, 10 (IBM), …, PowerPC 604, 605, 620, …
❑ ARM Cortex-M*,  ARM Cortex-A*, NVIDIA Denver, Apple A*, M1, …
❑ Alpha 21064, 21164, 21264, 21364, …
❑ RISC-V …
❑ z/Architecture …
❑ … 
69
ISA vs. Microarchitecture
◼ What is part of ISA vs. Uarch?
❑ Gas pedal: interface for “acceleration”
❑ Internals of the engine: implement “acceleration”
◼ Implementation (uarch) can be various as long as it 
satisfies the specification (ISA)
❑ Add instruction vs. Adder implementation
◼ Bit serial, ripple carry, carry lookahead adders are all part of 
microarchitecture (see H&H Chapter 5.2.1)
❑ x86 ISA has many implementations: 
◼ Intel 80486, Pentium, Pentium Pro, Pentium 4, Kaby Lake, Coffee Lake, Comet Lake, Ice 
Lake, Golden Cover, Sapphire Rapids, …, AMD K5, K7, K9, Bulldozer, BobCat, Ryzen X, …
◼ Microarchitecture usually changes faster than ISA
❑ Few ISAs (x86, ARM, SPARC, MIPS, Alpha, RISC-V) but many uarchs
❑ Why?
70
https://www.vox.com/2015/7/1/8877583/two-foot-driving-pedal-error
ISA: What Does It Specify?
◼ Instructions
❑ Opcodes, Addressing Modes, Data Types
❑ Instruction Types and Formats
❑ Registers, Condition Codes
◼ Memory
❑ Address space, Addressability, Alignment
❑ Virtual memory management
◼ Call, Interrupt/Exception Handling
◼ Access Control, Priority/Privilege 
◼ I/O: memory-mapped vs. instructions
◼ Task/thread Management
◼ Power & Thermal Management
◼ Multithreading & Multiprocessor support
◼ …
71

ISAs Keep Getting Extended
72https://www.intel.com/content/www/us/en/developer/articles/technical/intel -sdm.html 
ISAs Keep Getting Extended
73
https://developer.arm.com/documentation/ddi0602/latest/ 
ISA Manuals: Some Good Bedtime Reading
74
https://www.intel.com/content/www/us/en/developer/articles/technical/intel -sdm.html 
ISA Manuals: Some Good Bedtime Reading
75https://riscv.org/technical/specifications/  

Microarchitecture
◼ Implementation of the ISA under specific design constraints 
and goals
◼ Anything done in hardware without exposure to software
❑ Pipelining
❑ In-order versus out-of-order instruction execution
❑ Memory access scheduling policy
❑ Speculative execution
❑ Superscalar processing (multiple instruction issue?)
❑ Clock gating
❑ Caching? Levels, size, associativity, replacement policy
❑ Prefetching?
❑ Voltage/frequency scaling?
❑ Error correction?
76
Property of ISA vs. Uarch?
◼ ADD instruction’s opcode
◼ Type of adder used in the ALU (Bit-serial vs. Ripple-carry)
◼ Number of general purpose registers
◼ Number of cycles to execute the MUL instruction
◼ Number of ports to the register file
◼ Whether or not the machine employs pipelined instruction 
execution
◼ Program counter
◼ Remember
❑ Microarchitecture: Implementation of the ISA under specific 
design constraints and goals
77
Design Point
◼ A set of design considerations and their importance 
❑ leads to tradeoffs in both ISA and uarch
◼ Example considerations:
❑ Cost
❑ Performance
❑ Maximum power consumption, thermal
❑ Energy consumption (battery life)
❑ Availability
❑ Reliability and Correctness 
❑ Time to Market
❑ Security, safety, predictability, …
◼ Design point is determined by the “Problem” space 
(application space), the intended users/ market
78
Microarchitecture
ISA
Program
Algorithm
Problem
Circuits
Electrons
Application Space
Dream, and they will appear…
79
Patt, “Requirements, bottlenecks, 
and good fortune: agents for 
microprocessor evolution,” 
Proc. of the IEEE 2001.
Many other workloads:
Genome analysis
Machine learning
Robotics
Web search
Graph analytics
…
Increasingly Demanding Applications
Dream
and, they will come
80
As applications push boundaries, computing platforms will become increasingly strained.
Tradeoffs: Soul of Computer Architecture
◼ ISA-level tradeoffs
◼ Microarchitecture-level tradeoffs
◼ System and Task-level tradeoffs
❑ How to divide the labor between hardware and software
◼ Computer architecture is the science and art of making the 
appropriate trade-offs to meet a design point
❑ Why art?
81
Why Is It (Somewhat) Art?
82
Microarchitecture
ISA
Program/Language
Algorithm
Problem
Runtime System
(VM, OS, MM)
User
◼ We do not (fully) know the future (applications, users, market)
Logic
Circuits
Electrons
New demands 
from the top
(Look Up)
New issues and
capabilities
at the bottom
(Look Down)
New demands and
personalities of users
(Look Up)
Why Is It (Somewhat) Art?
83
Microarchitecture
ISA
Program/Language
Algorithm
Problem
Runtime System
(VM, OS, MM)
User
◼ And, the future is not constant (it changes)!
Logic
Circuits
Electrons
Changing demands 
at the top
(Look Up and Forward)
Changing issues and
capabilities
at the bottom
(Look Down and Forward)
Changing demands and
personalities of users
(Look Up and Forward)
Analogue from Macro-Architecture
◼ Future is not constant in macro-architecture, either
◼ Example: Can a mill be later used as a theater + restaurant 
+ conference room?
84
Mühle Tiefenbrunnen in Zurich
85
◼ Originally built as a brewery in 1889
❑ part of it was converted into a mill in 1913
❑ and the other part into a cold store
◼ Today is a center for a variety of activities: theater, 
conferences, restaurants, shops, museum …
Brewery in 1900
http://www.muehle-tiefenbrunnen.ch/
Another Example in Zurich (I)
86
Photo credit: Prof. Can Alkan
Another Example in Zurich (II)
87Photo credit: Prof. Can Alkan
88
By Roland zh (Own work) [CC BY-SA 3.0 
(https://creativecommons.org/licenses/by-sa/3.0)],
 via Wikimedia Commons
Yet Another Example from Pittsburgh (I)
89
https://www.pghcitypaper.com/pittsburgh/a-list-of-pittsburgh-area-churches-born-again-with-new-purposes/Content?oid=20743835
Yet Another Example from Pittsburgh (II)
90
https://en.wikipedia.org/wiki/The_Church_Brew_Works #/media/File:The_Church_Brew_Works.jpg
Extra Lecture on Assembly Programming
91https://www.youtube.com/watch?v=Tqc3XRJB9js  

Extra Lecture on Assembly Programming
92
https://www.youtube.com/watch?v=Tqc3XRJB9js  
Digital Design & Computer Arch.
Lecture 9a: ISA & Microarchitecture
Prof. Onur Mutlu
ETH Zürich
Spring 2026
19 March 2026
Additional Slides
94
Carnegie Mellon
95
How Do We Compile & Run an Application?
Assembly Code
High Level Code
Compiler
Object File
Assembler
Executable
Linker
Memory
Loader
Object Files
Library Files
H&H Chapter 6.6
Carnegie Mellon
96
What needs to be stored in memory?
 Instructions (also called text)
 Data
▪ Global/static: allocated before program begins
▪ Dynamic: allocated within program
 How big is memory?
▪ At most 232 = 4 gigabytes (4 GB)
▪ From address 0x00000000 to 0xFFFFFFFF
H&H Chapter 6.6
Carnegie Mellon
97
The MIPS Memory Map
SegmentAddress
0xFFFFFFFC
0x80000000
0x7FFFFFFC
0x10010000
0x1000FFFC
0x10000000
0x0FFFFFFC
0x00400000
0x003FFFFC
0x00000000
Reserved
Stack
Heap
Static Data
Text
Reserved
Dynamic Data
H&H Chapter 6.6
Carnegie Mellon
98
Example Program: C Code
int f, g, y;  // global variables
int main(void) 
{
  f = 2;
  g = 3;
  y = sum(f, g);
  return y;
}
int sum(int a, int b) {
  return (a + b);
}
Carnegie Mellon
99
Example Program: Assembly Code
int f, g, y;  // global
int main(void) 
{
  f = 2;
  g = 3;
  y = sum(f, g);
  return y;
}
int sum(int a, int b) {
  return (a + b);
}
.data
f:
g:
y:
.text
main: addi $sp, $sp, -4 # stack
      sw   $ra, 0($sp)  # store $ra
      addi $a0, $0, 2   # $a0 = 2
      sw   $a0, f       # f = 2
      addi $a1, $0, 3   # $a1 = 3
      sw   $a1, g       # g = 3
      jal  sum          # call sum
      sw   $v0, y       # y = sum()
      lw   $ra, 0($sp)  # rest. $ra
      addi $sp, $sp, 4  # rest. $sp
      jr   $ra          # return
sum:  add  $v0, $a0, $a1 # $v0= a+b
      jr   $ra          # return
Carnegie Mellon
100
Example Program: Symbol Table
Symbol Address
f 0x10000000
g 0x10000004
y 0x10000008
main 0x00400000
sum 0x0040002C
Carnegie Mellon
101
Example Program: Executable
Executable file header Text Size Data Size
Text segment
Data segment
Address Instruction
Address Data
0x00400000
0x00400004
0x00400008
0x0040000C
0x00400010
0x00400014
0x00400018
0x0040001C
0x00400020
0x00400024
0x00400028
0x0040002C
0x00400030
addi $sp, $sp, -4
sw    $ra, 0 ($sp)
addi $a0, $0, 2
sw    $a0, 0x8000 ($gp)
addi $a1, $0, 3
sw    $a1, 0x8004 ($gp)
jal     0x0040002C
sw    $v0, 0x8008 ($gp)
lw     $ra, 0 ($sp)
addi $sp, $sp, -4
jr      $ra
add  $v0, $a0, $a1
jr      $ra
0x10000000
0x10000004
0x10000008
f
g
y
0xC (12 bytes)0x34 (52 bytes)
0x23BDFFFC
0xAFBF0000
0x20040002
0xAF848000
0x20050003
0xAF858004
0x0C10000B
0xAF828008
0x8FBF0000
0x23BD0004
0x03E00008
0x00851020
0x03E0008
H&H Chapter 6.6
Carnegie Mellon
102
Example Program: In Memory
y
g
f
0x03E00008
0x00851020
0x03E00008
0x23BD0004
0x8FBF0000
0xAF828008
0x0C10000B
0xAF858004
0x20050003
0xAF848000
0x20040002
0xAFBF0000
0x23BDFFFC
MemoryAddress
$sp = 0x7FFFFFFC0x7FFFFFFC
0x10010000
0x00400000
Stack
Heap
$gp = 0x10008000
PC = 0x00400000
0x10000000
Reserved
Reserved
H&H Chapter 6.6