---
archive_policy: text-only
attachments:
- filename: web-computer-science-cpp-enum.txt
  kind: document
  media_type: text/plain
  role: original
  sha256: sha256:276e3dac80a27128d56a9a60575dd942795e27f51b4ee416ca44a9b99c28b103
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-a9c5a0247695
  position:
    end: 175
    start: 0
    type: TextPositionSelector
  quote_sha256: sha256:230942ade56cd1b86c8b2670d7f3f3689f4e14a9649e27cded954725508922f1
  selector:
    exact: An enumeration is a distinct type whose value is restricted to a range
      of values (see below for details), which may include several explicitly named
      constants ("enumerators").
    prefix: ''
    suffix: '


      The values of the constants ar'
    type: TextQuoteSelector
  selector_sha256: sha256:b5a524ad66d0a87ff14e5d9acf60366a0362b7b627deaa05432fafdb3b2bb666
  snapshot_sha256: sha256:276e3dac80a27128d56a9a60575dd942795e27f51b4ee416ca44a9b99c28b103
- evidence_id: evidence-19853330e477
  position:
    end: 693
    start: 514
    type: TextPositionSelector
  quote_sha256: sha256:eb16f4ca11e726f4158185c7621b26900edf14a89417d03e168ec74ea82c183b
  selector:
    exact: 'There are two distinct kinds of enumerations: unscoped enumeration (declared
      with the enum-key enum) and scoped enumeration (declared with the enum-key enum
      class or enum struct).'
    prefix: ' value of the underlying type.


      '
    suffix: '


      Each enumerator becomes a name'
    type: TextQuoteSelector
  selector_sha256: sha256:fcd5c4e5d1860fdb4ed904c656f28f69073bff14e27efdef3d63c77177393436
  snapshot_sha256: sha256:276e3dac80a27128d56a9a60575dd942795e27f51b4ee416ca44a9b99c28b103
extractor: utf8/1
id: web-computer-science-cpp-enum
local:
  file_sha256: sha256:276e3dac80a27128d56a9a60575dd942795e27f51b4ee416ca44a9b99c28b103
  path_ref: local-sidecar:public/web-computer-science-cpp-enum
media_type: text/plain
origin: external
raw_ref:
  path: archive/raw/276e3dac80a27128d56a9a60575dd942795e27f51b4ee416ca44a9b99c28b103.txt
  sha256: sha256:276e3dac80a27128d56a9a60575dd942795e27f51b4ee416ca44a9b99c28b103
read_status: retrieved
retrieval:
  acquisition: local-file
schema_version: source/v1
snapshot_sha256: sha256:276e3dac80a27128d56a9a60575dd942795e27f51b4ee416ca44a9b99c28b103
source_type: local-file
vault_id: public
---
An enumeration is a distinct type whose value is restricted to a range of values (see below for details), which may include several explicitly named constants ("enumerators").

The values of the constants are values of an integral type known as the underlying type of the enumeration. An enumeration has the same size, value representation, and alignment requirements as its underlying type. Furthermore, each value of an enumeration has the same representation as the corresponding value of the underlying type.

There are two distinct kinds of enumerations: unscoped enumeration (declared with the enum-key enum) and scoped enumeration (declared with the enum-key enum class or enum struct).

Each enumerator becomes a named constant of the enumeration's type (that is, name), visible in the enclosing scope, and can be used whenever constants are required. Each enumerator is associated with a value of the underlying type. When = are provided in an enumerator-list, the values of enumerators are defined by those associated constant-expressions. If the first enumerator does not have =, the associated value is zero. For any other enumerator whose definition does not have an =, the associated value is the value of the previous enumerator plus one.

A scoped enumeration whose underlying type is int (the keywords class and struct are exactly equivalent).
