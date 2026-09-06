---
archive_policy: text-only
attachments:
- filename: web-computer-science-observer-pattern.txt
  kind: document
  media_type: text/plain
  role: original
  sha256: sha256:dd2323c1caac5dace33f47a6cf5c8242931812b65fb0ca502da8a0435b29e05f
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-334b0ce05d11
  position:
    end: 133
    start: 45
    type: TextPositionSelector
  quote_sha256: sha256:2b1cbac77c34283ee38c2b1399e7538bfded2cd5a9b5968e005b51f447d6ade9
  selector:
    exact: the observer pattern is a software design pattern in which an object, called
      the subject
    prefix: 'esign and software engineering, '
    suffix: ' (also known as event source or '
    type: TextQuoteSelector
  selector_sha256: sha256:de3afadb7931493f7ac8a5855f6050ea994b8bddeb191f87d048d2a1ebf26334
  snapshot_sha256: sha256:dd2323c1caac5dace33f47a6cf5c8242931812b65fb0ca502da8a0435b29e05f
extractor: utf8/1
id: web-computer-science-observer-pattern
local:
  file_sha256: sha256:dd2323c1caac5dace33f47a6cf5c8242931812b65fb0ca502da8a0435b29e05f
  path_ref: local-sidecar:public/web-computer-science-observer-pattern
media_type: text/plain
origin: external
raw_ref:
  path: archive/raw/dd2323c1caac5dace33f47a6cf5c8242931812b65fb0ca502da8a0435b29e05f.txt
  sha256: sha256:dd2323c1caac5dace33f47a6cf5c8242931812b65fb0ca502da8a0435b29e05f
read_status: retrieved
retrieval:
  acquisition: local-file
schema_version: source/v1
snapshot_sha256: sha256:dd2323c1caac5dace33f47a6cf5c8242931812b65fb0ca502da8a0435b29e05f
source_type: local-file
vault_id: public
---
In software design and software engineering, the observer pattern is a software design pattern in which an object, called the subject (also known as event source or event stream), maintains a list of its dependents, called observers (also known as event sinks), and automatically notifies them of any state changes, typically by calling one of their methods. The subject knows its observers through a standardized interface and manages the subscription list directly.

The observer design pattern is a behavioural pattern listed among the 23 well-known Gang of Four design patterns that address recurring design challenges in order to design flexible and reusable object-oriented software, yielding objects that are easier to implement, change, test, and reuse.

The observer pattern addresses the following requirements:
- A one-to-many dependency between objects should be defined without making the objects tightly coupled.
- When one object changes state, an open-ended number of dependent objects should be updated automatically.
- An object can notify multiple other objects.

This pattern creates a one-to-many dependency where multiple observers can listen to a single subject, but the coupling is typically synchronous and direct - the subject calls observer methods when changes occur, though asynchronous implementations using event queues are possible. Unlike the publish-subscribe pattern, there is no intermediary broker; the subject and observers have direct references to each other.

It is commonly used to implement event handling systems in event-driven programming, particularly in-process systems like GUI toolkits or MVC frameworks. This makes the pattern well-suited to processing data that arrives unpredictably - such as user input, HTTP requests, GPIO signals, updates from distributed databases, or changes in a GUI model.
