---
archive_policy: text-only
attachments:
- filename: wiki-noise-reduction.txt
  kind: document
  media_type: text/plain
  role: original
  sha256: sha256:bf07555f2b3be2e2d2d967d5fd80c35e17d225807d09c9de73d31ed49ec15699
confidentiality: public
domain: multimedia
evidence_items:
- evidence_id: evidence-04c098537dac
  position:
    end: 453
    start: 80
    type: TextPositionSelector
  quote_sha256: sha256:442556fc1d1079f7ff330cc8f6dc6dc8ac74cc53f34890eaa07bfaf806a092c5
  selector:
    exact: 'There are many noise reduction algorithms in image processing. In selecting
      a noise reduction algorithm, one must weigh several factors: the available computer
      power and time available; whether sacrificing some real detail is acceptable
      if it allows more noise to be removed; and the characteristics of the noise
      and the detail in the image, to better make those decisions.'
    prefix: 'duction (retrieved 2026-09-04)


      '
    suffix: '


      Another approach for removing '
    type: TextQuoteSelector
  selector_sha256: sha256:cf93742fcad998207b1030e563155118ef7a13b49f3c24c680517d94964aa9f8
  snapshot_sha256: sha256:bf07555f2b3be2e2d2d967d5fd80c35e17d225807d09c9de73d31ed49ec15699
- evidence_id: evidence-b1196b6868bf
  position:
    end: 745
    start: 455
    type: TextPositionSelector
  quote_sha256: sha256:71b0eb63d7d7bf1e4d26243f98d499d77468712261fb3412b994d3b2b024b2b7
  selector:
    exact: Another approach for removing noise is based on non-local averaging of
      all the pixels in an image. In particular, the amount of weighting for a pixel
      is based on the degree of similarity between a small patch centered on that
      pixel and the small patch centered on the pixel being de-noised.
    prefix: 'o better make those decisions.


      '
    suffix: '


      A median filter is an example '
    type: TextQuoteSelector
  selector_sha256: sha256:3dfbc6eabdb1941921a7c3762f16c7f5f94366ca45398ba3cd3f3dde3f263f3c
  snapshot_sha256: sha256:bf07555f2b3be2e2d2d967d5fd80c35e17d225807d09c9de73d31ed49ec15699
- evidence_id: evidence-1f1b599dffe7
  position:
    end: 866
    start: 747
    type: TextPositionSelector
  quote_sha256: sha256:49052ad5369cbcc9ae08d81d62988cf2ab9844d3d939bdd65837af80d9d78d5c
  selector:
    exact: A median filter is an example of a nonlinear filter and, if properly designed,
      is very good at preserving image detail.
    prefix: ' on the pixel being de-noised.


      '
    suffix: ' To run a median filter: conside'
    type: TextQuoteSelector
  selector_sha256: sha256:fa2cf84f8fb611e79bdb7d7238760d8f45b653e6f3ebbe10b6caa1121d3db283
  snapshot_sha256: sha256:bf07555f2b3be2e2d2d967d5fd80c35e17d225807d09c9de73d31ed49ec15699
extractor: utf8/1
id: wiki-noise-reduction
local:
  file_sha256: sha256:bf07555f2b3be2e2d2d967d5fd80c35e17d225807d09c9de73d31ed49ec15699
  path_ref: local-sidecar:public/wiki-noise-reduction
media_type: text/plain
origin: external
raw_ref:
  path: archive/raw/bf07555f2b3be2e2d2d967d5fd80c35e17d225807d09c9de73d31ed49ec15699.txt
  sha256: sha256:bf07555f2b3be2e2d2d967d5fd80c35e17d225807d09c9de73d31ed49ec15699
read_status: retrieved
retrieval:
  acquisition: local-file
schema_version: source/v1
snapshot_sha256: sha256:bf07555f2b3be2e2d2d967d5fd80c35e17d225807d09c9de73d31ed49ec15699
source_type: local-file
vault_id: public
---
# Source: https://en.wikipedia.org/wiki/Noise_reduction (retrieved 2026-09-04)

There are many noise reduction algorithms in image processing. In selecting a noise reduction algorithm, one must weigh several factors: the available computer power and time available; whether sacrificing some real detail is acceptable if it allows more noise to be removed; and the characteristics of the noise and the detail in the image, to better make those decisions.

Another approach for removing noise is based on non-local averaging of all the pixels in an image. In particular, the amount of weighting for a pixel is based on the degree of similarity between a small patch centered on that pixel and the small patch centered on the pixel being de-noised.

A median filter is an example of a nonlinear filter and, if properly designed, is very good at preserving image detail. To run a median filter: consider each pixel in the image; sort the neighbouring pixels into order based upon their intensities; replace the original value of the pixel with the median value from the list.
