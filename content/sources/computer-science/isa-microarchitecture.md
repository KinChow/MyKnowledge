---
archive_policy: text-only
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-cc0375237772
  position:
    end: 507
    start: 358
    type: TextPositionSelector
  quote_sha256: sha256:df438a180a53ca753698241c60389f6e44c76c3f3a5801ef74715cbfe214e0e9
  selector:
    exact: ISA is the language of the CPU that tells it what operations it can perform,
      such as adding numbers, loading data, or jumping to another instruction.
    prefix: 'truction Set Architecture (ISA)

      '
    suffix: "\n It defines how software commun"
    type: TextQuoteSelector
  selector_sha256: sha256:9d21cea39cd2b4935bcd140c098d8f2c4d755aa4a632c62f651413637a349a60
  snapshot_sha256: sha256:3f7d5b603b80e4012d65d109a817d42edad672e2e8548664808843b181e99080
- evidence_id: evidence-2dd3071e634f
  position:
    end: 2317
    start: 2192
    type: TextPositionSelector
  quote_sha256: sha256:2d4cc319aa85fedce3ddd9cf4089fd1aef6f2d3703b24eb538ba74d2849b9b86
  selector:
    exact: ISA defines what a CPU can do, while microarchitecture is how the CPU is
      designed internally to carry out those instructions.
    prefix: 'different microarchitectures.

      - '
    suffix: '

      Importance of ISA

      1. Foundation'
    type: TextQuoteSelector
  selector_sha256: sha256:22a7b95d151c46b99ef4642b0b63e8c0bdf04c62db90919dac5a0f2f8d54007a
  snapshot_sha256: sha256:3f7d5b603b80e4012d65d109a817d42edad672e2e8548664808843b181e99080
extractor: trafilatura/2.2.0
id: isa-microarchitecture
media_type: text/html
origin: external
read_status: retrieved
retrieval:
  acquisition: fetch
  resolved_url: https://www.geeksforgeeks.org/computer-organization-architecture/microarchitecture-and-instruction-set-architecture/
  url: https://www.geeksforgeeks.org/computer-organization-architecture/microarchitecture-and-instruction-set-architecture/
schema_version: source/v1
snapshot_sha256: sha256:3f7d5b603b80e4012d65d109a817d42edad672e2e8548664808843b181e99080
source_type: doc
vault_id: public
---
Microarchitecture and Instruction Set Architecture (ISA) are two fundamental concepts in computer organization. When we use a computer or smartphone, there's a lot going on behind the scenes in the processor (CPU). Two important parts that make everything work are:
- ISA (Instruction Set Architecture)
- Microarchitecture
Instruction Set Architecture (ISA)
ISA is the language of the CPU that tells it what operations it can perform, such as adding numbers, loading data, or jumping to another instruction.
 It defines how software communicates with hardware through specific instruction rules and formats. It includes:
- Instruction types (ADD, LOAD, JUMP), registers, data types, and memory access
- Interrupt handling and system-level communication
Some Popular ISAs are x86 (PCs), ARM (phones), MIPS (education), RISC-V (open source).
Objective of ISA - MIPS ISA
To understand what an ISA aims to do, let’s take MIPS ISA as an example. MIPS is popular in computer science courses because it’s simple and clean.
Types of Instructions
MIPS divides instructions into three main types:
- Arithmetic/Logic Instructions perform basic operations such as ADD, SUB, AND, and OR on data stored in registers.
- Data Transfer Instructions are used to move data between memory and registers; for example, LW (load word) and SW (store word).
- Branch and Jump Instructions control the execution flow of the program, making decisions and handling loops or function calls; examples include BEQ (branch if equal) and J (jump).
Instruction Length
MIPS is a 32-bit ISA, meaning every instruction must be exactly 32 bits (4 bytes) long. This fixed length simplifies the design and makes it more efficient for both hardware and compiler developers.
Instruction Formats
Since all MIPS instructions are 32 bits long, the ISA defines how those 32 bits are organized for different instruction types. MIPS uses three instruction formats:
Microarchitecture vs ISA
Microarchitecture includes components like the ALU for calculations, pipelines for faster processing, cache for quick memory access, the control unit, and execution units.
- Processors with the same ISA, can have very different microarchitectures.
- ISA defines what a CPU can do, while microarchitecture is how the CPU is designed internally to carry out those instructions.
Importance of ISA
1. Foundation of Processor Design
ISA forms the core design element of any processor. Whether it’s RISC (Reduced Instruction Set Computing) or CISC (Complex Instruction Set Computing), the choice of ISA impacts all other design decisions.
2. Instruction Execution Understanding
Computer architecture often focus on instruction execution, pipelining, control unit design, and instruction formats — all of which are defined by the ISA.
3. Enables Assembly Language Programming
Understanding ISA is critical for assembly-level programming. It helps in:
- Writing instruction sequences
- Understanding how data is loaded/stored
- Analyzing program execution time
4. Impact on Performance Metrics
A well-designed ISA can lead to efficient hardware implementation and optimized software execution. ISA affects:
- CPI (Cycles Per Instruction)
- Instruction count
- Execution time
5. Compatibility and Portability
ISA determines software compatibility. If two processors implement the same ISA, they can run the same programs — even if their internal microarchitectures are different.
Types of ISA
There are multiple types of ISA, each designed with different goals in mind, such as simplifying instruction sets for faster execution, supporting complex operations with fewer instructions, or enabling parallel processing to improve performance.