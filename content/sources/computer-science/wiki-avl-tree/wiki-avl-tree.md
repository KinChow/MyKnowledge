---
archive_policy: text-only
attachments:
- filename: wiki-avl-tree.txt
  kind: document
  media_type: text/plain
  role: original
  sha256: sha256:29037d3b8291184706a57fbfe0fc00bc91358708877107ea7695f237eed54926
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-0e522fe6aa29
  position:
    end: 308
    start: 123
    type: TextPositionSelector
  quote_sha256: sha256:5198b3075fcc08a0730f428531462caf9265d8ed8e2e98be6417dafe168b58fa
  selector:
    exact: In an AVL tree, the heights of the two child subtrees of any node differ
      by not more than one; if at any time they differ by more than one, rebalancing
      is done to restore this property.
    prefix: 'f-balancing binary search tree. '
    suffix: ' Lookup, insertion, and deletion'
    type: TextQuoteSelector
  selector_sha256: sha256:65cf518136564451902e27e849205bb668e5944eaab7c571d420442fe3a625c4
  snapshot_sha256: sha256:29037d3b8291184706a57fbfe0fc00bc91358708877107ea7695f237eed54926
- evidence_id: evidence-6487166eddd5
  position:
    end: 467
    start: 309
    type: TextPositionSelector
  quote_sha256: sha256:dfc72c4afb18b270bfb11994190e189644fcd53208667b51851e6ed60dedbc68
  selector:
    exact: Lookup, insertion, and deletion all take O(log n) time in both the average
      and worst cases, where n is the number of nodes in the tree prior to the operation.
    prefix: ' done to restore this property. '
    suffix: ' Insertions and deletions may re'
    type: TextQuoteSelector
  selector_sha256: sha256:016778518b64869184f7a8d192b89c9c96490bcc8534143c6d9d14068ba7e169
  snapshot_sha256: sha256:29037d3b8291184706a57fbfe0fc00bc91358708877107ea7695f237eed54926
- evidence_id: evidence-6d8546da2df8
  position:
    end: 827
    start: 562
    type: TextPositionSelector
  quote_sha256: sha256:aef0042cd56e3edd6f78a804dedfdda705a3eff18aa14735917045655b42b195
  selector:
    exact: The AVL tree is named after its two Soviet inventors, Georgy Adelson-Velsky
      and Evgenii Landis, who published it in their 1962 paper "An algorithm for the
      organization of information". It is the first self-balancing binary search tree
      data structure to be invented.
    prefix: ' by one or more tree rotations.

      '
    suffix: '

      AVL trees are often compared wi'
    type: TextQuoteSelector
  selector_sha256: sha256:d428a160fdaa1af3add8be558451b5b5b9998c75da33a4eeaeb3ec01450ae299
  snapshot_sha256: sha256:29037d3b8291184706a57fbfe0fc00bc91358708877107ea7695f237eed54926
- evidence_id: evidence-b33ffb170466
  position:
    end: 1092
    start: 828
    type: TextPositionSelector
  quote_sha256: sha256:a0d7390b57958e9cac5db1a27572846a3b35b6981a890c6463ca12561f59d992
  selector:
    exact: AVL trees are often compared with red–black trees because both support
      the same set of operations and take O(log n) time for the basic operations.
      For lookup-intensive applications, AVL trees are faster than red–black trees
      because they are more strictly balanced.
    prefix: ' data structure to be invented.

      '
    suffix: ' Similar to red–black trees, AVL'
    type: TextQuoteSelector
  selector_sha256: sha256:2823d3b8d6f0b048aed9efeae196ebd525b8715c6dd0861384167fc63a40e3ae
  snapshot_sha256: sha256:29037d3b8291184706a57fbfe0fc00bc91358708877107ea7695f237eed54926
- evidence_id: evidence-3529b2a123b1
  position:
    end: 1367
    start: 1268
    type: TextPositionSelector
  quote_sha256: sha256:8a3efd2c351747c7a09f73bb83357eb4e9f21d3e1534a4a62878feb39446a163
  selector:
    exact: Indeed, every AVL tree can be colored red–black, but there are RB trees
      which are not AVL balanced.
    prefix: 'hey are related mathematically. '
    suffix: ' For maintaining the AVL (or RB)'
    type: TextQuoteSelector
  selector_sha256: sha256:7c996e4f51e4fdf9080f808fbc2aad52e714fb3ebeee246854c5fa7a62ebc0fc
  snapshot_sha256: sha256:29037d3b8291184706a57fbfe0fc00bc91358708877107ea7695f237eed54926
- evidence_id: evidence-ed8598496e30
  position:
    end: 2050
    start: 1705
    type: TextPositionSelector
  quote_sha256: sha256:b1aaa5cee1938c03115c5c5ee3a65ec157b0f3838e6a702e8ec89691d6d9aa34
  selector:
    exact: Since with a single deletion the height of an AVL subtree cannot decrease
      by more than one, the temporary balance factor of a node will be in the range
      from −2 to +2. If the balance factor remains in the range from −1 to +1 it can
      be adjusted in accord with the AVL rules. If it becomes ±2 then the subtree
      is unbalanced and needs to be rotated.
    prefix: ' case are also O(1) on average.

      '
    suffix: ' (Unlike insertion where a rotat'
    type: TextQuoteSelector
  selector_sha256: sha256:72f816a589b61b92c214345e57699645a809e492813f5aca7224490b84acaa00
  snapshot_sha256: sha256:29037d3b8291184706a57fbfe0fc00bc91358708877107ea7695f237eed54926
- evidence_id: evidence-fb396c902653
  position:
    end: 2632
    start: 2336
    type: TextPositionSelector
  quote_sha256: sha256:155da4723ae79f7ea069fcc86cafb5411a638547a2b787c21fad12ade68cc80b
  selector:
    exact: 'Right Right: X is rebalanced with a simple rotation rotate_Left. Left
      Left: X is rebalanced with a simple rotation rotate_Right (mirror-image). Right
      Left: X is rebalanced with a double rotation rotate_RightLeft. Left Right: X
      is rebalanced with a double rotation rotate_LeftRight (mirror-image).'
    prefix: 'gain on the next higher level.)

      '
    suffix: '

      Space complexity: O(n). Search:'
    type: TextQuoteSelector
  selector_sha256: sha256:391413dd60ad0185c605d9d71a7e1e49fc7f954eecd45dee347e41e1757626db
  snapshot_sha256: sha256:29037d3b8291184706a57fbfe0fc00bc91358708877107ea7695f237eed54926
- evidence_id: evidence-804dc90717c9
  position:
    end: 1704
    start: 1453
    type: TextPositionSelector
  quote_sha256: sha256:516e3c38e6d926aef9177dee63180571c047b139e0568590610c9ca875f1503f
  selector:
    exact: RB insertions and deletions and AVL insertions require from zero to three
      tail-recursive rotations and run in amortized O(1) time, thus equally constant
      on average. AVL deletions requiring O(log n) rotations in the worst case are
      also O(1) on average.
    prefix: 'tations play an important role.

      '
    suffix: '

      Since with a single deletion th'
    type: TextQuoteSelector
  selector_sha256: sha256:fe5b5fe7459d48b11e2c50f9a99958054b422bf58bffb3f2783f2840e1f8c165
  snapshot_sha256: sha256:29037d3b8291184706a57fbfe0fc00bc91358708877107ea7695f237eed54926
extractor: utf8/1
id: wiki-avl-tree
local:
  file_sha256: sha256:29037d3b8291184706a57fbfe0fc00bc91358708877107ea7695f237eed54926
  path_ref: local-sidecar:public/wiki-avl-tree
media_type: text/plain
origin: external
raw_ref:
  path: archive/raw/29037d3b8291184706a57fbfe0fc00bc91358708877107ea7695f237eed54926.txt
  sha256: sha256:29037d3b8291184706a57fbfe0fc00bc91358708877107ea7695f237eed54926
read_status: retrieved
retrieval:
  acquisition: local-file
schema_version: source/v1
snapshot_sha256: sha256:29037d3b8291184706a57fbfe0fc00bc91358708877107ea7695f237eed54926
source_type: local-file
vault_id: public
---
In computer science, an AVL tree (named after inventors Adelson-Velsky and Landis) is a self-balancing binary search tree. In an AVL tree, the heights of the two child subtrees of any node differ by not more than one; if at any time they differ by more than one, rebalancing is done to restore this property. Lookup, insertion, and deletion all take O(log n) time in both the average and worst cases, where n is the number of nodes in the tree prior to the operation. Insertions and deletions may require the tree to be rebalanced by one or more tree rotations.
The AVL tree is named after its two Soviet inventors, Georgy Adelson-Velsky and Evgenii Landis, who published it in their 1962 paper "An algorithm for the organization of information". It is the first self-balancing binary search tree data structure to be invented.
AVL trees are often compared with red–black trees because both support the same set of operations and take O(log n) time for the basic operations. For lookup-intensive applications, AVL trees are faster than red–black trees because they are more strictly balanced. Similar to red–black trees, AVL trees are height-balanced.
Both AVL trees and red–black (RB) trees are self-balancing binary search trees and they are related mathematically. Indeed, every AVL tree can be colored red–black, but there are RB trees which are not AVL balanced. For maintaining the AVL (or RB) tree's invariants, rotations play an important role.
RB insertions and deletions and AVL insertions require from zero to three tail-recursive rotations and run in amortized O(1) time, thus equally constant on average. AVL deletions requiring O(log n) rotations in the worst case are also O(1) on average.
Since with a single deletion the height of an AVL subtree cannot decrease by more than one, the temporary balance factor of a node will be in the range from −2 to +2. If the balance factor remains in the range from −1 to +1 it can be adjusted in accord with the AVL rules. If it becomes ±2 then the subtree is unbalanced and needs to be rotated. (Unlike insertion where a rotation always balances the tree, after delete, there may be BF(Z) ≠ 0, so that after the appropriate single or double rotation the height of the rebalanced subtree decreases by one meaning that the tree has to be rebalanced again on the next higher level.)
Right Right: X is rebalanced with a simple rotation rotate_Left. Left Left: X is rebalanced with a simple rotation rotate_Right (mirror-image). Right Left: X is rebalanced with a double rotation rotate_RightLeft. Left Right: X is rebalanced with a double rotation rotate_LeftRight (mirror-image).
Space complexity: O(n). Search: O(log n) amortized, O(log n) worst case. Insert: O(log n) amortized, O(log n) worst case. Delete: O(log n) amortized, O(log n) worst case.
