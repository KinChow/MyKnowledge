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
  quote_sha256: sha256:39152197d9ee61579dc5be988d70065a8f8359136e0a18951b3bc9ae6cce9c14
  selector:
    exact: ARM (stylised in lowercase as arm) is a family of RISC instruction set
      architectures for computer processors. Arm Holdings develops the instruction
      set architecture and licenses them to other companies, who build the physical
      devices that use the instruction set.
    prefix: ''
    suffix: ' It also designs and licenses co'
    type: TextQuoteSelector
  selector_sha256: sha256:5114fda0d5b7b627f4ca0d41680ff395e789655382f46d59dfc983517028d2ba
  snapshot_sha256: sha256:6a9a0c53c3c09fbfefdbdf3e87d25b8e30c6540a98742729d9e8f79da65a46a2
- evidence_id: evidence-58dcc8093664
  position:
    end: 700
    start: 352
    type: TextPositionSelector
  quote_sha256: sha256:16c8117e43439733b07c292cc1bf7cf65d8bd41b2fe4940269fc2c6f1a5aa4b6
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
  selector_sha256: sha256:181fd209d93d043254c04fd2040eab401f29c4a040ea5f1c76b3275ef0145753
  snapshot_sha256: sha256:6a9a0c53c3c09fbfefdbdf3e87d25b8e30c6540a98742729d9e8f79da65a46a2
- evidence_id: evidence-e8d2d7132c1c
  position:
    end: 1038
    start: 739
    type: TextPositionSelector
  quote_sha256: sha256:6f8811e06b2f201b540ca9e94b0c38fe880f1ae8351e2210850e36f502d63008
  selector:
    exact: To improve compiled code density, processors since the ARM7TDMI (released
      in 1994) have featured the Thumb compressed instruction set, which have their
      own state. When in this state, the processor executes the Thumb instruction
      set, a compact 16-bit encoding for a subset of the ARM instruction set.
    prefix: ' single clock-cycle execution.


      '
    suffix: ' Most of the Thumb instructions '
    type: TextQuoteSelector
  selector_sha256: sha256:438d4d1327a276bfee1443e92dda0fe3e0fd2c29aafd72f06a507c8538e4a994
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
  sha256: sha256:6a9a0c53c3c09fbfefdbdf3e87d25b8e30c6540a98742729d9e8f79da65a46a2
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
