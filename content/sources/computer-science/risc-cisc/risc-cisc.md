---
archive_policy: text-only
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-2339f6e0de43
  position:
    end: 235
    start: 101
    type: TextPositionSelector
  quote_sha256: sha256:1f4848b39e1e498c1cdf250e258526782dd8593adbb392f0f8cd14dd3bd9d5a8
  selector:
    exact: '- RISC uses a small set of simple, fixed-length instructions and follows
      a load/store approach, enabling efficient and fast execution.'
    prefix: 'nstruction handling strategies.

      '
    suffix: '

      - CISC uses a larger set of com'
    type: TextQuoteSelector
  selector_sha256: sha256:72f999df7bed14b21cd0827815461678982d57caed599fbe191b1179e9a43dca
  snapshot_sha256: sha256:ce9e46de2805ccea541a0684c3954f94a13e7e1cd11751dc4c921202350a7fd7
- evidence_id: evidence-a1d5f1e8c5ff
  position:
    end: 378
    start: 236
    type: TextPositionSelector
  quote_sha256: sha256:428c6ad66ff67650e2d9f703a79c75181274fdacffe97db02764ce15223ba6ca
  selector:
    exact: '- CISC uses a larger set of complex, variable-length instructions that
      can perform multiple operations, often requiring multiple clock cycles.'
    prefix: 'g efficient and fast execution.

      '
    suffix: '

      Reduced Instruction Set Archite'
    type: TextQuoteSelector
  selector_sha256: sha256:3a2a7ee4faa6f223a1b7b2e8cdc7f6f897adcfdfd6430f22ca115788ade73c9c
  snapshot_sha256: sha256:ce9e46de2805ccea541a0684c3954f94a13e7e1cd11751dc4c921202350a7fd7
extractor: trafilatura/2.2.0
id: risc-cisc
media_type: text/html
origin: external
read_status: retrieved
retrieval:
  acquisition: fetch
  resolved_url: https://www.geeksforgeeks.org/computer-organization-architecture/computer-organization-risc-and-cisc/
  url: https://www.geeksforgeeks.org/computer-organization-architecture/computer-organization-risc-and-cisc/
schema_version: source/v1
snapshot_sha256: sha256:ce9e46de2805ccea541a0684c3954f94a13e7e1cd11751dc4c921202350a7fd7
source_type: doc
vault_id: public
---
RISC and CISC are two approaches to processor design with different instruction handling strategies.
- RISC uses a small set of simple, fixed-length instructions and follows a load/store approach, enabling efficient and fast execution.
- CISC uses a larger set of complex, variable-length instructions that can perform multiple operations, often requiring multiple clock cycles.
Reduced Instruction Set Architecture (RISC)
RISC simplifies processor design by using a small, uniform set of instructions. Each instruction performs a basic operation (e.g., load, compute, store) and is designed to execute in a single clock cycle, enabling efficient pipelining and simpler hardware.
Characteristics of RISC
- Simpler instruction, hence simple instruction decoding.
- Instruction comes in the form of one word.
- An instruction takes a single clock cycle to get executed.
- More general-purpose registers for register-to-register operations.
- Simple Addressing Modes.
- Optimized for pipelining due to uniform instruction size and simplicity.
Complex Instruction Set Architecture (CISC)
CISC reduces the number of instructions a program needs by using a large set of complex, variable-length instructions. A single instruction can perform multiple operations (e.g., load, compute, and store), which may take multiple clock cycles.
Characteristics of CISC
- Complex instruction, hence complex instruction decoding.
- Instructions are larger than one-word size.
- Instruction may take more than a single clock cycle to get executed.
- Less number of general-purpose registers as operations get performed in memory itself.
- Complex Addressing Modes.
CPU Performance of RISC and CISC
Both approaches try to increase the CPU performance
- RISC: Reduce the cycles per instruction at the cost of the number of instructions per program.
- CISC: The CISC approach attempts to minimize the number of instructions per program but at the cost of an increase in the number of cycles per instruction.
Earlier when programming was done using assembly language, a need was felt to make instruction do more tasks because programming in assembly was tedious and error-prone due to which CISC architecture evolved but with the uprise of high-level language dependency on assembly reduced RISC architecture prevailed.
Example:
Suppose we have to add two 8-bit numbers:
- CISC approach: There will be a single command or instruction for this like ADD which will perform the task.
- RISC approach: Here programmer will write the first load command to load data in registers then it will use a suitable operator and then it will store the result in the desired location.
So, add operation is divided into parts i.e. load, operate, store due to which RISC programs are longer and require more memory to get stored but require fewer transistors due to less complex command.
Comparison Table
RISC and CISC are two processor designs, here is a comparison table between them: