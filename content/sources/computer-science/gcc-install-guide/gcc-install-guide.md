---
archive_policy: text-only
attachments:
- filename: gcc-install-guide.html
  kind: document
  media_type: text/html
  role: original
  sha256: sha256:816b026ae6443789ea7493988387043a6136cbd439a273863ab2e6fcb164923f
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-75cbde47441e
  position:
    end: 788
    start: 728
    type: TextPositionSelector
  selector:
    exact: The installation procedure itself is broken into five steps.
    prefix: 'nstructions before you proceed.

      '
    suffix: '

      Please note that GCC does not s'
    type: TextQuoteSelector
  snapshot_sha256: sha256:5fdea27e58380c3fe7411ef661e8497305116732e2872da00ad9b49b27ba34c8
- evidence_id: evidence-abe77873564d
  position:
    end: 1085
    start: 932
    type: TextPositionSelector
  selector:
    exact: we suggest that you install GCC into a directory of its own and simply
      remove that directory when you do not need that specific version of GCC any
      longer
    prefix: 'd open a can of worms. Instead, '
    suffix: ', and, if shared libraries are i'
    type: TextQuoteSelector
  snapshot_sha256: sha256:5fdea27e58380c3fe7411ef661e8497305116732e2872da00ad9b49b27ba34c8
- evidence_id: evidence-84712bc48f88
  position:
    end: 1085
    start: 789
    type: TextPositionSelector
  selector:
    exact: Please note that GCC does not support ‘make uninstall’ and probably won’t
      do so in the near future as this would open a can of worms. Instead, we suggest
      that you install GCC into a directory of its own and simply remove that directory
      when you do not need that specific version of GCC any longer
    prefix: 'self is broken into five steps.

      '
    suffix: ', and, if shared libraries are i'
    type: TextQuoteSelector
  snapshot_sha256: sha256:5fdea27e58380c3fe7411ef661e8497305116732e2872da00ad9b49b27ba34c8
extractor: trafilatura/2.2.0
id: gcc-install-guide
media_type: text/html
origin: external
raw_ref:
  path: archive/raw/816b026ae6443789ea7493988387043a6136cbd439a273863ab2e6fcb164923f.html
read_status: retrieved
retrieval:
  acquisition: fetch
  resolved_url: https://gcc.gnu.org/install/
  url: https://gcc.gnu.org/install/
schema_version: source/v1
snapshot_sha256: sha256:5fdea27e58380c3fe7411ef661e8497305116732e2872da00ad9b49b27ba34c8
source_type: doc
vault_id: public
---
The latest version of this document is always available at https://gcc.gnu.org/install/. It refers to the current development sources, instructions for specific released versions are included with the sources.
This document describes the generic installation procedure for GCC as well as detailing some target specific installation instructions.
GCC includes several components that previously were separate distributions with their own installation instructions. This document supersedes all package-specific installation instructions.
Before starting the build/install procedure please check the host/target specific installation notes. We recommend you browse the entire generic installation instructions before you proceed.
The installation procedure itself is broken into five steps.
Please note that GCC does not support ‘make uninstall’ and probably won’t do so in the near future as this would open a can of worms. Instead, we suggest that you install GCC into a directory of its own and simply remove that directory when you do not need that specific version of GCC any longer, and, if shared libraries are installed there as well, no more binaries exist that use them.
Copyright © 1988-2026 Free Software Foundation, Inc.
Permission is granted to copy, distribute and/or modify this document under the terms of the GNU Free Documentation License, Version 1.3 or any later version published by the Free Software Foundation; with no Invariant Sections, the Front-Cover texts being (a) (see below), and with the Back-Cover Texts being (b) (see below). A copy of the license is included in the section entitled “GNU Free Documentation License”.
(a) The FSF’s Front-Cover Text is:
A GNU Manual
(b) The FSF’s Back-Cover Text is:
You have freedom to copy and modify this GNU Manual, like GNU software. Copies published by the Free Software Foundation raise funds for GNU development.
Copyright (C) Free Software Foundation, Inc. Verbatim copying and distribution of this entire article is permitted in any medium, provided this notice is preserved.
These pages are maintained by the GCC team. Last modified 2026-07-21.