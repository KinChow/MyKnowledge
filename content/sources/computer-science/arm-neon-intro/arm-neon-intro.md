---
archive_policy: text-only
attachments:
- filename: arm-neon-intro.txt
  kind: document
  media_type: text/plain
  role: original
  sha256: sha256:33cde106b16f9f0fe18c1e65dd7dea285757d2d415889ddabaccbda40736609c
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-068c54a90cb8
  position:
    end: 359
    start: 29
    type: TextPositionSelector
  quote_sha256: sha256:ee40eeb7c1eb9a35ef7bb0cb5626a2986e6635d1f8beec2d4a1e64d058a8ccdb
  selector:
    exact: "Neon is the implementation of Arm’s Advanced SIMD architecture.  \n     \n
      \    The purpose of Neon is to accelerate data manipulation by providing: \n
      \     \n      Thirty-two 128-bit vector registers, each capable of containing
      multiple lanes of data. \n      SIMD instructions to operate simultaneously
      on those multiple lanes of data"
    prefix: "### What is Neon?\n \n    \n    "
    suffix: ". \n      \n     Applications that"
    type: TextQuoteSelector
  selector_sha256: sha256:3559b7f6327b0723cedb2d28565c7a4de5e2f7e324d54e61a8d576db13ec5ec2
  snapshot_sha256: sha256:33cde106b16f9f0fe18c1e65dd7dea285757d2d415889ddabaccbda40736609c
- evidence_id: evidence-1a3104fe62bf
  position:
    end: 1250
    start: 590
    type: TextPositionSelector
  quote_sha256: sha256:75f831da9d0edbf2c598610452b95594fb9f8f880413e4707227f3fc8b279caa
  selector:
    exact: "As a programmer, there are a number of ways you can make use of Neon technology:
      \n      \n      Neon-enabled open source libraries such as the Arm Compute Library
      provide one of the easiest ways to take advantage of Neon. \n      Auto-vectorization
      features in your compiler can automatically optimize your code to take advantage
      of Neon. \n      Neon intrinsics are function calls that the compiler replaces
      with appropriate Neon instructions. This gives you direct, low-level access
      to the exact Neon instructions you want, all from C, or C++ code. \n      For
      very high performance, hand-coded Neon assembler can be the best approach for
      experienced programmers"
    prefix: " performance is critical. \n     "
    suffix: ". \n      \n     In this guide we "
    type: TextQuoteSelector
  selector_sha256: sha256:d3767b88ade81289253d1061bf8a547ab19b102fe3802ee7c82741a1cb7e5c6e
  snapshot_sha256: sha256:33cde106b16f9f0fe18c1e65dd7dea285757d2d415889ddabaccbda40736609c
extractor: utf8/1
id: arm-neon-intro
local:
  file_sha256: sha256:33cde106b16f9f0fe18c1e65dd7dea285757d2d415889ddabaccbda40736609c
  path_ref: local-sidecar:public/arm-neon-intro
media_type: text/plain
origin: external
raw_ref:
  path: archive/raw/33cde106b16f9f0fe18c1e65dd7dea285757d2d415889ddabaccbda40736609c.txt
  sha256: sha256:33cde106b16f9f0fe18c1e65dd7dea285757d2d415889ddabaccbda40736609c
read_status: retrieved
retrieval:
  acquisition: local-file
schema_version: source/v1
snapshot_sha256: sha256:33cde106b16f9f0fe18c1e65dd7dea285757d2d415889ddabaccbda40736609c
source_type: local-file
vault_id: public
---
### What is Neon?
 
    
    Neon is the implementation of Arm’s Advanced SIMD architecture.  
     
     The purpose of Neon is to accelerate data manipulation by providing: 
      
      Thirty-two 128-bit vector registers, each capable of containing multiple lanes of data. 
      SIMD instructions to operate simultaneously on those multiple lanes of data. 
      
     Applications that can benefit from Neon technology include multimedia and signal processing, 3D graphics, speech, image processing, or other applications where fixed and floating-point performance is critical. 
     As a programmer, there are a number of ways you can make use of Neon technology: 
      
      Neon-enabled open source libraries such as the Arm Compute Library provide one of the easiest ways to take advantage of Neon. 
      Auto-vectorization features in your compiler can automatically optimize your code to take advantage of Neon. 
      Neon intrinsics are function calls that the compiler replaces with appropriate Neon instructions. This gives you direct, low-level access to the exact Neon instructions you want, all from C, or C++ code. 
      For very high performance, hand-coded Neon assembler can be the best approach for experienced programmers. 
      
     In this guide we focus on using the Neon intrinsics for AArch64, but they can also be compiled for AArch32. For more information about AArch32 Neon see Introducing Neon for Armv8-A.