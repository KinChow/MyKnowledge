---
archive_policy: text-only
attachments:
- filename: web-computer-science-cpp-class-and-struct.txt
  kind: document
  media_type: text/plain
  role: original
  sha256: sha256:36e90a879b087577270dfd55bc4a9867898e1c59f428677428253422a87a53bc
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-c1d493a5d1a7
  position:
    end: 122
    start: 0
    type: TextPositionSelector
  selector:
    exact: Classes are user-defined types, defined by class-specifier, which appears
      in decl-specifier-seq of the declaration syntax.
    prefix: ''
    suffix: '


      The class specifier has the fo'
    type: TextQuoteSelector
  snapshot_sha256: sha256:36e90a879b087577270dfd55bc4a9867898e1c59f428677428253422a87a53bc
- evidence_id: evidence-0d439ba9d56a
  position:
    end: 435
    start: 275
    type: TextPositionSelector
  selector:
    exact: class-key is one of class, struct and union. The keywords class and struct
      are identical except for the default member access and the default base class
      access.
    prefix: 'onal) { member-specification }. '
    suffix: ' If it is union, the declaration'
    type: TextQuoteSelector
  snapshot_sha256: sha256:36e90a879b087577270dfd55bc4a9867898e1c59f428677428253422a87a53bc
extractor: utf8/1
id: web-computer-science-cpp-class-and-struct
local:
  file_sha256: sha256:36e90a879b087577270dfd55bc4a9867898e1c59f428677428253422a87a53bc
  path_ref: local-sidecar:public/web-computer-science-cpp-class-and-struct
media_type: text/plain
origin: external
raw_ref:
  path: archive/raw/36e90a879b087577270dfd55bc4a9867898e1c59f428677428253422a87a53bc.txt
read_status: retrieved
retrieval:
  acquisition: local-file
schema_version: source/v1
snapshot_sha256: sha256:36e90a879b087577270dfd55bc4a9867898e1c59f428677428253422a87a53bc
source_type: local-file
vault_id: public
---
Classes are user-defined types, defined by class-specifier, which appears in decl-specifier-seq of the declaration syntax.

The class specifier has the following syntax: class-key attr(optional) class-head-name final(optional) base-clause(optional) { member-specification }. class-key is one of class, struct and union. The keywords class and struct are identical except for the default member access and the default base class access. If it is union, the declaration introduces a union type.

The class specifier for a union declaration is similar to class or struct declaration. A class can have member functions, data members, static members, nested classes, member templates, bit-fields, and using-declarations. Member access specifiers control the accessibility of members. Constructors and member initializer lists initialize members, and the destructor finalizes the object.

For class types, the default member access is private. For struct types, the default member access is public. Inheritance uses the same rule: a class derived with the class-key class has private base class access by default, and a class derived with the class-key struct has public base class access by default.
