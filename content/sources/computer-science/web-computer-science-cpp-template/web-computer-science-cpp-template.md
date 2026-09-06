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
  quote_sha256: sha256:93aacdf83ed90a8fd83fdfeac02f10b1e1d3bf4902989a9b6b051a9e99ec7023
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
  selector_sha256: sha256:2efdeec468c66983cf62b97daf3a0f87bb974112f44d9f78997a759ab7862e5a
  snapshot_sha256: sha256:0233647a3ddc9a4fbb0dc89c064267d0eaf44a9d9dec62ab4088927d43d97638
- evidence_id: evidence-a709323bd176
  position:
    end: 544
    start: 375
    type: TextPositionSelector
  quote_sha256: sha256:8f6aa372fccd9b7fccdf88748084ba895cba55db6651668c837a9602fc068331
  selector:
    exact: 'Templates are parameterized by one or more template parameters, of three
      kinds: type template parameters, non-type template parameters, and template
      template parameters.'
    prefix: 's and concepts) (since C++20).


      '
    suffix: '


      When template arguments are pr'
    type: TextQuoteSelector
  selector_sha256: sha256:8b1b4297832f03a3fbdcfc230c2670a50346b2022af848bf16047ff825c344d6
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
  sha256: sha256:0233647a3ddc9a4fbb0dc89c064267d0eaf44a9d9dec62ab4088927d43d97638
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
