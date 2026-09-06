---
archive_policy: text-only
attachments:
- filename: web-computer-science-strategy-pattern.txt
  kind: document
  media_type: text/plain
  role: original
  sha256: sha256:596a0973d1870e20092c67be12715b073b04ed1434b0e12b805a06877367664f
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-2b9d28717063
  position:
    end: 167
    start: 25
    type: TextPositionSelector
  quote_sha256: sha256:1144c51c6f9787c33115bc0eb99306961a7d538e5d790f79abdf020977bade23
  selector:
    exact: the strategy pattern (also known as the policy pattern) is a behavioral
      software design pattern that enables selecting an algorithm at runtime
    prefix: 'In computer programming, '
    suffix: . Instead of implementing a sing
    type: TextQuoteSelector
  selector_sha256: sha256:8aa632580eaa914dd516ea20ac196c87c6b764ff61d6a37875170b8844321d0a
  snapshot_sha256: sha256:596a0973d1870e20092c67be12715b073b04ed1434b0e12b805a06877367664f
extractor: utf8/1
id: web-computer-science-strategy-pattern
local:
  file_sha256: sha256:596a0973d1870e20092c67be12715b073b04ed1434b0e12b805a06877367664f
  path_ref: local-sidecar:public/web-computer-science-strategy-pattern
media_type: text/plain
origin: external
raw_ref:
  path: archive/raw/596a0973d1870e20092c67be12715b073b04ed1434b0e12b805a06877367664f.txt
  sha256: sha256:596a0973d1870e20092c67be12715b073b04ed1434b0e12b805a06877367664f
read_status: retrieved
retrieval:
  acquisition: local-file
schema_version: source/v1
snapshot_sha256: sha256:596a0973d1870e20092c67be12715b073b04ed1434b0e12b805a06877367664f
source_type: local-file
vault_id: public
---
In computer programming, the strategy pattern (also known as the policy pattern) is a behavioral software design pattern that enables selecting an algorithm at runtime. Instead of implementing a single algorithm directly, code receives runtime instructions as to which in a family of algorithms to use. Strategy lets the algorithm vary independently from clients that use it. Strategy is one of the patterns included in the influential book Design Patterns by Gamma et al. that popularized the concept of using design patterns to describe how to design flexible and reusable object-oriented software. Deferring the decision about which algorithm to use until runtime allows the calling code to be more flexible and reusable.

Typically, the strategy pattern stores a reference to code in a data structure and retrieves it. This can be achieved by mechanisms such as the native function pointer, the first-class function, classes or class instances in object-oriented programming languages, or accessing the language implementation's internal storage of code via reflection.

The strategy pattern uses composition instead of inheritance. In the strategy pattern, behaviors are defined as separate interfaces and specific classes that implement these interfaces. This allows better decoupling between the behavior and the class that uses the behavior. The behavior can be changed without breaking the classes that use it, and the classes can switch between behaviors by changing the specific implementation used without requiring any significant code changes. Behaviors can also be changed at runtime as well as at design-time. For instance, a car object's brake behavior can be changed from BrakeWithABS() to Brake() by changing the brakeBehavior member.
