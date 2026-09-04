---
archive_policy: text-only
attachments:
- filename: wiki-non-local-means.txt
  kind: document
  media_type: text/plain
  role: original
  sha256: sha256:1ecf5024d2368a37e5535883705ace1132f96606f5c61f01345740b0485b6e68
confidentiality: public
domain: multimedia
evidence_items:
- evidence_id: evidence-5a2113b47195
  position:
    end: 244
    start: 80
    type: TextPositionSelector
  quote_sha256: sha256:40dfdee05efff8ac62e9328d93db2ae1bf4b97a93ee111aa07e84c769200c8bf
  selector:
    exact: The computational complexity of the non-local means algorithm is quadratic
      in the number of pixels in the image, making it particularly expensive to apply
      directly.
    prefix: 'l_means (retrieved 2026-09-04)


      '
    suffix: ' Several techniques were propose'
    type: TextQuoteSelector
  selector_sha256: sha256:07957fc41246f231d8bb790b9f2b52a1d96fbda92cde35b184cedb7906f2a2bd
  snapshot_sha256: sha256:1ecf5024d2368a37e5535883705ace1132f96606f5c61f01345740b0485b6e68
extractor: utf8/1
id: wiki-non-local-means
local:
  file_sha256: sha256:1ecf5024d2368a37e5535883705ace1132f96606f5c61f01345740b0485b6e68
  path_ref: local-sidecar:public/wiki-non-local-means
media_type: text/plain
origin: external
raw_ref:
  path: archive/raw/1ecf5024d2368a37e5535883705ace1132f96606f5c61f01345740b0485b6e68.txt
  sha256: sha256:1ecf5024d2368a37e5535883705ace1132f96606f5c61f01345740b0485b6e68
read_status: retrieved
retrieval:
  acquisition: local-file
schema_version: source/v1
snapshot_sha256: sha256:1ecf5024d2368a37e5535883705ace1132f96606f5c61f01345740b0485b6e68
source_type: local-file
vault_id: public
---
# Source: https://en.wikipedia.org/wiki/Non-local_means (retrieved 2026-09-04)

The computational complexity of the non-local means algorithm is quadratic in the number of pixels in the image, making it particularly expensive to apply directly. Several techniques were proposed to speed up execution. One simple variant consists of restricting the computation of the mean for each pixel to a search window centred on the pixel itself, instead of the whole image.
