---
archive_policy: text-only
attachments:
- filename: web-computer-science-factory-pattern.txt
  kind: document
  media_type: text/plain
  role: original
  sha256: sha256:1b628712efc62ea34bad8471993c6161900d05e828b3b3dd7e3e67890954fa35
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-338be05a0097
  position:
    end: 195
    start: 32
    type: TextPositionSelector
  quote_sha256: sha256:ac1221966dd203e48e02c57f700263b397d6d98460c56f03c8b4353cfe5163c2
  selector:
    exact: the factory method pattern is a design pattern that uses factory methods
      to deal with the problem of creating objects without having to specify their
      exact classes
    prefix: 'In object-oriented programming, '
    suffix: . Rather than by calling a const
    type: TextQuoteSelector
  selector_sha256: sha256:2f9d0eb798eeed61e65672bc6cb461fe526f9dba512e3d615083275a90adc934
  snapshot_sha256: sha256:1b628712efc62ea34bad8471993c6161900d05e828b3b3dd7e3e67890954fa35
extractor: utf8/1
id: web-computer-science-factory-pattern
local:
  file_sha256: sha256:1b628712efc62ea34bad8471993c6161900d05e828b3b3dd7e3e67890954fa35
  path_ref: local-sidecar:public/web-computer-science-factory-pattern
media_type: text/plain
origin: external
raw_ref:
  path: archive/raw/1b628712efc62ea34bad8471993c6161900d05e828b3b3dd7e3e67890954fa35.txt
  sha256: sha256:1b628712efc62ea34bad8471993c6161900d05e828b3b3dd7e3e67890954fa35
read_status: retrieved
retrieval:
  acquisition: local-file
schema_version: source/v1
snapshot_sha256: sha256:1b628712efc62ea34bad8471993c6161900d05e828b3b3dd7e3e67890954fa35
source_type: local-file
vault_id: public
---
In object-oriented programming, the factory method pattern is a design pattern that uses factory methods to deal with the problem of creating objects without having to specify their exact classes. Rather than by calling a constructor, this is accomplished by invoking a factory method to create an object. Factory methods can be specified in an interface and implemented by subclasses or implemented in a base class and optionally overridden by subclasses. It is one of the 23 classic design patterns described in the book Design Patterns and is subcategorized as a creational pattern. According to Design Patterns: Elements of Reusable Object-Oriented Software: "Define an interface for creating an object, but let subclasses decide which class to instantiate. Factory method lets a class defer instantiation to subclasses." The factory method design pattern solves problems such as: how can an object's subclasses redefine its subsequent and distinct implementation? How can an object's instantiation be deferred to a subclass? The pattern involves creation of a factory method within the superclass that defers the object's creation to a subclass's factory method, and creating an object by calling a factory method instead of directly calling a constructor.
