---
archive_policy: text-only
attachments:
- filename: ddca-lecture8-isa-ii.pdf
  kind: document
  media_type: application/pdf
  role: original
  sha256: sha256:e9e3e5194e646960b8725a21069c8a968007075e22a0bda16b98f964b8b0be3c
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-1a37cd32c397
  position:
    end: 4201
    start: 3682
    type: TextPositionSelector
  quote_sha256: sha256:fe410f2cbda50b9c371a787503d111488337afd03b406f09cfd9fd4166ac92b4
  selector:
    exact: '◼ The ISA is the interface between what the software commands and what
      the hardware carries out ◼ The ISA specifies ❑ The memory organization ◼ Address
      space (LC-3: 2<sup>16</sup>, MIPS: 2<sup>32</sup>) ◼ Addressability (LC-3: 16
      bits, MIPS: 8 bits) ◼ Word- or Byte-addressable ❑ The register set ◼ 8 registers
      (R0 to R7) in LC-3 ◼ 32 registers in MIPS ❑ The instruction set ◼ Opcodes ◼
      Data types ◼ Addressing modes ◼ Length and format of instructions Microarchitecture
      ISA Program Algorithm Problem Circuits Electrons'
    prefix: 'e Instruction Set Architecture


      '
    suffix: '


      ![](_page_19_Diagram_2.jpeg)


      '
    type: TextQuoteSelector
  selector_sha256: sha256:ad2f2f397c4e4c7130b2f3efb8d2750e656581349461d2f6804f905eb670971b
  snapshot_sha256: sha256:fddb6f54728133fc75239a5ef5b621e2f2768ba604c8ebd057a57e155042e246
- evidence_id: evidence-fa9a29315420
  position:
    end: 33568
    start: 33252
    type: TextPositionSelector
  quote_sha256: sha256:66a5a480224c673ee6e4daa8cb4cf327a2d0b643aa2666feb26e67f9823c1ada
  selector:
    exact: ◼ **Traditional (ISA-only) definition:** "The term architecture is used
      here to describe the attributes of a system as seen by the programmer, i.e.,
      the conceptual structure and functional behavior **as distinct from** the organization
      of the dataflow and controls, the logic design, and the physical implementation.
    prefix: 'cost, and other specific goals. '
    suffix: '" Gene Amdahl, IBM Journal of R&'
    type: TextQuoteSelector
  selector_sha256: sha256:ff96745b8d936d96a55fab0baf9a86456442a1509e4d09c2c5f09337ab71abaf
  snapshot_sha256: sha256:fddb6f54728133fc75239a5ef5b621e2f2768ba604c8ebd057a57e155042e246
extractor: marker/2.0.0
id: ddca-lecture8-isa-ii
media_type: application/pdf
origin: external
raw_ref:
  path: archive/raw/e9e3e5194e646960b8725a21069c8a968007075e22a0bda16b98f964b8b0be3c.pdf
  sha256: sha256:e9e3e5194e646960b8725a21069c8a968007075e22a0bda16b98f964b8b0be3c
read_status: retrieved
retrieval:
  acquisition: fetch
  resolved_url: https://safari.ethz.ch/ddca/spring2026/lib/exe/fetch.php?media=onur-ddca-2026-lecture8-isa-ii-afterlecture.pdf
  url: https://safari.ethz.ch/ddca/spring2026/lib/exe/fetch.php?media=onur-ddca-2026-lecture8-isa-ii-afterlecture.pdf
schema_version: source/v1
snapshot_sha256: sha256:fddb6f54728133fc75239a5ef5b621e2f2768ba604c8ebd057a57e155042e246
source_type: doc
vault_id: public
---
# **Digital Design & Computer Arch.**

Lecture 8: Instruction Set Architectures II

Prof. Onur Mutlu

ETH Zürich

Spring 2026

13 March 2026

### Agenda for Today & Next Few Lectures

◼ The von Neumann model ◼ LC-3: An example of von Neumann machine ◼ LC-3 and MIPS Instruction Set Architectures ◼ LC-3 and MIPS assembly and programming ◼ Introduction to microarchitecture and single-cycle microarchitecture ◼Multi-cycle microarchitecture

![](_page_1_Diagram_2.jpeg)

### What Will We Learn Today?

◼ Basic elements of a computer & the von Neumann model ❑ LC-3: An example von Neumann machine ◼ Instruction Set Architectures: LC-3 and MIPS ❑ Operate instructions ❑ Data movement instructions ❑ Control instructions ◼ Instruction formats ◼ Addressing modes Algorithm Problem Logic

![](_page_2_Diagram_2.jpeg)

## Readings

◼ This week ❑ Von Neumann Model, ISA, LC-3, and MIPS ◼ P&P, Chapters 4, 5 (we will follow these today & tomorrow) ◼ H&H, Chapter 6 (until 6.5) ◼ P&P, Appendices A and C (ISA and microarchitecture of LC-3) ◼ H&H, Appendix B (MIPS instructions) ❑ Programming ◼ P&P, Chapter 6 (we will follow this tomorrow) ❑ **Recommended:** H&H Chapter 5, especially 5.1, 5.2, 5.4, 5.5 ◼ Next week ❑ Introduction to microarchitecture and single-cycle microarchitecture ◼ H&H, Chapter 7.1-7.3 ◼ P&P, Appendices A and C ❑ Multi-cycle microarchitecture ◼ H&H, Chapter 7.4 ◼P&P, Appendices A and C

## Quick Recap: The von Neumann Model

![](_page_4_Diagram_1.jpeg)

## Quick Recap: The von Neumann Model

### **Stored program**

### **Sequential instruction processing**

# LC-3: A von Neumann Machine

# LC-3: A von Neumann Machine

![](_page_7_Diagram_1.jpeg)

## Review: Instruction Types

◼ There are three main types of instructions ◼ Operate instructions ❑ Execute operations in the ALU ◼ Data movement instructions ❑ Read from or write to memory ◼ Control flow instructions ❑ Change the sequence of execution ◼Let us start with some example instructions

# Instruction (Processing) Cycle

## Recall: The Instruction Cycle

![](_page_10_Diagram_1.jpeg)

Whether a value fetched from memory is interpreted as an instruction depends on **when** that value is **fetched** in the instruction processing cycle

## Recall: Jump in LC-3

◼Unconditional branch or jump

◼

LC-3

❑ BaseR = Base register ❑ PC ← R2 (Register identified by BaseR) ❑ Variations ◼ RET: special case of JMP where BaseR = R7 ◼JSR, JSRR: jump to subroutine

JMP R2

![](_page_11_Diagram_4.jpeg)

This is register addressing mode

# PC UPDATE in LC-3

![](_page_12_Diagram_1.jpeg)

JMP loads SR1 into PC

## Control of the Instruction Cycle

![](_page_13_Diagram_1.jpeg)

◼ State 1 ❑ The FSM asserts GatePC and LD.MAR ❑ It selects input (+1) in PCMUX and asserts LD.PC ◼ State 2 ❑ MDR is loaded with the instruction ◼ State 3 ❑ The FSM asserts GateMDR and LD.IR ◼ State 4 ❑ The FSM goes to next state depending on opcode ◼ State 63 ❑ JMP loads register into PC ◼ Full state diagram in Patt&Pattel, Appendix C

## To Come: Full State Machine for LC-3b

![](_page_14_Diagram_1.jpeg)

## The Instruction Cycle

![](_page_15_Picture_1.jpeg)

# LC-3 and MIPS Instruction Set Architectures

### Agenda for Today & Next Few Lectures

◼ The von Neumann model ◼ LC-3: An example of von Neumann machine ◼ LC-3 and MIPS Instruction Set Architectures ◼ LC-3 and MIPS assembly and programming ◼ Introduction to microarchitecture and single-cycle microarchitecture ◼Multi-cycle microarchitecture

![](_page_17_Diagram_2.jpeg)

## The Instruction Set

◼ It defines opcodes, data types, and addressing modes ◼ADD and LDR have been our first examples

Register mode

Base+offset mode

### The Instruction Set Architecture

◼ The ISA is the interface between what the software commands and what the hardware carries out ◼ The ISA specifies ❑ The memory organization ◼ Address space (LC-3: 2<sup>16</sup>, MIPS: 2<sup>32</sup>) ◼ Addressability (LC-3: 16 bits, MIPS: 8 bits) ◼ Word- or Byte-addressable ❑ The register set ◼ 8 registers (R0 to R7) in LC-3 ◼ 32 registers in MIPS ❑ The instruction set ◼ Opcodes ◼ Data types ◼ Addressing modes ◼ Length and format of instructions Microarchitecture ISA Program Algorithm Problem Circuits Electrons

![](_page_19_Diagram_2.jpeg)

# Instructions (Opcodes)

### Opcodes

◼ A large or small set of opcodes could be defined ❑ E.g, HP Precision Architecture: an instruction for A\*B+C ❑ E.g, x86 ISA: multimedia extensions (MMX), later SSE, AVX, AMX ❑ E.g, VAX ISA: opcode to save all information of one program prior to switching to another program ◼ Tradeoffs are involved. Examples: ❑ Hardware complexity vs. software complexity ❑ Latency of simple vs. complex instructions ◼ In LC-3 and in MIPS there are three types of opcodes ❑ Operate ❑ Data movement ❑ Control

# Opcodes in LC-3

## Opcodes in LC-3b

## MIPS Instruction Types

I-type

J-type

# Funct in MIPS R-Type Instructions (I)

Opcode is 0 in MIPS R-Type instructions.

Funct defines the operation

# Funct in MIPS R-Type Instructions (II)

◼More complete list of instructions are in H&H Appendix B

# Data Types

### Data Types

◼ An ISA supports one or several data types ◼ LC-3 only supports 2's complement integers ❑ Negative of a 2's complement binary value X = NOT(X) + 1 ◼ MIPS supports ❑ 2's complement integers ❑ Unsigned integers ❑ Floating point ◼ Tradeoffs are involved. Examples: ❑ Hardware complexity vs. software complexity ❑ Latency of operations on supported vs. unsupported data types **H&H Chapter 1.4.6**

### Why Have Different Data Types in ISA?

◼ An example of programmer vs. microarchitect tradeoff ◼ Advantage of more data types: ❑ Enables better mapping of high-level programming constructs to hardware ◼ Hardware can directly operate on data types present in programming languages → small number of instructions and code size ❑ Matrix operations vs. individual multiply/add/load/store instructions ❑ Graph operations vs. individual load/store/add/… instructions ◼ Disadvantage: ❑ More work for the microarchitect ◼ who needs to implement the data types and instructions that operate on data types

### Data Types and Instruction Complexity

◼ Data types are coupled tightly to the semantic level, or complexity of instructions ◼ Concept of semantic gap ❑ how close instructions & data types are to high-level language ◼ Complex instructions + data types → small semantic gap ❑ E.g., insert into a doubly linked list, multiply two matrices ❑ VAX ISA: doubly-linked list, multi-dimensional arrays ◼ Simple instructions + data types → large semantic gap ❑ E.g., primitive operations: load, store, multiply, add, nor ❑ Early RISC machines: Only integer data type, simple operations

## Semantic Gap

◼ How close instructions & data types are to high-level language (HLL)

![](_page_31_Diagram_3.jpeg)

HW

Control

Signals

![](_page_31_Diagram_2.jpeg)

### Complex vs. Simple Instructions+Data Types

◼ Complex instruction: An instruction does a lot of work, e.g. many operations ❑ Insert in a doubly linked list ❑ Compute FFT ❑ String copy ❑ Matrix multiply ❑ … ◼ Simple instruction: An instruction does little work -- it is a primitive using which complex operations can be built ❑ Add ❑ XOR ❑ Multiply ❑ …

### Complex vs. Simple Instructions+Data Types

- ◼ Advantages of Complex Instructions + Data Types + Denser encoding → smaller code size → better memory utilization, saves off-chip bandwidth, better cache hit rate (better packing of instructions) + Simpler compiler: no need to optimize small instructions as much ◼ Disadvantages of Complex Instructions + Data Types
  - Larger chunks of work → compiler has less opportunity to optimize (limited in fine-grained optimizations it can do)
  - More complex hardware → translation from a high level to control signals and optimization needs to be done by hardware

## Aside: An Example: **B**inary**C**oded**D**ecimal

◼Each decimal digit is encoded with a fixed number of bits

![](_page_34_Picture_2.jpeg)

"Binary clock" by Alexander Jones & Eric Pierce - Own work, based on Wapcaplet's Binary clock.png on the English Wikipedia. Licensed under CC BY-SA 3.0 via Wikimedia Commons - http://commons.wikimedia.org/wiki/File:Binary\_clock.svg#mediaviewer/File:Binary\_clock.svg

## Aside: An Example: **B**inary**C**oded**D**ecimal

◼Each decimal digit is encoded with a fixed number of bits

![](_page_35_Picture_3.jpeg)

"Binary clock" by Alexander Jones & Eric Pierce - Own work, based on Wapcaplet's Binary clock.png on the English Wikipedia. Licensed under CC BY-SA 3.0 via Wikimedia Commons - http://commons.wikimedia.org/wiki/File:Binary\_clock.svg#mediaviewer/File:Binary\_clock.svg

# Addressing Modes

## Addressing Modes

◼ An addressing mode is a mechanism for specifying where an operand is located ◼ There are five addressing modes in LC-3 ❑ Immediate or literal (constant) ◼ The operand is in some bits of the instruction ❑ Register ◼ The operand is in one of R0 to R7 registers ❑ Three memory addressing modes ◼ PC-relative ◼ Indirect ◼ Base+offset ◼ MIPS has pseudo-direct addressing (for j and jal), additionally, but does **not** have indirect addressing

### Why Have Different Addressing Modes?

◼ Another example of programmer vs. microarchitect tradeoff ◼ Advantage of more addressing modes: ❑ Enables better mapping of high-level programming constructs to hardware ◼ some accesses are better expressed with a different mode → reduced number of instructions and code size ❑ Array indexing (one or multi-dimensional) ❑ Pointer-based accesses (indirection) ❑ Matrix element indexing; sparse matrix element indexing ◼ Disadvantages: ❑ More work for the microarchitect ❑ More options for the compiler to decide what to use

## Semantic Gap Applies to Addressing Modes

◼ How close instructions & data types & addressing modes are to high-level language (HLL)

![](_page_39_Diagram_2.jpeg)

HW

Control

Signals

![](_page_39_Diagram_3.jpeg)

### Many Tradeoffs in ISA Design...

◼ Execution model – sequencing model and processing style ◼ Instruction length ◼ Instruction format ◼ Instruction types ◼ Instruction complexity vs. simplicity ◼ Data types ◼ Number of registers ◼ Addressing mode types ◼ Memory organization (address space, addressability, endianness, …) ◼ Memory access restrictions and permissions ◼ Support for multiple instructions to execute in parallel? ◼…

# Operate Instructions

### Operate Instructions

◼ In LC-3, there are three operate instructions ❑ NOT is a unary operation (one source operand) ◼ It executes bitwise NOT ❑ ADD and AND are binary operations (two source operands) ◼ ADD is 2's complement addition ◼ AND is bitwise SR1 & SR2 ◼ In MIPS, there are many more ❑ Many R-type instructions (they are binary operations) ◼ E.g., add, and, nor, xor… ❑ I-type versions (i.e., with one immediate operand) of the Rtype operate instructions ❑ F-type operations, i.e., floating-point operations

### ◼

 NOT assembly and machine code LC-3 assembly

# NOT in LC-3

NOT R3, R5

### Field Values

### Machine Code

![](_page_43_Diagram_3.jpeg)

There is no NOT in MIPS. How is it implemented?

There is no NOT in LC-3b. How is it implemented?

### Operate Instructions

◼ We are already familiar with LC-3's ADD and AND with register mode (R-type in MIPS) ◼ Now let us see the versions with one literal (i.e., immediate) operand ◼ We will use Subtraction as an example ❑ How is it implemented in LC-3 and MIPS?

### Recall: LC-3 Operate Instruction Format

◼LC-3 Operate Instruction Format (Register OP Register)

❑ OP = opcode (what the instruction does)

◼

E.g., ADD = 0001

❑ Semantics: DR ← SR1 + SR2

◼

E.g., AND = 0101

❑ Semantics: DR ← SR1 AND SR2

❑ SR1, SR2 = source registers

❑ DR = destination register

| OP          | DR      | SR1    | 0 | 00  | SR2    |
|-------------|---------|--------|---|-----|--------|
| 4 bits      | 3 bits  | 3 bits |   |     | 3 bits |
| 15 14 13 12 | 11 10 9 | 8 7 6  | 5 | 4 3 | 2 1 0  |

## Operate Instr. with one Literal in LC-3

### ◼ADD and AND

❑ OP = operation ◼ E.g., ADD = 0001 (same OP as the register-mode ADD) ❑ DR ← SR1 + sign-extend(imm5) ◼ E.g., AND = 0101 (same OP as the register-mode AND) ❑ DR ← SR1 AND sign-extend(imm5) ❑ SR1 = source register ❑ DR = destination register ❑ imm5 = Literal or immediate (sign-extend to 16 bits)

◼ADD assembly and machine code

## ADD with one Literal in LC-3

ADD R1, R4, #-2

### LC-3 assembly

### Field Values

### Machine Code

![](_page_47_Diagram_3.jpeg)

# ADD with one Literal in LC-3 Data Path

![](_page_48_Diagram_1.jpeg)

## Instructions with one Literal in MIPS

◼ I-type MIPS Instructions ❑ 2 register operands and immediate ◼Some operate and data movement instructions

❑ opcode = operation ❑ rs = source register ❑ rt = ◼ destination register in some instructions (e.g., addi, lw) ◼ source register in others (e.g., sw) ❑ imm = Literal or immediate

![](_page_49_Diagram_2.jpeg)

### ◼Add immediate

## ADD with one Literal in MIPS

addi \$s0, \$s1, 5

### MIPS assembly

### Field Values

### Machine Code

### 0x22300005

rt ← rs + sign-extend(imm)

## Subtraction in MIPS vs. LC-3

### ◼MIPS assembly

### ◼LC-3 assembly

◼ Tradeoff in LC-3 ❑ More instructions ❑ But, simpler control logic

a = b + c - d; add \$t0, \$s0, \$s1 sub \$s3, \$t0, \$s2

High-level code MIPS assembly

a = b + c - d; ADD R2, R0, R1 NOT R4, R3 ADD R5, R4, #1 ADD R6, R2, R5 **2's complement of R3**

High-level code LC-3 assembly

### Subtract Immediate

### ◼MIPS assembly

### ◼LC-3

a = b - 3; subi \$s1, \$s0, 3

High-level code MIPS assembly

![](_page_52_Diagram_4.jpeg)

### Is subi necessary in MIPS?

addi \$s1, \$s0, -3

### MIPS assembly

a = b - 3; ADD R1, R0, #-3

High-level code LC-3 assembly

# Data Movement Instructions and Addressing Modes

### Data Movement Instructions

◼ In LC-3, there are seven data movement instructions ❑ LD, LDR, LDI, LEA, ST, STR, STI ◼ Format of load and store instructions ❑ Opcode (bits [15:12]) ❑ DR or SR (bits [11:9]) ❑ Address generation bits (bits [8:0]) ❑ Four ways to interpret bits, called addressing modes ◼ PC-Relative Mode ◼ Indirect Mode ◼ Base+Offset Mode ◼ Immediate Mode ◼ In MIPS, there are only Base+offset and Immediate modes for load and store instructions

## PC-Relative Addressing Mode

### ◼LD (Load) and ST (Store)

❑ OP = opcode ◼ E.g., LD = 0010 ◼ E.g., ST = 0011 ❑ DR = destination register in LD ❑ SR = source register in ST ❑ LD: DR ← Memory[PC + sign-extend(PCoffset9)] ❑ ST: Memory[PC + sign-extend(PCoffset9)] ← SR

| OP          | DR/SR   |   |   | PCoffset9 |   |   |
|-------------|---------|---|---|-----------|---|---|
| 4 bits      | 3 bits  |   |   | 9 bits    |   |   |
| 15 14 13 12 | 11 10 9 | 8 | 7 | 6 5 4 3 2 | 1 | 0 |

### ◼LD assembly and machine code

## LD in LC-3

LD R2, 0x1AF

### LC-3 assembly

### Field Values

### Machine Code

![](_page_56_Diagram_2.jpeg)

The memory address is only +255 to -256 locations away of the LD or ST instruction

Limitation: The PC-relative addressing mode cannot address far away from the instruction

## Indirect Addressing Mode

### ◼LDI (Load Indirect) and STI (Store Indirect)

❑ OP = opcode ◼ E.g., LDI = 1010 ◼ E.g., STI = 1011 ❑ DR = destination register in LDI ❑ SR = source register in STI ❑ LDI: DR ← Memory[Memory[PC + sign-extend(PCoffset9)]] ❑ STI: Memory[Memory[PC + sign-extend(PCoffset9)]] ← SR

| OP          | DR/SR   |   |   | PCoffset9 |   |   |
|-------------|---------|---|---|-----------|---|---|
| 4 bits      | 3 bits  |   |   | 9 bits    |   |   |
| 15 14 13 12 | 11 10 9 | 8 | 7 | 6 5 4 3 2 | 1 | 0 |

### ◼LDI assembly and machine code

## LDI in LC-3

LDI R3, 0x1CC

### LC-3 assembly

### Field Values

### Machine Code

Now the address of the operand can be anywhere in the memory

![](_page_58_Diagram_2.jpeg)

## Base+Offset Addressing Mode

◼LDR (Load Register) and STR (Store Register)

❑ OP = opcode ◼ E.g., LDR = 0110 ◼ E.g., STR = 0111 ❑ DR = destination register in LDR ❑ SR = source register in STR ❑ LDR: DR ← Memory[BaseR + sign-extend(offset6)] ❑ STR: Memory[BaseR + sign-extend(offset6)] ← SR

| OP          | DR/SR   |   |   |   |   | offset6 |   |
|-------------|---------|---|---|---|---|---------|---|
| 4 bits      | 3 bits  |   |   |   |   | 6 bits  |   |
| 15 14 13 12 | 11 10 9 | 8 | 7 | 6 | 5 | 4 3 2 1 | 0 |

### ◼LDR assembly and machine code

## LDR in LC-3

LDR R1, R2, 0x1D

### LC-3 assembly

Again, the address of the operand can be anywhere in the memory

![](_page_60_Diagram_2.jpeg)

### Field Values

### Machine Code

# Address Calculation in LC-3 Data Path

![](_page_61_Diagram_1.jpeg)

# Base+Offset Addressing Mode in MIPS

◼ In MIPS, lw and sw use base+offset mode (or base addressing mode)

◼imm is the 16-bit offset, which is sign-extended to 32 bits

A[2] = a; sw \$s3, 8(\$s0)

### High-level code MIPS assembly

Memory[\$s0 + 8] ← \$s3

### Field Values

### An Example Program in MIPS and LC-3

a = A[0];

c = a + b - 5;

B[0] = c;

A = \$s0

b = \$s2

B = \$s1

### High-level code MIPS registers

LDR R5, R0, #0

ADD R6, R5, R2

ADD R7, R6, #-5

STR R7, R1, #0

### LC-3 assembly

lw \$t0, 0(\$s0) add \$t1, \$t0, \$s2 addi \$t2, \$t1, -5 sw \$t2, 0(\$s1)

### MIPS assembly

A = R0

b = R2

B = R1

LC-3 registers

## Immediate Addressing Mode (in LC-3)

### ◼LEA (Load Effective Address)

❑ OP = 1110 ❑ DR = destination register ❑ LEA: DR ← PC + sign-extend(PCoffset9)

| OP          | DR      |   |   | PCoffset9 |   |   |
|-------------|---------|---|---|-----------|---|---|
| 4 bits      | 3 bits  |   |   | 9 bits    |   |   |
| 15 14 13 12 | 11 10 9 | 8 | 7 | 6 5 4 3 2 | 1 | 0 |

What is the difference from PC-Relative addressing mode?

Answer: Instructions with PC-Relative mode load from memory, but LEA does not → Hence the name Load Effective Address

### ◼LEA assembly and machine code

## LEA in LC-3

LEA R5, #-3

### LC-3 assembly

### Field Values

### Machine Code

![](_page_65_Diagram_3.jpeg)

# Address Calculation in LC-3 Data Path

![](_page_66_Diagram_1.jpeg)

## Immediate Addressing Mode in MIPS

◼ In MIPS, lui (load upper immediate) loads a 16-bit immediate into the upper half of a register and sets the lower half to 0 ◼It is used to assign 32-bit constants to a register

a = 0x6d5e4f3c; # \$s0 = a

lui \$s0, 0x6d5e ori \$s0, 0x4f3c

High-level code MIPS assembly

## Addressing Example in LC-3

◼What is the final value of R3?

**x30F4**

**P&P, Chapter 5.3.5**

# LC- ISA Instruction Encodings

### **Patt & Patel, Back cover inside**

◼What is the final value of R3?

◼The final value of R3 is 5

**x30F4** LEA ADD ST AND ADD STR LDI -3 14 -5 5 14 -9 0 R3 = M[M[PC – 9]] = M[M[0x30FD – 9]] = R1 = PC – 3 = 0x30F7 – 3 = 0x30F4 R2 = R1 + 14 = 0x30F4 + 14 = 0x3102 M[PC - 5] = M[0x030F4] = 0x3102 R2 = 0 R2 = R2 + 5 = 5 M[R1 + 14] = M[0x30F4 + 14] = M[0x3102] = 5 M[M[0x30F4]] = M[0x3102] = 5

## Addressing Example in LC-3

**P&P, Chapter 5.3.5**

# Control Flow Instructions

## Control Flow Instructions

◼ Allow a program to execute out of sequence ◼ Conditional branches and unconditional jumps ❑ Conditional branches are used to make decisions ◼ E.g., if-else statement ❑ In LC-3, three condition codes are used ❑ Jumps are used to implement ◼ Loops ◼ Function calls ❑ JMP in LC-3 and j in MIPS ◼We have already seen these

Conditional Control Flow (Conditional Branching)

## Condition Codes in LC-3

◼ Each time one GPR (R0-R7) is written, three single-bit registers are updated ◼ Each of these condition codes are either set (set to 1) or cleared (set to 0) ❑ If the written value is negative ◼ N is set, Z and P are cleared ❑ If the written value is zero ◼ Z is set, N and P are cleared ❑ If the written value is positive ◼ P is set, N and Z are cleared ◼x86 and SPARC are examples of ISAs that use condition codes

# Conditional Branches in LC-3

### ◼BRz (Branch if Zero)

❑ n, z, p = which condition code is tested (N, Z, and/or P) ◼ n, z, p: instruction bits to identify the condition codes to be tested ◼ N, Z, P: values of the corresponding condition codes ❑ PCoffset9 = immediate or constant value ❑ if ((n AND N) OR (p AND P) OR (z AND Z)) ◼ then PC ← PC + sign-extend(PCoffset9) ❑ Variations: BRn, BRz, BRp, BRzp, BRnp, BRnz, BRnzp

BRz PCoffset9

0000 n PCoffset9

4 bits 9 bits

z p

# Conditional Branches in LC-3

### ◼BRz

BRz 0x0D9

What if n = z = p = 1?\* (i.e., BRnzp)

And what if n = z = p = 0?

![](_page_76_Diagram_1.jpeg)

# Conditional Branches in MIPS

### ◼beq (Branch if Equal)

❑ 4 = opcode ❑ rs, rt = source registers ❑ offset = immediate or constant value ❑ if rs == rt ◼ then PC ← PC + sign-extend(offset) \* 4 ❑ Variations: beq, bne, blez, bgtz

beq \$s0, \$s1, offset

◼ This is an example of tradeoff in the instruction set ❑ The same functionality requires more instructions in LC-3 ❑ But, the control logic requires more complexity in MIPS

beq \$s0, \$s1, offset

## Branch If Equal in MIPS and LC-3

### MIPS assembly LC-3 assembly

NOT R2, R1 ADD R3, R2, #1 ADD R4, R3, R0 BRz offset **Subtract (R0 - R1)**

### What We Learned

◼ Basic elements of a computer & the von Neumann model ❑ LC-3: An example von Neumann machine ◼ Instruction Set Architectures: LC-3 and MIPS ❑ Operate instructions ❑ Data movement instructions ❑ Control instructions ◼ Instruction formats ◼ Addressing modes Micro-architecture SW/HW Interface Algorithm Problem Logic Devices System Software

## There Is A Lot More to Cover on ISAs

![](_page_80_Picture_1.jpeg)

### Many Different ISAs Over Decades

◼ x86 ◼ PDP-x: Programmed Data Processor (PDP-11) ◼ VAX ◼ IBM 360 ◼ CDC 6600 ◼ SIMD ISAs: CRAY-1, Connection Machine ◼ VLIW ISAs: Multiflow, Cydrome, IA-64 (EPIC) ◼ PowerPC, POWER ◼ RISC ISAs: Alpha, MIPS, SPARC, ARM, RISC-V, … ◼ What are the fundamental differences? ❑ E.g., how instructions are specified and what they do ❑ E.g., how complex are instructions, data types, addr. modes

### Complex vs. Simple Instructions+Data Types

◼ Complex instruction: An instruction does a lot of work, e.g. many operations ❑ Insert in a doubly linked list ❑ Compute FFT ❑ String copy ❑ Matrix multiply ❑ … ◼ Simple instruction: An instruction does little work -- it is a primitive using which complex operations can be built ❑ Add ❑ XOR ❑ Multiply ❑ …

### Complex vs. Simple Instructions+Data Types

- ◼ Advantages of Complex Instructions + Data Types + Denser encoding → smaller code size → better memory utilization, saves off-chip bandwidth, better cache hit rate (better packing of instructions) + Simpler compiler: no need to optimize small instructions as much ◼ Disadvantages of Complex Instructions + Data Types
  - Larger chunks of work → compiler has less opportunity to optimize (limited in fine-grained optimizations it can do)
  - More complex hardware → translation from a high level to control signals and optimization needs to be done by hardware

Harder mapping of HLL to ISA **More work for software designer Less work for hardware designer** Optimization burden on SW

## Semantic Gap

◼ How close instructions & data types & addressing modes are to high-level language (HLL)

![](_page_84_Diagram_2.jpeg)

HW

Control

Signals

![](_page_84_Diagram_3.jpeg)

Easier mapping of HLL to ISA **Less work for software designer More work for hardware designer** Optimization burden on HW

# **We Covered Until Here in Lecture**

# **Digital Design & Computer Arch.**

Lecture 8: Instruction Set Architectures II

Prof. Onur Mutlu

ETH Zürich

Spring 2026

13 March 2026

**Further Slides for Your Own Study (May Be Covered in Future Lectures)**

### How to Change the Semantic Gap Tradeoffs

◼Translate from one ISA into a different "implementation" ISA

![](_page_88_Diagram_2.jpeg)

## An Example: Rosetta 2 Binary Translator

![](_page_89_Picture_4.jpeg)

## An Example: Rosetta 2 Binary Translator

![](_page_90_Picture_1.jpeg)

Apple M1, 2021

### Another Example: Intel and AMD Processors

![](_page_91_Diagram_1.jpeg)

### Another Example: Intel and AMD Processors

![](_page_92_Figure_1.jpeg)

Intel Alder Lake, 2021

### Another Example: Intel and AMD Processors

![](_page_93_Picture_1.jpeg)

AMD Ryzen 5000, 2020

Core Count: 8 cores/16 threads

L1 Caches: 32 KB per core

### L2 Caches:

512 KB per core

### L3 Cache:

32 MB shared

# Another Example: NVIDIA Denver

![](_page_94_Diagram_1.jpeg)

## Another Example: NVIDIA Denver

![](_page_95_Picture_4.jpeg)

![](_page_95_Diagram_5.jpeg)

### Transmeta: x86 to VLIW Translation

Klaiber, "The Technology Behind Crusoe Processors," Transmeta White Paper 2000.

![](_page_96_Diagram_1.jpeg)

![](_page_96_Picture_2.jpeg)

## ISA-level Tradeoffs: Number of Registers

◼ Affects: ❑ Number of bits used for encoding register address ❑ Number of values kept in fast storage (register file) ❑ (uarch) Size, access time, power consumption of register file ◼ Large number of registers: + Enables better register allocation (and optimizations) by compiler → fewer saves/restores -- Larger instruction size -- Larger register file size

## There Is A Lot More to Cover on ISAs

![](_page_98_Picture_1.jpeg)

## There Is A Lot More to Cover on ISAs

![](_page_99_Figure_1.jpeg)

### Detailed Lectures on ISAs & ISA Tradeoffs

◼ Computer Architecture, Spring 2015, Lecture 3 ❑ ISA Tradeoffs (CMU, Spring 2015) [❑](https://www.youtube.com/watch?v=KDy632z23UE&list=PL5Q2soXY2Zi9xidyIgBxUz7xRPS-wisBN&index=8) [https://www.youtube.com/watch?v=QKdiZSfwg](https://www.youtube.com/watch?v=KDy632z23UE&list=PL5Q2soXY2Zi9xidyIgBxUz7xRPS-wisBN&index=8)[g&list=PL5PHm2jkkXmi5CxxI7b3JCL1TWybTDtKq&index=3](https://www.youtube.com/watch?v=KDy632z23UE&list=PL5Q2soXY2Zi9xidyIgBxUz7xRPS-wisBN&index=8) ◼ Computer Architecture, Spring 2015, Lecture 4 ❑ ISA Tradeoffs & MIPS ISA (CMU, Spring 2015) [❑](https://www.youtube.com/watch?v=pwRw7QqK_qA&list=PL5Q2soXY2Zi9xidyIgBxUz7xRPS-wisBN&index=9) [https://www.youtube.com/watch?v=RBgeCCW5Hjs&list=PL5PHm2jkkXmi5CxxI7b3J](https://www.youtube.com/watch?v=pwRw7QqK_qA&list=PL5Q2soXY2Zi9xidyIgBxUz7xRPS-wisBN&index=9) [CL1TWybTDtKq&index=4](https://www.youtube.com/watch?v=pwRw7QqK_qA&list=PL5Q2soXY2Zi9xidyIgBxUz7xRPS-wisBN&index=9) ◼ Computer Architecture, Spring 2015, Lecture 2 ❑ Fundamental Concepts and ISA (CMU, Spring 2015) [❑](https://www.youtube.com/watch?v=gR7XR-Eepcg&list=PL5Q2soXY2Zi9xidyIgBxUz7xRPS-wisBN&index=10) [https://www.youtube.com/watch?v=NpC39uS4K4o&list=PL5PHm2jkkXmi5CxxI7b3J](https://www.youtube.com/watch?v=gR7XR-Eepcg&list=PL5Q2soXY2Zi9xidyIgBxUz7xRPS-wisBN&index=10) [CL1TWybTDtKq&index=2](https://www.youtube.com/watch?v=gR7XR-Eepcg&list=PL5Q2soXY2Zi9xidyIgBxUz7xRPS-wisBN&index=10) 

ISA Design and Tradeoffs: More Critical Thinking

## The Von Neumann Model/Architecture

### **Stored program**

### **Sequential instruction processing**

### The von Neumann Model/Architecture

◼ Von Neumann model is also called stored program computer (instructions in memory). It has two key properties: ◼ Stored program ❑ Instructions stored in a linear memory array ❑ Memory is unified between instructions and data ◼ The interpretation of a stored value depends on the control signals ◼ Sequential instruction processing When is a value interpreted as an instruction?

## Recall: The Instruction Cycle

![](_page_104_Diagram_1.jpeg)

Whether a value fetched from memory is interpreted as an instruction depends on **when** that value is **fetched** in the instruction processing cycle.

### The von Neumann Model/Architecture

◼ Von Neumann model is also called stored program computer (instructions in memory). It has two key properties: ◼ Stored program ❑ Instructions stored in a linear memory array ❑ Memory is unified between instructions and data ◼ The interpretation of a stored value depends on the control signals ◼ Sequential instruction processing ❑ One instruction processed (fetched, executed, completed) at a time ❑ Program counter (instruction pointer) identifies the current instruction ❑ Program counter is advanced sequentially except for control transfer instructions When is a value interpreted as an instruction?

### The von Neumann Model/Architecture

◼ Recommended reading ❑ Burks, Goldstein, von Neumann, "Preliminary discussion of the logical design of an electronic computing instrument, " 1946. ◼ Important reading ❑ Patt and Patel book, Chapter 4, "The von Neumann Model" ◼ **Stored program** ◼**Sequential instruction processing**

## The Von Neumann Model (of a Computer)

![](_page_107_Diagram_1.jpeg)

◼ Q: Is this the only way that a computer can process computer programs?

![](_page_108_Picture_3.jpeg)

◼ A: No. ◼ Qualified Answer: No. But, it has been the dominant way ❑ i.e., the dominant paradigm for computing ❑ for N decades

## The Von Neumann Model (of a Computer)

# The Dataflow Execution Model of a Computer

### The Dataflow Model (of a Computer)

◼ Von Neumann model: An instruction is fetched and executed in control flow order ❑ As specified by the program counter (instruction pointer) ❑ Sequential unless explicit control flow instruction ◼ Dataflow model: An instruction is fetched and executed in data flow order ❑ i.e., when its operands are ready ❑ i.e., there is no program counter (instruction pointer) ❑ Instruction ordering specified by data flow dependence ◼ Each instruction specifies "who" should receive the result ◼ An instruction can "fire" whenever all operands are received ❑ Potentially many instructions can execute at the same time ◼Inherently more parallel

## Von Neumann vs. Dataflow

◼ Consider a Von Neumann program ❑ What is the significance of the program order? ❑ What is the significance of the storage locations?

**v = a + b; w = b \* 2; x = v - w y = v + w z = x \* y**

![](_page_111_Diagram_2.jpeg)

**Sequential**

**a, b** are the only inputs **z** is the only output

### More on Dataflow

◼ In a dataflow machine, a program consists of dataflow nodes ❑ A dataflow node fires (fetched and executed) when all it inputs are ready ◼ i.e. when all inputs have tokens ◼Dataflow node and its ISA representation

![](_page_112_Diagram_2.jpeg)

## Example Dataflow Nodes

![](_page_113_Diagram_1.jpeg)

# A Simple Example Dataflow Program

![](_page_114_Diagram_1.jpeg)

**N is a non-negative integer**

**What is the value of OUT?**

### ISA-level Tradeoff: Program Counter

◼ Do we want a Program Counter (PC or IP) in the ISA? ❑ Yes: Control-driven, sequential execution ◼ An instruction is executed when the PC points to it ◼ PC automatically changes sequentially (except for control flow instructions) → sequential ❑ No: Data-driven, parallel execution ◼ An instruction is executed when all its operand values are available → dataflow ◼ Tradeoffs: MANY high-level ones ❑ Ease of programming (for average programmers)? ❑ Ease of compilation? ❑ Performance: Extraction of parallelism? ❑ Hardware complexity?

### ISA vs. Microarchitecture Level Tradeoff

◼ A similar tradeoff (control vs. data-driven execution) can be made at the microarchitecture level ◼ ISA: Specifies how the **programmer sees** the instructions to be executed ❑ Programmer sees a sequential, control-flow execution order vs. ❑ Programmer sees a dataflow execution order ◼ Microarchitecture: How the **underlying implementation actually executes** instructions ❑ Microarchitecture can execute instructions in any order as long as it obeys the semantics specified by the ISA when making the instruction results visible to software ◼Programmer should see the order specified by the ISA

### Let's Get Back to the von Neumann Model

◼ But, if you want to learn more about dataflow… ◼ Dennis and Misunas, "A preliminary architecture for a basic data-flow processor, " ISCA 1974. ◼ Gurd et al., "The Manchester prototype dataflow computer, " CACM 1985. ◼ A later lecture ◼ If you are really impatient: [❑](http://www.youtube.com/watch?v=D2uue7izU2c) <http://www.youtube.com/watch?v=D2uue7izU2c> [❑](http://www.ece.cmu.edu/~ece740/f13/lib/exe/fetch.php?media=onur-740-fall13-module5.2.1-dataflow-part1.ppt) [http://www.ece.cmu.edu/~ece740/f13/lib/exe/fetch.php?medi](http://www.ece.cmu.edu/~ece740/f13/lib/exe/fetch.php?media=onur-740-fall13-module5.2.1-dataflow-part1.ppt) [a=onur-740-fall13-module5.2.1-dataflow-part1.ppt](http://www.ece.cmu.edu/~ece740/f13/lib/exe/fetch.php?media=onur-740-fall13-module5.2.1-dataflow-part1.ppt)

## Lecture Video on Dataflow Architectures

### The von Neumann Model

◼ All major instruction set architectures today use this model ❑ x86, ARM, MIPS, SPARC, Alpha, POWER, RISC-V, … ◼ Underneath (at the microarchitecture level), the execution model of almost all implementations (or, microarchitectures) is very different ❑ Pipelined instruction execution: Intel 80486 uarch ❑ Multiple instructions at a time: Intel Pentium uarch ❑ Out-of-order execution: Intel Pentium Pro uarch ❑ Separate instruction and data caches ◼ But, what happens underneath that is **not consistent** with the von Neumann model is **not exposed** to software ❑ Difference between ISA and microarchitecture

## What is Computer Architecture?

◼ **ISA+implementation definition:** The science and art of designing, selecting, and interconnecting hardware components and designing the hardware/software interface to create a computing system that meets functional, performance, energy consumption, cost, and other specific goals. ◼ **Traditional (ISA-only) definition:** "The term architecture is used here to describe the attributes of a system as seen by the programmer, i.e., the conceptual structure and functional behavior **as distinct from** the organization of the dataflow and controls, the logic design, and the physical implementation." Gene Amdahl, IBM Journal of R&D, April 1964

### ISA vs. Microarchitecture

### ◼

 ISA ❑ Agreed upon interface between software and hardware ◼ SW/compiler assumes, HW promises ❑ What the software writer needs to know to write and debug system/user programs Microarchitecture ❑ Specific implementation of an ISA ❑ Not visible to the software Microprocessor ❑ **ISA, uarch**, circuits ❑ "Architecture" = ISA + microarchitecture

### ◼

### ◼

Microarchitecture

ISA

Program

Algorithm

Problem

Circuits

Electrons

## Microarchitecture

◼ A specific **implementation** of the ISA ◼ How do we implement the ISA? ❑ We will discuss this for many lectures ◼ There can be many implementations of the same ISA ❑ **MIPS** R2000, R3000, R4000, R6000, R8000, R10000, … ❑ **x86**: Intel 80486, Pentium, Pentium Pro, Pentium 4, Kaby Lake, Coffee Lake, Comet Lake, Ice Lake, Golden Cove, Sapphire Rapids, …, AMD K5, K7, K9, Bulldozer, BobCat, Ryzen X, … ❑ **POWER** 4, 5, 6, 7, 8, 9, 10 (IBM), …, **PowerPC** 604, 605, 620, … ❑ **ARM** Cortex-M\*, ARM Cortex-A\*, NVIDIA Denver, Apple A\*, M1, … ❑ **Alpha** 21064, 21164, 21264, 21364, … ❑ **RISC-V** … ❑ …

## ISA vs. Microarchitecture

![](_page_123_Picture_1.jpeg)

◼ What is part of ISA vs. Uarch? ❑ Gas pedal: interface for "acceleration" ❑ Internals of the engine: implement "acceleration" ◼ Implementation (uarch) can be various as long as it satisfies the specification (ISA) ❑ Add instruction vs. Adder implementation ◼ Bit serial, ripple carry, carry lookahead adders are all part of microarchitecture **(see H&H Chapter 5.2.1)** ❑ x86 ISA has many implementations: ◼ Intel 80486, Pentium, Pentium Pro, Pentium 4, Kaby Lake, Coffee Lake, Comet Lake, Ice Lake, Golden Cover, Sapphire Rapids, …, AMD K5, K7, K9, Bulldozer, BobCat, Ryzen X, … ◼ Microarchitecture usually changes faster than ISA ❑ Few ISAs (x86, ARM, SPARC, MIPS, Alpha, RISC-V) but many uarchs ❑ Why?

## ISA: What Does It Specify?

◼ Instructions ❑ Opcodes, Addressing Modes, Data Types ❑ Instruction Types and Formats ❑ Registers, Condition Codes ◼ Memory ❑ Address space, Addressability, Alignment ❑ Virtual memory management ◼ Call, Interrupt/Exception Handling ◼ Access Control, Priority/Privilege ◼ I/O: memory-mapped vs. instructions ◼ Task/thread Management ◼ Power & Thermal Management ◼ Multithreading & Multiprocessor support ◼…

## ISAs Keep Getting Extended

## ISAs Keep Getting Extended

# ISA Manuals: Some Good Bedtime Reading

# ISA Manuals: Some Good Bedtime Reading

## Lecture 9b: Assembly Programming

![](_page_129_Picture_1.jpeg)

![](_page_129_Picture_7.jpeg)

# Lecture 9b: Assembly Programming