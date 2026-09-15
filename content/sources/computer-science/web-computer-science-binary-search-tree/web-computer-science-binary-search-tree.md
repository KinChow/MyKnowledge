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
  selector:
    exact: 'A Binary Search Tree (BST) is a type of binary tree data structure in
      which each node contains a unique key and satisfies a specific ordering property:'
    prefix: ''
    suffix: '

      - All nodes in the left subtree'
    type: TextQuoteSelector
  snapshot_sha256: sha256:1921c4f32210362ce3be70ac4f8a6cc8a19329c03929dc7c061a96b30d084853
- evidence_id: evidence-43de59ee6712
  position:
    end: 245
    start: 154
    type: TextPositionSelector
  selector:
    exact: All nodes in the left subtree of a node contain values strictly less than
      the node’s value.
    prefix: 'a specific ordering property:

      - '
    suffix: '

      - All nodes in the right subtre'
    type: TextQuoteSelector
  snapshot_sha256: sha256:1921c4f32210362ce3be70ac4f8a6cc8a19329c03929dc7c061a96b30d084853
- evidence_id: evidence-5c0f2e90f128
  position:
    end: 343
    start: 248
    type: TextPositionSelector
  selector:
    exact: All nodes in the right subtree of a node contain values strictly greater
      than the node’s value.
    prefix: 'y less than the node’s value.

      - '
    suffix: '

      This structure enables efficien'
    type: TextQuoteSelector
  snapshot_sha256: sha256:1921c4f32210362ce3be70ac4f8a6cc8a19329c03929dc7c061a96b30d084853
- evidence_id: evidence-09784d528634
  position:
    end: 893
    start: 734
    type: TextPositionSelector
  selector:
    exact: Operations like search, insertion, and deletion work in O(Log n) time for
      a balanced binary search tree. In the worst-case (unbalanced), these degrade
      to O(n).
    prefix: 'intain sorted stream of data.

      - '
    suffix: ' With self-balancing BSTs like A'
    type: TextQuoteSelector
  snapshot_sha256: sha256:1921c4f32210362ce3be70ac4f8a6cc8a19329c03929dc7c061a96b30d084853
- evidence_id: evidence-15be3480495f
  position:
    end: 482
    start: 344
    type: TextPositionSelector
  selector:
    exact: This structure enables efficient operations for searching, insertion, and
      deletion of elements, especially when the tree remains balanced.
    prefix: ' greater than the node’s value.

      '
    suffix: '

      - BSTs are widely used in datab'
    type: TextQuoteSelector
  snapshot_sha256: sha256:1921c4f32210362ce3be70ac4f8a6cc8a19329c03929dc7c061a96b30d084853
extractor: trafilatura/2.2.0
id: web-computer-science-binary-search-tree
media_type: text/html
origin: external
raw_ref:
  path: archive/raw/68ad47f5f0cd8a5659afa556ea0aaa51f93d2a09580139b2035cd8f2568949cc.html
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