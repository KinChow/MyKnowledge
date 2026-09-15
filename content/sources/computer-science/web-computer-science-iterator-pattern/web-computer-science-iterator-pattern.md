---
archive_policy: text-only
attachments:
- filename: web-computer-science-iterator-pattern.txt
  kind: document
  media_type: text/plain
  role: original
  sha256: sha256:9f88098e2da58e286aa113ea3b41d6065d92f3416a87c38fe6fbe8f95a03288b
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-05b5c0c26a06
  position:
    end: 161
    start: 32
    type: TextPositionSelector
  selector:
    exact: the iterator pattern is a design pattern in which an iterator is used to
      traverse a container and access the container's elements
    prefix: 'In object-oriented programming, '
    suffix: . The iterator pattern decouples
    type: TextQuoteSelector
  snapshot_sha256: sha256:9f88098e2da58e286aa113ea3b41d6065d92f3416a87c38fe6fbe8f95a03288b
extractor: utf8/1
id: web-computer-science-iterator-pattern
local:
  file_sha256: sha256:9f88098e2da58e286aa113ea3b41d6065d92f3416a87c38fe6fbe8f95a03288b
  path_ref: local-sidecar:public/web-computer-science-iterator-pattern
media_type: text/plain
origin: external
raw_ref:
  path: archive/raw/9f88098e2da58e286aa113ea3b41d6065d92f3416a87c38fe6fbe8f95a03288b.txt
read_status: retrieved
retrieval:
  acquisition: local-file
schema_version: source/v1
snapshot_sha256: sha256:9f88098e2da58e286aa113ea3b41d6065d92f3416a87c38fe6fbe8f95a03288b
source_type: local-file
vault_id: public
---
In object-oriented programming, the iterator pattern is a design pattern in which an iterator is used to traverse a container and access the container's elements. The iterator pattern decouples algorithms from containers; in some cases, algorithms are necessarily container-specific and thus cannot be decoupled.

For example, the hypothetical algorithm searchForElement() can be implemented generally using a specified type of iterator rather than implementing it as a container-specific algorithm. This allows searchForElement() to be used on any container that supports the required type of iterator.

The essence of the Iterator Pattern is to Provide a way to access the elements of an aggregate object sequentially without exposing its underlying representation. Different iterators can be used to access and traverse an aggregate in different ways. New access and traversal operations can be defined independently by defining new iterators.

The Iterator design pattern is one of the 23 well-known Gang of Four design patterns that describe how to solve recurring design problems to design flexible and reusable object-oriented software, that is, objects that are easier to implement, change, test, and reuse. Defining access and traversal operations in the aggregate interface is inflexible because it commits the aggregate to particular access and traversal operations and makes it impossible to add new operations later without having to change the aggregate interface.
