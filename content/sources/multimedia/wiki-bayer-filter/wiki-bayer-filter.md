---
archive_policy: text-only
attachments:
- filename: wiki-bayer-filter.txt
  kind: document
  media_type: text/plain
  role: original
  sha256: sha256:3cf1e4976c3115232071e794d895fe0ca80158f2acf16fbbda34e070055cf4da
confidentiality: public
domain: multimedia
evidence_items:
- evidence_id: evidence-429e23e81582
  position:
    end: 196
    start: 77
    type: TextPositionSelector
  quote_sha256: sha256:819de1dfb6c7cb4dd42bcd295077eb3e2407cf8c473b9d2c363b3860a4cb3409
  selector:
    exact: The filter pattern is half green, one quarter red and one quarter blue,
      hence is also called BGGR, RGBG, GRBG, or RGGB.
    prefix: '_filter (retrieved 2026-09-04)


      '
    suffix: ' It is named after its inventor,'
    type: TextQuoteSelector
  selector_sha256: sha256:746696a13ea7b49ca7be676f2f2812057ebbd0acffec1dd651b926e56fa6cf4f
  snapshot_sha256: sha256:3cf1e4976c3115232071e794d895fe0ca80158f2acf16fbbda34e070055cf4da
- evidence_id: evidence-1717e3722229
  position:
    end: 1307
    start: 1159
    type: TextPositionSelector
  quote_sha256: sha256:b3bf58307523ae1c26e823e138a85d535dbf50d47b3d293de68d89138940f606
  selector:
    exact: The most frequent artifact is Moiré, which may appear as repeating patterns,
      color artifacts or pixels arranged in an unrealistic maze-like pattern.
    prefix: 'h does not look like the model. '
    suffix: '

      '
    type: TextQuoteSelector
  selector_sha256: sha256:5f01f4ef8cc2c835bfd25cee3681d65e91210904bdddaf60a3bb3df7c1716179
  snapshot_sha256: sha256:3cf1e4976c3115232071e794d895fe0ca80158f2acf16fbbda34e070055cf4da
- evidence_id: evidence-d3cba69be38a
  position:
    end: 699
    start: 260
    type: TextPositionSelector
  quote_sha256: sha256:4f25bebbd0017ef9e2bc8addfab0b4d83daafd637d9b87e942b22ba9a5232004
  selector:
    exact: Since each pixel is filtered to record only one of three colors, the data
      from each pixel cannot fully specify each of the red, green, and blue values
      on its own. To obtain a full-color image, various demosaicing algorithms can
      be used to interpolate a set of complete red, green, and blue values for each
      pixel. These algorithms make use of the surrounding pixels of the corresponding
      colors to estimate the values for a particular pixel.
    prefix: ' Bryce Bayer of Eastman Kodak.


      '
    suffix: '


      The raw output of Bayer-filter'
    type: TextQuoteSelector
  selector_sha256: sha256:2543a4e76e31d05e28e26ba7f0f76928a9086b677cc231422ef64a22aa614988
  snapshot_sha256: sha256:3cf1e4976c3115232071e794d895fe0ca80158f2acf16fbbda34e070055cf4da
extractor: utf8/1
id: wiki-bayer-filter
local:
  file_sha256: sha256:3cf1e4976c3115232071e794d895fe0ca80158f2acf16fbbda34e070055cf4da
  path_ref: local-sidecar:public/wiki-bayer-filter
media_type: text/plain
origin: external
raw_ref:
  path: archive/raw/3cf1e4976c3115232071e794d895fe0ca80158f2acf16fbbda34e070055cf4da.txt
  sha256: sha256:3cf1e4976c3115232071e794d895fe0ca80158f2acf16fbbda34e070055cf4da
read_status: retrieved
retrieval:
  acquisition: local-file
schema_version: source/v1
snapshot_sha256: sha256:3cf1e4976c3115232071e794d895fe0ca80158f2acf16fbbda34e070055cf4da
source_type: local-file
vault_id: public
---
# Source: https://en.wikipedia.org/wiki/Bayer_filter (retrieved 2026-09-04)

The filter pattern is half green, one quarter red and one quarter blue, hence is also called BGGR, RGBG, GRBG, or RGGB. It is named after its inventor, Bryce Bayer of Eastman Kodak.

Since each pixel is filtered to record only one of three colors, the data from each pixel cannot fully specify each of the red, green, and blue values on its own. To obtain a full-color image, various demosaicing algorithms can be used to interpolate a set of complete red, green, and blue values for each pixel. These algorithms make use of the surrounding pixels of the corresponding colors to estimate the values for a particular pixel.

The raw output of Bayer-filter cameras is referred to as a Bayer pattern image.

The Foveon X3 sensor (which layers red, green, and blue sensors vertically rather than using a mosaic) and arrangements of three separate CCDs (one for each color) does not need demosaicing.

Images with small-scale detail close to the resolution limit of the digital sensor can be a problem to the demosaicing algorithm, producing a result which does not look like the model. The most frequent artifact is Moiré, which may appear as repeating patterns, color artifacts or pixels arranged in an unrealistic maze-like pattern.
