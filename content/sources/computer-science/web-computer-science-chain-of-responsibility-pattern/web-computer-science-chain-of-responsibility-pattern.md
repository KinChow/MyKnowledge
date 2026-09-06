---
archive_policy: text-only
attachments:
- filename: web-computer-science-chain-of-responsibility-pattern.txt
  kind: document
  media_type: text/plain
  role: original
  sha256: sha256:897a8a2b41966ae13e8d1b2851baf0bee166d85e861501e8b083a67b62dbe1bb
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-7da1c940faf7
  position:
    end: 170
    start: 27
    type: TextPositionSelector
  quote_sha256: sha256:a93e04e37a4977c3b10641aaa71377e07fe9642c682c222c2f04fa0b37eaa159
  selector:
    exact: the chain-of-responsibility pattern is a behavioral design pattern consisting
      of a source of command objects and a series of processing objects
    prefix: 'In object-oriented design, '
    suffix: . Each processing object contain
    type: TextQuoteSelector
  selector_sha256: sha256:7bbf875d724a512f043e4943e7ed1c889094624f22a42ce15f8d46372d5e9c6c
  snapshot_sha256: sha256:897a8a2b41966ae13e8d1b2851baf0bee166d85e861501e8b083a67b62dbe1bb
extractor: utf8/1
id: web-computer-science-chain-of-responsibility-pattern
local:
  file_sha256: sha256:897a8a2b41966ae13e8d1b2851baf0bee166d85e861501e8b083a67b62dbe1bb
  path_ref: local-sidecar:public/web-computer-science-chain-of-responsibility-pattern
media_type: text/plain
origin: external
raw_ref:
  path: archive/raw/897a8a2b41966ae13e8d1b2851baf0bee166d85e861501e8b083a67b62dbe1bb.txt
  sha256: sha256:897a8a2b41966ae13e8d1b2851baf0bee166d85e861501e8b083a67b62dbe1bb
read_status: retrieved
retrieval:
  acquisition: local-file
schema_version: source/v1
snapshot_sha256: sha256:897a8a2b41966ae13e8d1b2851baf0bee166d85e861501e8b083a67b62dbe1bb
source_type: local-file
vault_id: public
---
In object-oriented design, the chain-of-responsibility pattern is a behavioral design pattern consisting of a source of command objects and a series of processing objects. Each processing object contains logic that defines the types of command objects that it can handle; the rest are passed to the next processing object in the chain. A mechanism also exists for adding new processing objects to the end of this chain. This pattern promotes the idea of loose coupling.

The chain-of-responsibility pattern is structurally nearly identical to the decorator pattern, the difference being that for the decorator, all classes handle the request, while for the chain of responsibility, exactly one of the classes in the chain handles the request. This is a strict definition of the Responsibility concept in the Gang of Four Design Patterns book. However, many implementations (such as loggers below, or UI event handling, or servlet filters in Java, etc.) allow several elements in the chain to take responsibility.

The Chain of Responsibility design pattern is one of the twenty-three well-known Gang of Four design patterns that describe common solutions to recurring design problems when designing flexible and reusable object-oriented software, that is, objects that are easier to implement, change, test, and reuse. It solves these problems: Coupling the sender of a request to its receiver should be avoided. It should be possible that more than one receiver can handle a request. The solution is to define a chain of receiver objects having the responsibility, depending on run-time conditions, to either handle a request or forward it to the next receiver on the chain (if any). This enables us to send a request to a chain of receivers without having to know which one handles the request. The request gets passed along the chain until a receiver handles the request. The sender of a request is no longer coupled to a particular receiver.
