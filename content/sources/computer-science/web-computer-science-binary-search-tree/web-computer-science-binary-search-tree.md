---
archive_policy: text-only
attachments:
- filename: web-computer-science-binary-search-tree.html
  kind: document
  media_type: text/html
  role: original
  sha256: sha256:68ad47f5f0cd8a5659afa556ea0aaa51f93d2a09580139b2035cd8f2568949cc
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-48d9322f8dc0
  position:
    end: 151
    start: 0
    type: TextPositionSelector
  quote_sha256: sha256:f622a23cd664dd73c81b699bf020eb651b20edb733c4dfd46c7035487f0d93c4
  selector:
    exact: 'A Binary Search Tree (BST) is a type of binary tree data structure in
      which each node contains a unique key and satisfies a specific ordering property:'
    prefix: ''
    suffix: '

      - All nodes in the left subtree'
    type: TextQuoteSelector
  selector_sha256: sha256:9c3eee14a9e54a3c9200f7120f23123a6f417e4dc268cc900e562f05e64ef420
  snapshot_sha256: sha256:1921c4f32210362ce3be70ac4f8a6cc8a19329c03929dc7c061a96b30d084853
- evidence_id: evidence-43de59ee6712
  position:
    end: 245
    start: 154
    type: TextPositionSelector
  quote_sha256: sha256:10f408ff5a3a76a524d2e40ca40f5acfd7117f056ce3a896365df4951dd80693
  selector:
    exact: All nodes in the left subtree of a node contain values strictly less than
      the node’s value.
    prefix: 'a specific ordering property:

      - '
    suffix: '

      - All nodes in the right subtre'
    type: TextQuoteSelector
  selector_sha256: sha256:b1869201664beb8fedfbb17060ac8adbd370dafe4673fc4d3ee88609c9c44155
  snapshot_sha256: sha256:1921c4f32210362ce3be70ac4f8a6cc8a19329c03929dc7c061a96b30d084853
- evidence_id: evidence-5c0f2e90f128
  position:
    end: 343
    start: 248
    type: TextPositionSelector
  quote_sha256: sha256:123e0e795a2d3dac2b7ec8b930ebd8c72d948c3e19272e0df285dbdc7eb3b541
  selector:
    exact: All nodes in the right subtree of a node contain values strictly greater
      than the node’s value.
    prefix: 'y less than the node’s value.

      - '
    suffix: '

      This structure enables efficien'
    type: TextQuoteSelector
  selector_sha256: sha256:cdb2e8c67712738ad3299f09d8eac1f1d4b3e7f0628c7a4a029d2de71160aaf3
  snapshot_sha256: sha256:1921c4f32210362ce3be70ac4f8a6cc8a19329c03929dc7c061a96b30d084853
- evidence_id: evidence-09784d528634
  position:
    end: 893
    start: 734
    type: TextPositionSelector
  quote_sha256: sha256:cc06b78cc48aa74e76476e7524d07b05ce0c21525d2a5f9702a2b3a607c79cee
  selector:
    exact: Operations like search, insertion, and deletion work in O(Log n) time for
      a balanced binary search tree. In the worst-case (unbalanced), these degrade
      to O(n).
    prefix: 'intain sorted stream of data.

      - '
    suffix: ' With self-balancing BSTs like A'
    type: TextQuoteSelector
  selector_sha256: sha256:adecf33ae7b525e92f73f75ece5d1a6ab53b5e9a29432f05ac930914c9eab2c1
  snapshot_sha256: sha256:1921c4f32210362ce3be70ac4f8a6cc8a19329c03929dc7c061a96b30d084853
- evidence_id: evidence-15be3480495f
  position:
    end: 482
    start: 344
    type: TextPositionSelector
  quote_sha256: sha256:cab8637b505a34223629906d09bc84d6c76460d92caef7999ede4e80331099c0
  selector:
    exact: This structure enables efficient operations for searching, insertion, and
      deletion of elements, especially when the tree remains balanced.
    prefix: ' greater than the node’s value.

      '
    suffix: '

      - BSTs are widely used in datab'
    type: TextQuoteSelector
  selector_sha256: sha256:fdc9a91de6c831511b765612e430c5ec8608df99b7cc532c5d9b05c5d2ac37d2
  snapshot_sha256: sha256:1921c4f32210362ce3be70ac4f8a6cc8a19329c03929dc7c061a96b30d084853
extractor: trafilatura/2.2.0
id: web-computer-science-binary-search-tree
media_type: text/html
origin: external
raw_ref:
  path: archive/raw/68ad47f5f0cd8a5659afa556ea0aaa51f93d2a09580139b2035cd8f2568949cc.html
  sha256: sha256:68ad47f5f0cd8a5659afa556ea0aaa51f93d2a09580139b2035cd8f2568949cc
read_status: retrieved
retrieval:
  acquisition: fetch
  resolved_url: https://www.geeksforgeeks.org/dsa/binary-search-tree-data-structure/
  url: https://www.geeksforgeeks.org/dsa/binary-search-tree-data-structure/
schema_version: source/v1
snapshot_sha256: sha256:1921c4f32210362ce3be70ac4f8a6cc8a19329c03929dc7c061a96b30d084853
source_type: doc
vault_id: public
---
A Binary Search Tree (BST) is a type of binary tree data structure in which each node contains a unique key and satisfies a specific ordering property:
- All nodes in the left subtree of a node contain values strictly less than the node’s value.
- All nodes in the right subtree of a node contain values strictly greater than the node’s value.
This structure enables efficient operations for searching, insertion, and deletion of elements, especially when the tree remains balanced.
- BSTs are widely used in database indexing, symbol tables, range queries, and are foundational for advanced structures like AVL tree and Red-Black tree. In problem solving, BSTs are used in problems where we need to maintain sorted stream of data.
- Operations like search, insertion, and deletion work in O(Log n) time for a balanced binary search tree. In the worst-case (unbalanced), these degrade to O(n). With self-balancing BSTs like AVL and Red Black Trees, we can ensure the worst case as O(Log n).
Basics
- Introduction
- Applications
- Insertion, Search and Delete
- Minimum and Maximum
- Floor and Ceil
- Inorder Successor and Inorder Predecessor
- Handling duplicates in BST
Easy Problems
Medium Problems
Hard Problems
Important Links