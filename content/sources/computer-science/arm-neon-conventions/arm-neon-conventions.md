---
archive_policy: text-only
attachments:
- filename: arm-neon-conventions.txt
  kind: document
  media_type: text/plain
  role: original
  sha256: sha256:1bcc9b9ae1f357e0a69a33499eb547ce025902b487872248b83f0d3009f5e7e7
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-a49ec0ff171a
  position:
    end: 1364
    start: 1287
    type: TextPositionSelector
  quote_sha256: sha256:0f8e3927a56c936b621778806ad1d2fd2845778bf905f9231ed363c6d6c9c0e9
  selector:
    exact: "data types \n      baseWxL_t vector data types \n      baseWxLxN_t vector
      array"
    prefix: "s: \n      \n      baseW_t scalar "
    suffix: " data types \n      \n     Where: "
    type: TextQuoteSelector
  selector_sha256: sha256:35ef06ca27c56e85631def42615d030a563e4f4beab8fbcc68231d26795d3a1d
  snapshot_sha256: sha256:1bcc9b9ae1f357e0a69a33499eb547ce025902b487872248b83f0d3009f5e7e7
- evidence_id: evidence-83f47882ed36
  position:
    end: 1375
    start: 1159
    type: TextPositionSelector
  quote_sha256: sha256:68c06994d1abbc5fd5762f046ecf11ed70d9bba960a3018a9a7c3d2f4171c586
  selector:
    exact: "There are three major categories of data type available in arm_neon.h
      which follow these patterns: \n      \n      baseW_t scalar data types \n      baseWxL_t
      vector data types \n      baseWxLxN_t vector array data types"
    prefix: "   \n     \n     ### Types\n \n     "
    suffix: " \n      \n     Where: \n      \n   "
    type: TextQuoteSelector
  selector_sha256: sha256:c324a449adc8e956af0ee74788d3ea86b9e33bb77cea01956c5aca3c4537a7ff
  snapshot_sha256: sha256:1bcc9b9ae1f357e0a69a33499eb547ce025902b487872248b83f0d3009f5e7e7
extractor: utf8/1
id: arm-neon-conventions
local:
  file_sha256: sha256:1bcc9b9ae1f357e0a69a33499eb547ce025902b487872248b83f0d3009f5e7e7
  path_ref: local-sidecar:public/arm-neon-conventions
media_type: text/plain
origin: external
raw_ref:
  path: archive/raw/1bcc9b9ae1f357e0a69a33499eb547ce025902b487872248b83f0d3009f5e7e7.txt
  sha256: sha256:1bcc9b9ae1f357e0a69a33499eb547ce025902b487872248b83f0d3009f5e7e7
read_status: retrieved
retrieval:
  acquisition: local-file
schema_version: source/v1
snapshot_sha256: sha256:1bcc9b9ae1f357e0a69a33499eb547ce025902b487872248b83f0d3009f5e7e7
source_type: local-file
vault_id: public
---
### Program conventions
 
    
    Program conventions are a set of guidelines for a specific programming language.  
     
     
     
     ### Macros
 
     In order to use the intrinsics the Advanced SIMD architecture must be supported, and some specific instructions may or may not be enabled in any case. When the following macros are defined and equal to 1, the corresponding features are available: 
      
       
       __ARM_NEON 
       
      
        Advanced SIMD is supported by the compiler. Always 1 for AArch64. 
       
       
       __ARM_NEON_FP 
       
      
        Neon floating-point operations are supported. Always 1 for AArch64. 
       
       
       __ARM_FEATURE_CRYPTO 
       
      
        Crypto instructions are available. Cryptographic Neon intrinsics are therefore available. 
       
       
       __ARM_FEATURE_FMA 
       
      
        The fused multiply-accumulate instructions are available. Neon intrinsics which use these are therefore available. 
       
      
     This list is not exhaustive and further macros are detailed in the Arm C Language Extensions document. 
     
     
     ### Types
 
     There are three major categories of data type available in arm_neon.h which follow these patterns: 
      
      baseW_t scalar data types 
      baseWxL_t vector data types 
      baseWxLxN_t vector array data types 
      
     Where: 
      
      base refers to the fundamental data type. 
      W is the width of the fundamental type. 
      L is the number of scalar data type instances in a vector data type, for example an array of scalars. 
      N is the number of vector data type instances in a vector array type, for example a struct of arrays of scalars. 
      
     Generally W and L are such that the vector data types are 64 or 128 bits long, and so fit completely into a Neon register. N corresponds with those instructions which operate on multiple registers at once. 
     In our earlier code we encountered an example of all three: 
      
      uint8_t 
      uint8x16_t 
      uint8x16x3_t 
      
     
     
     ### Functions
 
     As per the Arm C Language Extensions, the function prototypes from arm_neon.h follow a common pattern. At the most general level this is: 
     ret v[p][q][r]name[u][n][q][x][_high][_lane | laneq][_n][_result]_type(args) 
     Be wary that some of the letters and names are overloaded, but in the order above: 
      
       
       ret 
       
      
        the return type of the function. 
       
       
       v 
       
      
        short for 
       vector and is present on all the intrinsics. 
       
       
       p 
       
      
        indicates a pairwise operation. ( 
       [value] means 
       value may be present). 
       
       
       q 
       
      
        indicates a saturating operation (with the exception of 
       vqtb[l][x] in AArch64 operations where the 
       q indicates 128-bit index and result operands). 
       
       
       r 
       
      
        indicates a rounding operation. 
       
       
       name 
       
      
        the descriptive name of the basic operation. Often this is an Advanced SIMD instruction, but it does not have to be. 
       
       
       u 
       
      
        indicates signed-to-unsigned saturation. 
       
       
       n 
       
      
        indicates a narrowing operation. 
       
       
       q 
       
      
        postfixing the name indicates an operation on 128-bit vectors. 
       
       
       x 
       
      
        indicates an Advanced SIMD scalar operation in AArch64. It can be one of 
       b, 
       h, 
       s or 
       d (that is, 8, 16, 32, or 64 bits). 
       
       
       _high 
       
      
        In AArch64, used for widening and narrowing operations involving 128-bit operands. For widening 128-bit operands, 
       high refers to the top 64-bits of the source operand(s). For narrowing, it refers to the top 64-bits of the destination operand. 
       
       
       _n 
       
      
        indicates a scalar operand supplied as an argument. 
       
       
       _lane 
       
      
        indicates a scalar operand taken from the lane of a vector. 
       _laneq indicates a scalar operand taken from the lane of an input vector of 128-bit width. ( 
       left | right means only 
       left or 
       right would appear). 
       
       
       type 
       
      
        the primary operand type in short form. 
       
       
       args 
       
      
        the function’s arguments.