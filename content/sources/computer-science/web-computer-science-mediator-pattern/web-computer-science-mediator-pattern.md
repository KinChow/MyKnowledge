---
archive_policy: text-only
attachments:
- filename: web-computer-science-mediator-pattern.txt
  kind: document
  media_type: text/plain
  role: original
  sha256: sha256:52700d5734943b551e457a664348a234339c27d5debec90c856e830fac33c7f7
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-8ceb83051de3
  position:
    end: 111
    start: 25
    type: TextPositionSelector
  quote_sha256: sha256:898d71b55b00a8c3a554b04a3408d2d9ccc2ea36358981aeb1c91de123865ec3
  selector:
    exact: the mediator pattern defines an object that encapsulates how a set of objects
      interact
    prefix: 'In software engineering, '
    suffix: '. This pattern is considered to '
    type: TextQuoteSelector
  selector_sha256: sha256:f8585aa305b428d2ba6a733c4a90d3e53d0d8f3468ce47249a97c39687e19b25
  snapshot_sha256: sha256:52700d5734943b551e457a664348a234339c27d5debec90c856e830fac33c7f7
extractor: utf8/1
id: web-computer-science-mediator-pattern
local:
  file_sha256: sha256:52700d5734943b551e457a664348a234339c27d5debec90c856e830fac33c7f7
  path_ref: local-sidecar:public/web-computer-science-mediator-pattern
media_type: text/plain
origin: external
raw_ref:
  path: archive/raw/52700d5734943b551e457a664348a234339c27d5debec90c856e830fac33c7f7.txt
  sha256: sha256:52700d5734943b551e457a664348a234339c27d5debec90c856e830fac33c7f7
read_status: retrieved
retrieval:
  acquisition: local-file
schema_version: source/v1
snapshot_sha256: sha256:52700d5734943b551e457a664348a234339c27d5debec90c856e830fac33c7f7
source_type: local-file
vault_id: public
---
In software engineering, the mediator pattern defines an object that encapsulates how a set of objects interact. This pattern is considered to be a behavioral pattern due to the way it can alter the program's running behavior.

The essence of the mediator pattern is to define an object that encapsulates how a set of objects interact. It promotes loose coupling by keeping objects from referring to each other explicitly, and it allows their interaction to be varied independently. Client classes can use the mediator to send messages to other clients, and can receive messages from other clients via an event on the mediator class.

With the mediator pattern, communication between objects is encapsulated within a mediator object. Objects no longer communicate directly with each other, but instead communicate through the mediator. This reduces the dependencies between communicating objects, thereby reducing coupling.

The mediator design pattern is one of the twenty-three well-known design patterns that describe how to solve recurring design problems to design flexible and reusable object-oriented software, that is, objects that are easier to implement, change, test, and reuse. Objects delegate their interaction to a mediator object instead of interacting with each other directly. The objects interact with each other indirectly through a mediator object that controls and coordinates the interaction. This makes the objects loosely coupled. They only refer to and know about their mediator object and have no explicit knowledge of each other.
