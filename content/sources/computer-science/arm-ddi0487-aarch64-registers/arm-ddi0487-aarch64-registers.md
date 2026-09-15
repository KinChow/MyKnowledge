---
archive_policy: text-only
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-29cc639ee281
  position:
    end: 123
    start: 58
    type: TextPositionSelector
  selector:
    exact: '31 general-purpose registers, R0 to R30. Each can be accessed as:'
    prefix: 'e visible at EL0 using AArch64:

      '
    suffix: '

      A 64-bit general-purpose regist'
    type: TextQuoteSelector
  snapshot_sha256: sha256:0c1115f2e56a5721746e54218d904b1ded258bbfe6b44c9d8e19094e7dc196f4
- evidence_id: evidence-1061d87ee77e
  position:
    end: 174
    start: 124
    type: TextPositionSelector
  selector:
    exact: A 64-bit general-purpose register named X0 to X30.
    prefix: 'o R30. Each can be accessed as:

      '
    suffix: '

      A 32-bit general-purpose regist'
    type: TextQuoteSelector
  snapshot_sha256: sha256:0c1115f2e56a5721746e54218d904b1ded258bbfe6b44c9d8e19094e7dc196f4
- evidence_id: evidence-8c92e4905685
  position:
    end: 225
    start: 175
    type: TextPositionSelector
  selector:
    exact: A 32-bit general-purpose register named W0 to W30.
    prefix: 'rpose register named X0 to X30.

      '
    suffix: '

      The X30 general-purpose registe'
    type: TextQuoteSelector
  snapshot_sha256: sha256:0c1115f2e56a5721746e54218d904b1ded258bbfe6b44c9d8e19094e7dc196f4
- evidence_id: evidence-c1301b51c8bc
  position:
    end: 442
    start: 304
    type: TextPositionSelector
  selector:
    exact: A 64-bit dedicated Stack Pointer register. The least significant 32 bits
      of the stack pointer can be accessed using the register name WSP.
    prefix: 'e procedure call link register.

      '
    suffix: '

      The use of SP as an operand in '
    type: TextQuoteSelector
  snapshot_sha256: sha256:0c1115f2e56a5721746e54218d904b1ded258bbfe6b44c9d8e19094e7dc196f4
- evidence_id: evidence-6d7187d33635
  position:
    end: 779
    start: 707
    type: TextPositionSelector
  selector:
    exact: A 64-bit Program Counter holding the address of the current instruction.
    prefix: 'or the Arm 64-bit Architecture.

      '
    suffix: '

      Software cannot write directly '
    type: TextQuoteSelector
  snapshot_sha256: sha256:0c1115f2e56a5721746e54218d904b1ded258bbfe6b44c9d8e19094e7dc196f4
extractor: trafilatura/2.2.0
id: arm-ddi0487-aarch64-registers
media_type: text/html
origin: external
read_status: retrieved
retrieval:
  acquisition: fetch
  resolved_url: https://documentation-service.arm.com/documentation/ddi0487/mc/-Part-B-The-AArch64-Application-Level-Architecture/-Chapter-B1-The-AArch64-Application-Level-Programmers--Model/-B1-2-Registers-in-AArch64-Execution-state?lang=en&rev=1
  url: https://documentation-service.arm.com/documentation/ddi0487/mc/-Part-B-The-AArch64-Application-Level-Architecture/-Chapter-B1-The-AArch64-Application-Level-Programmers--Model/-B1-2-Registers-in-AArch64-Execution-state?lang=en&rev=1
schema_version: source/v1
snapshot_sha256: sha256:0c1115f2e56a5721746e54218d904b1ded258bbfe6b44c9d8e19094e7dc196f4
source_type: doc
vault_id: public
---
The following registers are visible at EL0 using AArch64:
31 general-purpose registers, R0 to R30. Each can be accessed as:
A 64-bit general-purpose register named X0 to X30.
A 32-bit general-purpose register named W0 to W30.
The X30 general-purpose register is used as the procedure call link register.
A 64-bit dedicated Stack Pointer register. The least significant 32 bits of the stack pointer can be accessed using the register name WSP.
The use of SP as an operand in an instruction, indicates the use of the current stack pointer.
 
     Note
Stack pointer alignment to a 16-byte boundary is configurable at EL1. For more information, see the Procedure Call Standard for the Arm 64-bit Architecture.
A 64-bit Program Counter holding the address of the current instruction.
Software cannot write directly to the PC. It can be updated only on a branch, exception entry or exception return.
 
     Note
Attempting to execute an A64 instruction that is not word-aligned generates a PC alignment fault, see PC alignment checking.
32 SIMD&FP registers, V0 to V31. Each can be accessed as:
A 128-bit register named Q0 to Q31.
A 64-bit register named D0 to D31.
A 32-bit register named S0 to S31.
A 16-bit register named H0 to H31.
An 8-bit register named B0 to B31.
A 128-bit vector of elements. See Figure A1-1.
A 64-bit vector of elements. See Figure A1-1.
Where the number of bits described by a register name does not occupy an entire SIMD&FP register, it refers to the least significant bits. See Figure B1-2.
For more information about data types and vector formats, see Supported data types.
The FPCR is the floating-point control register. The FPSR is the floating-point status register.
32 SVE scalable vector registers, Z0 to Z31, of equal length. Each register can be accessed as:
A configurable-length vector of elements. The length, VL, is a power of two, from a minimum of 128 bits to an IMPLEMENTATION DEFINED maximum no greater than 2048 bits. See Figure B1-3, Figure A1-5, and Configurable SVE vector lengths.
A SIMD&FP register, as described in V0-V31. Bits[127:0] of each Zn register hold the correspondingly numbered V0-V31 SIMD&FP register, as Figure B1-3 shows:
See also:
16 SVE predicate registers, named P0 to P15. Each SVE predicate register holds one bit for each byte of an SVE scalar vector register.
 
     Note
The Maximum implemented SVE predicate length is the Maximum implemented SVE vector length divided by 8. See Maximum implemented SVE vector lengths.
Also see Vector predication.
The dedicated SVE First Fault Register that has the same size and format as the SVE predicate registers, P0-P15. See FFR, First Fault Register.
Architectural state capable of holding a two-dimensional array of bytes. See ZA storage.
A 512-bit SME2 lookup table register. See SME2 ZT0 register.