---
archive_policy: text-only
attachments:
- filename: web-computer-science-red-black-tree.html
  kind: document
  media_type: text/html
  role: original
  sha256: sha256:bc36a2b5aa751836d5d188717df9608a64af7c705ab77cb87f235a2e78c77bc2
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-ed7e35043048
  position:
    end: 441
    start: 0
    type: TextPositionSelector
  quote_sha256: sha256:d3f2c3faf30e1c4c522515a5cee146a1286ed8fd5172bdc526a2bf72602697db
  selector:
    exact: 'A Red-Black Tree is a self-balancing binary search tree with a height
      limit of O(logN), enabling efficient search, insertion, and deletion operations
      in O(logN) time, unlike standard binary search trees which can take O(N) time.

      - Each node has an additional attribute: a color, which can be either red or
      black.

      - These colors are used to maintain balance during insertions and deletions,
      ensuring efficient data retrieval and manipulation.'
    prefix: ''
    suffix: '

      Properties of Red-Black Trees

      A'
    type: TextQuoteSelector
  selector_sha256: sha256:10fdf22a8f5bac4f16ce72d93389def6213b8051c5a2ce7548437390245eaf0d
  snapshot_sha256: sha256:6d3ec93b28c20f1d6c6ed715f5d74f3bb9926711504984be17e6cef7464bb9ea
- evidence_id: evidence-fe34e8b4d9cb
  position:
    end: 228
    start: 0
    type: TextPositionSelector
  quote_sha256: sha256:6bf5176d63940f3210ff8717ea852c1a7b6d5345cafa47d938ba4cf41ffe4af9
  selector:
    exact: A Red-Black Tree is a self-balancing binary search tree with a height limit
      of O(logN), enabling efficient search, insertion, and deletion operations in
      O(logN) time, unlike standard binary search trees which can take O(N) time.
    prefix: ''
    suffix: '

      - Each node has an additional a'
    type: TextQuoteSelector
  selector_sha256: sha256:fbdd4a0f24459c20dd4200964c3c777c81ca880eb4ed06708f76f8d90a400fb2
  snapshot_sha256: sha256:6d3ec93b28c20f1d6c6ed715f5d74f3bb9926711504984be17e6cef7464bb9ea
- evidence_id: evidence-70d3bddd4fb5
  position:
    end: 566
    start: 521
    type: TextPositionSelector
  quote_sha256: sha256:82df058ccedf70f094e1a1201253614e7e636ae77ea064ef24523c7232046317
  selector:
    exact: 'Node Color: Each node is either red or black.'
    prefix: 'has the following properties:

      - '
    suffix: '

      - Root Property: The root of th'
    type: TextQuoteSelector
  selector_sha256: sha256:66231f3b100ad7036764c510d518fa093056fd20a18755f9bef5d9ba388d6a7c
  snapshot_sha256: sha256:6d3ec93b28c20f1d6c6ed715f5d74f3bb9926711504984be17e6cef7464bb9ea
- evidence_id: evidence-0d5d6b70154b
  position:
    end: 621
    start: 569
    type: TextPositionSelector
  quote_sha256: sha256:eb42943e3ecc57dfbecb7ab6d3bf815e3338cff9f6d3e7b4781fce6d573e857e
  selector:
    exact: 'Root Property: The root of the tree is always black.'
    prefix: ' node is either red or black.

      - '
    suffix: '

      - Red Node Property: Red nodes '
    type: TextQuoteSelector
  selector_sha256: sha256:554e5e473a660466befe9babbe0af17e1ef27c67279e4984f7477cc74fcdf52b
  snapshot_sha256: sha256:6d3ec93b28c20f1d6c6ed715f5d74f3bb9926711504984be17e6cef7464bb9ea
- evidence_id: evidence-96b26ae2b99c
  position:
    end: 709
    start: 624
    type: TextPositionSelector
  quote_sha256: sha256:e3a28eea642fbe26c77991a4aab1f158c24c45c199015775a30efa9d4070b373
  selector:
    exact: 'Red Node Property: Red nodes cannot have red children (Red nodes cannot
      be adjacent).'
    prefix: ' of the tree is always black.

      - '
    suffix: '

      - Black Node Property: Every pa'
    type: TextQuoteSelector
  selector_sha256: sha256:86f38772947271cd5f500548650cb6b01bdda25f62e94b463cf958827616e627
  snapshot_sha256: sha256:6d3ec93b28c20f1d6c6ed715f5d74f3bb9926711504984be17e6cef7464bb9ea
- evidence_id: evidence-0cb659e294c6
  position:
    end: 822
    start: 712
    type: TextPositionSelector
  quote_sha256: sha256:c15242bebaaabad640f559d3d79bded99ca20cdabb63952869f1fd7991c4797e
  selector:
    exact: 'Black Node Property: Every path from a node to its descendant leaves must
      have the same number of black nodes.'
    prefix: 'ed nodes cannot be adjacent).

      - '
    suffix: '

      - Leaf Property: All leaves (NI'
    type: TextQuoteSelector
  selector_sha256: sha256:8eec3e0f2f15ad32719a9e2ba1edb5ea96de6bc8ca3813f01b11177577d29734
  snapshot_sha256: sha256:6d3ec93b28c20f1d6c6ed715f5d74f3bb9926711504984be17e6cef7464bb9ea
- evidence_id: evidence-53b7c761e0ab
  position:
    end: 873
    start: 825
    type: TextPositionSelector
  quote_sha256: sha256:6141e611668c624c1ec206a179ea9da3291993fe58ca75a07403193a447c7265
  selector:
    exact: 'Leaf Property: All leaves (NIL nodes) are black.'
    prefix: 'e same number of black nodes.

      - '
    suffix: '

      These properties (no two consec'
    type: TextQuoteSelector
  selector_sha256: sha256:ba7d665bdfa9f80e92a0660585c16b0fd9a186968107a0cf7cfed9a14e051f73
  snapshot_sha256: sha256:6d3ec93b28c20f1d6c6ed715f5d74f3bb9926711504984be17e6cef7464bb9ea
- evidence_id: evidence-9ab60d16945e
  position:
    end: 1103
    start: 874
    type: TextPositionSelector
  quote_sha256: sha256:c14fe41e4f917dedb004d3afa50646b4fdac273156333287f142ec3cbd395441
  selector:
    exact: These properties (no two consecutive reds and same black height) ensure
      that the longest path from the root to any leaf is no more than twice as long
      as the shortest path, maintaining the tree's balance and efficient performance.
    prefix: 'l leaves (NIL nodes) are black.

      '
    suffix: '

      Balancing

      A simple example to u'
    type: TextQuoteSelector
  selector_sha256: sha256:d0b154c7523c80273add6e98b4ad8848fda650d72b3b83a65e4d23daa740c013
  snapshot_sha256: sha256:6d3ec93b28c20f1d6c6ed715f5d74f3bb9926711504984be17e6cef7464bb9ea
- evidence_id: evidence-6acfc182afc6
  position:
    end: 1718
    start: 1593
    type: TextPositionSelector
  quote_sha256: sha256:f1d27e37267d7ddd74bf2bb088dcf1712b64678ff3aeb819f142414acc259a4e
  selector:
    exact: 'Insertion: Inserting a new node involves a two-step process: BST insertion,
      followed by fixing Red-Black property violations.'
    prefix: 'perations on Red-Black Tree:

      1. '
    suffix: ' Consider:

      - If the parent of th'
    type: TextQuoteSelector
  selector_sha256: sha256:6db198339c29a55dd31861b4b24e337e70adfe3e301e7a3612be7318ddf18a0e
  snapshot_sha256: sha256:6d3ec93b28c20f1d6c6ed715f5d74f3bb9926711504984be17e6cef7464bb9ea
- evidence_id: evidence-cbddd783092e
  position:
    end: 2046
    start: 1945
    type: TextPositionSelector
  quote_sha256: sha256:209ab95fe843301b4d9afd22dca07d54eb7303452a060cd967170fa99541b2fc
  selector:
    exact: 'Case 1 (Uncle is Red): Recolor parent and uncle to black, grandparent
      to red. Then, move up the tree.'
    prefix: 'red, several cases may occur:

      - '
    suffix: '

      - Case 2 (Uncle is Black): If n'
    type: TextQuoteSelector
  selector_sha256: sha256:2e91c2b2afddceaae72af62441e69147fa11c01e6168ffad428328a0a0fc6239
  snapshot_sha256: sha256:6d3ec93b28c20f1d6c6ed715f5d74f3bb9926711504984be17e6cef7464bb9ea
- evidence_id: evidence-60331b073563
  position:
    end: 2224
    start: 2049
    type: TextPositionSelector
  quote_sha256: sha256:e4a3858c3df895c70b9207ef49d1205299c520f6cad8e6451bb50860485d2636
  selector:
    exact: 'Case 2 (Uncle is Black): If node is a right child, perform a left rotation
      on the parent. If the node is a left child, perform a right rotation on the
      grandparent and recolor.'
    prefix: ' red. Then, move up the tree.

      - '
    suffix: '

      2. Searching: Searching in Red-'
    type: TextQuoteSelector
  selector_sha256: sha256:92a227a90d39efeb17dd10beaf21e378e4f7491807fcd2dd56cf34b2e000a467
  snapshot_sha256: sha256:6d3ec93b28c20f1d6c6ed715f5d74f3bb9926711504984be17e6cef7464bb9ea
- evidence_id: evidence-c83b40239805
  position:
    end: 2290
    start: 2228
    type: TextPositionSelector
  quote_sha256: sha256:1c2f94da883f08a4e2ee4207227861fbe8d679f66da72be8b25b11d005d71965
  selector:
    exact: 'Searching: Searching in Red-Black Trees mirrors BST searching.'
    prefix: 'the grandparent and recolor.

      2. '
    suffix: ' Begin traversal from the root:

      '
    type: TextQuoteSelector
  selector_sha256: sha256:9dd2af085c17d26f7e9c558fb163f1a4784b6c3af1e54a3d37b4cb31dfb69843
  snapshot_sha256: sha256:6d3ec93b28c20f1d6c6ed715f5d74f3bb9926711504984be17e6cef7464bb9ea
- evidence_id: evidence-6724bb114559
  position:
    end: 2629
    start: 2588
    type: TextPositionSelector
  quote_sha256: sha256:9769b978bb659e9b2c732bcd6d36845448a67d3090296005ee016ff41ad75d55
  selector:
    exact: Remove the node using standard BST rules.
    prefix: 'ollowed by fixing violations.

      - '
    suffix: '

      - If a black node is deleted, a'
    type: TextQuoteSelector
  selector_sha256: sha256:ce43eecf7f44a58a6b836bcebfc5d6aec300160827fee29eaf176db555ec7621
  snapshot_sha256: sha256:6d3ec93b28c20f1d6c6ed715f5d74f3bb9926711504984be17e6cef7464bb9ea
- evidence_id: evidence-0c72d8fee0ea
  position:
    end: 2730
    start: 2632
    type: TextPositionSelector
  quote_sha256: sha256:5e7843b0578bf09f0cfab1be2848da2133de89e5b479ba31b61f04bea58ff7e5
  selector:
    exact: If a black node is deleted, a "double black" condition might arise, which
      requires specific fixes.
    prefix: 'ode using standard BST rules.

      - '
    suffix: '

      When deleting a black node, res'
    type: TextQuoteSelector
  selector_sha256: sha256:b908f149823812c71a77de2929e85f1b59c9f51102af16213c5dc8b61e640588
  snapshot_sha256: sha256:6d3ec93b28c20f1d6c6ed715f5d74f3bb9926711504984be17e6cef7464bb9ea
- evidence_id: evidence-61a045cc5983
  position:
    end: 3573
    start: 3452
    type: TextPositionSelector
  quote_sha256: sha256:cef087bb6aed7924045afa06f637df6a491046ee822e4e02fde05d55a4a4fcac
  selector:
    exact: 'Left Rotation: A left rotation at node x pivots the tree to the left,
      promoting its right child y to x''s former position.'
    prefix: 't path. These are two types:

      i. '
    suffix: ' The Transformation Steps are as'
    type: TextQuoteSelector
  selector_sha256: sha256:1a7bbd92384ef6a7b034649e961014a37df4522ba8b7bc866d05ce8b4fa8f338
  snapshot_sha256: sha256:6d3ec93b28c20f1d6c6ed715f5d74f3bb9926711504984be17e6cef7464bb9ea
- evidence_id: evidence-d9751cdd107c
  position:
    end: 4723
    start: 4600
    type: TextPositionSelector
  quote_sha256: sha256:93c40ba92e041fee3ec89ef83877609381a29ffde589969f5fa918ec4f246435
  selector:
    exact: 'Right Rotation: A right rotation at node x pivots the tree to the right,
      promoting its left child y to x’s former position.'
    prefix: "ft = x;\n    x.parent = y;\n}\nii. "
    suffix: '

      - Detach Subtree: Move y’s righ'
    type: TextQuoteSelector
  selector_sha256: sha256:8ef5777566bd25b9ba0abf9cda9a8f1ed873807d2aa50032c9d0414af9b2503b
  snapshot_sha256: sha256:6d3ec93b28c20f1d6c6ed715f5d74f3bb9926711504984be17e6cef7464bb9ea
- evidence_id: evidence-46854131a1bf
  position:
    end: 28522
    start: 28368
    type: TextPositionSelector
  quote_sha256: sha256:2bd8c822bcf66dfcb0fc63e5e8affbb9beaf51e0f67dee2560e5b230ee8d7cfa
  selector:
    exact: Because of their self-balancing property, they offer high efficiency in
      searching, insertion, and deletion, with a worst-case time complexity of O(log
      n).
    prefix: "(BLACK) 30(BLACK) \nAdvantages\n- "
    suffix: '

      - Red-Black Trees have straight'
    type: TextQuoteSelector
  selector_sha256: sha256:09c4d9d4f64bb906768e942da2e30ffca4587a417747e5325c860c850fe4a003
  snapshot_sha256: sha256:6d3ec93b28c20f1d6c6ed715f5d74f3bb9926711504984be17e6cef7464bb9ea
- evidence_id: evidence-adb4ade9ca09
  position:
    end: 28647
    start: 28525
    type: TextPositionSelector
  quote_sha256: sha256:4d7481ae955dd7e19e0bb8d1a3fc04af34db4ae433c649df42739076dd63129c
  selector:
    exact: Red-Black Trees have straightforward rules for insertion, deletion, and
      balance, making them relatively easy to implement.
    prefix: ' time complexity of O(log n).

      - '
    suffix: '

      - Suitable for use in maps, set'
    type: TextQuoteSelector
  selector_sha256: sha256:6f356a57aa47ed881e60a20c85827b9af384f3dd3ed3570cb854b7ad463a6791
  snapshot_sha256: sha256:6d3ec93b28c20f1d6c6ed715f5d74f3bb9926711504984be17e6cef7464bb9ea
- evidence_id: evidence-0420728272cc
  position:
    end: 28702
    start: 28650
    type: TextPositionSelector
  quote_sha256: sha256:715fd3aa999a34e4c60c9f76da6da046cbcf141357a3e53f95efee75bb232e10
  selector:
    exact: Suitable for use in maps, sets, and priority queues.
    prefix: 'relatively easy to implement.

      - '
    suffix: '

      Disadvantages

      - Red-Black Trees'
    type: TextQuoteSelector
  selector_sha256: sha256:4bc942a60f5d5c066d3e30b24bb9b31780dfe32fd7bdcfd97db874e6e6496ac7
  snapshot_sha256: sha256:6d3ec93b28c20f1d6c6ed715f5d74f3bb9926711504984be17e6cef7464bb9ea
- evidence_id: evidence-8c7950f5de01
  position:
    end: 28834
    start: 28719
    type: TextPositionSelector
  quote_sha256: sha256:31df9aab403fbd29e59605714ad3f1b05ccba6345f97f9d0ea2c5c17460fe590
  selector:
    exact: Red-Black Trees have more intricate insertion and deletion rules compared
      to simpler balanced trees like AVL trees.
    prefix: 'riority queues.

      Disadvantages

      - '
    suffix: '

      - Maintaining the Red-Black Tre'
    type: TextQuoteSelector
  selector_sha256: sha256:6484b948cedd7e1a9e5e0ba6381f266453c5739b01efd349f46c2d1487fc6c48
  snapshot_sha256: sha256:6d3ec93b28c20f1d6c6ed715f5d74f3bb9926711504984be17e6cef7464bb9ea
- evidence_id: evidence-f63611b667a8
  position:
    end: 28948
    start: 28837
    type: TextPositionSelector
  quote_sha256: sha256:df43ca6726f216ce95ed4b16db16e84054aeed57f54fe2a842fc6ef77fa0edf3
  selector:
    exact: Maintaining the Red-Black Tree properties introduces a minor overhead during
      insertion and deletion operations.
    prefix: 'alanced trees like AVL trees.

      - '
    suffix: '

      Applications of Red-Black Trees'
    type: TextQuoteSelector
  selector_sha256: sha256:254410b4fba26dee161e61b86f7245a867e52ffe911544986c8ea17072112ca5
  snapshot_sha256: sha256:6d3ec93b28c20f1d6c6ed715f5d74f3bb9926711504984be17e6cef7464bb9ea
- evidence_id: evidence-f5427bc1aaa0
  position:
    end: 29066
    start: 28984
    type: TextPositionSelector
  quote_sha256: sha256:c638fe500187f8ae99220addd97c83eba52ae59bf88f0c4ac36a08e3c734496d
  selector:
    exact: Powers high-performance containers such as map and set in C++ and TreeMap
      in Java.
    prefix: 'lications of Red-Black Trees:

      - '
    suffix: '

      - In operating systems, it enab'
    type: TextQuoteSelector
  selector_sha256: sha256:2a8aca250654116bd18b5fa9f54207af9d8a6e857dad60863ff45f6cff6f8354
  snapshot_sha256: sha256:6d3ec93b28c20f1d6c6ed715f5d74f3bb9926711504984be17e6cef7464bb9ea
- evidence_id: evidence-f362a701ea73
  position:
    end: 29176
    start: 29069
    type: TextPositionSelector
  quote_sha256: sha256:c59f3605299264c4824446acd11303edf0ded46abb8b14a57dd0a025cdfbedbe
  selector:
    exact: In operating systems, it enables efficient process scheduling (e.g., Linux
      CFS) and virtual memory mapping.
    prefix: 't in C++ and TreeMap in Java.

      - '
    suffix: '

      - It organizes directory struct'
    type: TextQuoteSelector
  selector_sha256: sha256:2f87819cad349137abd5b88d2906abb6b45387580cc0cc8ceaa26463a2660b6f
  snapshot_sha256: sha256:6d3ec93b28c20f1d6c6ed715f5d74f3bb9926711504984be17e6cef7464bb9ea
- evidence_id: evidence-4bfb3ccb8bd6
  position:
    end: 29270
    start: 29179
    type: TextPositionSelector
  quote_sha256: sha256:5605f9f5ad7d378028fe7086b3ffed89312cc292731ae1a6d91f75756fc5bcca
  selector:
    exact: It organizes directory structures and tracks disk blocks in file systems
      like XFS and Ext4.
    prefix: ') and virtual memory mapping.

      - '
    suffix: '

      - It also handles high-speed pa'
    type: TextQuoteSelector
  selector_sha256: sha256:6d3fb90998b28532f840c0b1e10e78492d9bec08391bcfceb6210f6feefa08de
  snapshot_sha256: sha256:6d3ec93b28c20f1d6c6ed715f5d74f3bb9926711504984be17e6cef7464bb9ea
extractor: trafilatura/2.2.0
id: web-computer-science-red-black-tree
media_type: text/html
origin: external
raw_ref:
  path: archive/raw/bc36a2b5aa751836d5d188717df9608a64af7c705ab77cb87f235a2e78c77bc2.html
  sha256: sha256:bc36a2b5aa751836d5d188717df9608a64af7c705ab77cb87f235a2e78c77bc2
read_status: retrieved
retrieval:
  acquisition: fetch
  resolved_url: https://www.geeksforgeeks.org/dsa/introduction-to-red-black-tree/
  url: https://www.geeksforgeeks.org/dsa/introduction-to-red-black-tree/
schema_version: source/v1
snapshot_sha256: sha256:6d3ec93b28c20f1d6c6ed715f5d74f3bb9926711504984be17e6cef7464bb9ea
source_type: doc
vault_id: public
---
A Red-Black Tree is a self-balancing binary search tree with a height limit of O(logN), enabling efficient search, insertion, and deletion operations in O(logN) time, unlike standard binary search trees which can take O(N) time.
- Each node has an additional attribute: a color, which can be either red or black.
- These colors are used to maintain balance during insertions and deletions, ensuring efficient data retrieval and manipulation.
Properties of Red-Black Trees
A Red-Black Tree has the following properties:
- Node Color: Each node is either red or black.
- Root Property: The root of the tree is always black.
- Red Node Property: Red nodes cannot have red children (Red nodes cannot be adjacent).
- Black Node Property: Every path from a node to its descendant leaves must have the same number of black nodes.
- Leaf Property: All leaves (NIL nodes) are black.
These properties (no two consecutive reds and same black height) ensure that the longest path from the root to any leaf is no more than twice as long as the shortest path, maintaining the tree's balance and efficient performance.
Balancing
A simple example to understand balancing is that a chain of 3 nodes is not possible in a Red-Black tree. You can try any color combination to see how they violate the Red-Black tree property.
Inferred properties
- The number of black nodes from root to leaf (including NIL); blackHeight >= h/2.
- Height of a red-black tree with N nodes is h <= 2log(N+1)
- The black depth of a node is the number of black nodes from the root to that node.
Basic Operations on Red-Black Tree:
1. Insertion: Inserting a new node involves a two-step process: BST insertion, followed by fixing Red-Black property violations. Consider:
- If the parent of the new node is black, no properties are violated.
- If the parent is red, the tree might violate the Red Property, requiring fixes.
After inserting the new node as red, several cases may occur:
- Case 1 (Uncle is Red): Recolor parent and uncle to black, grandparent to red. Then, move up the tree.
- Case 2 (Uncle is Black): If node is a right child, perform a left rotation on the parent. If the node is a left child, perform a right rotation on the grandparent and recolor.
2. Searching: Searching in Red-Black Trees mirrors BST searching. Begin traversal from the root:
- If the target value equals the current node's value, the node is found.
- If less, move left; if greater, move right.
- Repeat until the target is found or a NIL node is reached.
3. Deletion: Deleting a node involves BST deletion, followed by fixing violations.
- Remove the node using standard BST rules.
- If a black node is deleted, a "double black" condition might arise, which requires specific fixes.
When deleting a black node, resolve "double-black" based on the sibling's color:
- If the sibling is red, rotate the parent, and recolor.
- If the sibling is black:
  - If all of the sibling's children are black, recolor the sibling and propagate the issue.
  - If at least one of the sibling's child is red: 
 a. If the far child is red, rotate the parent and sibling, and recolor.
b. If the near child is red, rotate the sibling and its child, then handle as above.
4. Rotation: Rotations are fundamental for maintaining the balanced structure of a Red-Black Tree (RBT). They preserve tree properties, ensuring the longest path from the root to any leaf is no more than twice the shortest path. These are two types:
i. Left Rotation: A left rotation at node x pivots the tree to the left, promoting its right child y to x's former position. The Transformation Steps are as follows:
- Detach Subtree: Move y's left subtree to become x's new right subtree.
- Shift Parent Link: Update y’s parent to be x’s current parent.
- Relink Parent: Update x’s parent to point to y instead of x.
- Promote Child: Set y’s left child to x.
- Finalize Parent: Set x’s parent to y.
Pseudo-Code Implementation for Left Rotation
void leftRotate(Node* x) {
    // Identify the node to be promoted
    Node* y = x.right;
    // 1. HANDOVER: y's left subtree becomes x's right child
    x.right = y.left;
    if (y.left != NIL) {
        y.left.parent = x;
    }
    // 2. PARENT LINK: Connect y to the rest of the tree
    y.parent = x.parent;
    if (x.parent == NIL) {
        root = y;               // x was the root
    } 
    else if (x == x.parent.left) {
        x.parent.left = y;      // x was a left child
    } 
    else {
        x.parent.right = y;     // x was a right child
    }
    // 3. PIVOT: Finalize the new parent-child bond
    y.left = x;
    x.parent = y;
}
ii. Right Rotation: A right rotation at node x pivots the tree to the right, promoting its left child y to x’s former position.
- Detach Subtree: Move y’s right subtree to become x’s new left subtree.
- Shift Parent Link: Update y’s parent to be x’s current parent.
- Relink Parent: Update x’s parent to point to y instead of x.
- Promote Child: Set y’s right child to x.
- Finalize Parent: Set x’s parent to y.
Pseudo-Code Implementation for Right Rotation
void rightRotate(Node* x) {
    // Identify the node to be promoted (the left child)
    Node* y = x.left;
    // 1. HANDOVER: y's right subtree becomes x's left child
    x.left = y.right;
    if (y.right != NIL) {
        y.right.parent = x;
    }
    // 2. PARENT LINK: Connect y to the rest of the tree
    y.parent = x.parent;
    if (x.parent == nullptr) {
        root = y;                // x was the root
    } 
    else if (x == x.parent.right) {
        x.parent.right = y;      // x was a right child
    } 
    else {
        x.parent.left = y;       // x was a left child
    }
    // 3. PIVOT: Finalize the new parent-child bond
    y.right = x;
    x.parent = y;
}
Here's a detailed implementation of a Red-Black Tree, including all of the operations mentioned above:
#include <iostream>
#include <string>
using namespace std;
// Node structure with explicit pointers for tree navigation
struct Node {
    int data;
    string color; // "RED" or "BLACK"
    Node *left, *right, *parent;
    Node(int data) : data(data), color("RED"), 
                     left(nullptr), right(nullptr), parent(nullptr) {}
};
class RedBlackTree {
private:
    Node* root;
    Node* NIL; // Sentinel node used to represent leaves (always BLACK)
    // --- Rotations: Essential for maintaining tree balance ---
    void leftRotate(Node* x) {
        Node* y = x->right;
        x->right = y->left;
        if (y->left != NIL) y->left->parent = x;
        y->parent = x->parent;
        if (x->parent == nullptr)      root = y;
        else if (x == x->parent->left) x->parent->left = y;
        else                          x->parent->right = y;
        y->left = x;
        x->parent = y;
    }
    void rightRotate(Node* x) {
        Node* y = x->left;
        x->left = y->right;
        if (y->right != NIL) y->right->parent = x;
        y->parent = x->parent;
        if (x->parent == nullptr)       root = y;
        else if (x == x->parent->right) x->parent->right = y;
        else                           x->parent->left = y;
        y->right = x;
        x->parent = y;
    }
    // --- RB Fix-up: Resolves Double-Red violations ---
    void fixInsert(Node* k) {
        // Continue while the parent is Red (violates RB property)
        while (k != root && k->parent->color == "RED") {
            if (k->parent == k->parent->parent->left) {
                Node* uncle = k->parent->parent->right;
                if (uncle->color == "RED") {            
                    // Case 1: Uncle is Red -> Recolor parent, uncle, and grandparent
                    k->parent->color = "BLACK";
                    uncle->color = "BLACK";
                    k->parent->parent->color = "RED";
                    k = k->parent->parent;
                } else {
                    if (k == k->parent->right) {       
                        // Case 2: Triangle shape -> Left rotate parent to form a line
                        k = k->parent;
                        leftRotate(k);
                    }
                    // Case 3: Line shape -> Recolor and right rotate grandparent
                    k->parent->color = "BLACK";        
                    k->parent->parent->color = "RED";
                    rightRotate(k->parent->parent);
                }
            } else {                                   
                // Mirror Case: Parent is the right child
                Node* uncle = k->parent->parent->left;
                if (uncle->color == "RED") {
                    k->parent->color = "BLACK";
                    uncle->color = "BLACK";
                    k->parent->parent->color = "RED";
                    k = k->parent->parent;
                } else {
                    if (k == k->parent->left) {
                        k = k->parent;
                        rightRotate(k);
                    }
                    k->parent->color = "BLACK";
                    k->parent->parent->color = "RED";
                    leftRotate(k->parent->parent);
                }
            }
        }
        root->color = "BLACK"; // Root must always be Black
    }
public:
    RedBlackTree() {
        NIL = new Node(0);
        NIL->color = "BLACK";
        NIL->left = NIL->right = NIL;
        root = NIL;
    }
    void insert(int data) {
        Node* node = new Node(data);
        node->left = node->right = NIL;
        Node* parent = nullptr;
        Node* current = root;
        // Step 1: Standard Binary Search Tree insertion
        while (current != NIL) {
            parent = current;
            if (node->data < current->data) current = current->left;
            else current = current->right;
        }
        node->parent = parent;
        if (parent == nullptr)      root = node;
        else if (node->data < parent->data) parent->left = node;
        else                               parent->right = node;
        // Step 2: Handle edge cases and fix RB properties
        if (node->parent == nullptr) {
            node->color = "BLACK";
            return;
        }
        if (node->parent->parent == nullptr) return;
        fixInsert(node);
    }
    void inorder(Node* node) {
        if (node != NIL) {
            inorder(node->left);
            cout << node->data << "(" << node->color << ") ";
            inorder(node->right);
        }
    }
    Node* getRoot() { return root; }
};
int main() {
    RedBlackTree rbt;
    rbt.insert(10);
    rbt.insert(20);
    rbt.insert(30);
    rbt.insert(15);
    cout << "Inorder Traversal -> ";
    rbt.inorder(rbt.getRoot());
    cout << endl;
    return 0;
}
import java.util.*;
class Node {
    int data;
    String color; // "RED" or "BLACK"
    Node left, right, parent;
    Node(int data) {
        this.data = data;
        this.color = "RED";
        this.left = null;
        this.right = null;
        this.parent = null;
    }
}
class RedBlackTree {
    private Node root;
    private Node NIL; // Sentinel node used to represent leaves (always BLACK)
    // --- Rotations: Essential for maintaining tree balance ---
    private void leftRotate(Node x) {
        Node y = x.right;
        x.right = y.left;
        if (y.left!= NIL) y.left.parent = x;
        y.parent = x.parent;
        if (x.parent == null) root = y;
        else if (x == x.parent.left) x.parent.left = y;
        else x.parent.right = y;
        y.left = x;
        x.parent = y;
    }
    private void rightRotate(Node x) {
        Node y = x.left;
        x.left = y.right;
        if (y.right!= NIL) y.right.parent = x;
        y.parent = x.parent;
        if (x.parent == null) root = y;
        else if (x == x.parent.right) x.parent.right = y;
        else x.parent.left = y;
        y.right = x;
        x.parent = y;
    }
    // --- RB Fix-up: Resolves Double-Red violations ---
    private void fixInsert(Node k) {
        // Continue while the parent is Red (violates RB property)
        while (k!= root && k.parent.color.equals("RED")) {
            if (k.parent == k.parent.parent.left) {
                Node uncle = k.parent.parent.right;
                if (uncle.color.equals("RED")) {
                    // Case 1: Uncle is Red -> Recolor parent, uncle, and grandparent
                    k.parent.color = "BLACK";
                    uncle.color = "BLACK";
                    k.parent.parent.color = "RED";
                    k = k.parent.parent;
                } else {
                    if (k == k.parent.right) {
                        // Case 2: Triangle shape -> Left rotate parent to form a line
                        k = k.parent;
                        leftRotate(k);
                    }
                    // Case 3: Line shape -> Recolor and right rotate grandparent
                    k.parent.color = "BLACK";
                    k.parent.parent.color = "RED";
                    rightRotate(k.parent.parent);
                }
            } else {
                // Mirror Case: Parent is the right child
                Node uncle = k.parent.parent.left;
                if (uncle.color.equals("RED")) {
                    k.parent.color = "BLACK";
                    uncle.color = "BLACK";
                    k.parent.parent.color = "RED";
                    k = k.parent.parent;
                } else {
                    if (k == k.parent.left) {
                        k = k.parent;
                        rightRotate(k);
                    }
                    k.parent.color = "BLACK";
                    k.parent.parent.color = "RED";
                    leftRotate(k.parent.parent);
                }
            }
        }
        root.color = "BLACK"; // Root must always be Black
    }
    public RedBlackTree() {
        NIL = new Node(0);
        NIL.color = "BLACK";
        NIL.left = NIL.right = NIL;
        root = NIL;
    }
    public void insert(int data) {
        Node node = new Node(data);
        node.left = node.right = NIL;
        Node parent = null;
        Node current = root;
        // Step 1: Standard Binary Search Tree insertion
        while (current!= NIL) {
            parent = current;
            if (node.data < current.data) current = current.left;
            else current = current.right;
        }
        node.parent = parent;
        if (parent == null) root = node;
        else if (node.data < parent.data) parent.left = node;
        else parent.right = node;
        // Step 2: Handle edge cases and fix RB properties
        if (node.parent == null) {
            node.color = "BLACK";
            return;
        }
        if (node.parent.parent == null) return;
        fixInsert(node);
    }
    public void inorder(Node node) {
        if (node!= NIL) {
            inorder(node.left);
            System.out.print(node.data + "(" + node.color + ") ");
            inorder(node.right);
        }
    }
    public Node getRoot() { return root; }
}
public class Main {
    public static void main(String[] args) {
        RedBlackTree rbt = new RedBlackTree();
        rbt.insert(10);
        rbt.insert(20);
        rbt.insert(30);
        rbt.insert(15);
        System.out.print("Inorder Traversal -> ");
        rbt.inorder(rbt.getRoot());
        System.out.println();
    }
}
from typing import Optional
# Node structure with explicit pointers for tree navigation
class Node:
    def __init__(self, data: int):
        self.data = data
        self.color = "RED"  # "RED" or "BLACK"
        self.left = None
        self.right = None
        self.parent = None
class RedBlackTree:
    def __init__(self):
        self.NIL = Node(0)
        self.NIL.color = "BLACK"
        self.root = self.NIL
    # --- Rotations: Essential for maintaining tree balance ---
    def left_rotate(self, x: Node):
        y = x.right
        x.right = y.left
        if y.left is not self.NIL:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y
    def right_rotate(self, x: Node):
        y = x.left
        x.left = y.right
        if y.right is not self.NIL:
            y.right.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y
    # --- RB Fix-up: Resolves Double-Red violations ---
    def fix_insert(self, k: Node):
        while k!= self.root and k.parent.color == "RED":
            if k.parent == k.parent.parent.left:
                uncle = k.parent.parent.right
                if uncle.color == "RED":
                    k.parent.color = "BLACK"
                    uncle.color = "BLACK"
                    k.parent.parent.color = "RED"
                    k = k.parent.parent
                else:
                    if k == k.parent.right:
                        k = k.parent
                        self.left_rotate(k)
                    k.parent.color = "BLACK"
                    k.parent.parent.color = "RED"
                    self.right_rotate(k.parent.parent)
            else:
                uncle = k.parent.parent.left
                if uncle.color == "RED":
                    k.parent.color = "BLACK"
                    uncle.color = "BLACK"
                    k.parent.parent.color = "RED"
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        k = k.parent
                        self.right_rotate(k)
                    k.parent.color = "BLACK"
                    k.parent.parent.color = "RED"
                    self.left_rotate(k.parent.parent)
        self.root.color = "BLACK"  # Root must always be Black
    def insert(self, data: int):
        node = Node(data)
        node.left = self.NIL
        node.right = self.NIL
        parent = None
        current = self.root
        # Step 1: Standard Binary Search Tree insertion
        while current!= self.NIL:
            parent = current
            if node.data < current.data:
                current = current.left
            else:
                current = current.right
        node.parent = parent
        if parent is None:
            self.root = node
        elif node.data < parent.data:
            parent.left = node
        else:
            parent.right = node
        # Step 2: Handle edge cases and fix RB properties
        if node.parent is None:
            node.color = "BLACK"
            return
        if node.parent.parent is None:
            return
        self.fix_insert(node)
    def inorder(self, node: Node):
        if node!= self.NIL:
            self.inorder(node.left)
            print(f"{node.data}({node.color})", end=" ")
            self.inorder(node.right)
if __name__ == "__main__":
    rbt = RedBlackTree()
    rbt.insert(10)
    rbt.insert(20)
    rbt.insert(30)
    rbt.insert(15)
    print("Inorder Traversal ->", end=" ")
    rbt.inorder(rbt.root)
    print()
using System;
// Node structure with explicit pointers for tree navigation
public class Node {
    public int Data;
    public string Color; // "RED" or "BLACK"
    public Node Left, Right, Parent;
    public Node(int data) {
        Data = data;
        Color = "RED";
        Left = null;
        Right = null;
        Parent = null;
    }
}
public class RedBlackTree {
    private Node root;
    private Node NIL; // Sentinel node used to represent leaves (always BLACK)
    // --- Rotations: Essential for maintaining tree balance ---
    private void LeftRotate(Node x) {
        Node y = x.Right;
        x.Right = y.Left;
        if (y.Left!= NIL) y.Left.Parent = x;
        y.Parent = x.Parent;
        if (x.Parent == null)      root = y;
        else if (x == x.Parent.Left) x.Parent.Left = y;
        else                          x.Parent.Right = y;
        y.Left = x;
        x.Parent = y;
    }
    private void RightRotate(Node x) {
        Node y = x.Left;
        x.Left = y.Right;
        if (y.Right!= NIL) y.Right.Parent = x;
        y.Parent = x.Parent;
        if (x.Parent == null)       root = y;
        else if (x == x.Parent.Right) x.Parent.Right = y;
        else                           x.Parent.Left = y;
        y.Right = x;
        x.Parent = y;
    }
    // --- RB Fix-up: Resolves Double-Red violations ---
    private void FixInsert(Node k) {
        // Continue while the parent is Red (violates RB property)
        while (k!= root && k.Parent.Color == "RED") {
            if (k.Parent == k.Parent.Parent.Left) {
                Node uncle = k.Parent.Parent.Right;
                if (uncle.Color == "RED") {            
                    // Case 1: Uncle is Red -> Recolor parent, uncle, and grandparent
                    k.Parent.Color = "BLACK";
                    uncle.Color = "BLACK";
                    k.Parent.Parent.Color = "RED";
                    k = k.Parent.Parent;
                } else {
                    if (k == k.Parent.Right) {       
                        // Case 2: Triangle shape -> Left rotate parent to form a line
                        k = k.Parent;
                        LeftRotate(k);
                    }
                    // Case 3: Line shape -> Recolor and right rotate grandparent
                    k.Parent.Color = "BLACK";        
                    k.Parent.Parent.Color = "RED";
                    RightRotate(k.Parent.Parent);
                }
            } else {                    
                // Mirror Case: Parent is the right child
                Node uncle = k.Parent.Parent.Left;
                if (uncle.Color == "RED") {
                    k.Parent.Color = "BLACK";
                    uncle.Color = "BLACK";
                    k.Parent.Parent.Color = "RED";
                    k = k.Parent.Parent;
                } else {
                    if (k == k.Parent.Left) {
                        k = k.Parent;
                        RightRotate(k);
                    }
                    k.Parent.Color = "BLACK";
                    k.Parent.Parent.Color = "RED";
                    LeftRotate(k.Parent.Parent);
                }
            }
        }
        root.Color = "BLACK"; // Root must always be Black
    }
    public RedBlackTree() {
        NIL = new Node(0);
        NIL.Color = "BLACK";
        NIL.Left = NIL.Right = NIL;
        root = NIL;
    }
    public void Insert(int data) {
        Node node = new Node(data);
        node.Left = node.Right = NIL;
        Node parent = null;
        Node current = root;
        // Step 1: Standard Binary Search Tree insertion
        while (current!= NIL) {
            parent = current;
            if (node.Data < current.Data) current = current.Left;
            else current = current.Right;
        }
        node.Parent = parent;
        if (parent == null)      root = node;
        else if (node.Data < parent.Data) parent.Left = node;
        else                               parent.Right = node;
        // Step 2: Handle edge cases and fix RB properties
        if (node.Parent == null) {
            node.Color = "BLACK";
            return;
        }
        if (node.Parent.Parent == null) return;
        FixInsert(node);
    }
    public void Inorder(Node node) {
        if (node!= NIL) {
            Inorder(node.Left);
            Console.Write(node.Data + "(" + node.Color + ") ");
            Inorder(node.Right);
        }
    }
    public Node GetRoot() { return root; }
}
public class GFG {
    public static void Main() {
        RedBlackTree rbt = new RedBlackTree();
        rbt.Insert(10);
        rbt.Insert(20);
        rbt.Insert(30);
        rbt.Insert(15);
        Console.Write("Inorder Traversal -> ");
        rbt.Inorder(rbt.GetRoot());
        Console.WriteLine();
    }
}
// Node structure with explicit pointers for tree navigation
class Node {
    constructor(data) {
        this.data = data;
        this.color = "RED";  // "RED" or "BLACK"
        this.left = null;
        this.right = null;
        this.parent = null;
    }
}
class RedBlackTree {
    constructor() {
        this.NIL = new Node(0);
        this.NIL.color = "BLACK";
        this.root = this.NIL;
    }
    // --- Rotations: Essential for maintaining tree balance ---
    leftRotate(x) {
        let y = x.right;
        x.right = y.left;
        if (y.left !== this.NIL) {
            y.left.parent = x;
        }
        y.parent = x.parent;
        if (x.parent === null) {
            this.root = y;
        } else if (x === x.parent.left) {
            x.parent.left = y;
        } else {
            x.parent.right = y;
        }
        y.left = x;
        x.parent = y;
    }
    rightRotate(x) {
        let y = x.left;
        x.left = y.right;
        if (y.right !== this.NIL) {
            y.right.parent = x;
        }
        y.parent = x.parent;
        if (x.parent === null) {
            this.root = y;
        } else if (x === x.parent.right) {
            x.parent.right = y;
        } else {
            x.parent.left = y;
        }
        y.right = x;
        x.parent = y;
    }
    // --- RB Fix-up: Resolves Double-Red violations ---
    fixInsert(k) {
        while (k !== this.root && k.parent.color === "RED") {
            if (k.parent === k.parent.parent.left) {
                let uncle = k.parent.parent.right;
                if (uncle.color === "RED") {
                    k.parent.color = "BLACK";
                    uncle.color = "BLACK";
                    k.parent.parent.color = "RED";
                    k = k.parent.parent;
                } else {
                    if (k === k.parent.right) {
                        k = k.parent;
                        this.leftRotate(k);
                    }
                    k.parent.color = "BLACK";
                    k.parent.parent.color = "RED";
                    this.rightRotate(k.parent.parent);
                }
            } else {
                let uncle = k.parent.parent.left;
                if (uncle.color === "RED") {
                    k.parent.color = "BLACK";
                    uncle.color = "BLACK";
                    k.parent.parent.color = "RED";
                    k = k.parent.parent;
                } else {
                    if (k === k.parent.left) {
                        k = k.parent;
                        this.rightRotate(k);
                    }
                    k.parent.color = "BLACK";
                    k.parent.parent.color = "RED";
                    this.leftRotate(k.parent.parent);
                }
            }
        }
        // Root must always be Black
        this.root.color = "BLACK";
    }
    insert(data) {
        let node = new Node(data);
        node.left = this.NIL;
        node.right = this.NIL;
        let parent = null;
        let current = this.root;
        // Step 1: Standard Binary Search Tree insertion
        while (current !== this.NIL) {
            parent = current;
            if (node.data < current.data) {
                current = current.left;
            } else {
                current = current.right;
            }
        }
        node.parent = parent;
        if (parent === null) {
            this.root = node;
        } else if (node.data < parent.data) {
            parent.left = node;
        } else {
            parent.right = node;
        }
        // Step 2: Handle edge cases and fix RB properties
        if (node.parent === null) {
            node.color = "BLACK";
            return;
        }
        if (node.parent.parent === null) {
            return;
        }
        this.fixInsert(node);
    }
    inorder(node, result = []) {
        if (node !== this.NIL) {
            this.inorder(node.left, result);
            result.push(`${node.data}(${node.color})`);
            this.inorder(node.right, result);
        }
        return result;
    }
}
// ---------------- MAIN ----------------
const rbt = new RedBlackTree();
rbt.insert(10);
rbt.insert(20);
rbt.insert(30);
rbt.insert(15);
const traversal = rbt.inorder(rbt.root);
console.log("Inorder Traversal ->", traversal.join(" "));
Output
Inorder Traversal -> 10(BLACK) 15(RED) 20(BLACK) 30(BLACK) 
Advantages
- Because of their self-balancing property, they offer high efficiency in searching, insertion, and deletion, with a worst-case time complexity of O(log n).
- Red-Black Trees have straightforward rules for insertion, deletion, and balance, making them relatively easy to implement.
- Suitable for use in maps, sets, and priority queues.
Disadvantages
- Red-Black Trees have more intricate insertion and deletion rules compared to simpler balanced trees like AVL trees.
- Maintaining the Red-Black Tree properties introduces a minor overhead during insertion and deletion operations.
Applications of Red-Black Trees:
- Powers high-performance containers such as map and set in C++ and TreeMap in Java.
- In operating systems, it enables efficient process scheduling (e.g., Linux CFS) and virtual memory mapping.
- It organizes directory structures and tracks disk blocks in file systems like XFS and Ext4.
- It also handles high-speed packet filtering and routing table lookups in network routing.
- Optimizing in-memory storage and data retrieval speed in key-value stores using database indexing.