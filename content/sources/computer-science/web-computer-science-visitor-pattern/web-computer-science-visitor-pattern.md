---
archive_policy: text-only
attachments:
- filename: web-computer-science-visitor-pattern.txt
  kind: document
  media_type: text/plain
  role: original
  sha256: sha256:73ebdc3edcb780bc89cc94ba9cdee5e59aa46908598487de749348f87ed6a87e
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-d6bf0661e3cf
  position:
    end: 101
    start: 0
    type: TextPositionSelector
  quote_sha256: sha256:85c5072071f47f221659fc6b34b0c81f164dba240e1fec2140bd2d5cb6f3a49c
  selector:
    exact: A visitor pattern is a software design pattern that separates the algorithm
      from the object structure
    prefix: ''
    suffix: . Because of this separation, ne
    type: TextQuoteSelector
  selector_sha256: sha256:de97a3cd29063d41249f93082f620b519ec25dfab89a568c2e3e0360f542f2b4
  snapshot_sha256: sha256:73ebdc3edcb780bc89cc94ba9cdee5e59aa46908598487de749348f87ed6a87e
extractor: utf8/1
id: web-computer-science-visitor-pattern
local:
  file_sha256: sha256:73ebdc3edcb780bc89cc94ba9cdee5e59aa46908598487de749348f87ed6a87e
  path_ref: local-sidecar:public/web-computer-science-visitor-pattern
media_type: text/plain
origin: external
raw_ref:
  path: archive/raw/73ebdc3edcb780bc89cc94ba9cdee5e59aa46908598487de749348f87ed6a87e.txt
  sha256: sha256:73ebdc3edcb780bc89cc94ba9cdee5e59aa46908598487de749348f87ed6a87e
read_status: retrieved
retrieval:
  acquisition: local-file
schema_version: source/v1
snapshot_sha256: sha256:73ebdc3edcb780bc89cc94ba9cdee5e59aa46908598487de749348f87ed6a87e
source_type: local-file
vault_id: public
---
A visitor pattern is a software design pattern that separates the algorithm from the object structure. Because of this separation, new operations can be added to existing object structures without modifying the structures. It is one way to follow the open/closed principle in object-oriented programming and software engineering.

In essence, the visitor allows adding new virtual functions to a family of classes, without modifying the classes. Instead, a visitor class is created that implements all of the appropriate specializations of the virtual function. The visitor takes the instance reference as input, and implements the goal through double dispatch. This makes it possible to create new operations independently from the classes of an object structure by adding new visitor objects.

The Gang of Four defines the Visitor as: Representing an operation to be performed on elements of an object structure. Visitor lets you define a new operation without changing the classes of the elements on which it operates.

The nature of the Visitor makes it an ideal pattern to plug into public APIs, thus allowing its clients to perform operations on a class using a visiting class without having to modify the source.
