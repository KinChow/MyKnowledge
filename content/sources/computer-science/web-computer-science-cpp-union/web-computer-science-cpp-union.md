---
archive_policy: text-only
attachments:
- filename: web-computer-science-cpp-union.txt
  kind: document
  media_type: text/plain
  role: original
  sha256: sha256:40a0fce62cf1f8956ecbc54f56618c3445bc65d200ca913bf3dc73daf467994c
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-299f8a4a797c
  position:
    end: 96
    start: 0
    type: TextPositionSelector
  quote_sha256: sha256:a3a6b782c2922a57783a449667baaeae1a3359c7b103b07144830e500fd283de
  selector:
    exact: A union is a special class type that can hold only one of its non-static
      data members at a time.
    prefix: ''
    suffix: '


      The class specifier for a unio'
    type: TextQuoteSelector
  selector_sha256: sha256:e062106f09d74ecc30b98abfcca4bccf6bf88cb62bddff8f3f6af1f9fbead155
  snapshot_sha256: sha256:40a0fce62cf1f8956ecbc54f56618c3445bc65d200ca913bf3dc73daf467994c
- evidence_id: evidence-33493e72bb98
  position:
    end: 780
    start: 684
    type: TextPositionSelector
  quote_sha256: sha256:68cd953243fe3ed50a42658c82db37dc1da2cf85c2696271383d9e40cc0db872
  selector:
    exact: It is undefined behavior to read from the member of the union that wasn't
      most recently written.
    prefix: ' members have the same address. '
    suffix: ' Many compilers implement, as a '
    type: TextQuoteSelector
  selector_sha256: sha256:a0369c37ddd93fce95ec59d6be6beb61993d1f4c076af76b744a399bdc798365
  snapshot_sha256: sha256:40a0fce62cf1f8956ecbc54f56618c3445bc65d200ca913bf3dc73daf467994c
extractor: utf8/1
id: web-computer-science-cpp-union
local:
  file_sha256: sha256:40a0fce62cf1f8956ecbc54f56618c3445bc65d200ca913bf3dc73daf467994c
  path_ref: local-sidecar:public/web-computer-science-cpp-union
media_type: text/plain
origin: external
raw_ref:
  path: archive/raw/40a0fce62cf1f8956ecbc54f56618c3445bc65d200ca913bf3dc73daf467994c.txt
  sha256: sha256:40a0fce62cf1f8956ecbc54f56618c3445bc65d200ca913bf3dc73daf467994c
read_status: retrieved
retrieval:
  acquisition: local-file
schema_version: source/v1
snapshot_sha256: sha256:40a0fce62cf1f8956ecbc54f56618c3445bc65d200ca913bf3dc73daf467994c
source_type: local-file
vault_id: public
---
A union is a special class type that can hold only one of its non-static data members at a time.

The class specifier for a union declaration is similar to class or struct declaration. A union can have member functions (including constructors and destructors), but not virtual functions. A union cannot have base classes and cannot be used as a base class.

The union is at least as big as necessary to hold its largest data member, but is usually not larger. The other data members are intended to be allocated in the same bytes as part of that largest member. The details of that allocation are implementation-defined, except that all non-static data members have the same address. It is undefined behavior to read from the member of the union that wasn't most recently written. Many compilers implement, as a non-standard language extension, the ability to read inactive members of a union.

An anonymous union is an unnamed union definition that does not simultaneously define any variables (including objects of the union type, references, or pointers to the union).

The lifetime of a union member begins when the member is made active. If another member was active previously, its lifetime ends.
