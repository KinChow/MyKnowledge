---
archive_policy: text-only
attachments:
- filename: web-computer-science-memento-pattern.txt
  kind: document
  media_type: text/plain
  role: original
  sha256: sha256:4f5b3145dcbbedeffc6637969610677581868f38591981fa36730dcabca62943
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-24fca6832d34
  position:
    end: 137
    start: 0
    type: TextPositionSelector
  quote_sha256: sha256:db418f75b92f251011d6ce61b13988b732aaea60f374dc807dadf5e89f07f369
  selector:
    exact: The memento pattern is a software design pattern in the field of object-oriented
      programming that allows reverting the state of an object
    prefix: ''
    suffix: . Uses of this design pattern in
    type: TextQuoteSelector
  selector_sha256: sha256:5de1ba115cee5f105828c4210dc90a8c1f513c4ac1686e0780d014f6cd9e463f
  snapshot_sha256: sha256:4f5b3145dcbbedeffc6637969610677581868f38591981fa36730dcabca62943
extractor: utf8/1
id: web-computer-science-memento-pattern
local:
  file_sha256: sha256:4f5b3145dcbbedeffc6637969610677581868f38591981fa36730dcabca62943
  path_ref: local-sidecar:public/web-computer-science-memento-pattern
media_type: text/plain
origin: external
raw_ref:
  path: archive/raw/4f5b3145dcbbedeffc6637969610677581868f38591981fa36730dcabca62943.txt
  sha256: sha256:4f5b3145dcbbedeffc6637969610677581868f38591981fa36730dcabca62943
read_status: retrieved
retrieval:
  acquisition: local-file
schema_version: source/v1
snapshot_sha256: sha256:4f5b3145dcbbedeffc6637969610677581868f38591981fa36730dcabca62943
source_type: local-file
vault_id: public
---
The memento pattern is a software design pattern in the field of object-oriented programming that allows reverting the state of an object. Uses of this design pattern include undo, version control, and serialization.

The memento pattern is implemented with three objects: the originator, a caretaker and a memento. The originator is some object that has an internal state. The caretaker is going to do something to the originator, but wants to be able to easily bring back the prior state. The caretaker first asks the originator for a memento object. Then it does whatever operation (or sequence of operations) it was going to do. To roll back to the state before the operations, it returns the memento object to the originator. The memento object itself is immutable. When using this pattern, care should be taken if the originator may change other objects or resources - the memento pattern operates on a single object.

One classic example of this pattern is the pseudorandom number generator (PRNG). In this case, each consumer of the PRNG serves as a caretaker who can initialize the PRNG (the originator) with a particular seed (the memento) to produce an identical sequence of pseudorandom numbers.
