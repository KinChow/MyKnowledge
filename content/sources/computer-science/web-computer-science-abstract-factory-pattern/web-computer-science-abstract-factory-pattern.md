---
archive_policy: text-only
attachments:
- filename: web-computer-science-abstract-factory-pattern.txt
  kind: document
  media_type: text/plain
  role: original
  sha256: sha256:15e1ca9ac948543e2a173aa6bc7f32902f6fe5c046b66d12753aacd652a09710
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-a5bf12e5cae1
  position:
    end: 170
    start: 0
    type: TextPositionSelector
  selector:
    exact: The abstract factory pattern in software engineering is a design pattern
      that provides a way to create families of related objects without imposing their
      concrete classes
    prefix: ''
    suffix: ', by encapsulating a group of in'
    type: TextQuoteSelector
  snapshot_sha256: sha256:15e1ca9ac948543e2a173aa6bc7f32902f6fe5c046b66d12753aacd652a09710
extractor: utf8/1
id: web-computer-science-abstract-factory-pattern
local:
  file_sha256: sha256:15e1ca9ac948543e2a173aa6bc7f32902f6fe5c046b66d12753aacd652a09710
  path_ref: local-sidecar:public/web-computer-science-abstract-factory-pattern
media_type: text/plain
origin: external
raw_ref:
  path: archive/raw/15e1ca9ac948543e2a173aa6bc7f32902f6fe5c046b66d12753aacd652a09710.txt
read_status: retrieved
retrieval:
  acquisition: local-file
schema_version: source/v1
snapshot_sha256: sha256:15e1ca9ac948543e2a173aa6bc7f32902f6fe5c046b66d12753aacd652a09710
source_type: local-file
vault_id: public
---
The abstract factory pattern in software engineering is a design pattern that provides a way to create families of related objects without imposing their concrete classes, by encapsulating a group of individual factories that have a common theme without specifying their concrete classes. According to this pattern, a client software component creates a concrete implementation of the abstract factory and then uses the generic interface of the factory to create the concrete objects that are part of the family. The client does not know which concrete objects it receives from each of these internal factories, as it uses only the generic interfaces of their products. This pattern separates the details of implementation of a set of objects from their general usage and relies on object composition, as object creation is implemented in methods exposed in the factory interface. Design Patterns describes the abstract factory pattern as "an interface for creating families of related or dependent objects without specifying their concrete classes." The factory determines the concrete type of object to be created, and it is here that the object is actually created. However, the factory only returns a reference (in Java, for instance, by the new operator) or a pointer of an abstract type to the created concrete object.
