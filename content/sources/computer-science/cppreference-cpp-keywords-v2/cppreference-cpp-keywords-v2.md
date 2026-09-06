---
archive_policy: text-only
attachments:
- filename: cppreference-cpp-keywords-v2.html
  kind: document
  media_type: text/html
  role: original
  sha256: sha256:f40639d418eb8d8e966f97cb50c0bcf924b1d5301565187dc6e6e0a49818eac0
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-281234d66ee1
  position:
    end: 160
    start: 13
    type: TextPositionSelector
  quote_sha256: sha256:1e03f811bb4f29dade8d65557a8df60d2a71ccc7d990e7248025ba4ccd96c270
  selector:
    exact: This is a list of reserved keywords in C++. Since they are used by the
      language, these keywords are not available for re-definition or overloading.
    prefix: 'C++ keywords

      '
    suffix: ' As an exception, they are not c'
    type: TextQuoteSelector
  selector_sha256: sha256:b1ba234d4765b7783dd21116d17b4bff730428c336b7ad3cf6921e2fa2365d30
  snapshot_sha256: sha256:437bd2ca5d9ec849f3a9fbf3b5930f1951215b1eea897a98b387e7029cc8e241
extractor: trafilatura/2.2.0
id: cppreference-cpp-keywords-v2
local:
  file_sha256: sha256:f40639d418eb8d8e966f97cb50c0bcf924b1d5301565187dc6e6e0a49818eac0
  path_ref: local-sidecar:public/cppreference-cpp-keywords-v2
media_type: text/html
origin: external
raw_ref:
  path: archive/raw/f40639d418eb8d8e966f97cb50c0bcf924b1d5301565187dc6e6e0a49818eac0.html
  sha256: sha256:f40639d418eb8d8e966f97cb50c0bcf924b1d5301565187dc6e6e0a49818eac0
read_status: retrieved
retrieval:
  acquisition: local-file
  url: https://en.cppreference.com/w/cpp/keyword
schema_version: source/v1
snapshot_sha256: sha256:437bd2ca5d9ec849f3a9fbf3b5930f1951215b1eea897a98b387e7029cc8e241
source_type: local-file
vault_id: public
---
C++ keywords
This is a list of reserved keywords in C++. Since they are used by the language, these keywords are not available for re-definition or overloading. As an exception, they are not considered reserved in attributes (excluding attribute argument lists).(since C++11)
- (A) — alternative represenation (see below).
- (1) — meaning changed or new meaning added in C++11.
- (2) — new meaning added in C++14.
- (3) — meaning changed or new meaning added in C++17.
- (4) — meaning changed or new meaning added in C++20.
- (5) — new meaning added in C++23.
Note that: and, bitor, or, xor, compl, bitand, and_eq, or_eq, xor_eq, not and not_eq (along with digraphs: <%, %>, <:, :>, %:, %:%: and trigraphs: ??<, ??>, ??(, ??), ??=, ??/, ??', ??!, ??-(until C++17)) provide an alternative way to represent standard tokens. These keywords are also considered reserved in attributes (excluding attribute argument lists), but some implementations handle them the same as the others.(since C++11)
In addition to keywords, there are identifiers with special meaning, which may be used as names of objects or functions, but have special meaning in certain contexts.
final (C++11)
override (C++11)
transaction_safe (TM TS)
transaction_safe_dynamic (TM TS)
import (C++20)
module (C++20)
pre (C++26)
post (C++26)
Also, all identifiers that contain a double underscore __ in any position and each identifier that begins with an underscore followed by an uppercase letter is always reserved, and all identifiers that begin with an underscore are reserved for use as names in the global namespace. See identifiers for more details.
The namespace std is used to place names of the standard C++ library. See Extending namespace std for the rules about adding names to it.
The name posix is reserved for a future top-level namespace. The behavior is undefined if a program declares or defines anything in that namespace.
The following tokens are recognized by the preprocessor when in context of a preprocessor directive:
if
elif
else
endif
ifdef
ifndef
elifdef (C++23)
elifndef (C++23)
define
undef
include
embed (C++26)
line
error
warning (C++23)
pragma
defined
__has_include (C++17)
__has_cpp_attribute (C++20)
__has_embed (C++26)
export (C++20)
import (C++20)
module (C++20)
The following tokens are recognized by the preprocessor outside the context of a preprocessor directive:
_Pragma (C++11)