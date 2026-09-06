---
archive_policy: text-only
attachments:
- filename: web-computer-science-cpp-course.txt
  kind: document
  media_type: text/plain
  role: original
  sha256: sha256:370ef0beecf12cb5bb3548370e2581a8cfee17270e96fdbb85877b36b9d9f4a7
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-66af4c868854
  position:
    end: 597
    start: 0
    type: TextPositionSelector
  quote_sha256: sha256:c45f8d2c9240e6194cbf321657155ba06f412fcd6f317c7f208c437536780b3a
  selector:
    exact: C++ is a high-level, general-purpose programming language created by Danish
      computer scientist Bjarne Stroustrup. First released in 1985 as an extension
      of the C programming language, adding object-oriented (OOP) features, it has
      since expanded significantly over time adding more OOP and other features; as
      of 1997 standardization, C++ has added functional features, in addition to facilities
      for low-level memory manipulation for systems like microcomputers or to make
      operating systems like Linux or Windows, and even later came features like generic
      programming (through the use of templates).
    prefix: ''
    suffix: ' C++ is usually implemented as a'
    type: TextQuoteSelector
  selector_sha256: sha256:0c72e6c52620e226b9713c8aea69bbdd32014149ced9fe33dc3cc0c6e3ed3a24
  snapshot_sha256: sha256:370ef0beecf12cb5bb3548370e2581a8cfee17270e96fdbb85877b36b9d9f4a7
- evidence_id: evidence-1f513b7ce17d
  position:
    end: 1070
    start: 690
    type: TextPositionSelector
  quote_sha256: sha256:694f6d947e392f1b58d687a972559d5bbb4e9bd3c7f82cdfda9c138505afa65c
  selector:
    exact: The Standard Template Library (STL) was a software library originally designed
      by Alexander Stepanov for the C++ programming language that influenced many
      parts of the C++ Standard Library, though no longer is actively maintained and
      is now mostly integrated into the C++ standard library itself. It provides four
      components called algorithms, containers, functors, and iterators.
    prefix: 'vendors provide C++ compilers.


      '
    suffix: '


      The STL provides a set of comm'
    type: TextQuoteSelector
  selector_sha256: sha256:0b9926725ea7a3dd6c9b386ff71ed7f74ee9b38ef396e95fcc5a2dd15b03574f
  snapshot_sha256: sha256:370ef0beecf12cb5bb3548370e2581a8cfee17270e96fdbb85877b36b9d9f4a7
- evidence_id: evidence-a18f9c4f3194
  position:
    end: 1704
    start: 1407
    type: TextPositionSelector
  quote_sha256: sha256:933928891786fb085334153aad7a63dc1c8571f5191b593019bf85de4b51fba8
  selector:
    exact: The STL contains sequence containers and associative containers. The containers
      are objects that store data. The standard sequence containers include vector,
      deque, and list. The standard associative containers are set, multiset, map,
      multimap, hash_set, hash_map, hash_multiset and hash_multimap.
    prefix: 'the complexity of the library.


      '
    suffix: ' There are also container adapto'
    type: TextQuoteSelector
  selector_sha256: sha256:1ad0106b01ea325ce057862956f97d48677c3a55c12657bfd4d238660d6976b1
  snapshot_sha256: sha256:370ef0beecf12cb5bb3548370e2581a8cfee17270e96fdbb85877b36b9d9f4a7
extractor: utf8/1
id: web-computer-science-cpp-course
local:
  file_sha256: sha256:370ef0beecf12cb5bb3548370e2581a8cfee17270e96fdbb85877b36b9d9f4a7
  path_ref: local-sidecar:public/web-computer-science-cpp-course
media_type: text/plain
origin: external
raw_ref:
  path: archive/raw/370ef0beecf12cb5bb3548370e2581a8cfee17270e96fdbb85877b36b9d9f4a7.txt
  sha256: sha256:370ef0beecf12cb5bb3548370e2581a8cfee17270e96fdbb85877b36b9d9f4a7
read_status: retrieved
retrieval:
  acquisition: local-file
schema_version: source/v1
snapshot_sha256: sha256:370ef0beecf12cb5bb3548370e2581a8cfee17270e96fdbb85877b36b9d9f4a7
source_type: local-file
vault_id: public
---
C++ is a high-level, general-purpose programming language created by Danish computer scientist Bjarne Stroustrup. First released in 1985 as an extension of the C programming language, adding object-oriented (OOP) features, it has since expanded significantly over time adding more OOP and other features; as of 1997 standardization, C++ has added functional features, in addition to facilities for low-level memory manipulation for systems like microcomputers or to make operating systems like Linux or Windows, and even later came features like generic programming (through the use of templates). C++ is usually implemented as a compiled language, and many vendors provide C++ compilers.

The Standard Template Library (STL) was a software library originally designed by Alexander Stepanov for the C++ programming language that influenced many parts of the C++ Standard Library, though no longer is actively maintained and is now mostly integrated into the C++ standard library itself. It provides four components called algorithms, containers, functors, and iterators.

The STL provides a set of common classes for C++, such as containers and associative arrays, that can be used with any built-in type or user-defined type that supports some elementary operations (such as copying and assignment). STL algorithms are independent of containers, which significantly reduces the complexity of the library.

The STL contains sequence containers and associative containers. The containers are objects that store data. The standard sequence containers include vector, deque, and list. The standard associative containers are set, multiset, map, multimap, hash_set, hash_map, hash_multiset and hash_multimap. There are also container adaptors queue, priority_queue, and stack, that are containers with specific interface, using other containers as implementation.

Iterators are the major feature that allow the generality of the STL. For example, an algorithm to reverse a sequence can be implemented using bidirectional iterators, and then the same implementation can be used on lists, vectors and deques.
