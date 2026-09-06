---
archive_policy: text-only
attachments:
- filename: web-computer-science-cpp-pointer.txt
  kind: document
  media_type: text/plain
  role: original
  sha256: sha256:ec6401656461d56bd6825843a5067227a76f5509b2cbe47725362f9b6396947a
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-8a6e78baf7e3
  position:
    end: 59
    start: 0
    type: TextPositionSelector
  quote_sha256: sha256:2d63bdd101084c72eb157dc12e2d9246d9345fe521410719afea21f280d88d38
  selector:
    exact: Declares a variable of a pointer or pointer-to-member type.
    prefix: ''
    suffix: ' A pointer declaration is any si'
    type: TextQuoteSelector
  selector_sha256: sha256:5fcc7082c193b17e5b67cfab6fefc74e08ac1564718e3b72778530a78b938076
  snapshot_sha256: sha256:ec6401656461d56bd6825843a5067227a76f5509b2cbe47725362f9b6396947a
- evidence_id: evidence-ce3a391eb822
  position:
    end: 1143
    start: 847
    type: TextPositionSelector
  quote_sha256: sha256:16d57bc8a2473dcfade9ae0ef1f8a5c0b297916f975470b7ab4f33e495944f7d
  selector:
    exact: Pointers of every type have a special value known as null pointer value
      of that type. A pointer whose value is null does not point to an object or a
      function (the behavior of dereferencing a null pointer is undefined), and compares
      equal to all pointers of the same type whose value is also null.
    prefix: '(*p2)(int) = f; // same as &f.


      '
    suffix: ' A null pointer constant can be '
    type: TextQuoteSelector
  selector_sha256: sha256:62163e2c62e197e49fc6a63924f577b536c6ca4f31abc8c7f42916fdacb1decf
  snapshot_sha256: sha256:ec6401656461d56bd6825843a5067227a76f5509b2cbe47725362f9b6396947a
extractor: utf8/1
id: web-computer-science-cpp-pointer
local:
  file_sha256: sha256:ec6401656461d56bd6825843a5067227a76f5509b2cbe47725362f9b6396947a
  path_ref: local-sidecar:public/web-computer-science-cpp-pointer
media_type: text/plain
origin: external
raw_ref:
  path: archive/raw/ec6401656461d56bd6825843a5067227a76f5509b2cbe47725362f9b6396947a.txt
  sha256: sha256:ec6401656461d56bd6825843a5067227a76f5509b2cbe47725362f9b6396947a
read_status: retrieved
retrieval:
  acquisition: local-file
schema_version: source/v1
snapshot_sha256: sha256:ec6401656461d56bd6825843a5067227a76f5509b2cbe47725362f9b6396947a
source_type: local-file
vault_id: public
---
Declares a variable of a pointer or pointer-to-member type. A pointer declaration is any simple declaration whose declarator has the form. Pointer declarator: the declaration S D; declares D as a pointer to the type determined by the declaration specifier sequence S.

Pointers to void are used to pass objects of unknown type, which is common in C interfaces: std::malloc returns void, std::qsort expects a user-provided callback that accepts two const void arguments. In all cases, it is the caller's responsibility to cast the pointer to the correct type before use.

A pointer to function can be initialized with an address of a non-member function or a static member function. Because of the function-to-pointer implicit conversion, the address-of operator is optional: void f(int); void (*p1)(int) = &f; void (*p2)(int) = f; // same as &f.

Pointers of every type have a special value known as null pointer value of that type. A pointer whose value is null does not point to an object or a function (the behavior of dereferencing a null pointer is undefined), and compares equal to all pointers of the same type whose value is also null. A null pointer constant can be used to initialize a pointer to null or to assign the null value to an existing pointer, it is one of the following values: an integer literal with value zero, or (since C++11) a prvalue of type std::nullptr_t (usually nullptr). The macro NULL can also be used, it expands to an implementation-defined null pointer constant.

Null pointers can be used to indicate the absence of an object (e.g. std::function::target()), or as other error condition indicators (e.g. dynamic_cast). In general, a function that receives a pointer argument almost always needs to check if the value is null and handle that case differently (for example, the delete expression does nothing when a null pointer is passed).
