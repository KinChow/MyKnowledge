---
archive_policy: text-only
attachments:
- filename: wiki-demosaicing.txt
  kind: document
  media_type: text/plain
  role: original
  sha256: sha256:d2e32e18644b22b99fd033cec167d5b6719395501b390a63349542fc34e06b7b
confidentiality: public
domain: multimedia
evidence_items:
- evidence_id: evidence-1b4036ae3965
  position:
    end: 330
    start: 76
    type: TextPositionSelector
  quote_sha256: sha256:dac32fe23df218c37602fdc2596f522bd9d43d8a10979231c5227603701c726a
  selector:
    exact: Demosaicing, also known as color reconstruction, is a digital image processing
      algorithm used to reconstruct a full color image from the incomplete color samples
      output from an image sensor overlaid with a color filter array (CFA) such as
      a Bayer filter.
    prefix: 'saicing (retrieved 2026-09-04)


      '
    suffix: ' It is also known as CFA interpo'
    type: TextQuoteSelector
  selector_sha256: sha256:e13b67566fb8488b21e8b3f44280eb129c9178cf5a5f651f17a943558f05b65a
  snapshot_sha256: sha256:d2e32e18644b22b99fd033cec167d5b6719395501b390a63349542fc34e06b7b
- evidence_id: evidence-97ea187b1d05
  position:
    end: 878
    start: 584
    type: TextPositionSelector
  quote_sha256: sha256:e99e39028ad9fe4f417a1f8ce4a1405fa4ae0e762cdebdaf064d78c418b18f9b
  selector:
    exact: Since each pixel of the sensor is behind a color filter, the output is
      an array of pixel values, each indicating a raw intensity of one of the three
      filter colors. Thus, an algorithm is needed to estimate for each pixel the color
      levels for all color components, rather than a single component.
    prefix: 'images into a viewable format.


      '
    suffix: '


      To reconstruct a full color im'
    type: TextQuoteSelector
  selector_sha256: sha256:ae56d5f0d020404f44bf83dd4ce6e97287dd1e5ca5c662683bf61ace14998819
  snapshot_sha256: sha256:d2e32e18644b22b99fd033cec167d5b6719395501b390a63349542fc34e06b7b
- evidence_id: evidence-453b0e3eba11
  position:
    end: 1386
    start: 1026
    type: TextPositionSelector
  quote_sha256: sha256:1ec3650d91f8db73f26c16724d5014d0cb5725f86e92245b1dd62e17561a1f42
  selector:
    exact: More sophisticated demosaicing algorithms exploit the spatial and/or spectral
      correlation of pixels within a color image. Spatial correlation is the tendency
      of pixels to assume similar color values within a small homogeneous region of
      an image. Spectral correlation is the dependency between the pixel values of
      different color planes in a small image region.
    prefix: ' needed to fill in the blanks.


      '
    suffix: '

      '
    type: TextQuoteSelector
  selector_sha256: sha256:4ad0ab63956161a7a1e2e7e46609f306511b8995445714398fbebbdd3406748d
  snapshot_sha256: sha256:d2e32e18644b22b99fd033cec167d5b6719395501b390a63349542fc34e06b7b
extractor: utf8/1
id: wiki-demosaicing
local:
  file_sha256: sha256:d2e32e18644b22b99fd033cec167d5b6719395501b390a63349542fc34e06b7b
  path_ref: local-sidecar:public/wiki-demosaicing
media_type: text/plain
origin: external
raw_ref:
  path: archive/raw/d2e32e18644b22b99fd033cec167d5b6719395501b390a63349542fc34e06b7b.txt
  sha256: sha256:d2e32e18644b22b99fd033cec167d5b6719395501b390a63349542fc34e06b7b
read_status: retrieved
retrieval:
  acquisition: local-file
schema_version: source/v1
snapshot_sha256: sha256:d2e32e18644b22b99fd033cec167d5b6719395501b390a63349542fc34e06b7b
source_type: local-file
vault_id: public
---
# Source: https://en.wikipedia.org/wiki/Demosaicing (retrieved 2026-09-04)

Demosaicing, also known as color reconstruction, is a digital image processing algorithm used to reconstruct a full color image from the incomplete color samples output from an image sensor overlaid with a color filter array (CFA) such as a Bayer filter. It is also known as CFA interpolation or debayering.

Most modern digital cameras acquire images using a single image sensor overlaid with a CFA, so demosaicing is part of the processing pipeline required to render these images into a viewable format.

Since each pixel of the sensor is behind a color filter, the output is an array of pixel values, each indicating a raw intensity of one of the three filter colors. Thus, an algorithm is needed to estimate for each pixel the color levels for all color components, rather than a single component.

To reconstruct a full color image from the data collected by the color filtering array, a form of interpolation is needed to fill in the blanks.

More sophisticated demosaicing algorithms exploit the spatial and/or spectral correlation of pixels within a color image. Spatial correlation is the tendency of pixels to assume similar color values within a small homogeneous region of an image. Spectral correlation is the dependency between the pixel values of different color planes in a small image region.
