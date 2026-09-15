---
archive_policy: text-only
attachments:
- filename: web-computer-science-cpp-template.txt
  kind: document
  media_type: text/plain
  role: original
  sha256: sha256:0233647a3ddc9a4fbb0dc89c064267d0eaf44a9d9dec62ab4088927d43d97638
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-39b24f86fcf1
  position:
    end: 373
    start: 0
    type: TextPositionSelector
  selector:
    exact: 'A template is a C++ entity that defines one of the following: a family
      of classes (class template), which may be nested classes; a family of functions
      (function template), which may be member functions; an alias to a family of
      types (alias template) (since C++11); a family of variables (variable template)
      (since C++14); a concept (constraints and concepts) (since C++20).'
    prefix: ''
    suffix: '


      Templates are parameterized by'
    type: TextQuoteSelector
  snapshot_sha256: sha256:0233647a3ddc9a4fbb0dc89c064267d0eaf44a9d9dec62ab4088927d43d97638
- evidence_id: evidence-a709323bd176
  position:
    end: 544
    start: 375
    type: TextPositionSelector
  selector:
    exact: 'Templates are parameterized by one or more template parameters, of three
      kinds: type template parameters, non-type template parameters, and template
      template parameters.'
    prefix: 's and concepts) (since C++20).


      '
    suffix: '


      When template arguments are pr'
    type: TextQuoteSelector
  snapshot_sha256: sha256:0233647a3ddc9a4fbb0dc89c064267d0eaf44a9d9dec62ab4088927d43d97638
extractor: utf8/1
id: web-computer-science-cpp-template
local:
  file_sha256: sha256:0233647a3ddc9a4fbb0dc89c064267d0eaf44a9d9dec62ab4088927d43d97638
  path_ref: local-sidecar:public/web-computer-science-cpp-template
media_type: text/plain
origin: external
raw_ref:
  path: archive/raw/0233647a3ddc9a4fbb0dc89c064267d0eaf44a9d9dec62ab4088927d43d97638.txt
read_status: retrieved
retrieval:
  acquisition: local-file
schema_version: source/v1
snapshot_sha256: sha256:0233647a3ddc9a4fbb0dc89c064267d0eaf44a9d9dec62ab4088927d43d97638
source_type: local-file
vault_id: public
---
A template is a C++ entity that defines one of the following: a family of classes (class template), which may be nested classes; a family of functions (function template), which may be member functions; an alias to a family of types (alias template) (since C++11); a family of variables (variable template) (since C++14); a concept (constraints and concepts) (since C++20).

Templates are parameterized by one or more template parameters, of three kinds: type template parameters, non-type template parameters, and template template parameters.

When template arguments are provided, or, for function and class (since C++17) templates only, deduced, they are substituted for the template parameters to obtain a specialization of the template, that is, a specific type or a specific function lvalue.
