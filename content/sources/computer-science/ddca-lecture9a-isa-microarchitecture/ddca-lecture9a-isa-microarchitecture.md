---
archive_policy: text-only
attachments:
- filename: ddca-lecture9a-isa-microarchitecture.pdf
  kind: document
  media_type: application/pdf
  role: original
  sha256: sha256:a5e3aa45dc7fc68e53679300647c0f2dd79bf3bd3c9f729e4dd081355f4fd201
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-99b25955f40a
  position:
    end: 14527
    start: 14170
    type: TextPositionSelector
  quote_sha256: sha256:3380320bff8bd31a0382c750bac92fc5b0f886a5e7ed0ff65ad2a4217288d251
  selector:
    exact: '❑ Programmer sees a dataflow execution order ◼ Microarchitecture: How
      the **underlying implementation actually executes** instructions ❑ Microarchitecture
      can execute instructions in any order as long as it obeys the semantics specified
      by the ISA when making the instruction results visible to software ◼Programmer
      should see the order specified by the ISA'
    prefix: 'ontrol-flow execution order vs. '
    suffix: '


      #### Let''s Get Back to the von'
    type: TextQuoteSelector
  selector_sha256: sha256:60d7a8b6df7f0750418e7d9caf182b1942c062e2d159a534a6574abd22d775f3
  snapshot_sha256: sha256:1dbffebf15f7207b7dacd72198b4839e727f0bc560151afa8bdadbe92d9ce1b8
- evidence_id: evidence-962563aa0e01
  position:
    end: 17844
    start: 17211
    type: TextPositionSelector
  quote_sha256: sha256:9a155cf5c8656bb4d74d595bee434207e9437aae52662bb455acd1b8cb9a9790
  selector:
    exact: '◼ A specific **implementation** of the ISA ◼ How do we implement the ISA?
      ❑ We will discuss this for many lectures ◼ There can be many implementations
      of the same ISA ❑ **MIPS** R2000, R3000, R4000, R6000, R8000, R10000, … ❑ **x86**:
      Intel 80486, Pentium, Pentium Pro, Pentium 4, Kaby Lake, Coffee Lake, Comet
      Lake, Ice Lake, Golden Cove, Sapphire Rapids, …, AMD K5, K7, K9, Bulldozer,
      BobCat, Ryzen X, … ❑ **POWER** 4, 5, 6, 7, 8, 9, 10 (IBM), …, **PowerPC** 604,
      605, 620, … ❑ **ARM** Cortex-M\*, ARM Cortex-A\*, NVIDIA Denver, Apple A\*,
      M1, … ❑ **Alpha** 21064, 21164, 21264, 21364, … ❑ **RISC-V** … ❑ **z/Architecture**
      … ❑ … 69'
    prefix: 'ectrons


      ### Microarchitecture


      '
    suffix: '


      ### ISA vs. Microarchitecture

      '
    type: TextQuoteSelector
  selector_sha256: sha256:a21949a274c84976e6d7c4e5f333878015094f5c06ef514470ab2cc9d57b7655
  snapshot_sha256: sha256:1dbffebf15f7207b7dacd72198b4839e727f0bc560151afa8bdadbe92d9ce1b8
extractor: marker/2.0.0
id: ddca-lecture9a-isa-microarchitecture
media_type: application/pdf
origin: external
raw_ref:
  path: archive/raw/a5e3aa45dc7fc68e53679300647c0f2dd79bf3bd3c9f729e4dd081355f4fd201.pdf
  sha256: sha256:a5e3aa45dc7fc68e53679300647c0f2dd79bf3bd3c9f729e4dd081355f4fd201
read_status: retrieved
retrieval:
  acquisition: fetch
  resolved_url: https://safari.ethz.ch/ddca/spring2026/lib/exe/fetch.php?media=onur-ddca-2026-lecture9a-isa-microarchitecture-afterlecture.pdf
  url: https://safari.ethz.ch/ddca/spring2026/lib/exe/fetch.php?media=onur-ddca-2026-lecture9a-isa-microarchitecture-afterlecture.pdf
schema_version: source/v1
snapshot_sha256: sha256:1dbffebf15f7207b7dacd72198b4839e727f0bc560151afa8bdadbe92d9ce1b8
source_type: doc
vault_id: public
---
## **Digital Design & Computer Arch.**

Lecture 9a: ISA & Microarchitecture

Prof. Onur Mutlu

ETH Zürich

Spring 2026

19 March 2026

### **Extra Credit Assignment:** Talk Analysis

◼ The Story of RowHammer, RowPress & Beyond ◼ **Watch and analyze this short lecture (30 minutes)** [❑](https://www.youtube.com/watch?v=U1EcqXlclKU) <https://www.youtube.com/watch?v=U1EcqXlclKU> (June 2024)

![](_page_1_Picture_2.jpeg)

◼ **Assignment – for 1% extra credit** ❑ **Write a good 1-page individualized summary (no AI use)**  ◼ What are your key takeaways? What did you learn? ◼ What surprised you about the content presented? What excited you? ◼ What do you think solutions should be like? ◼Submit your summary to Moodle – deadline March 21

### Agenda for Today & Next Few Lectures

◼ The von Neumann model ◼ LC-3: An example of von Neumann machine ◼ LC-3 and MIPS Instruction Set Architectures ◼ LC-3 and MIPS assembly and programming ◼ Introduction to microarchitecture and single-cycle microarchitecture ◼Multi-cycle microarchitecture

![](_page_2_Diagram_2.jpeg)

### What Have We Been Learning?

◼ Basic elements of a computer & the von Neumann model ❑ LC-3: An example von Neumann machine ◼ Instruction Set Architectures: LC-3 and MIPS ❑ Operate instructions ❑ Data movement instructions ❑ Control instructions ◼ Instruction formats ◼ Addressing modes Algorithm Problem Logic

![](_page_3_Diagram_2.jpeg)

### Readings

◼ Last week ❑ Von Neumann Model, ISA, LC-3, and MIPS ◼ P&P, Chapters 4, 5 (we will follow these today & tomorrow) ◼ H&H, Chapter 6 (until 6.5) ◼ P&P, Appendices A and C (ISA and microarchitecture of LC-3) ◼ H&H, Appendix B (MIPS instructions) ❑ Programming ◼ P&P, Chapter 6 (we will follow this tomorrow) ❑ **Recommended:** H&H Chapter 5, especially 5.1, 5.2, 5.4, 5.5 ◼ This week ❑ Introduction to microarchitecture and single-cycle microarchitecture ◼ H&H, Chapter 7.1-7.3 ◼ P&P, Appendices A and C ❑ Multi-cycle microarchitecture ◼ H&H, Chapter 7.4 ◼P&P, Appendices A and C

Instruction (Processing) Cycle

### Recall: The Instruction (Processing) Cycle

![](_page_6_Picture_1.jpeg)

## Recall: Control of the Instruction Cycle

![](_page_7_Diagram_1.jpeg)

◼ State 1 ❑ The FSM asserts GatePC and LD.MAR ❑ It selects input (+1) in PCMUX and asserts LD.PC ◼ State 2 ❑ MDR is loaded with the instruction ◼ State 3 ❑ The FSM asserts GateMDR and LD.IR ◼ State 4 ❑ The FSM goes to next state depending on opcode ◼ State 63 ❑ JMP loads register into PC ◼ Full state diagram in Patt&Pattel, Appendix C

## Recall: Full State Machine for LC-3b

![](_page_8_Diagram_1.jpeg)

## Recall: LC-3: A von Neumann Machine

![](_page_9_Diagram_1.jpeg)

# LC-3 and MIPS Instruction Set Architectures

# Instructions (Opcodes)

# Data Types

# Addressing Modes

# Operate Instructions

# Data Movement Instructions and Addressing Modes

# Control Flow Instructions

Conditional Control Flow (Conditional Branching)

### There Is A Lot More to Cover on ISAs

![](_page_18_Picture_1.jpeg)

# Bigger Picture: Program Execution

#### **How Do We Compile & Run an Application?**

![](_page_20_Diagram_1.jpeg)

#### **What is Stored in Memory?**

#### **Instructions (also called text)**

#### **Data**

▪ Global/static: allocated before program begins ▪Dynamic: allocated within program

#### **How big is memory (in MIPS ISA)?**

▪ At most 2<sup>32</sup> = 4 gigabytes (4 GB) ▪From address 0x00000000 to 0xFFFFFFFF

#### **The MIPS Memory Map**

![](_page_22_Diagram_0.jpeg)

**H&H Chapter 6.6**

#### **Example Program: C Code**

**int** f, g, y; // global variables **int** main(void) { f = 2; g = 3; y = sum(f, g); **return** y; } **int** sum(int a, int b) { **return** (a + b); }

#### **Example Program: Assembly Code**

**int** f, g, y; // global **int** main(void) { f = 2; g = 3; y = sum(f, g); **return** y; } **int** sum(**int** a, **int** b) { **return** (a + b); }

.data f: g: y: .text main: **addi** \$sp, \$sp, -4 # stack **sw** \$ra, 0(\$sp) # store \$ra **addi** \$a0, \$0, 2 # \$a0 = 2 **sw** \$a0, f # f = 2 **addi** \$a1, \$0, 3 # \$a1 = 3 **sw** \$a1, g # g = 3 **jal** sum # call sum **sw** \$v0, y # y = sum() **lw** \$ra, 0(\$sp) # rest. \$ra **addi** \$sp, \$sp, 4 # rest. \$sp **jr** \$ra # return sum: **add** \$v0, \$a0, \$a1 # \$v0= a+b **jr** \$ra # return

#### **Example Program: Symbol Table**

| Symbol | Address    |
|--------|------------|
| f      | 0x10000000 |
| g      | 0x10000004 |
| y      | 0x10000008 |
| main   | 0x00400000 |
| sum    | 0x0040002C |

#### **Example Program: Executable**

| Executable file header Text Size | Data Size      |
|----------------------------------|----------------|
| Address                          | Instruction    |
| Address                          | Data           |
| 0x34 (52 bytes)                  | 0xC (12 bytes) |

addi \$sp, \$sp, -4 sw \$ra, 0 (\$sp) addi \$a0, \$0, 2 sw \$a0, 0x8000 (\$gp) addi \$a1, \$0, 3 sw \$a1, 0x8004 (\$gp) jal 0x0040002C sw \$v0, 0x8008 (\$gp) lw \$ra, 0 (\$sp) addi \$sp, \$sp, -4 jr \$ra add \$v0, \$a0, \$a1 jr \$ra

#### **Example Program: In Memory**

![](_page_27_Diagram_1.jpeg)

![](_page_27_Figure_2.jpeg)

### Extra Lecture on Assembly Programming

![](_page_28_Picture_1.jpeg)

![](_page_28_Picture_7.jpeg)

### Extra Lecture on Assembly Programming

# Some More on ISA Tradeoffs

#### Complex vs. Simple Instructions+Data Types

◼ Complex instruction: An instruction does a lot of work, e.g. many operations ❑ Insert in a doubly linked list ❑ Compute FFT ❑ String copy ❑ Matrix multiply ❑ … ◼ Simple instruction: An instruction does little work -- it is a primitive using which complex operations can be built ❑ Add ❑ XOR ❑ Multiply ❑ …

Harder mapping of HLL to ISA **More work for software designer Less work for hardware designer** Optimization burden on SW

### Recall: Semantic Gap

◼ How close instructions & data types & addressing modes are to high-level language (HLL)

![](_page_32_Diagram_2.jpeg)

HW

Control

Signals

![](_page_32_Diagram_3.jpeg)

Easier mapping of HLL to ISA **Less work for software designer More work for hardware designer** Optimization burden on HW

#### How to Change the Semantic Gap Tradeoffs

◼Translate from one ISA into a different "implementation" ISA

![](_page_33_Diagram_2.jpeg)

## An Example: Rosetta 2 Binary Translator

![](_page_34_Picture_4.jpeg)

### An Example: Rosetta 2 Binary Translator

![](_page_35_Picture_1.jpeg)

Apple M1, 2021

#### Another Example: Intel and AMD Processors

![](_page_36_Diagram_1.jpeg)

#### Another Example: Intel and AMD Processors

![](_page_37_Figure_1.jpeg)

Intel Alder Lake, 2021

#### Another Example: Intel and AMD Processors

![](_page_38_Picture_1.jpeg)

AMD Ryzen 5000, 2020

Core Count: 8 cores/16 threads

L1 Caches: 32 KB per core

#### L2 Caches:

512 KB per core

#### L3 Cache:

32 MB shared

## Another Example: NVIDIA Denver

![](_page_39_Diagram_1.jpeg)

### Another Example: NVIDIA Denver

![](_page_40_Picture_4.jpeg)

![](_page_40_Diagram_5.jpeg)

### Transmeta: x86 to VLIW Translation

Klaiber, "The Technology Behind Crusoe Processors," Transmeta White Paper 2000.

![](_page_41_Diagram_1.jpeg)

![](_page_41_Picture_2.jpeg)

### Principle: Indirection

◼ "Any problem in computer science can be solved with another level of indirection." ❑ David Wheeler ❑ Attributed in Butler Lampson's "Principles for Computer Systems Design" <https://arxiv.org/pdf/2011.02455> ◼ Tradeoffs can change and new opportunities become enabled once you add a level of indirection ◼ But indirection comes with extra complexity and latency ◼We will see this again when we discuss Virtual Memory

### ISA-level Tradeoffs: Number of Registers

◼ Affects: ❑ Number of bits used for encoding register address ❑ Number of values kept in fast storage (register file) ❑ (uarch) Size, access time, power consumption of register file ◼ Large number of registers: + Enables better register allocation (and optimizations) by compiler → fewer saves/restores -- Larger instruction size -- Larger register file size ◼We already saw this tradeoff: LC-3 vs MIPS

### There Is A Lot More to Cover on ISAs

![](_page_44_Picture_1.jpeg)

### There Is A Lot More to Cover on ISAs

![](_page_45_Figure_1.jpeg)

#### Detailed Lectures on ISAs & ISA Tradeoffs

◼ Computer Architecture, Spring 2015, Lecture 3 ❑ ISA Tradeoffs (CMU, Spring 2015) [❑](https://www.youtube.com/watch?v=KDy632z23UE&list=PL5Q2soXY2Zi9xidyIgBxUz7xRPS-wisBN&index=8) [https://www.youtube.com/watch?v=QKdiZSfwg](https://www.youtube.com/watch?v=KDy632z23UE&list=PL5Q2soXY2Zi9xidyIgBxUz7xRPS-wisBN&index=8)[g&list=PL5PHm2jkkXmi5CxxI7b3JCL1TWybTDtKq&index=3](https://www.youtube.com/watch?v=KDy632z23UE&list=PL5Q2soXY2Zi9xidyIgBxUz7xRPS-wisBN&index=8) ◼ Computer Architecture, Spring 2015, Lecture 4 ❑ ISA Tradeoffs & MIPS ISA (CMU, Spring 2015) [❑](https://www.youtube.com/watch?v=pwRw7QqK_qA&list=PL5Q2soXY2Zi9xidyIgBxUz7xRPS-wisBN&index=9) [https://www.youtube.com/watch?v=RBgeCCW5Hjs&list=PL5PHm2jkkXmi5CxxI7b3J](https://www.youtube.com/watch?v=pwRw7QqK_qA&list=PL5Q2soXY2Zi9xidyIgBxUz7xRPS-wisBN&index=9) [CL1TWybTDtKq&index=4](https://www.youtube.com/watch?v=pwRw7QqK_qA&list=PL5Q2soXY2Zi9xidyIgBxUz7xRPS-wisBN&index=9) ◼ Computer Architecture, Spring 2015, Lecture 2 ❑ Fundamental Concepts and ISA (CMU, Spring 2015) [❑](https://www.youtube.com/watch?v=gR7XR-Eepcg&list=PL5Q2soXY2Zi9xidyIgBxUz7xRPS-wisBN&index=10) [https://www.youtube.com/watch?v=NpC39uS4K4o&list=PL5PHm2jkkXmi5CxxI7b3J](https://www.youtube.com/watch?v=gR7XR-Eepcg&list=PL5Q2soXY2Zi9xidyIgBxUz7xRPS-wisBN&index=10) [CL1TWybTDtKq&index=2](https://www.youtube.com/watch?v=gR7XR-Eepcg&list=PL5Q2soXY2Zi9xidyIgBxUz7xRPS-wisBN&index=10) 

ISA Design and Tradeoffs: More Critical Thinking

### The Von Neumann Model/Architecture

#### **Stored program**

#### **Sequential instruction processing**

#### The von Neumann Model/Architecture

◼ Von Neumann model is also called stored program computer (instructions in memory). It has two key properties: ◼ Stored program ❑ Instructions stored in a linear memory array ❑ Memory is unified between instructions and data ◼ The interpretation of a stored value depends on the control signals ◼ Sequential instruction processing When is a value interpreted as an instruction?

### Recall: The Instruction Cycle

![](_page_50_Diagram_1.jpeg)

Whether a value fetched from memory is interpreted as an instruction depends on **when** that value is **fetched** in the instruction processing cycle.

### The von Neumann Model/Architecture

◼ Von Neumann model is also called stored program computer (instructions in memory). It has two key properties: ◼ Stored program ❑ Instructions stored in a linear memory array ❑ Memory is unified between instructions and data ◼ The interpretation of a stored value depends on the control signals ◼ Sequential instruction processing ❑ One instruction processed (fetched, executed, completed) at a time ❑ Program counter (instruction pointer) identifies the current instruction ❑ Program counter is advanced sequentially except for control transfer instructions When is a value interpreted as an instruction?

### The von Neumann Model/Architecture

◼ Recommended reading ❑ Burks, Goldstein, von Neumann, "Preliminary discussion of the logical design of an electronic computing instrument, " 1946. ◼ Important reading ❑ Patt and Patel book, Chapter 4, "The von Neumann Model" ◼ **Stored program** ◼**Sequential instruction processing**

### The Von Neumann Model (of a Computer)

![](_page_53_Diagram_1.jpeg)

◼ Q: Is this the only way that a computer can process computer programs?

![](_page_54_Picture_3.jpeg)

◼ A: No. ◼ Qualified Answer: No. But, it has been the dominant way ❑ i.e., the dominant paradigm for computing ❑ for N decades

### The Von Neumann Model (of a Computer)

# The Dataflow Execution Model of a Computer

#### The Dataflow Model (of a Computer)

◼ Von Neumann model: An instruction is fetched and executed in control flow order ❑ As specified by the program counter (instruction pointer) ❑ Sequential unless explicit control flow instruction ◼ Dataflow model: An instruction is fetched and executed in data flow order ❑ i.e., when its operands are ready ❑ i.e., there is no program counter (instruction pointer) ❑ Instruction ordering specified by data flow dependence ◼ Each instruction specifies "who" should receive the result ◼ An instruction can "fire" whenever all operands are received ❑ Potentially many instructions can execute at the same time ◼Inherently more parallel

### Von Neumann vs. Dataflow

◼ Consider a Von Neumann program ❑ What is the significance of the program order? ❑ What is the significance of the storage locations?

**v = a + b; w = b \* 2; x = v - w y = v + w z = x \* y**

![](_page_57_Diagram_2.jpeg)

**Sequential**

**a, b** are the only inputs **z** is the only output

#### More on Dataflow

◼ In a dataflow machine, a program consists of dataflow nodes ❑ A dataflow node fires (fetched and executed) when all it inputs are ready ◼ i.e. when all inputs have tokens ◼Dataflow node and its ISA representation

![](_page_58_Diagram_2.jpeg)

### Example Dataflow Nodes

![](_page_59_Diagram_1.jpeg)

## A Simple Example Dataflow Program

![](_page_60_Diagram_1.jpeg)

**N is a non-negative integer**

**What is the value of OUT?**

#### ISA-level Tradeoff: Program Counter

◼ Do we want a Program Counter (PC or IP) in the ISA? ❑ Yes: Control-driven, sequential execution ◼ An instruction is executed when the PC points to it ◼ PC automatically changes sequentially (except for control flow instructions) → sequential ❑ No: Data-driven, parallel execution ◼ An instruction is executed when all its operand values are available → dataflow ◼ Tradeoffs: MANY high-level ones ❑ Ease of programming (for average programmers)? ❑ Ease of compilation? ❑ Performance: Extraction of parallelism? ❑ Hardware complexity?

### ISA vs. Microarchitecture Level Tradeoff

◼ A similar tradeoff (control vs. data-driven execution) can be made at the microarchitecture level ◼ ISA: Specifies how the **programmer sees** the instructions to be executed ❑ Programmer sees a sequential, control-flow execution order vs. ❑ Programmer sees a dataflow execution order ◼ Microarchitecture: How the **underlying implementation actually executes** instructions ❑ Microarchitecture can execute instructions in any order as long as it obeys the semantics specified by the ISA when making the instruction results visible to software ◼Programmer should see the order specified by the ISA

#### Let's Get Back to the von Neumann Model

◼ But, if you want to learn more about dataflow… ◼ Dennis and Misunas, "A preliminary architecture for a basic data-flow processor, " ISCA 1974. ◼ Gurd et al., "The Manchester prototype dataflow computer, " CACM 1985. ◼ Some Lecture Videos: [❑](http://www.youtube.com/watch?v=D2uue7izU2c) <http://www.youtube.com/watch?v=D2uue7izU2c> [❑](http://www.ece.cmu.edu/~ece740/f13/lib/exe/fetch.php?media=onur-740-fall13-module5.2.1-dataflow-part1.ppt) [http://www.ece.cmu.edu/~ece740/f13/lib/exe/fetch.php?medi](http://www.ece.cmu.edu/~ece740/f13/lib/exe/fetch.php?media=onur-740-fall13-module5.2.1-dataflow-part1.ppt) [a=onur-740-fall13-module5.2.1-dataflow-part1.ppt](http://www.ece.cmu.edu/~ece740/f13/lib/exe/fetch.php?media=onur-740-fall13-module5.2.1-dataflow-part1.ppt)

## Lecture Video on Dataflow Architectures

### The von Neumann Model

◼ All major instruction set architectures today use this model ❑ x86, ARM, MIPS, SPARC, Alpha, POWER, RISC-V, … ◼ Underneath (at the microarchitecture level), the execution model of almost all implementations (or, microarchitectures) is very different ❑ Pipelined instruction execution: Intel 80486 uarch ❑ Multiple instructions at a time: Intel Pentium uarch ❑ Out-of-order execution: Intel Pentium Pro uarch ❑ Separate instruction and data caches ◼ But, what happens underneath that is **not consistent** with the von Neumann model is **not exposed** to software ❑ Difference between ISA and microarchitecture

### What is Computer Architecture?

◼ **ISA+implementation definition:** The science and art of designing, selecting, and interconnecting hardware components and designing the hardware/software interface to create a computing system that meets functional, performance, energy consumption, cost, and other specific goals. ◼ **Traditional (ISA-only) definition:** "The term architecture is used here to describe the attributes of a system as seen by the programmer, i.e., the conceptual structure and functional behavior **as distinct from** the organization of the dataflow and controls, the logic design, and the physical implementation." Gene Amdahl, IBM Journal of R&D, April 1964

### ISA vs. Microarchitecture

#### ◼

 ISA ❑ Agreed upon interface between software and hardware ◼ SW/compiler assumes, HW promises ❑ What the software writer needs to know to write and debug system/user programs Microarchitecture ❑ Specific implementation of an ISA ❑ Not visible to the software Microprocessor ❑ **ISA, uarch**, circuits ❑ "Architecture" = ISA + microarchitecture

#### ◼

#### ◼

Microarchitecture

ISA

Program

Algorithm

Problem

Circuits

Electrons

### Microarchitecture

◼ A specific **implementation** of the ISA ◼ How do we implement the ISA? ❑ We will discuss this for many lectures ◼ There can be many implementations of the same ISA ❑ **MIPS** R2000, R3000, R4000, R6000, R8000, R10000, … ❑ **x86**: Intel 80486, Pentium, Pentium Pro, Pentium 4, Kaby Lake, Coffee Lake, Comet Lake, Ice Lake, Golden Cove, Sapphire Rapids, …, AMD K5, K7, K9, Bulldozer, BobCat, Ryzen X, … ❑ **POWER** 4, 5, 6, 7, 8, 9, 10 (IBM), …, **PowerPC** 604, 605, 620, … ❑ **ARM** Cortex-M\*, ARM Cortex-A\*, NVIDIA Denver, Apple A\*, M1, … ❑ **Alpha** 21064, 21164, 21264, 21364, … ❑ **RISC-V** … ❑ **z/Architecture** … ❑ … 69

### ISA vs. Microarchitecture

![](_page_69_Picture_1.jpeg)

◼ What is part of ISA vs. Uarch? ❑ Gas pedal: interface for "acceleration" ❑ Internals of the engine: implement "acceleration" ◼ Implementation (uarch) can be various as long as it satisfies the specification (ISA) ❑ Add instruction vs. Adder implementation ◼ Bit serial, ripple carry, carry lookahead adders are all part of microarchitecture **(see H&H Chapter 5.2.1)** ❑ x86 ISA has many implementations: ◼ Intel 80486, Pentium, Pentium Pro, Pentium 4, Kaby Lake, Coffee Lake, Comet Lake, Ice Lake, Golden Cover, Sapphire Rapids, …, AMD K5, K7, K9, Bulldozer, BobCat, Ryzen X, … ◼ Microarchitecture usually changes faster than ISA ❑ Few ISAs (x86, ARM, SPARC, MIPS, Alpha, RISC-V) but many uarchs ❑ Why?

### ISA: What Does It Specify?

◼ Instructions ❑ Opcodes, Addressing Modes, Data Types ❑ Instruction Types and Formats ❑ Registers, Condition Codes ◼ Memory ❑ Address space, Addressability, Alignment ❑ Virtual memory management ◼ Call, Interrupt/Exception Handling ◼ Access Control, Priority/Privilege ◼ I/O: memory-mapped vs. instructions ◼ Task/thread Management ◼ Power & Thermal Management ◼ Multithreading & Multiprocessor support ◼…

## ISAs Keep Getting Extended

### ISAs Keep Getting Extended

## ISA Manuals: Some Good Bedtime Reading

## ISA Manuals: Some Good Bedtime Reading

### Microarchitecture

◼ Implementation of the ISA under specific design constraints and goals ◼ Anything done in hardware without exposure to software ❑ Pipelining ❑ In-order versus out-of-order instruction execution ❑ Memory access scheduling policy ❑ Speculative execution ❑ Superscalar processing (multiple instruction issue?) ❑ Clock gating ❑ Caching? Levels, size, associativity, replacement policy ❑ Prefetching? ❑ Voltage/frequency scaling? ❑ Error correction?

#### Property of ISA vs. Uarch?

◼ ADD instruction's opcode ◼ Type of adder used in the ALU (Bit-serial vs. Ripple-carry) ◼ Number of general purpose registers ◼ Number of cycles to execute the MUL instruction ◼ Number of ports to the register file ◼ Whether or not the machine employs pipelined instruction execution ◼ Program counter ◼ Remember ❑ Microarchitecture: Implementation of the ISA under specific design constraints and goals

#### Design Point

◼ A set of design considerations and their importance ❑ leads to tradeoffs in both ISA and uarch ◼ Example considerations: ❑ Cost ❑ Performance ❑ Maximum power consumption, thermal ❑ Energy consumption (battery life) ❑ Availability ❑ Reliability and Correctness ❑ Time to Market ❑ Security, safety, predictability, … ◼ Design point is determined by the "Problem" space (application space), the intended users/market Microarchitecture ISA Program Algorithm Problem Circuits Electrons

![](_page_77_Diagram_2.jpeg)

## Application Space

#### **Dream, and they will appear…**

Patt, "Requirements, bottlenecks, and good fortune: agents for microprocessor evolution," Proc. of the IEEE 2001.

**Many other workloads:**

**Genome analysis Machine learning Robotics Web search Graph analytics**

**…**

### Increasingly Demanding Applications

# Dream

and, they will come

As applications push boundaries, computing platforms will become increasingly strained.

## Tradeoffs: Soul of Computer Architecture

◼ ISA-level tradeoffs ◼ Microarchitecture-level tradeoffs ◼ System and Task-level tradeoffs ❑ How to divide the labor between hardware and software ◼ Computer architecture is the science and art of making the appropriate trade-offs to meet a design point ❑ Why **art**?

### Why Is It (Somewhat) Art?

![](_page_81_Diagram_1.jpeg)

◼We do not (fully) know the future (applications, users, market)

New demands from the top (Look Up)

New issues and capabilities at the bottom (Look Down)

### Why Is It (Somewhat) Art?

![](_page_82_Diagram_1.jpeg)

◼And, the future is not constant (it changes)!

Changing demands at the top (Look Up and Forward)

Changing issues and capabilities at the bottom (Look Down and Forward) Changing demands and personalities of users (Look Up and Forward)

### Analogue from Macro-Architecture

◼ Future is not constant in macro-architecture, either ◼ Example: Can a mill be later used as a theater + restaurant + conference room?

### Mühle Tiefenbrunnen in Zurich

◼ Originally built as a brewery in 1889 ❑ part of it was converted into a mill in 1913 ❑ and the other part into a cold store ◼ Today is a center for a variety of activities: theater, conferences, restaurants, shops, museum…

![](_page_84_Picture_2.jpeg)

![](_page_84_Picture_3.jpeg)

Brewery in 1900

## Another Example in Zurich (I)

![](_page_85_Picture_1.jpeg)

## Another Example in Zurich (II)

![](_page_86_Picture_1.jpeg)

![](_page_87_Picture_0.jpeg)

By Roland zh (Own work) [CC BY-SA 3.0 ([https://creativecommons.org/licenses/by-sa/3.0\)\]](https://creativecommons.org/licenses/by-sa/3.0)), via Wikimedia Commons

## Yet Another Example from Pittsburgh (I)

![](_page_88_Picture_1.jpeg)

## Yet Another Example from Pittsburgh (II)

![](_page_89_Picture_1.jpeg)

### Extra Lecture on Assembly Programming

![](_page_90_Picture_1.jpeg)

![](_page_90_Picture_7.jpeg)

### Extra Lecture on Assembly Programming

## **Digital Design & Computer Arch.**

Lecture 9a: ISA & Microarchitecture

Prof. Onur Mutlu

ETH Zürich

Spring 2026

19 March 2026

# Additional Slides

#### **How Do We Compile & Run an Application?**

![](_page_94_Diagram_1.jpeg)

#### **What needs to be stored in memory?**

#### **Instructions (also called text)**

#### **Data**

▪ Global/static: allocated before program begins ▪Dynamic: allocated within program

#### **How big is memory?**

▪ At most 2<sup>32</sup> = 4 gigabytes (4 GB) ▪From address 0x00000000 to 0xFFFFFFFF

#### **The MIPS Memory Map**

![](_page_96_Diagram_0.jpeg)

**H&H Chapter 6.6**

#### **Example Program: C Code**

**int** f, g, y; // global variables **int** main(void) { f = 2; g = 3; y = sum(f, g); **return** y; } **int** sum(int a, int b) { **return** (a + b); }

#### **Example Program: Assembly Code**

**int** f, g, y; // global **int** main(void) { f = 2; g = 3; y = sum(f, g); **return** y; } **int** sum(**int** a, **int** b) { **return** (a + b); }

.data f: g: y: .text main: **addi** \$sp, \$sp, -4 # stack **sw** \$ra, 0(\$sp) # store \$ra **addi** \$a0, \$0, 2 # \$a0 = 2 **sw** \$a0, f # f = 2 **addi** \$a1, \$0, 3 # \$a1 = 3 **sw** \$a1, g # g = 3 **jal** sum # call sum **sw** \$v0, y # y = sum() **lw** \$ra, 0(\$sp) # rest. \$ra **addi** \$sp, \$sp, 4 # rest. \$sp **jr** \$ra # return sum: **add** \$v0, \$a0, \$a1 # \$v0= a+b **jr** \$ra # return

#### **Example Program: Symbol Table**

| Symbol | Address    |
|--------|------------|
| f      | 0x10000000 |
| g      | 0x10000004 |
| y      | 0x10000008 |
| main   | 0x00400000 |
| sum    | 0x0040002C |

#### **Example Program: Executable**

| Executable file header Text Size | Data Size      |
|----------------------------------|----------------|
| Address                          | Instruction    |
| Address                          | Data           |
| 0x34 (52 bytes)                  | 0xC (12 bytes) |

addi \$sp, \$sp, -4 sw \$ra, 0 (\$sp) addi \$a0, \$0, 2 sw \$a0, 0x8000 (\$gp) addi \$a1, \$0, 3 sw \$a1, 0x8004 (\$gp) jal 0x0040002C sw \$v0, 0x8008 (\$gp) lw \$ra, 0 (\$sp) addi \$sp, \$sp, -4 jr \$ra add \$v0, \$a0, \$a1 jr \$ra

#### **Example Program: In Memory**

![](_page_101_Diagram_1.jpeg)

![](_page_101_Figure_2.jpeg)