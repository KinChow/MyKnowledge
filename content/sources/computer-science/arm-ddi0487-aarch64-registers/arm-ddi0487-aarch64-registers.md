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
  quote_sha256: sha256:1f5446f2c31b8f4901e2982492a239cdd099d04771db2f7ea68469c1bc1da357
  selector:
    exact: '31 general-purpose registers, R0 to R30. Each can be accessed as:'
    prefix: 'e visible at EL0 using AArch64:

      '
    suffix: '

      A 64-bit general-purpose regist'
    type: TextQuoteSelector
  selector_sha256: sha256:b9be2e70a8bf621970a8dfe683234288e0b0583c5cb55eba3f8439489dad8874
  snapshot_sha256: sha256:0c1115f2e56a5721746e54218d904b1ded258bbfe6b44c9d8e19094e7dc196f4
- evidence_id: evidence-1061d87ee77e
  position:
    end: 174
    start: 124
    type: TextPositionSelector
  quote_sha256: sha256:874ccbe59a9550fe66ec633b8ebbc6d1ed16d9a5f7180eb7ec5fbdba897beb8d
  selector:
    exact: A 64-bit general-purpose register named X0 to X30.
    prefix: 'o R30. Each can be accessed as:

      '
    suffix: '

      A 32-bit general-purpose regist'
    type: TextQuoteSelector
  selector_sha256: sha256:7f3158896c18dbe34cd4f6173338f0895ce15e11f40a0bfdb50c59d9535afbd8
  snapshot_sha256: sha256:0c1115f2e56a5721746e54218d904b1ded258bbfe6b44c9d8e19094e7dc196f4
- evidence_id: evidence-8c92e4905685
  position:
    end: 225
    start: 175
    type: TextPositionSelector
  quote_sha256: sha256:322510c365f2310196a478ec85c9d84636339dcf4b4e756ece666ea6c679b207
  selector:
    exact: A 32-bit general-purpose register named W0 to W30.
    prefix: 'rpose register named X0 to X30.

      '
    suffix: '

      The X30 general-purpose registe'
    type: TextQuoteSelector
  selector_sha256: sha256:e0b3910cceb720f83f460534306aca46bf751bc3aa3d1edd36c0b86285e6c91e
  snapshot_sha256: sha256:0c1115f2e56a5721746e54218d904b1ded258bbfe6b44c9d8e19094e7dc196f4
- evidence_id: evidence-c1301b51c8bc
  position:
    end: 442
    start: 304
    type: TextPositionSelector
  quote_sha256: sha256:95e5d3f617b6cc0565fea806464dddbe17d56f3ce12329bcddc7984f82ed646e
  selector:
    exact: A 64-bit dedicated Stack Pointer register. The least significant 32 bits
      of the stack pointer can be accessed using the register name WSP.
    prefix: 'e procedure call link register.

      '
    suffix: '

      The use of SP as an operand in '
    type: TextQuoteSelector
  selector_sha256: sha256:baf1f0bcca0e1caf2b06f0fb7e71b0f4b7d94bc3a7be8b9290e4a8b37f6beaaf
  snapshot_sha256: sha256:0c1115f2e56a5721746e54218d904b1ded258bbfe6b44c9d8e19094e7dc196f4
- evidence_id: evidence-6d7187d33635
  position:
    end: 779
    start: 707
    type: TextPositionSelector
  quote_sha256: sha256:fd3dc1fc02ebc8676515aedce8ae6cd3a850e100ca9df1a0476ee385756fa91a
  selector:
    exact: A 64-bit Program Counter holding the address of the current instruction.
    prefix: 'or the Arm 64-bit Architecture.

      '
    suffix: '

      Software cannot write directly '
    type: TextQuoteSelector
  selector_sha256: sha256:e2be07152429a98ae1e4ffc89ceebe8d756e6adfd5faf45c13b73558ca1fbbc0
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