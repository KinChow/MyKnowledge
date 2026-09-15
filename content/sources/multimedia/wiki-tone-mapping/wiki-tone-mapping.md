---
archive_policy: text-only
attachments:
- filename: wiki-tone-mapping.txt
  kind: document
  media_type: text/plain
  role: original
  sha256: sha256:3fe116d85d8721842c18fffb7f905f31a4c4394f2008db011491c7f66f836850
confidentiality: public
domain: multimedia
evidence_items:
- evidence_id: evidence-0682d4015b96
  position:
    end: 303
    start: 77
    type: TextPositionSelector
  selector:
    exact: Tone mapping is a technique used in image processing and computer graphics
      to map one set of colors to another to approximate the appearance of high-dynamic-range
      (HDR) images in a medium that has a more limited dynamic range.
    prefix: 'mapping (retrieved 2026-09-04)


      '
    suffix: '


      Tone mapping addresses the pro'
    type: TextQuoteSelector
  snapshot_sha256: sha256:3fe116d85d8721842c18fffb7f905f31a4c4394f2008db011491c7f66f836850
- evidence_id: evidence-cb52956d0035
  position:
    end: 1081
    start: 527
    type: TextPositionSelector
  selector:
    exact: 'Local (or spatially varying) operators: the parameters of the non-linear
      function change in each pixel, according to features extracted from the surrounding
      parameters. In other words, the effect of the algorithm changes in each pixel
      according to the local features of the image. Those algorithms are more complicated
      than the global ones; they can show artifacts (e.g. halo effect and ringing);
      and the output can look unrealistic, but they can (if used correctly) provide
      the best performance, since human vision is mainly sensitive to local contrast.'
    prefix: 'te the original scene content.


      '
    suffix: '


      A simple example of global ton'
    type: TextQuoteSelector
  snapshot_sha256: sha256:3fe116d85d8721842c18fffb7f905f31a4c4394f2008db011491c7f66f836850
- evidence_id: evidence-5f91df4675bb
  position:
    end: 1261
    start: 1083
    type: TextPositionSelector
  selector:
    exact: A simple example of global tone mapping filter is Vout = Vin/(Vin+1) (Reinhard),
      where Vin is the luminance of the original pixel and Vout is the luminance of
      the filtered pixel.
    prefix: 'y sensitive to local contrast.


      '
    suffix: '


      Those tone mapping methods usu'
    type: TextQuoteSelector
  snapshot_sha256: sha256:3fe116d85d8721842c18fffb7f905f31a4c4394f2008db011491c7f66f836850
extractor: utf8/1
id: wiki-tone-mapping
local:
  file_sha256: sha256:3fe116d85d8721842c18fffb7f905f31a4c4394f2008db011491c7f66f836850
  path_ref: local-sidecar:public/wiki-tone-mapping
media_type: text/plain
origin: external
raw_ref:
  path: archive/raw/3fe116d85d8721842c18fffb7f905f31a4c4394f2008db011491c7f66f836850.txt
read_status: retrieved
retrieval:
  acquisition: local-file
schema_version: source/v1
snapshot_sha256: sha256:3fe116d85d8721842c18fffb7f905f31a4c4394f2008db011491c7f66f836850
source_type: local-file
vault_id: public
---
# Source: https://en.wikipedia.org/wiki/Tone_mapping (retrieved 2026-09-04)

Tone mapping is a technique used in image processing and computer graphics to map one set of colors to another to approximate the appearance of high-dynamic-range (HDR) images in a medium that has a more limited dynamic range.

Tone mapping addresses the problem of strong contrast reduction from the scene radiance to the displayable range while preserving the image details and color appearance important to appreciate the original scene content.

Local (or spatially varying) operators: the parameters of the non-linear function change in each pixel, according to features extracted from the surrounding parameters. In other words, the effect of the algorithm changes in each pixel according to the local features of the image. Those algorithms are more complicated than the global ones; they can show artifacts (e.g. halo effect and ringing); and the output can look unrealistic, but they can (if used correctly) provide the best performance, since human vision is mainly sensitive to local contrast.

A simple example of global tone mapping filter is Vout = Vin/(Vin+1) (Reinhard), where Vin is the luminance of the original pixel and Vout is the luminance of the filtered pixel.

Those tone mapping methods usually produce very sharp images, which preserve very well small contrast details; however, this is often done at the cost of flattening an overall image contrast, and may as a side effect produce halo-like glows around dark objects.
