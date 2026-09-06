---
archive_policy: text-only
attachments:
- filename: arxiv-transformer-v2.html
  kind: document
  media_type: text/html
  role: original
  sha256: sha256:29e42a996471db9c019f1122825cdac0e6d64c96767d9ee5c0b8891de6204bee
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-d7079eb046ba
  position:
    end: 268
    start: 126
    type: TextPositionSelector
  quote_sha256: sha256:ea6c68e4ef849869240ba81504ad63a559cd4dfef3a0c2501ee0cbda93cd847c
  selector:
    exact: The dominant sequence transduction models are based on complex recurrent
      or convolutional neural networks in an encoder-decoder configuration.
    prefix: "erimental)\n            Abstract:"
    suffix: ' The best performing models also'
    type: TextQuoteSelector
  selector_sha256: sha256:932206aee846213ae69d28a57c9db3f5442712b7ca6ec0e05d70f8858444756a
  snapshot_sha256: sha256:4d129544139195919bb231863be8978995e85901cb246675d79b23acd9e493a1
- evidence_id: evidence-edeba6920028
  position:
    end: 519
    start: 365
    type: TextPositionSelector
  quote_sha256: sha256:ed7631200a18f20fc81a069dbaec1e4780737fd416877c9496ab815a38eb1fd7
  selector:
    exact: We propose a new simple network architecture, the Transformer, based solely
      on attention mechanisms, dispensing with recurrence and convolutions entirely.
    prefix: 'through an attention mechanism. '
    suffix: ' Experiments on two machine tran'
    type: TextQuoteSelector
  selector_sha256: sha256:b4d978d4936334db299e1abcd70aaa26b051f58c37982211eeca83431a7912ce
  snapshot_sha256: sha256:4d129544139195919bb231863be8978995e85901cb246675d79b23acd9e493a1
extractor: trafilatura/2.2.0
id: arxiv-transformer-v2
local:
  file_sha256: sha256:29e42a996471db9c019f1122825cdac0e6d64c96767d9ee5c0b8891de6204bee
  path_ref: local-sidecar:public/arxiv-transformer-v2
media_type: text/html
origin: external
raw_ref:
  path: archive/raw/29e42a996471db9c019f1122825cdac0e6d64c96767d9ee5c0b8891de6204bee.html
  sha256: sha256:29e42a996471db9c019f1122825cdac0e6d64c96767d9ee5c0b8891de6204bee
read_status: retrieved
retrieval:
  acquisition: local-file
  url: https://arxiv.org/abs/1706.03762
schema_version: source/v1
snapshot_sha256: sha256:4d129544139195919bb231863be8978995e85901cb246675d79b23acd9e493a1
source_type: local-file
vault_id: public
---
Computer Science > Computation and Language
Title:Attention Is All You Need
View PDF HTML (experimental)
            Abstract:The dominant sequence transduction models are based on complex recurrent or convolutional neural networks in an encoder-decoder configuration. The best performing models also connect the encoder and decoder through an attention mechanism. We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely. Experiments on two machine translation tasks show these models to be superior in quality while being more parallelizable and requiring significantly less time to train. Our model achieves 28.4 BLEU on the WMT 2014 English-to-German translation task, improving over the existing best results, including ensembles by over 2 BLEU. On the WMT 2014 English-to-French translation task, our model establishes a new single-model state-of-the-art BLEU score of 41.8 after training for 3.5 days on eight GPUs, a small fraction of the training costs of the best models from the literature. We show that the Transformer generalizes well to other tasks by applying it successfully to English constituency parsing both with large and limited training data.
    
Submission history
From: Llion Jones [view email]
[v1] Mon, 12 Jun 2017 17:57:34 UTC (1,102 KB)
[v2] Mon, 19 Jun 2017 16:49:45 UTC (1,125 KB)
[v3] Tue, 20 Jun 2017 05:20:02 UTC (1,125 KB)
[v4] Fri, 30 Jun 2017 17:29:30 UTC (1,124 KB)
[v5] Wed, 6 Dec 2017 03:30:32 UTC (1,124 KB)
[v6] Mon, 24 Jul 2023 00:48:54 UTC (1,124 KB)
[v7] Wed, 2 Aug 2023 00:41:18 UTC (1,124 KB)
Bibliographic and Citation Tools
Code, Data and Media Associated with this Article
Demos
Recommenders and Search Tools
arXivLabs: experimental projects with community collaborators
arXivLabs is a framework that allows collaborators to develop and share new arXiv features directly on our website.
Both individuals and organizations that work with arXivLabs have embraced and accepted our values of openness, community, excellence, and user data privacy. arXiv is committed to these values and only works with partners that adhere to them.
Have an idea for a project that will add value for arXiv's community? Learn more about arXivLabs.