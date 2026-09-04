---
archive_policy: text-only
attachments:
- filename: wiki-raw-image-format.txt
  kind: document
  media_type: text/plain
  role: original
  sha256: sha256:e3fbb6c65232fc6e96a7e294cb19e40794ce750d5c88fa03232c8645047f0168
confidentiality: public
domain: multimedia
evidence_items:
- evidence_id: evidence-a67ba30f551a
  position:
    end: 544
    start: 409
    type: TextPositionSelector
  quote_sha256: sha256:30f4e30cd44fc9ad56e67759f1123f3ef44a0363cf4280559645a85b33739bb2
  selector:
    exact: Raw files thus contain the full dynamic range (typically 12- or 14-bit)
      data as read out from each of the camera's image sensor pixels.
    prefix: 'of potentially redundant data.


      '
    suffix: '


      The camera''s sensor is almost '
    type: TextQuoteSelector
  selector_sha256: sha256:a10b03f54028c9dd974a0f0d9248d59f7a88feebc7b82be2fb83ddf323a58e25
  snapshot_sha256: sha256:e3fbb6c65232fc6e96a7e294cb19e40794ce750d5c88fa03232c8645047f0168
- evidence_id: evidence-e17f2ae0d40a
  position:
    end: 739
    start: 546
    type: TextPositionSelector
  quote_sha256: sha256:ca8567e2890d9396d8746a3048e18d34cbcc494cbdae7db8a4019715b7026839
  selector:
    exact: The camera's sensor is almost invariably overlaid with a color filter array
      (CFA), usually a Bayer filter, consisting of a mosaic of a 2x2 matrix of red,
      green, blue and (second) green filters.
    prefix: ' camera''s image sensor pixels.


      '
    suffix: '


      Because of the lack of widespr'
    type: TextQuoteSelector
  selector_sha256: sha256:fc24b4fe41f08eb9ff962ecbff00b0505e93690d7a370047a9e51b0ee1d8ed8c
  snapshot_sha256: sha256:e3fbb6c65232fc6e96a7e294cb19e40794ce750d5c88fa03232c8645047f0168
- evidence_id: evidence-c499a5131665
  position:
    end: 407
    start: 81
    type: TextPositionSelector
  quote_sha256: sha256:a1d7d420da1fc851b23feee50ad1ab13d65f212e493520cd01ceef7646a28faa
  selector:
    exact: A camera raw image file is a file that contains unprocessed data straight
      from a digital camera. Such data can later be changed into a photo, either within
      a digital camera itself or by usage of external tools. Raw files are so named
      because they are not yet processed, and contain large amounts of potentially
      redundant data.
    prefix: '_format (retrieved 2026-09-04)


      '
    suffix: '


      Raw files thus contain the ful'
    type: TextQuoteSelector
  selector_sha256: sha256:a6eee79fa23eef632e3bdabade45974b3e713473faf57567bec1510b337daaab
  snapshot_sha256: sha256:e3fbb6c65232fc6e96a7e294cb19e40794ce750d5c88fa03232c8645047f0168
extractor: utf8/1
id: wiki-raw-image-format
local:
  file_sha256: sha256:e3fbb6c65232fc6e96a7e294cb19e40794ce750d5c88fa03232c8645047f0168
  path_ref: local-sidecar:public/wiki-raw-image-format
media_type: text/plain
origin: external
raw_ref:
  path: archive/raw/e3fbb6c65232fc6e96a7e294cb19e40794ce750d5c88fa03232c8645047f0168.txt
  sha256: sha256:e3fbb6c65232fc6e96a7e294cb19e40794ce750d5c88fa03232c8645047f0168
read_status: retrieved
retrieval:
  acquisition: local-file
schema_version: source/v1
snapshot_sha256: sha256:e3fbb6c65232fc6e96a7e294cb19e40794ce750d5c88fa03232c8645047f0168
source_type: local-file
vault_id: public
---
# Source: https://en.wikipedia.org/wiki/Raw_image_format (retrieved 2026-09-04)

A camera raw image file is a file that contains unprocessed data straight from a digital camera. Such data can later be changed into a photo, either within a digital camera itself or by usage of external tools. Raw files are so named because they are not yet processed, and contain large amounts of potentially redundant data.

Raw files thus contain the full dynamic range (typically 12- or 14-bit) data as read out from each of the camera's image sensor pixels.

The camera's sensor is almost invariably overlaid with a color filter array (CFA), usually a Bayer filter, consisting of a mosaic of a 2x2 matrix of red, green, blue and (second) green filters.

Because of the lack of widespread adoption of a standard raw format, more specialized software may be required to open raw files than for standardized formats like JPEG or TIFF.
