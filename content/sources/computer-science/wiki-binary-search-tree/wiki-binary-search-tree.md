---
archive_policy: text-only
attachments:
- filename: wiki-binary-search-tree.txt
  kind: document
  media_type: text/plain
  role: original
  sha256: sha256:4852c973ccc2be195199bc70acac8e698488ecc19201c12a87c49df755ddc8a2
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-6c9f3729e870
  position:
    end: 254
    start: 0
    type: TextPositionSelector
  selector:
    exact: Binary search tree, also called an ordered or sorted binary tree, is a
      rooted binary tree data structure with the key of each internal node being greater
      than all the keys in the respective node's left subtree and less than the ones
      in its right subtree.
    prefix: ''
    suffix: ' The time complexity of operatio'
    type: TextQuoteSelector
  snapshot_sha256: sha256:4852c973ccc2be195199bc70acac8e698488ecc19201c12a87c49df755ddc8a2
- evidence_id: evidence-25a94489f8e2
  position:
    end: 364
    start: 255
    type: TextPositionSelector
  selector:
    exact: The time complexity of operations on the binary search tree is linear with
      respect to the height of the tree.
    prefix: ' the ones in its right subtree. '
    suffix: '

      Binary search trees allow binar'
    type: TextQuoteSelector
  snapshot_sha256: sha256:4852c973ccc2be195199bc70acac8e698488ecc19201c12a87c49df755ddc8a2
- evidence_id: evidence-8fd0ef8100e7
  position:
    end: 628
    start: 365
    type: TextPositionSelector
  selector:
    exact: Binary search trees allow binary search for fast lookup, addition, and
      removal of data items. Since the nodes in a BST are laid out so that each comparison
      skips about half of the remaining tree, the lookup performance is proportional
      to that of binary logarithm.
    prefix: 'pect to the height of the tree.

      '
    suffix: '

      BSTs were devised in the 1960s '
    type: TextQuoteSelector
  snapshot_sha256: sha256:4852c973ccc2be195199bc70acac8e698488ecc19201c12a87c49df755ddc8a2
- evidence_id: evidence-3aa8c8e52e3e
  position:
    end: 772
    start: 629
    type: TextPositionSelector
  selector:
    exact: BSTs were devised in the 1960s for the problem of efficient storage of
      labeled data and are attributed to Conway Berners-Lee and David Wheeler.
    prefix: 'al to that of binary logarithm.

      '
    suffix: '

      The performance of a binary sea'
    type: TextQuoteSelector
  snapshot_sha256: sha256:4852c973ccc2be195199bc70acac8e698488ecc19201c12a87c49df755ddc8a2
- evidence_id: evidence-30007c0cb00e
  position:
    end: 1027
    start: 773
    type: TextPositionSelector
  selector:
    exact: The performance of a binary search tree is dependent on the order of insertion
      of the nodes into the tree since arbitrary insertions may lead to degeneracy;
      several variations of the binary search tree can be built with guaranteed worst-case
      performance.
    prefix: ' Berners-Lee and David Wheeler.

      '
    suffix: ' The basic operations include: s'
    type: TextQuoteSelector
  snapshot_sha256: sha256:4852c973ccc2be195199bc70acac8e698488ecc19201c12a87c49df755ddc8a2
- evidence_id: evidence-d5faef464cb6
  position:
    end: 1251
    start: 1096
    type: TextPositionSelector
  selector:
    exact: Binary search trees are also a fundamental data structure used in construction
      of abstract data structures such as sets, multisets, and associative arrays.
    prefix: ', traversal, insert and delete.

      '
    suffix: '

      Time complexity in big O notati'
    type: TextQuoteSelector
  snapshot_sha256: sha256:4852c973ccc2be195199bc70acac8e698488ecc19201c12a87c49df755ddc8a2
- evidence_id: evidence-54af1c56b7d6
  position:
    end: 1673
    start: 1461
    type: TextPositionSelector
  selector:
    exact: In worst case, successive operations in the binary search tree may lead
      to degeneracy and form a singly linked list (or "unbalanced tree") like structure,
      thus has the same worst-case complexity as a linked list.
    prefix: ' Θ(n) average, O(n) worst case.

      '
    suffix: '

      If Z has only one child, the ch'
    type: TextQuoteSelector
  snapshot_sha256: sha256:4852c973ccc2be195199bc70acac8e698488ecc19201c12a87c49df755ddc8a2
- evidence_id: evidence-af0e76f257a0
  position:
    end: 1865
    start: 1674
    type: TextPositionSelector
  selector:
    exact: If Z has only one child, the child node of Z gets elevated by modifying
      the parent node of Z to point to the child node, consequently taking Z's position
      in the tree, as shown in (b) and (c).
    prefix: 'se complexity as a linked list.

      '
    suffix: '

      If Z has both left and right ch'
    type: TextQuoteSelector
  snapshot_sha256: sha256:4852c973ccc2be195199bc70acac8e698488ecc19201c12a87c49df755ddc8a2
- evidence_id: evidence-ff0802491fcb
  position:
    end: 1980
    start: 1866
    type: TextPositionSelector
  selector:
    exact: 'If Z has both left and right children, the in-order successor of Z, say
      Y, displaces Z by following the two cases:'
    prefix: ' tree, as shown in (b) and (c).

      '
    suffix: '

      If Y is Z''s right child, Y disp'
    type: TextQuoteSelector
  snapshot_sha256: sha256:4852c973ccc2be195199bc70acac8e698488ecc19201c12a87c49df755ddc8a2
- evidence_id: evidence-2b52cbf6cd14
  position:
    end: 2057
    start: 1981
    type: TextPositionSelector
  selector:
    exact: If Y is Z's right child, Y displaces Z and Y's right child remain unchanged.
    prefix: 's Z by following the two cases:

      '
    suffix: '

      If Y lies within Z''s right subt'
    type: TextQuoteSelector
  snapshot_sha256: sha256:4852c973ccc2be195199bc70acac8e698488ecc19201c12a87c49df755ddc8a2
- evidence_id: evidence-c6bb2944b119
  position:
    end: 2214
    start: 2058
    type: TextPositionSelector
  selector:
    exact: If Y lies within Z's right subtree but is not Z's right child, Y first
      gets replaced by its own right child, and then it displaces Z's position in
      the tree.
    prefix: 's right child remain unchanged.

      '
    suffix: '

      Alternatively, the in-order pre'
    type: TextQuoteSelector
  snapshot_sha256: sha256:4852c973ccc2be195199bc70acac8e698488ecc19201c12a87c49df755ddc8a2
- evidence_id: evidence-aadcbd15a301
  position:
    end: 2272
    start: 2215
    type: TextPositionSelector
  selector:
    exact: Alternatively, the in-order predecessor can also be used.
    prefix: 'laces Z''s position in the tree.

      '
    suffix: '

      Inorder tree walk: Nodes from t'
    type: TextQuoteSelector
  snapshot_sha256: sha256:4852c973ccc2be195199bc70acac8e698488ecc19201c12a87c49df755ddc8a2
- evidence_id: evidence-b2b0afcf337e
  position:
    end: 2466
    start: 2273
    type: TextPositionSelector
  selector:
    exact: 'Inorder tree walk: Nodes from the left subtree get visited first, followed
      by the root node and right subtree. Such a traversal visits all the nodes in
      the order of non-decreasing key sequence.'
    prefix: 'r predecessor can also be used.

      '
    suffix: '

      Preorder tree walk: The root no'
    type: TextQuoteSelector
  snapshot_sha256: sha256:4852c973ccc2be195199bc70acac8e698488ecc19201c12a87c49df755ddc8a2
- evidence_id: evidence-c1634aa0ad23
  position:
    end: 2557
    start: 2467
    type: TextPositionSelector
  selector:
    exact: 'Preorder tree walk: The root node gets visited first, followed by left
      and right subtrees.'
    prefix: 'of non-decreasing key sequence.

      '
    suffix: '

      Postorder tree walk: Nodes from'
    type: TextQuoteSelector
  snapshot_sha256: sha256:4852c973ccc2be195199bc70acac8e698488ecc19201c12a87c49df755ddc8a2
- evidence_id: evidence-8d3abacce66c
  position:
    end: 2679
    start: 2558
    type: TextPositionSelector
  selector:
    exact: 'Postorder tree walk: Nodes from the left subtree get visited first, followed
      by the right subtree, and finally, the root.'
    prefix: 'wed by left and right subtrees.

      '
    suffix: '

      There are several self-balanced'
    type: TextQuoteSelector
  snapshot_sha256: sha256:4852c973ccc2be195199bc70acac8e698488ecc19201c12a87c49df755ddc8a2
- evidence_id: evidence-109717c4bbe1
  position:
    end: 2807
    start: 2680
    type: TextPositionSelector
  selector:
    exact: There are several self-balanced binary search trees, including T-tree,
      treap, red-black tree, B-tree, 2–3 tree, and Splay tree.
    prefix: 'subtree, and finally, the root.

      '
    suffix: '

      Binary search trees are used in'
    type: TextQuoteSelector
  snapshot_sha256: sha256:4852c973ccc2be195199bc70acac8e698488ecc19201c12a87c49df755ddc8a2
- evidence_id: evidence-1a2ba9876653
  position:
    end: 3004
    start: 2808
    type: TextPositionSelector
  selector:
    exact: Binary search trees are used in sorting algorithms such as tree sort, where
      all the elements are inserted at once and the tree is traversed at an in-order
      fashion. BSTs are also used in quicksort.
    prefix: 'tree, 2–3 tree, and Splay tree.

      '
    suffix: '

      Binary search trees are used in'
    type: TextQuoteSelector
  snapshot_sha256: sha256:4852c973ccc2be195199bc70acac8e698488ecc19201c12a87c49df755ddc8a2
- evidence_id: evidence-4e4f979c165d
  position:
    end: 3102
    start: 3005
    type: TextPositionSelector
  selector:
    exact: Binary search trees are used in implementing priority queues, using the
      node's key as priorities.
    prefix: 'STs are also used in quicksort.

      '
    suffix: '

      '
    type: TextQuoteSelector
  snapshot_sha256: sha256:4852c973ccc2be195199bc70acac8e698488ecc19201c12a87c49df755ddc8a2
extractor: utf8/1
id: wiki-binary-search-tree
local:
  file_sha256: sha256:4852c973ccc2be195199bc70acac8e698488ecc19201c12a87c49df755ddc8a2
  path_ref: local-sidecar:public/wiki-binary-search-tree
media_type: text/plain
origin: external
raw_ref:
  path: archive/raw/4852c973ccc2be195199bc70acac8e698488ecc19201c12a87c49df755ddc8a2.txt
read_status: retrieved
retrieval:
  acquisition: local-file
schema_version: source/v1
snapshot_sha256: sha256:4852c973ccc2be195199bc70acac8e698488ecc19201c12a87c49df755ddc8a2
source_type: local-file
vault_id: public
---
Binary search tree, also called an ordered or sorted binary tree, is a rooted binary tree data structure with the key of each internal node being greater than all the keys in the respective node's left subtree and less than the ones in its right subtree. The time complexity of operations on the binary search tree is linear with respect to the height of the tree.
Binary search trees allow binary search for fast lookup, addition, and removal of data items. Since the nodes in a BST are laid out so that each comparison skips about half of the remaining tree, the lookup performance is proportional to that of binary logarithm.
BSTs were devised in the 1960s for the problem of efficient storage of labeled data and are attributed to Conway Berners-Lee and David Wheeler.
The performance of a binary search tree is dependent on the order of insertion of the nodes into the tree since arbitrary insertions may lead to degeneracy; several variations of the binary search tree can be built with guaranteed worst-case performance. The basic operations include: search, traversal, insert and delete.
Binary search trees are also a fundamental data structure used in construction of abstract data structures such as sets, multisets, and associative arrays.
Time complexity in big O notation: Search average Θ(log n), worst case O(n); Insert average Θ(log n), worst case O(n); Delete average Θ(log n), worst case O(n); Space complexity Θ(n) average, O(n) worst case.
In worst case, successive operations in the binary search tree may lead to degeneracy and form a singly linked list (or "unbalanced tree") like structure, thus has the same worst-case complexity as a linked list.
If Z has only one child, the child node of Z gets elevated by modifying the parent node of Z to point to the child node, consequently taking Z's position in the tree, as shown in (b) and (c).
If Z has both left and right children, the in-order successor of Z, say Y, displaces Z by following the two cases:
If Y is Z's right child, Y displaces Z and Y's right child remain unchanged.
If Y lies within Z's right subtree but is not Z's right child, Y first gets replaced by its own right child, and then it displaces Z's position in the tree.
Alternatively, the in-order predecessor can also be used.
Inorder tree walk: Nodes from the left subtree get visited first, followed by the root node and right subtree. Such a traversal visits all the nodes in the order of non-decreasing key sequence.
Preorder tree walk: The root node gets visited first, followed by left and right subtrees.
Postorder tree walk: Nodes from the left subtree get visited first, followed by the right subtree, and finally, the root.
There are several self-balanced binary search trees, including T-tree, treap, red-black tree, B-tree, 2–3 tree, and Splay tree.
Binary search trees are used in sorting algorithms such as tree sort, where all the elements are inserted at once and the tree is traversed at an in-order fashion. BSTs are also used in quicksort.
Binary search trees are used in implementing priority queues, using the node's key as priorities.
