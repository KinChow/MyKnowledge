---
archive_policy: text-only
attachments:
- filename: arm-neon-why-intrinsics.txt
  kind: document
  media_type: text/plain
  role: original
  sha256: sha256:289696a6de76c6d4e11c321bb08efcecd13f759fe4dfa55ce4d08c26002d8c38
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-b972ba96913c
  position:
    end: 580
    start: 40
    type: TextPositionSelector
  quote_sha256: sha256:d0f9966d03562cc590c295273b5a0191fcfcb0f44886324ba85505a5be033ffc
  selector:
    exact: Intrinsics are functions whose precise implementation is known to a compiler.
      The Neon intrinsics are a set of C and C++ functions defined in arm_neon.h which
      are supported by the Arm compilers and GCC. These functions let you use Neon
      without having to write assembly code directly, since the functions themselves
      contain short assembly kernels which are inlined into the calling code. Additionally,
      register allocation and pipeline optimization are handled by the compiler so
      many difficulties faced by the assembly programmer are avoided
    prefix: "use Neon intrinsics?\n \n    \n    "
    suffix: ".  \n     \n     See the Neon Intr"
    type: TextQuoteSelector
  selector_sha256: sha256:e84976b6da32ed87b18c0e7e48b5fb97519412b87e7d4943dc82939144c8cef5
  snapshot_sha256: sha256:289696a6de76c6d4e11c321bb08efcecd13f759fe4dfa55ce4d08c26002d8c38
extractor: utf8/1
id: arm-neon-why-intrinsics
local:
  file_sha256: sha256:289696a6de76c6d4e11c321bb08efcecd13f759fe4dfa55ce4d08c26002d8c38
  path_ref: local-sidecar:public/arm-neon-why-intrinsics
media_type: text/plain
origin: external
raw_ref:
  path: archive/raw/289696a6de76c6d4e11c321bb08efcecd13f759fe4dfa55ce4d08c26002d8c38.txt
  sha256: sha256:289696a6de76c6d4e11c321bb08efcecd13f759fe4dfa55ce4d08c26002d8c38
read_status: retrieved
retrieval:
  acquisition: local-file
schema_version: source/v1
snapshot_sha256: sha256:289696a6de76c6d4e11c321bb08efcecd13f759fe4dfa55ce4d08c26002d8c38
source_type: local-file
vault_id: public
---
### Why use Neon intrinsics?
 
    
    Intrinsics are functions whose precise implementation is known to a compiler. The Neon intrinsics are a set of C and C++ functions defined in arm_neon.h which are supported by the Arm compilers and GCC. These functions let you use Neon without having to write assembly code directly, since the functions themselves contain short assembly kernels which are inlined into the calling code. Additionally, register allocation and pipeline optimization are handled by the compiler so many difficulties faced by the assembly programmer are avoided.  
     
     See the Neon Intrinsics Reference for a list of all the Neon intrinsics. The Neon intrinsics engineering specification is contained in the Arm C Language Extensions (ACLE). 
     Using the Neon intrinsics has a number of benefits: 
      
      Powerful: Intrinsics give the programmer direct access to the Neon instruction set without the need for hand-written assembly code. 
      Portable: Hand-written Neon assembly instructions might need to be rewritten for different target processors. C and C++ code containing Neon intrinsics can be compiled for a new target or a new execution state (for example, migrating from AArch32 to AArch64) with minimal or no code changes. 
      Flexible: The programmer can exploit Neon when needed or use C/C++ when it isn’t needed, while avoiding many low-level engineering concerns. 
      
     However, intrinsics might not be the right choice in all situations: 
      
      There is a steeper learning curve to use Neon intrinsics than importing a library or relying on a compiler. 
      Hand-optimized assembly code might offer the greatest scope for performance improvement even if it is more difficult to write. 
      
     We look at examples where we reimplement some C functions using Neon intrinsics. The examples chosen do not reflect the full complexity of their application, but they illustrate the use of intrinsics and act as a starting point for more complex code.