---
archive_policy: text-only
attachments:
- filename: web-computer-science-interpreter-pattern.txt
  kind: document
  media_type: text/plain
  role: original
  sha256: sha256:c347edd8da7bd990f93e44a73d7073b07cc24abf4c37dcce065dab628c7c2d92
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-5d69d4a730fc
  position:
    end: 123
    start: 25
    type: TextPositionSelector
  quote_sha256: sha256:9fe66dc8deeebeeee302c38cb61733d66b47de415a689279f7f807757616169f
  selector:
    exact: the interpreter pattern is a design pattern that specifies how to evaluate
      sentences in a language
    prefix: 'In computer programming, '
    suffix: . The basic idea is to have a cl
    type: TextQuoteSelector
  selector_sha256: sha256:94ac5c488f54a18c2afc097dd8926d788993d38f5f18b5d66261ad16fec27b1a
  snapshot_sha256: sha256:c347edd8da7bd990f93e44a73d7073b07cc24abf4c37dcce065dab628c7c2d92
extractor: utf8/1
id: web-computer-science-interpreter-pattern
local:
  file_sha256: sha256:c347edd8da7bd990f93e44a73d7073b07cc24abf4c37dcce065dab628c7c2d92
  path_ref: local-sidecar:public/web-computer-science-interpreter-pattern
media_type: text/plain
origin: external
raw_ref:
  path: archive/raw/c347edd8da7bd990f93e44a73d7073b07cc24abf4c37dcce065dab628c7c2d92.txt
  sha256: sha256:c347edd8da7bd990f93e44a73d7073b07cc24abf4c37dcce065dab628c7c2d92
read_status: retrieved
retrieval:
  acquisition: local-file
schema_version: source/v1
snapshot_sha256: sha256:c347edd8da7bd990f93e44a73d7073b07cc24abf4c37dcce065dab628c7c2d92
source_type: local-file
vault_id: public
---
In computer programming, the interpreter pattern is a design pattern that specifies how to evaluate sentences in a language. The basic idea is to have a class for each symbol (terminal or nonterminal) in a specialized computer language. The syntax tree of a sentence in the language is an instance of the composite pattern and is used to evaluate (interpret) the sentence for a client.

The Interpreter design pattern is one of the twenty-three well-known GoF design patterns that describe how to solve recurring design problems to design flexible and reusable object-oriented software, that is, objects that are easier to implement, change, test, and reuse.

Define a grammar for a simple language by defining an Expression class hierarchy and implementing an interpret() operation. Represent a sentence in the language by an abstract syntax tree (AST) made up of Expression instances. Interpret a sentence by calling interpret() on the AST. The expression objects are composed recursively into a composite/tree structure that is called abstract syntax tree (see Composite pattern). The Interpreter pattern doesn't describe how to build an abstract syntax tree. This can be done either manually by a client or automatically by a parser.

Uses: Specialized database query languages such as SQL. Specialized computer languages that are often used to describe communication protocols. Most general-purpose computer languages actually incorporate several specialized languages.
