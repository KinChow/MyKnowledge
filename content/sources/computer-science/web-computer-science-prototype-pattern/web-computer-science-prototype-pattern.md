---
archive_policy: text-only
attachments:
- filename: web-computer-science-prototype-pattern.txt
  kind: document
  media_type: text/plain
  role: original
  sha256: sha256:07375e6de6c5ed1522e5e7b53e98a01eb3b66fae949a4d0f29749f0515f8942a
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-12a7d834f0c6
  position:
    end: 206
    start: 0
    type: TextPositionSelector
  quote_sha256: sha256:950c21bdfa9c6d9ee6599e86b06cfcfa5c63fe1d0addcbc4662e4b97e7c1b533
  selector:
    exact: The prototype pattern is a creational design pattern in software development.
      It is used when the types of objects to create is determined by a prototypical
      instance, which is cloned to produce new objects.
    prefix: ''
    suffix: ' This pattern is used to avoid s'
    type: TextQuoteSelector
  selector_sha256: sha256:8035c3f04c5eccfb0f4c4ce649fb3db282912c958723622cb9d580054cecf43b
  snapshot_sha256: sha256:07375e6de6c5ed1522e5e7b53e98a01eb3b66fae949a4d0f29749f0515f8942a
extractor: utf8/1
id: web-computer-science-prototype-pattern
local:
  file_sha256: sha256:07375e6de6c5ed1522e5e7b53e98a01eb3b66fae949a4d0f29749f0515f8942a
  path_ref: local-sidecar:public/web-computer-science-prototype-pattern
media_type: text/plain
origin: external
raw_ref:
  path: archive/raw/07375e6de6c5ed1522e5e7b53e98a01eb3b66fae949a4d0f29749f0515f8942a.txt
  sha256: sha256:07375e6de6c5ed1522e5e7b53e98a01eb3b66fae949a4d0f29749f0515f8942a
read_status: retrieved
retrieval:
  acquisition: local-file
schema_version: source/v1
snapshot_sha256: sha256:07375e6de6c5ed1522e5e7b53e98a01eb3b66fae949a4d0f29749f0515f8942a
source_type: local-file
vault_id: public
---
The prototype pattern is a creational design pattern in software development. It is used when the types of objects to create is determined by a prototypical instance, which is cloned to produce new objects. This pattern is used to avoid subclasses of an object creator in the client application, like the factory method pattern does, and to avoid the inherent cost of creating a new object in the standard way (e.g., using the 'new' keyword) when it is prohibitively expensive for a given application. The prototype design pattern is one of the 23 Gang of Four design patterns that describe how to solve recurring design problems to design flexible and reusable object-oriented software, that is, objects that are easier to implement, change, test, and reuse. The prototype design pattern solves problems like: how can objects be created so that the specific type of object can be determined at runtime? How can dynamically loaded classes be instantiated? The pattern describes how to solve such problems by defining a Prototype object that returns a copy of itself and creating new objects by copying a Prototype object. This enables configuration of a class with different Prototype objects, which are copied to create new objects, and even more, Prototype objects can be added and removed at run-time.
