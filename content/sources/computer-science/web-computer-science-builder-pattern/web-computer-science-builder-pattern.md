---
archive_policy: text-only
attachments:
- filename: web-computer-science-builder-pattern.txt
  kind: document
  media_type: text/plain
  role: original
  sha256: sha256:dab1bcc21bdd3b493f250c8bed5c858a9d61d850053f3007740bec4c75333bcc
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-d8f8bf13741f
  position:
    end: 232
    start: 142
    type: TextPositionSelector
  quote_sha256: sha256:0c1ad5f0f090ab1c9bc13a644df6faddef19cccac3bba0d52710dce594583a0e
  selector:
    exact: The builder pattern separates the construction of a complex object from
      its representation
    prefix: 'in object-oriented programming. '
    suffix: . It is one of the 23 classic de
    type: TextQuoteSelector
  selector_sha256: sha256:ec41ff349ea485bee38a9be3ded54c104d09a6aeef62085c7bddfc448f820987
  snapshot_sha256: sha256:dab1bcc21bdd3b493f250c8bed5c858a9d61d850053f3007740bec4c75333bcc
extractor: utf8/1
id: web-computer-science-builder-pattern
local:
  file_sha256: sha256:dab1bcc21bdd3b493f250c8bed5c858a9d61d850053f3007740bec4c75333bcc
  path_ref: local-sidecar:public/web-computer-science-builder-pattern
media_type: text/plain
origin: external
raw_ref:
  path: archive/raw/dab1bcc21bdd3b493f250c8bed5c858a9d61d850053f3007740bec4c75333bcc.txt
  sha256: sha256:dab1bcc21bdd3b493f250c8bed5c858a9d61d850053f3007740bec4c75333bcc
read_status: retrieved
retrieval:
  acquisition: local-file
schema_version: source/v1
snapshot_sha256: sha256:dab1bcc21bdd3b493f250c8bed5c858a9d61d850053f3007740bec4c75333bcc
source_type: local-file
vault_id: public
---
The builder pattern is a design pattern that provides a flexible solution to various object creation problems in object-oriented programming. The builder pattern separates the construction of a complex object from its representation. It is one of the 23 classic design patterns described in the book Design Patterns and is sub-categorized as a creational pattern. The intent of the builder design pattern is to separate the construction of a complex object from its representation. By doing so, the same construction process can create different representations. The builder design pattern solves problems like: how can a class (the same construction process) create different representations of a complex object? How can a class that includes creating a complex object be simplified? Creating and assembling the parts of a complex object directly within a class is inflexible. It commits the class to creating a particular representation of the complex object and makes it impossible to change the representation later independently from (without having to change) the class. Typically, this is done with method chaining and a fluent API. The pattern encapsulates creating and assembling the parts of a complex object in a separate Builder object; a class delegates object creation to a Builder object instead of creating the objects directly, and the same construction process can delegate to different Builder objects to create different representations of a complex object.
