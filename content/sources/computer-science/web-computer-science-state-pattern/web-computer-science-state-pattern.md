---
archive_policy: text-only
attachments:
- filename: web-computer-science-state-pattern.txt
  kind: document
  media_type: text/plain
  role: original
  sha256: sha256:895e29c1236e9a83509576a67608661c6a2ff35ba30cb965daa1a6b81bbe5768
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-2a74aa5b6462
  position:
    end: 133
    start: 0
    type: TextPositionSelector
  quote_sha256: sha256:e35a647a4c6a0f27a74051ce86715256226d07d1f4d1f61bc2ab5aa87eff4a08
  selector:
    exact: The state pattern is a behavioral software design pattern that allows an
      object to alter its behavior when its internal state changes
    prefix: ''
    suffix: . This pattern is close to the c
    type: TextQuoteSelector
  selector_sha256: sha256:7038284c19ec4a4771ab11270acf82e075b4c84728d2f9c9a7eb08755eaa5ff8
  snapshot_sha256: sha256:895e29c1236e9a83509576a67608661c6a2ff35ba30cb965daa1a6b81bbe5768
extractor: utf8/1
id: web-computer-science-state-pattern
local:
  file_sha256: sha256:895e29c1236e9a83509576a67608661c6a2ff35ba30cb965daa1a6b81bbe5768
  path_ref: local-sidecar:public/web-computer-science-state-pattern
media_type: text/plain
origin: external
raw_ref:
  path: archive/raw/895e29c1236e9a83509576a67608661c6a2ff35ba30cb965daa1a6b81bbe5768.txt
  sha256: sha256:895e29c1236e9a83509576a67608661c6a2ff35ba30cb965daa1a6b81bbe5768
read_status: retrieved
retrieval:
  acquisition: local-file
schema_version: source/v1
snapshot_sha256: sha256:895e29c1236e9a83509576a67608661c6a2ff35ba30cb965daa1a6b81bbe5768
source_type: local-file
vault_id: public
---
The state pattern is a behavioral software design pattern that allows an object to alter its behavior when its internal state changes. This pattern is close to the concept of finite-state machines. The state pattern can be interpreted as a strategy pattern, which is able to switch a strategy through invocations of methods defined in the pattern's interface.

The Context object delegates state-specific behavior to different State objects. First, Context calls handle(this) on its current (initial) state object (ConcreteStateA), which performs the operation and calls setState(ConcreteStateB) on Context to change context's current state to ConcreteStateB. The next time, Context again calls handle(this) on its current state object (ConcreteStateB), which performs the operation and changes context's current state to ConcreteStateA.

The state pattern is used in computer programming to encapsulate varying behavior for the same object, based on its internal state. This can be a cleaner way for an object to change its behavior at runtime without resorting to conditional statements and thus improve maintainability. New states can be added by defining new state classes. A class can change its behavior at run-time by changing its current state object.

In the class diagram, the Context class doesn't implement state-specific behavior directly. Instead, Context refers to the State interface for performing state-specific behavior (state.handle()), which makes Context independent of how state-specific behavior is implemented. The ConcreteStateA and ConcreteStateB classes implement the State interface, that is, implement (encapsulate) the state-specific behavior for each state.
