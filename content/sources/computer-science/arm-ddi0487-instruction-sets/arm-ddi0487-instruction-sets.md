---
archive_policy: text-only
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-1bf0681f2918
  position:
    end: 200
    start: 61
    type: TextPositionSelector
  quote_sha256: sha256:1206468cce4ef05897518afd0897c568a0667a36d84a9909e409d5f4e08f464a
  selector:
    exact: AArch64 state supports a single instruction set, called A64. This is a
      fixed-length instruction set that uses 32-bit instruction encodings.
    prefix: ' depend on the Execution state:

      '
    suffix: '

      For information on the A64 inst'
    type: TextQuoteSelector
  selector_sha256: sha256:2732216738e216838d25d5c2dc4c2bb8421a80b2aa4a6ef032a630b40c4496a8
  snapshot_sha256: sha256:ccf816fe505c04568f1a42673f567e9003ac679a45fa433e5432c6ed63c39578
extractor: trafilatura/2.2.0
id: arm-ddi0487-instruction-sets
media_type: text/html
origin: external
read_status: retrieved
retrieval:
  acquisition: fetch
  resolved_url: https://documentation-service.arm.com/documentation/ddi0487/mc/-Part-A-Arm-Architecture-Introduction-and-Overview/-Chapter-A1-Introduction-to-the-Arm-Architecture/-A1-3-Arm-architectural-concepts/-A1-3-2-The-instruction-sets?lang=en&rev=1
  url: https://documentation-service.arm.com/documentation/ddi0487/mc/-Part-A-Arm-Architecture-Introduction-and-Overview/-Chapter-A1-Introduction-to-the-Arm-Architecture/-A1-3-Arm-architectural-concepts/-A1-3-2-The-instruction-sets?lang=en&rev=1
schema_version: source/v1
snapshot_sha256: sha256:ccf816fe505c04568f1a42673f567e9003ac679a45fa433e5432c6ed63c39578
source_type: doc
vault_id: public
---
The possible instruction sets depend on the Execution state:
AArch64 state supports a single instruction set, called A64. This is a fixed-length instruction set that uses 32-bit instruction encodings.
For information on the A64 instruction set, see A64 Instruction Set Overview.
If FEAT_SVE is implemented, the A64 instruction set supports scalable vector instructions. See About the SVE instructions.
If FEAT_SME is implemented, the A64 instruction set supports scalable matrix instructions. See About the SME instructions.
AArch32 state supports the following instruction sets:
This is a variable-length instruction set that uses both 16-bit and 32-bit instruction encodings.
In previous documentation, these instruction sets were called the ARM and Thumb® instruction sets. Armv8 and Armv9 extend each of these instruction sets. In AArch32 state, the Instruction set state determines the instruction set that the PE executes.
For information on the T32 and A32 instruction sets, see The AArch32 Instruction Sets Overview.
The instruction sets support SIMD and scalar floating-point instructions. See Floating-point support.