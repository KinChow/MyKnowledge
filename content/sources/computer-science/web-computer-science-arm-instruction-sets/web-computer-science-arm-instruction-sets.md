---
archive_policy: text-only
attachments:
- filename: web-computer-science-arm-instruction-sets.txt
  kind: document
  media_type: text/plain
  role: original
  sha256: sha256:6a9a0c53c3c09fbfefdbdf3e87d25b8e30c6540a98742729d9e8f79da65a46a2
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-c6331b5d1245
  position:
    end: 263
    start: 0
    type: TextPositionSelector
  selector:
    exact: ARM (stylised in lowercase as arm) is a family of RISC instruction set
      architectures for computer processors. Arm Holdings develops the instruction
      set architecture and licenses them to other companies, who build the physical
      devices that use the instruction set.
    prefix: ''
    suffix: ' It also designs and licenses co'
    type: TextQuoteSelector
  snapshot_sha256: sha256:6a9a0c53c3c09fbfefdbdf3e87d25b8e30c6540a98742729d9e8f79da65a46a2
- evidence_id: evidence-58dcc8093664
  position:
    end: 700
    start: 352
    type: TextPositionSelector
  selector:
    exact: The ARM architecture is a load–store architecture. Uniform 16 × 32-bit
      register file (including the program counter, stack pointer and the link register).
      Fixed instruction width of 32 bits to ease decoding and pipelining, at the cost
      of decreased code density. Later, the Thumb instruction set added 16-bit instructions
      and increased code density.
    prefix: 'instruction set architectures.


      '
    suffix: ' Mostly single clock-cycle execu'
    type: TextQuoteSelector
  snapshot_sha256: sha256:6a9a0c53c3c09fbfefdbdf3e87d25b8e30c6540a98742729d9e8f79da65a46a2
- evidence_id: evidence-e8d2d7132c1c
  position:
    end: 1038
    start: 739
    type: TextPositionSelector
  selector:
    exact: To improve compiled code density, processors since the ARM7TDMI (released
      in 1994) have featured the Thumb compressed instruction set, which have their
      own state. When in this state, the processor executes the Thumb instruction
      set, a compact 16-bit encoding for a subset of the ARM instruction set.
    prefix: ' single clock-cycle execution.


      '
    suffix: ' Most of the Thumb instructions '
    type: TextQuoteSelector
  snapshot_sha256: sha256:6a9a0c53c3c09fbfefdbdf3e87d25b8e30c6540a98742729d9e8f79da65a46a2
extractor: utf8/1
id: web-computer-science-arm-instruction-sets
local:
  file_sha256: sha256:6a9a0c53c3c09fbfefdbdf3e87d25b8e30c6540a98742729d9e8f79da65a46a2
  path_ref: local-sidecar:public/web-computer-science-arm-instruction-sets
media_type: text/plain
origin: external
raw_ref:
  path: archive/raw/6a9a0c53c3c09fbfefdbdf3e87d25b8e30c6540a98742729d9e8f79da65a46a2.txt
read_status: retrieved
retrieval:
  acquisition: local-file
schema_version: source/v1
snapshot_sha256: sha256:6a9a0c53c3c09fbfefdbdf3e87d25b8e30c6540a98742729d9e8f79da65a46a2
source_type: local-file
vault_id: public
---
ARM (stylised in lowercase as arm) is a family of RISC instruction set architectures for computer processors. Arm Holdings develops the instruction set architecture and licenses them to other companies, who build the physical devices that use the instruction set. It also designs and licenses cores that implement these instruction set architectures.

The ARM architecture is a load–store architecture. Uniform 16 × 32-bit register file (including the program counter, stack pointer and the link register). Fixed instruction width of 32 bits to ease decoding and pipelining, at the cost of decreased code density. Later, the Thumb instruction set added 16-bit instructions and increased code density. Mostly single clock-cycle execution.

To improve compiled code density, processors since the ARM7TDMI (released in 1994) have featured the Thumb compressed instruction set, which have their own state. When in this state, the processor executes the Thumb instruction set, a compact 16-bit encoding for a subset of the ARM instruction set. Most of the Thumb instructions are directly mapped to normal ARM instructions. The space saving comes from making some of the instruction operands implicit and limiting the number of possibilities compared to the ARM instructions executed in the ARM instruction set state.

Branching in the ARM architecture uses condition code, compare and branch instructions.
