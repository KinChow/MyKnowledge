---
archive_policy: text-only
attachments:
- filename: web-computer-science-singleton-pattern.txt
  kind: document
  media_type: text/plain
  role: original
  sha256: sha256:fa1fba9176ed21232eeedd6b2717026b473d0ce065e60aa6fd7a992549a16332
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-325ec7d0f256
  position:
    end: 149
    start: 32
    type: TextPositionSelector
  selector:
    exact: the singleton pattern is a software design pattern that restricts the instantiation
      of a class to a singular instance
    prefix: 'In object-oriented programming, '
    suffix: . It is one of the well-known "G
    type: TextQuoteSelector
  snapshot_sha256: sha256:fa1fba9176ed21232eeedd6b2717026b473d0ce065e60aa6fd7a992549a16332
extractor: utf8/1
id: web-computer-science-singleton-pattern
local:
  file_sha256: sha256:fa1fba9176ed21232eeedd6b2717026b473d0ce065e60aa6fd7a992549a16332
  path_ref: local-sidecar:public/web-computer-science-singleton-pattern
media_type: text/plain
origin: external
raw_ref:
  path: archive/raw/fa1fba9176ed21232eeedd6b2717026b473d0ce065e60aa6fd7a992549a16332.txt
read_status: retrieved
retrieval:
  acquisition: local-file
schema_version: source/v1
snapshot_sha256: sha256:fa1fba9176ed21232eeedd6b2717026b473d0ce065e60aa6fd7a992549a16332
source_type: local-file
vault_id: public
---
In object-oriented programming, the singleton pattern is a software design pattern that restricts the instantiation of a class to a singular instance. It is one of the well-known "Gang of Four" design patterns, which describe how to solve recurring problems in object-oriented software. The pattern is useful when exactly one object is needed to coordinate actions across a system. More specifically, the singleton pattern allows classes to ensure they only have one instance, provide easy access to that instance, and control their instantiation (for example, by hiding the constructors of a class). The term comes from the mathematical concept of a singleton. Singletons are often preferred to global variables because they do not pollute the global namespace (or their containing namespace). Additionally, they permit lazy allocation and initialization, whereas global variables in many languages will always consume resources. The singleton pattern can also be used as a basis for other design patterns, such as the abstract factory, factory method, builder and prototype patterns.
