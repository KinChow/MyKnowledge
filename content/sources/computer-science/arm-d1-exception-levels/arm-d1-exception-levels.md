---
archive_policy: text-only
attachments:
- filename: arm-d1-exception-levels.txt
  kind: document
  media_type: text/plain
  role: original
  sha256: sha256:e0874b85f90d0cfa1dcca7ab40b2e992f10050afe29e8f030c2f79d0fa4d3772
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-f20a3948ce05
  position:
    end: 297
    start: 89
    type: TextPositionSelector
  selector:
    exact: "The architecture defines four Exception levels: EL0, EL1, EL2, and EL3.
      \n      \n     \n    \n   \n   \n    \n     \n     R \n     VPSDB \n     \n
      \    \n      \n      EL3 is the highest Exception level and EL0 the lowest"
    prefix: "FYTFG \n     \n     \n      \n      "
    suffix: '. Therefore, EL3 is higher than '
    type: TextQuoteSelector
  snapshot_sha256: sha256:e0874b85f90d0cfa1dcca7ab40b2e992f10050afe29e8f030c2f79d0fa4d3772
extractor: utf8/1
id: arm-d1-exception-levels
local:
  file_sha256: sha256:e0874b85f90d0cfa1dcca7ab40b2e992f10050afe29e8f030c2f79d0fa4d3772
  path_ref: local-sidecar:public/arm-d1-exception-levels
media_type: text/plain
origin: external
raw_ref:
  path: archive/raw/e0874b85f90d0cfa1dcca7ab40b2e992f10050afe29e8f030c2f79d0fa4d3772.txt
read_status: retrieved
retrieval:
  acquisition: local-file
schema_version: source/v1
snapshot_sha256: sha256:e0874b85f90d0cfa1dcca7ab40b2e992f10050afe29e8f030c2f79d0fa4d3772
source_type: local-file
vault_id: public
---
#### D1.1 Exception levels
 
   
    
     
     R 
     FYTFG 
     
     
      
      The architecture defines four Exception levels: EL0, EL1, EL2, and EL3. 
      
     
    
   
   
    
     
     R 
     VPSDB 
     
     
      
      EL3 is the highest Exception level and EL0 the lowest. Therefore, EL3 is higher than EL2, EL2 is higher than EL1, and EL1 is higher than EL0. 
      
     
    
   
   
    
     
     R 
     CCQWK 
     
     
      
      Unprivileged execution is any execution that occurs at EL0. 
      
     
    
   
   
    
     
     I 
     WRRKQ 
     
     
      
      EL2 provides support for the virtualization of EL0 and EL1. 
      
     
    
   
   
    
     
     R 
     NXCRB 
     
     
      
      A PE: 
       
       Implements EL1 and EL0. 
       Also implements EL3 and EL2 if FEAT_RME is implemented. 
       
      In a PE without FEAT_RME, all the following are true: 
       
       Whether EL3 is implemented is IMPLEMENTATION DEFINED. 
       Whether EL2 is implemented is IMPLEMENTATION DEFINED. 
       Implementing a contiguous set of Exception levels is not required. 
       
      For which Security state each Exception level can be in, see Security states. 
      For which Execution state each Exception level is using, see Execution states. 
      
     
    
   
   
    
     
     R 
     NZZNS 
     
     
      
      The current Exception level changes only when any of the following occur: 
       
       Taking an exception. 
       Returning from an exception. 
       Processor reset. 
       Exiting from Debug state. 
       If in Debug state, executing a DCPSx instruction. 
       If in Debug state, executing a DRPS instruction. 
       
      
     
    
   
   
    
     
     R 
     XRQKF 
     
     
      
      The target Exception level is the Exception level to which an exception is taken. 
      
     
    
   
   
    
     
     R 
     FFJBB 
     
     
      
      Each exception type has a target Exception level that is either: 
       
       Implicit in the type of the exception. 
       Defined by configuration bits in the System registers. 
       
      
     
    
   
   
    
     
     R 
     TKYYF 
     
     
      
      An exception cannot be taken to EL0. 
      
     
    
   
   
    
     
     R 
     QNTPB 
     
     
      
      An exception cannot cause entry to a lower Exception level.