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
  selector:
    exact: In an AVL tree, the heights of the two child subtrees of any node differ
      by not more than one; if at any time they differ by more than one, rebalancing
      is done to restore this property.
    prefix: 'f-balancing binary search tree. '
    suffix: ' Lookup, insertion, and deletion'
    type: TextQuoteSelector
  snapshot_sha256: sha256:29037d3b8291184706a57fbfe0fc00bc91358708877107ea7695f237eed54926
- evidence_id: evidence-6487166eddd5
  position:
    end: 467
    start: 309
    type: TextPositionSelector
  selector:
    exact: Lookup, insertion, and deletion all take O(log n) time in both the average
      and worst cases, where n is the number of nodes in the tree prior to the operation.
    prefix: ' done to restore this property. '
    suffix: ' Insertions and deletions may re'
    type: TextQuoteSelector
  snapshot_sha256: sha256:29037d3b8291184706a57fbfe0fc00bc91358708877107ea7695f237eed54926
- evidence_id: evidence-6d8546da2df8
  position:
    end: 827
    start: 562
    type: TextPositionSelector
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
  snapshot_sha256: sha256:29037d3b8291184706a57fbfe0fc00bc91358708877107ea7695f237eed54926
- evidence_id: evidence-b33ffb170466
  position:
    end: 1092
    start: 828
    type: TextPositionSelector
  selector:
    exact: AVL trees are often compared with red–black trees because both support
      the same set of operations and take O(log n) time for the basic operations.
      For lookup-intensive applications, AVL trees are faster than red–black trees
      because they are more strictly balanced.
    prefix: ' data structure to be invented.

      '
    suffix: ' Similar to red–black trees, AVL'
    type: TextQuoteSelector
  snapshot_sha256: sha256:29037d3b8291184706a57fbfe0fc00bc91358708877107ea7695f237eed54926
- evidence_id: evidence-3529b2a123b1
  position:
    end: 1367
    start: 1268
    type: TextPositionSelector
  selector:
    exact: Indeed, every AVL tree can be colored red–black, but there are RB trees
      which are not AVL balanced.
    prefix: 'hey are related mathematically. '
    suffix: ' For maintaining the AVL (or RB)'
    type: TextQuoteSelector
  snapshot_sha256: sha256:29037d3b8291184706a57fbfe0fc00bc91358708877107ea7695f237eed54926
- evidence_id: evidence-ed8598496e30
  position:
    end: 2050
    start: 1705
    type: TextPositionSelector
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
  snapshot_sha256: sha256:29037d3b8291184706a57fbfe0fc00bc91358708877107ea7695f237eed54926
- evidence_id: evidence-fb396c902653
  position:
    end: 2632
    start: 2336
    type: TextPositionSelector
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
  snapshot_sha256: sha256:29037d3b8291184706a57fbfe0fc00bc91358708877107ea7695f237eed54926
- evidence_id: evidence-804dc90717c9
  position:
    end: 1704
    start: 1453
    type: TextPositionSelector
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
