---
archive_policy: text-only
attachments:
- filename: arm-a-profile-architectures.txt
  kind: document
  media_type: text/plain
  role: original
  sha256: sha256:21c2545aafe0b249647c49343242cb9251dd2bbc49bcfb0b582acbb2c78106f5
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-802fb55860c5
  position:
    end: 297
    start: 140
    type: TextPositionSelector
  quote_sha256: sha256:fd0c0134ffbe49ca39a343a58bfb2b16feea85a5ed41d1f305e7e9bb3f954a6a
  selector:
    exact: Nine major versions of the architecture have been defined to date, denoted
      by the version numbers 1 to 9. Of these, the first three versions are now obsolete
    prefix: 'nd Arm continues to develop it. '
    suffix: ". \n  The generic names AArch64 a"
    type: TextQuoteSelector
  selector_sha256: sha256:281cb08579361bd19a52d338e4088a901d92a88170e1f390e81320cc7fe92738
  snapshot_sha256: sha256:21c2545aafe0b249647c49343242cb9251dd2bbc49bcfb0b582acbb2c78106f5
- evidence_id: evidence-3dc4401ba81e
  position:
    end: 643
    start: 426
    type: TextPositionSelector
  quote_sha256: sha256:8332318de5dfc3601fb7e86cbe4a10d162beb67f7300d022ffecfaf0e70a048b
  selector:
    exact: Is the 64-bit Execution state, meaning addresses are held in 64-bit registers,
      and instructions in the base instruction set can use 64-bit registers for their
      processing. AArch64 state supports the A64 instruction set
    prefix: "   \n     AArch64 \n    \n    \n    "
    suffix: ". \n    \n   \n     AArch32 \n    \n "
    type: TextQuoteSelector
  selector_sha256: sha256:1af70610203117ad92a245b7bef6bf3112cf0715a90e1d36272b02b91feec781
  snapshot_sha256: sha256:21c2545aafe0b249647c49343242cb9251dd2bbc49bcfb0b582acbb2c78106f5
extractor: utf8/1
id: arm-a-profile-architectures
local:
  file_sha256: sha256:21c2545aafe0b249647c49343242cb9251dd2bbc49bcfb0b582acbb2c78106f5
  path_ref: local-sidecar:public/arm-a-profile-architectures
media_type: text/plain
origin: external
raw_ref:
  path: archive/raw/21c2545aafe0b249647c49343242cb9251dd2bbc49bcfb0b582acbb2c78106f5.txt
  sha256: sha256:21c2545aafe0b249647c49343242cb9251dd2bbc49bcfb0b582acbb2c78106f5
read_status: retrieved
retrieval:
  acquisition: local-file
schema_version: source/v1
snapshot_sha256: sha256:21c2545aafe0b249647c49343242cb9251dd2bbc49bcfb0b582acbb2c78106f5
source_type: local-file
vault_id: public
---
#### A1.2 Architecture profiles
 
  The Arm architecture has evolved significantly since its introduction, and Arm continues to develop it. Nine major versions of the architecture have been defined to date, denoted by the version numbers 1 to 9. Of these, the first three versions are now obsolete. 
  The generic names AArch64 and AArch32 describe the 64-bit and 32-bit Execution states: 
   
   
     AArch64 
    
    
    Is the 64-bit Execution state, meaning addresses are held in 64-bit registers, and instructions in the base instruction set can use 64-bit registers for their processing. AArch64 state supports the A64 instruction set. 
    
   
     AArch32 
    
    
    Is the 32-bit Execution state, meaning addresses are held in 32-bit registers, and instructions in the base instruction sets use 32-bit registers for their processing. AArch32 state supports the T32 and A32 instruction sets. 
    
   
   
   #### Note
 
   The Base instruction set comprises the supported instructions other than the floating-point instructions. 
   
  See sections Execution state and The instruction sets for more information. 
  Arm defines three architecture profiles: 
   
   
     A 
    
    
    Application profile, described in this Manual: 
     
     Supports a Virtual Memory System Architecture (VMSA) based on a Memory Management Unit (MMU). 
       
       #### Note
 
       An Armv8-A implementation can be called an AArchv8-A implementation and an Armv9-A implementation can be called an AArchv9-A implementation. 
       
     Supports the A64, A32, and T32 instruction sets. 
     
    
   
     R 
    
    
    Real-time profile: 
     
     Supports a Protected Memory System Architecture (PMSA) based on a Memory Protection Unit (MPU). 
     Supports an optional VMSA based on an MMU in the R-profile AArch64 architecture. 
     Supports the A64, or the A32 and T32 instruction sets. 
     
    
   
     M 
    
    
    Microcontroller profile: 
     
     Implements a programmers' model designed for low-latency interrupt processing, with hardware stacking of registers and support for writing interrupt handlers in high-level languages. 
     Supports a PMSA based on an MPU. 
     Supports a variant of the T32 instruction set. 
     
    
   
  This Manual describes only Armv8-A and Armv9-A. For information about the R and M architecture profiles, and earlier Arm architecture versions, see: 
   
   The Arm® Architecture Reference Manual, for Armv8-R AArch64 architecture profile. 
   The Arm® Architecture Reference Manual, for Armv8-R AArch32 architecture profile. 
   The ARM® Architecture Reference Manual ARMv7-A and ARMv7-R edition. 
   The Armv8-M Architecture Reference Manual. 
   The Armv7-M Architecture Reference Manual. 
   The Armv6-M Architecture Reference Manual.