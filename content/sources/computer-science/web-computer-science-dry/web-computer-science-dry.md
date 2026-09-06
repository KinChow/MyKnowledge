---
archive_policy: text-only
attachments:
- filename: web-computer-science-dry.txt
  kind: document
  media_type: text/plain
  role: original
  sha256: sha256:bedfa360a7ea40e91575708fbef84f8fae9fff219f6c43f854ccbcf340d9a59d
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-3e823b953bf6
  position:
    end: 274
    start: 0
    type: TextPositionSelector
  quote_sha256: sha256:9a02465ccb69a251380f7c436260834dde73572784f7d4acd88817256de800c0
  selector:
    exact: '"Don''t repeat yourself" (DRY) is a principle of software development
      aimed at reducing repetition of information which is likely to change, replacing
      it with abstractions that are less likely to change, or using data normalization
      which avoids redundancy in the first place.'
    prefix: ''
    suffix: '


      The DRY principle is stated as'
    type: TextQuoteSelector
  selector_sha256: sha256:e19ef985e1b30d196e405504356bfc435ffbc16e2e8dd0937cd33a2bdf1da602
  snapshot_sha256: sha256:bedfa360a7ea40e91575708fbef84f8fae9fff219f6c43f854ccbcf340d9a59d
- evidence_id: evidence-66159e87920c
  position:
    end: 515
    start: 276
    type: TextPositionSelector
  quote_sha256: sha256:0f1e5e7a7a6303b5cbac64b3e98c497661733c57798ecb5f0977c298085b1d05
  selector:
    exact: The DRY principle is stated as "Every piece of knowledge must have a single,
      unambiguous, authoritative representation within a system". The principle has
      been formulated by Andy Hunt and Dave Thomas in their book The Pragmatic Programmer.
    prefix: 'redundancy in the first place.


      '
    suffix: ' They apply it quite broadly to '
    type: TextQuoteSelector
  selector_sha256: sha256:68c70da4f68a346dc69c1aa56cde090be98438ec241fca2ed9bd88de6c2cd4b4
  snapshot_sha256: sha256:bedfa360a7ea40e91575708fbef84f8fae9fff219f6c43f854ccbcf340d9a59d
extractor: utf8/1
id: web-computer-science-dry
local:
  file_sha256: sha256:bedfa360a7ea40e91575708fbef84f8fae9fff219f6c43f854ccbcf340d9a59d
  path_ref: local-sidecar:public/web-computer-science-dry
media_type: text/plain
origin: external
raw_ref:
  path: archive/raw/bedfa360a7ea40e91575708fbef84f8fae9fff219f6c43f854ccbcf340d9a59d.txt
  sha256: sha256:bedfa360a7ea40e91575708fbef84f8fae9fff219f6c43f854ccbcf340d9a59d
read_status: retrieved
retrieval:
  acquisition: local-file
schema_version: source/v1
snapshot_sha256: sha256:bedfa360a7ea40e91575708fbef84f8fae9fff219f6c43f854ccbcf340d9a59d
source_type: local-file
vault_id: public
---
"Don't repeat yourself" (DRY) is a principle of software development aimed at reducing repetition of information which is likely to change, replacing it with abstractions that are less likely to change, or using data normalization which avoids redundancy in the first place.

The DRY principle is stated as "Every piece of knowledge must have a single, unambiguous, authoritative representation within a system". The principle has been formulated by Andy Hunt and Dave Thomas in their book The Pragmatic Programmer. They apply it quite broadly to include database schemas, test plans, the build system, even documentation. When the DRY principle is applied successfully, a modification of any single element of a system does not require a change in other logically unrelated elements. Additionally, elements that are logically related all change predictably and uniformly, and are thus kept in sync.

A particular case of DRY is the single choice principle. It was defined by Bertrand Meyer as: "Whenever a software system must support a set of alternatives, one and only one module in the system should know their exhaustive list."

The opposing view to DRY is called WET, a backronym commonly taken to stand for write everything twice (alternatively write every time, we enjoy typing or waste everyone's time). WET solutions are common in multi-tiered architectures where a developer may be tasked with, for example, adding a comment field on a form in a web application. The text string "comment" might be repeated in the label, the HTML tag, in a read function name, a private variable, database DDL, queries, and so on. A DRY approach eliminates that redundancy by using frameworks that reduce or eliminate all those editing tasks except the most important ones, leaving the extensibility of adding new knowledge variables in one place.
