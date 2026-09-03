---
archive_policy: text-only
attachments:
- filename: mpc-official.html
  kind: document
  media_type: text/html
  role: original
  sha256: sha256:4a18c27628ce5777d9f4c4a2f854e60439b61695677c7b9d8fc05023ab585020
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-2554ad492f8c
  position:
    end: 464
    start: 394
    type: TextPositionSelector
  quote_sha256: sha256:c4fac18bd4f84039aa032b2624640d898abcd5c3625cfcc6259610d1bbfb76f0
  selector:
    exact: The library is built upon and follows the same principles as GNU MPFR.
    prefix: 'ecision is a major design goal.

      '
    suffix: ' It is written by Andreas Enge, '
    type: TextQuoteSelector
  selector_sha256: sha256:f0d2dc736a0aa0e31ac44e3f2c8a41875c7e2d833ba7679a42571ce67b4a1621
  snapshot_sha256: sha256:b1e1638deedda65076f74716e40c50d622f1f0fc42df5c9f1fec0474322757c9
- evidence_id: evidence-949c1e14484a
  position:
    end: 463
    start: 13
    type: TextPositionSelector
  quote_sha256: sha256:be4d56d3fbe43630baf4e10a23c140c9086e1509fb55ef0b046e50e2ac0a825c
  selector:
    exact: 'GNU MPC is a C library for the arithmetic of complex numbers with arbitrarily
      high precision and correct rounding of the result. It extends the principles
      of the IEEE-754 standard for fixed precision real floating point numbers to
      complex numbers, providing well-defined semantics for every operation. At the
      same time, speed of operation at high precision is a major design goal.

      The library is built upon and follows the same principles as GNU MPFR'
    prefix: 'Introduction

      '
    suffix: . It is written by Andreas Enge,
    type: TextQuoteSelector
  selector_sha256: sha256:0346c11099763584a96126e811083c645e590b9592b80f32860c8a96a4dfc6e9
  snapshot_sha256: sha256:b1e1638deedda65076f74716e40c50d622f1f0fc42df5c9f1fec0474322757c9
extractor: trafilatura/2.2.0
id: mpc-official
media_type: text/html
origin: external
raw_ref:
  path: archive/raw/4a18c27628ce5777d9f4c4a2f854e60439b61695677c7b9d8fc05023ab585020.html
  sha256: sha256:4a18c27628ce5777d9f4c4a2f854e60439b61695677c7b9d8fc05023ab585020
read_status: retrieved
retrieval:
  acquisition: fetch
  resolved_url: https://www.multiprecision.org/mpc/
  url: https://www.multiprecision.org/mpc/
schema_version: source/v1
snapshot_sha256: sha256:b1e1638deedda65076f74716e40c50d622f1f0fc42df5c9f1fec0474322757c9
source_type: doc
vault_id: public
---
Introduction
GNU MPC is a C library for the arithmetic of complex numbers with arbitrarily high precision and correct rounding of the result. It extends the principles of the IEEE-754 standard for fixed precision real floating point numbers to complex numbers, providing well-defined semantics for every operation. At the same time, speed of operation at high precision is a major design goal.
The library is built upon and follows the same principles as GNU MPFR. It is written by Andreas Enge, Mickaël Gastineau, Philippe Théveny and Paul Zimmermann and is distributed under the GNU Lesser General Public License, either version 3 of the licence, or (at your option) any later version (LGPLv3+). The GNU MPC library has been registered in France by the Agence pour la Protection des Programmes on 2003-02-05 under the number IDDN FR 001 060029 000 R P 2003 000 10000.
News
Version 1.4.1, "Jasminum grandiflorum", released in April 2026, comes with the following new features:
- 
Bug fix: mpc_fr_div :
Fix memory leak introduced in release 1.4.0.
Version 1.4.0, "Jasminum grandiflorum", released in March 2026, comes with the following new features:
- 
New functions:
mpc_exp10 ,mpc_exp2 ,mpc_log2
- 
Bug fixes:
  - 
mpc_tan andmpc_tanh :
Fix wrong values and slowness for large imaginary part.
  - 
mpc_pow : Agree on and implement the sign of the imaginary part
when both inputs are real.
  - 
mpc_fr_div andmpc_ui_div :
Treat the imaginary part of the dividend as an exact zero and not as +0,
following the C2Y draft of the C standard. This changes the signs of zeroes
in some results.
- 
- 
Generate the pkg-config file mpc.pc .
- 
Add support for non-standard complex types
(_Dcomplex ,_Lcomplex ) under Windows.