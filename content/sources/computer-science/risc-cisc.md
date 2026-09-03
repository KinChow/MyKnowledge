---
archive_policy: text-only
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-a8d12c44797d
  position:
    end: 235
    start: 103
    type: TextPositionSelector
  quote_sha256: sha256:9009d4667e809100bddf9e166e28e789b7ebaedb882583fdcaed13350198c1a0
  selector:
    exact: RISC uses a small set of simple, fixed-length instructions and follows
      a load/store approach, enabling efficient and fast execution.
    prefix: 'truction handling strategies.

      - '
    suffix: '

      - CISC uses a larger set of com'
    type: TextQuoteSelector
  selector_sha256: sha256:268a636646238a71de72c91d8d6a7b1fbbdd934cfdefcc12a402773128b2e386
  snapshot_sha256: sha256:ce9e46de2805ccea541a0684c3954f94a13e7e1cd11751dc4c921202350a7fd7
- evidence_id: evidence-fc615f4beb99
  position:
    end: 378
    start: 238
    type: TextPositionSelector
  quote_sha256: sha256:c5894a1d9a967dce5b6c71e4685a6a26d2133d2640f941811da4bf781f2653f2
  selector:
    exact: CISC uses a larger set of complex, variable-length instructions that can
      perform multiple operations, often requiring multiple clock cycles.
    prefix: 'efficient and fast execution.

      - '
    suffix: '

      Reduced Instruction Set Archite'
    type: TextQuoteSelector
  selector_sha256: sha256:2ca34414d0921012a6bb99dbb06d919ffd0c5a80da0f663188f96de267a41127
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