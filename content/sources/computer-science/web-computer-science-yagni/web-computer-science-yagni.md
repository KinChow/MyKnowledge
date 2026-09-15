---
archive_policy: text-only
attachments:
- filename: web-computer-science-yagni.txt
  kind: document
  media_type: text/plain
  role: original
  sha256: sha256:781568ca05d4284ca0c58b286dc0c3ea3a49eb8ce8a8528f8eaadeffdd7f2931
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-ab404e6b660d
  position:
    end: 169
    start: 0
    type: TextPositionSelector
  selector:
    exact: '"You aren''t gonna need it" (YAGNI) is a principle which arose from extreme
      programming (XP) that states a programmer should not add functionality until
      deemed necessary.'
    prefix: ''
    suffix: ' Other forms of the phrase inclu'
    type: TextQuoteSelector
  snapshot_sha256: sha256:781568ca05d4284ca0c58b286dc0c3ea3a49eb8ce8a8528f8eaadeffdd7f2931
extractor: utf8/1
id: web-computer-science-yagni
local:
  file_sha256: sha256:781568ca05d4284ca0c58b286dc0c3ea3a49eb8ce8a8528f8eaadeffdd7f2931
  path_ref: local-sidecar:public/web-computer-science-yagni
media_type: text/plain
origin: external
raw_ref:
  path: archive/raw/781568ca05d4284ca0c58b286dc0c3ea3a49eb8ce8a8528f8eaadeffdd7f2931.txt
read_status: retrieved
retrieval:
  acquisition: local-file
schema_version: source/v1
snapshot_sha256: sha256:781568ca05d4284ca0c58b286dc0c3ea3a49eb8ce8a8528f8eaadeffdd7f2931
source_type: local-file
vault_id: public
---
"You aren't gonna need it" (YAGNI) is a principle which arose from extreme programming (XP) that states a programmer should not add functionality until deemed necessary. Other forms of the phrase include "You aren't going to need it" and "You ain't gonna need it".

Ron Jeffries, a co-founder of XP, explained the philosophy: "Always implement things when you actually need them, never when you just foresee that you [will] need them."

YAGNI is a principle behind the XP practice of "do the simplest thing that could possibly work" (DTSTTCPW). It is meant to be used in combination with several other practices, such as continuous refactoring, continuous automated unit testing, and continuous integration. Used without continuous refactoring, it could lead to disorganized code and massive rework, known as technical debt. YAGNI's dependency on supporting practices is part of the original definition of XP.
