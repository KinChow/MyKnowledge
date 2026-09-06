---
archive_policy: text-only
attachments:
- filename: web-computer-science-command-pattern.txt
  kind: document
  media_type: text/plain
  role: original
  sha256: sha256:b230788fadc1ccad47836514a8f4bd24c4817bd7a4110ec930f8df9dd478b68c
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-30fa1d2cc7b2
  position:
    end: 204
    start: 32
    type: TextPositionSelector
  quote_sha256: sha256:e522222e60fa65d7bdd1ca8b2f94dac13ed35205dfafe0a4e116de2d527025f4
  selector:
    exact: the command pattern is a behavioral design pattern in which an object is
      used to encapsulate all information needed to perform an action or trigger an
      event at a later time
    prefix: 'In object-oriented programming, '
    suffix: '. This information includes the '
    type: TextQuoteSelector
  selector_sha256: sha256:0b1c75fa8545788d158093ea65aed4c41a891050e88e919ab691818cec9265ff
  snapshot_sha256: sha256:b230788fadc1ccad47836514a8f4bd24c4817bd7a4110ec930f8df9dd478b68c
extractor: utf8/1
id: web-computer-science-command-pattern
local:
  file_sha256: sha256:b230788fadc1ccad47836514a8f4bd24c4817bd7a4110ec930f8df9dd478b68c
  path_ref: local-sidecar:public/web-computer-science-command-pattern
media_type: text/plain
origin: external
raw_ref:
  path: archive/raw/b230788fadc1ccad47836514a8f4bd24c4817bd7a4110ec930f8df9dd478b68c.txt
  sha256: sha256:b230788fadc1ccad47836514a8f4bd24c4817bd7a4110ec930f8df9dd478b68c
read_status: retrieved
retrieval:
  acquisition: local-file
schema_version: source/v1
snapshot_sha256: sha256:b230788fadc1ccad47836514a8f4bd24c4817bd7a4110ec930f8df9dd478b68c
source_type: local-file
vault_id: public
---
In object-oriented programming, the command pattern is a behavioral design pattern in which an object is used to encapsulate all information needed to perform an action or trigger an event at a later time. This information includes the method name, the object that owns the method and values for the method parameters.

Four terms always associated with the command pattern are command, receiver, invoker and client. A command object knows about receiver and invokes a method of the receiver. Values for parameters of the receiver method are stored in the command. The receiver object to execute these methods is also stored in the command object by aggregation. The receiver then does the work when the execute() method in command is called. An invoker object knows how to execute a command, and optionally does bookkeeping about the command execution. The invoker does not know anything about a concrete command, it knows only about the command interface. Invoker object(s), command objects and receiver objects are held by a client object. The client decides which receiver objects it assigns to the command objects, and which commands it assigns to the invoker. The client decides which commands to execute at which points. To execute a command, it passes the command object to the invoker object.

The command design pattern is one of the twenty-three well-known GoF design patterns that describe how to solve recurring design problems to design flexible and reusable object-oriented software, that is, objects that are easier to implement, change, test, and reuse. Using the command design pattern can solve these problems: Coupling the invoker of a request to a particular request should be avoided. That is, hard-wired requests should be avoided. It should be possible to configure an object (that invokes a request) with a request. Implementing (hard-wiring) a request directly into a class is inflexible because it couples the class to a particular request at compile-time, which makes it impossible to specify a request at run-time.
