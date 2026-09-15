---
archive_policy: text-only
attachments:
- filename: web-computer-science-strings.txt
  kind: document
  media_type: text/plain
  role: original
  sha256: sha256:80e9e666a4018865c467f95ec88825ac0f897305db397dd81778ec26edbda820
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-1447528d9989
  position:
    end: 409
    start: 0
    type: TextPositionSelector
  selector:
    exact: In computer programming, a string is traditionally a sequence of characters,
      either as a literal constant or as some kind of variable. The latter may allow
      its elements to be mutated and the length changed, or it may be fixed (after
      creation). A string is often implemented as an array data structure of bytes
      (or words) that stores a sequence of elements, typically characters, using some
      character encoding.
    prefix: ''
    suffix: '


      Strings are typically made up '
    type: TextQuoteSelector
  snapshot_sha256: sha256:80e9e666a4018865c467f95ec88825ac0f897305db397dd81778ec26edbda820
- evidence_id: evidence-812fbabfc66a
  position:
    end: 794
    start: 534
    type: TextPositionSelector
  selector:
    exact: Strings are typically implemented as arrays of bytes, characters, or code
      units, to allow fast access to individual units or substrings, including characters
      when they have a fixed length. A few languages such as Haskell implement them
      as linked lists instead.
    prefix: 'a, such as words or sentences.


      '
    suffix: '


      Many high-level languages prov'
    type: TextQuoteSelector
  snapshot_sha256: sha256:80e9e666a4018865c467f95ec88825ac0f897305db397dd81778ec26edbda820
- evidence_id: evidence-18083865b0a7
  position:
    end: 1030
    start: 796
    type: TextPositionSelector
  selector:
    exact: Many high-level languages provide strings as a primitive data type, such
      as JavaScript and PHP, while most others provide them as a composite data type,
      some with special language support in writing literals, for example, Java and
      C#.
    prefix: ' them as linked lists instead.


      '
    suffix: '


      The core data structure in a t'
    type: TextQuoteSelector
  snapshot_sha256: sha256:80e9e666a4018865c467f95ec88825ac0f897305db397dd81778ec26edbda820
- evidence_id: evidence-0ba90d1d9d6c
  position:
    end: 1548
    start: 1032
    type: TextPositionSelector
  selector:
    exact: The core data structure in a text editor is the one that manages the string
      (sequence of characters) that represents the current state of the file being
      edited. While that state could be stored in a single long consecutive array
      of characters, a typical text editor instead uses an alternative representation
      as its sequence data structure—a gap buffer, a linked list of lines, a piece
      table, or a rope—which makes certain string operations, such as insertions,
      deletions, and undoing previous edits, more efficient.
    prefix: 'als, for example, Java and C#.


      '
    suffix: '

      '
    type: TextQuoteSelector
  snapshot_sha256: sha256:80e9e666a4018865c467f95ec88825ac0f897305db397dd81778ec26edbda820
extractor: utf8/1
id: web-computer-science-strings
local:
  file_sha256: sha256:80e9e666a4018865c467f95ec88825ac0f897305db397dd81778ec26edbda820
  path_ref: local-sidecar:public/web-computer-science-strings
media_type: text/plain
origin: external
raw_ref:
  path: archive/raw/80e9e666a4018865c467f95ec88825ac0f897305db397dd81778ec26edbda820.txt
read_status: retrieved
retrieval:
  acquisition: local-file
schema_version: source/v1
snapshot_sha256: sha256:80e9e666a4018865c467f95ec88825ac0f897305db397dd81778ec26edbda820
source_type: local-file
vault_id: public
---
In computer programming, a string is traditionally a sequence of characters, either as a literal constant or as some kind of variable. The latter may allow its elements to be mutated and the length changed, or it may be fixed (after creation). A string is often implemented as an array data structure of bytes (or words) that stores a sequence of elements, typically characters, using some character encoding.

Strings are typically made up of characters, and are often used to store human-readable data, such as words or sentences.

Strings are typically implemented as arrays of bytes, characters, or code units, to allow fast access to individual units or substrings, including characters when they have a fixed length. A few languages such as Haskell implement them as linked lists instead.

Many high-level languages provide strings as a primitive data type, such as JavaScript and PHP, while most others provide them as a composite data type, some with special language support in writing literals, for example, Java and C#.

The core data structure in a text editor is the one that manages the string (sequence of characters) that represents the current state of the file being edited. While that state could be stored in a single long consecutive array of characters, a typical text editor instead uses an alternative representation as its sequence data structure—a gap buffer, a linked list of lines, a piece table, or a rope—which makes certain string operations, such as insertions, deletions, and undoing previous edits, more efficient.
