---
archive_policy: text-only
attachments:
- filename: wiki-apex-system.txt
  kind: document
  media_type: text/plain
  role: original
  sha256: sha256:60753153f1014ee0c963fb98cd8e4b913e63b1c77595ee25ad243a63481219ed
confidentiality: public
domain: multimedia
evidence_items:
- evidence_id: evidence-d5683985cdc6
  position:
    end: 627
    start: 270
    type: TextPositionSelector
  quote_sha256: sha256:171db05e6e3f7b49015eaba1311e8727f811d133777060b78d51b1db344c42db
  selector:
    exact: The relationship of recommended photographic exposure to a scene's average
      luminance is given by the camera exposure equation A^2/T = B*Sx/K, where A is
      the relative aperture (f-number), T is the exposure time (shutter speed) in
      seconds, B is the scene luminance, Sx is the ASA arithmetic film speed, and
      K is the reflected-light meter calibration constant.
    prefix: 'plifying exposure computation.


      '
    suffix: '


      Taking base-2 logarithms of bo'
    type: TextQuoteSelector
  selector_sha256: sha256:291915ca898561de18662bc096ccbc80bcdf825615487168bd293220edd08900
  snapshot_sha256: sha256:60753153f1014ee0c963fb98cd8e4b913e63b1c77595ee25ad243a63481219ed
- evidence_id: evidence-94fb33e0def3
  position:
    end: 968
    start: 629
    type: TextPositionSelector
  quote_sha256: sha256:76672017e688b1d56398201eea16d871e3f77a067f1d61f659d2babf276ae6bd
  selector:
    exact: 'Taking base-2 logarithms of both sides of the exposure equation and separating
      numerators and denominators reduces exposure calculation to a matter of addition:
      Ev = Av + Tv = Bv + Sv, where Av is the aperture value, Tv is the time value,
      Sv is the speed value (aka sensitivity value), and Bv is the luminance value
      (aka brightness value).'
    prefix: 'ht meter calibration constant.


      '
    suffix: '

      '
    type: TextQuoteSelector
  selector_sha256: sha256:850a0997ba9ad73178189d45f17b6e0d36bf325f6b6fe1fe4394dbabef440c68
  snapshot_sha256: sha256:60753153f1014ee0c963fb98cd8e4b913e63b1c77595ee25ad243a63481219ed
extractor: utf8/1
id: wiki-apex-system
local:
  file_sha256: sha256:60753153f1014ee0c963fb98cd8e4b913e63b1c77595ee25ad243a63481219ed
  path_ref: local-sidecar:public/wiki-apex-system
media_type: text/plain
origin: external
raw_ref:
  path: archive/raw/60753153f1014ee0c963fb98cd8e4b913e63b1c77595ee25ad243a63481219ed.txt
  sha256: sha256:60753153f1014ee0c963fb98cd8e4b913e63b1c77595ee25ad243a63481219ed
read_status: retrieved
retrieval:
  acquisition: local-file
schema_version: source/v1
snapshot_sha256: sha256:60753153f1014ee0c963fb98cd8e4b913e63b1c77595ee25ad243a63481219ed
source_type: local-file
vault_id: public
---
# Source: https://en.wikipedia.org/wiki/APEX_system (retrieved 2026-09-04)

APEX stands for Additive System of Photographic Exposure, which was proposed in the 1960 ASA standard for monochrome film speed, ASA PH2.5-1960, as a means of simplifying exposure computation.

The relationship of recommended photographic exposure to a scene's average luminance is given by the camera exposure equation A^2/T = B*Sx/K, where A is the relative aperture (f-number), T is the exposure time (shutter speed) in seconds, B is the scene luminance, Sx is the ASA arithmetic film speed, and K is the reflected-light meter calibration constant.

Taking base-2 logarithms of both sides of the exposure equation and separating numerators and denominators reduces exposure calculation to a matter of addition: Ev = Av + Tv = Bv + Sv, where Av is the aperture value, Tv is the time value, Sv is the speed value (aka sensitivity value), and Bv is the luminance value (aka brightness value).
