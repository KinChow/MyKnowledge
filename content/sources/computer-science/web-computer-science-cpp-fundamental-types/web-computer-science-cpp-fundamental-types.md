---
archive_policy: text-only
attachments:
- filename: web-computer-science-cpp-fundamental-types.txt
  kind: document
  media_type: text/plain
  role: original
  sha256: sha256:5ec71696d60af3df617c396e4f1eb5f256188a5267f04d3930f9f7fc3f29b55b
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-d2dd17001b46
  position:
    end: 160
    start: 0
    type: TextPositionSelector
  quote_sha256: sha256:e3dc1b4b46a6badcd6f4f5327ae15dcc5163f5de5412c17e107f5a89be56b504
  selector:
    exact: 'The following types are collectively called fundamental types: (possibly
      cv-qualified) void; std::nullptr_t (since C++11); integral types; floating-point
      types.'
    prefix: ''
    suffix: '


      void is a type with an empty s'
    type: TextQuoteSelector
  selector_sha256: sha256:84a5273bd094370ce39512029e5ee7e14611feb58aa5f8d9a0f2b4417a1ad022
  snapshot_sha256: sha256:5ec71696d60af3df617c396e4f1eb5f256188a5267f04d3930f9f7fc3f29b55b
- evidence_id: evidence-760eedda3335
  position:
    end: 1935
    start: 1783
    type: TextPositionSelector
  quote_sha256: sha256:855927ea2183db112c79b4b9292adcea380e9f7666432a25500e9224fe819d87
  selector:
    exact: Besides the minimal bit counts, the C++ Standard guarantees that 1 == sizeof(char)
      <= sizeof(short) <= sizeof(int) <= sizeof(long) <= sizeof(long long).
    prefix: 'a distinct type (since C++20).


      '
    suffix: ' Note: this allows the extreme c'
    type: TextQuoteSelector
  selector_sha256: sha256:c37414ad63b5d8f7a5095b5e33cd4e51b6f0a216bf703c43260398653f3a1f29
  snapshot_sha256: sha256:5ec71696d60af3df617c396e4f1eb5f256188a5267f04d3930f9f7fc3f29b55b
extractor: utf8/1
id: web-computer-science-cpp-fundamental-types
local:
  file_sha256: sha256:5ec71696d60af3df617c396e4f1eb5f256188a5267f04d3930f9f7fc3f29b55b
  path_ref: local-sidecar:public/web-computer-science-cpp-fundamental-types
media_type: text/plain
origin: external
raw_ref:
  path: archive/raw/5ec71696d60af3df617c396e4f1eb5f256188a5267f04d3930f9f7fc3f29b55b.txt
  sha256: sha256:5ec71696d60af3df617c396e4f1eb5f256188a5267f04d3930f9f7fc3f29b55b
read_status: retrieved
retrieval:
  acquisition: local-file
schema_version: source/v1
snapshot_sha256: sha256:5ec71696d60af3df617c396e4f1eb5f256188a5267f04d3930f9f7fc3f29b55b
source_type: local-file
vault_id: public
---
The following types are collectively called fundamental types: (possibly cv-qualified) void; std::nullptr_t (since C++11); integral types; floating-point types.

void is a type with an empty set of values. It is an incomplete type that cannot be completed (consequently, objects of type void are disallowed). There are no arrays of void, nor references to void. However, pointers to void and functions returning type void (procedures in other languages) are permitted.

std::nullptr_t names the type of the null pointer literal, nullptr. It is a distinct type that is not itself a pointer type or a pointer to member type. All its prvalues are null pointer constants. sizeof(std::nullptr_t) is equal to sizeof(void*).

int is the basic integer type. The keyword int may be omitted if any of the modifiers listed below are used. If no length modifiers are present, it's guaranteed to have a width of at least 16 bits. However, on 32/64 bit systems it is almost exclusively guaranteed to have width of at least 32 bits.

char16_t is a type for UTF-16 character representation, required to be large enough to represent any UTF-16 code unit (16 bits). It has the same size, signedness, and alignment as std::uint_least16_t, but is a distinct type. char32_t is a type for UTF-32 character representation, required to be large enough to represent any UTF-32 code unit (32 bits). It has the same size, signedness, and alignment as std::uint_least32_t, but is a distinct type (since C++11).

char8_t is a type for UTF-8 character representation, required to be large enough to represent any UTF-8 code unit (8 bits). It has the same size, signedness, and alignment as unsigned char (and therefore, the same size and alignment as char and signed char), but is a distinct type (since C++20).

Besides the minimal bit counts, the C++ Standard guarantees that 1 == sizeof(char) <= sizeof(short) <= sizeof(int) <= sizeof(long) <= sizeof(long long). Note: this allows the extreme case in which bytes are sized 64 bits, all types (including char) are 64 bits wide, and sizeof returns 1 for every type.

The standard floating-point types include float, double, and long double.
