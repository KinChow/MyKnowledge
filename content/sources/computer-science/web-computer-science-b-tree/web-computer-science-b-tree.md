---
archive_policy: text-only
attachments:
- filename: web-computer-science-b-tree.html
  kind: document
  media_type: text/html
  role: original
  sha256: sha256:3b92b8acaee5004285117dedea42ed05303d7de4783daf0cf9e9ebbc6cc7dd66
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-66214b606544
  position:
    end: 112
    start: 0
    type: TextPositionSelector
  selector:
    exact: A B-Tree is a specialized m-way tree designed to optimize data access,
      especially on disk-based storage systems.
    prefix: ''
    suffix: '

      - In a B-Tree of order m, each '
    type: TextQuoteSelector
  snapshot_sha256: sha256:16676146810fb0eb8a30a3fadb08b27a08230ed4b540533f51130ac4a02ed3c2
- evidence_id: evidence-8ae77e263dd5
  position:
    end: 238
    start: 115
    type: TextPositionSelector
  selector:
    exact: In a B-Tree of order m, each node can have up to m children and m-1 keys,
      allowing it to efficiently manage large datasets.
    prefix: 'n disk-based storage systems.

      - '
    suffix: '

      - The value of m is decided bas'
    type: TextQuoteSelector
  snapshot_sha256: sha256:16676146810fb0eb8a30a3fadb08b27a08230ed4b540533f51130ac4a02ed3c2
- evidence_id: evidence-6f6c354a5f7a
  position:
    end: 1116
    start: 1015
    type: TextPositionSelector
  selector:
    exact: All leaf nodes of a B tree are at the same level, i.e. they have the same
      depth (height of the tree).
    prefix: 'ies the following properties:

      - '
    suffix: '

      - The keys of each node of a B '
    type: TextQuoteSelector
  snapshot_sha256: sha256:16676146810fb0eb8a30a3fadb08b27a08230ed4b540533f51130ac4a02ed3c2
- evidence_id: evidence-52ff34eab568
  position:
    end: 841
    start: 724
    type: TextPositionSelector
  selector:
    exact: B-Trees deliver consistent and efficient performance for critical operations
      such as search, insertion, and deletion.
    prefix: 'anced structure at all times,

      - '
    suffix: '

      Following is an example of a B-'
    type: TextQuoteSelector
  snapshot_sha256: sha256:16676146810fb0eb8a30a3fadb08b27a08230ed4b540533f51130ac4a02ed3c2
- evidence_id: evidence-9816f0e07ebc
  position:
    end: 301
    start: 241
    type: TextPositionSelector
  selector:
    exact: The value of m is decided based on disk block and key sizes.
    prefix: 'iently manage large datasets.

      - '
    suffix: '

      - One of the standout features '
    type: TextQuoteSelector
  snapshot_sha256: sha256:16676146810fb0eb8a30a3fadb08b27a08230ed4b540533f51130ac4a02ed3c2
- evidence_id: evidence-d8f1cb6c82c0
  position:
    end: 530
    start: 448
    type: TextPositionSelector
  selector:
    exact: It significantly reduces the tree’s height, hence reducing costly disk
      operations.
    prefix: 'de, including large key values. '
    suffix: '

      - B Trees allow faster data ret'
    type: TextQuoteSelector
  snapshot_sha256: sha256:16676146810fb0eb8a30a3fadb08b27a08230ed4b540533f51130ac4a02ed3c2
- evidence_id: evidence-c030dbd0c441
  position:
    end: 1664
    start: 1596
    type: TextPositionSelector
  selector:
    exact: A non-leaf node with n-1 key values should have n non NULL children.
    prefix: 'hildren and at least one key.

      - '
    suffix: '

      We can see in the above diagram'
    type: TextQuoteSelector
  snapshot_sha256: sha256:16676146810fb0eb8a30a3fadb08b27a08230ed4b540533f51130ac4a02ed3c2
- evidence_id: evidence-a2c2600534ba
  position:
    end: 2414
    start: 2329
    type: TextPositionSelector
  selector:
    exact: While M-way trees can be either balanced or skewed, B-Trees are always
      self-balanced.
    prefix: 'd Performance Over M-way Trees: '
    suffix: ' This self-balancing property en'
    type: TextQuoteSelector
  snapshot_sha256: sha256:16676146810fb0eb8a30a3fadb08b27a08230ed4b540533f51130ac4a02ed3c2
- evidence_id: evidence-c36ad82f4456
  position:
    end: 3257
    start: 3203
    type: TextPositionSelector
  selector:
    exact: Search is similar to the search in Binary Search Tree.
    prefix: 'tree

      Search Operation in B-Tree

      '
    suffix: ' Let the key to be searched is k'
    type: TextQuoteSelector
  snapshot_sha256: sha256:16676146810fb0eb8a30a3fadb08b27a08230ed4b540533f51130ac4a02ed3c2
- evidence_id: evidence-6c2e5c8c86d0
  position:
    end: 3341
    start: 3291
    type: TextPositionSelector
  selector:
    exact: Start from the root and recursively traverse down.
    prefix: 'et the key to be searched is k.

      '
    suffix: ' 

      For every visited non-leaf nod'
    type: TextQuoteSelector
  snapshot_sha256: sha256:16676146810fb0eb8a30a3fadb08b27a08230ed4b540533f51130ac4a02ed3c2
- evidence_id: evidence-8214458f5d1a
  position:
    end: 6663
    start: 6600
    type: TextPositionSelector
  selector:
    exact: It is used in large databases to access data stored on the disk
    prefix: 'k);

      }

      Applications of B-Trees

      - '
    suffix: '

      - Searching for data in a data '
    type: TextQuoteSelector
  snapshot_sha256: sha256:16676146810fb0eb8a30a3fadb08b27a08230ed4b540533f51130ac4a02ed3c2
- evidence_id: evidence-2759f2b8a2fa
  position:
    end: 6824
    start: 6761
    type: TextPositionSelector
  selector:
    exact: With the indexing feature, multilevel indexing can be achieved.
    prefix: 'ly less time using the B-Tree

      - '
    suffix: '

      - Most of the servers also use '
    type: TextQuoteSelector
  snapshot_sha256: sha256:16676146810fb0eb8a30a3fadb08b27a08230ed4b540533f51130ac4a02ed3c2
- evidence_id: evidence-b73b4224b61e
  position:
    end: 6876
    start: 6827
    type: TextPositionSelector
  selector:
    exact: Most of the servers also use the B-tree approach.
    prefix: 'vel indexing can be achieved.

      - '
    suffix: '

      - B-Trees are used in CAD syste'
    type: TextQuoteSelector
  snapshot_sha256: sha256:16676146810fb0eb8a30a3fadb08b27a08230ed4b540533f51130ac4a02ed3c2
- evidence_id: evidence-1c09cbbe9339
  position:
    end: 6949
    start: 6879
    type: TextPositionSelector
  selector:
    exact: B-Trees are used in CAD systems to organize and search geometric data.
    prefix: 'also use the B-tree approach.

      - '
    suffix: '

      - B-Trees are also used in othe'
    type: TextQuoteSelector
  snapshot_sha256: sha256:16676146810fb0eb8a30a3fadb08b27a08230ed4b540533f51130ac4a02ed3c2
- evidence_id: evidence-5363f1317e57
  position:
    end: 7276
    start: 7087
    type: TextPositionSelector
  selector:
    exact: B-Trees have a guaranteed time complexity of O(log n) for basic operations
      like insertion, deletion, and searching, which makes them suitable for large
      data sets and real-time applications.
    prefix: 'graphy.

      Advantages of B-Trees

      - '
    suffix: '

      - B-Trees are self-balancing.

      -'
    type: TextQuoteSelector
  snapshot_sha256: sha256:16676146810fb0eb8a30a3fadb08b27a08230ed4b540533f51130ac4a02ed3c2
- evidence_id: evidence-106c338287c4
  position:
    end: 7306
    start: 7279
    type: TextPositionSelector
  selector:
    exact: B-Trees are self-balancing.
    prefix: 's and real-time applications.

      - '
    suffix: '

      - High-concurrency and high-thr'
    type: TextQuoteSelector
  snapshot_sha256: sha256:16676146810fb0eb8a30a3fadb08b27a08230ed4b540533f51130ac4a02ed3c2
- evidence_id: evidence-2f0c8558da51
  position:
    end: 7346
    start: 7309
    type: TextPositionSelector
  selector:
    exact: High-concurrency and high-throughput.
    prefix: '- B-Trees are self-balancing.

      - '
    suffix: '

      - Efficient storage utilization'
    type: TextQuoteSelector
  snapshot_sha256: sha256:16676146810fb0eb8a30a3fadb08b27a08230ed4b540533f51130ac4a02ed3c2
- evidence_id: evidence-8c0c9f65c122
  position:
    end: 7379
    start: 7349
    type: TextPositionSelector
  selector:
    exact: Efficient storage utilization.
    prefix: 'currency and high-throughput.

      - '
    suffix: '

      Disadvantages of B-Trees

      - B-Tr'
    type: TextQuoteSelector
  snapshot_sha256: sha256:16676146810fb0eb8a30a3fadb08b27a08230ed4b540533f51130ac4a02ed3c2
- evidence_id: evidence-ecdd8791e2b1
  position:
    end: 7486
    start: 7407
    type: TextPositionSelector
  selector:
    exact: B-Trees are based on disk-based data structures and can have a high disk
      usage.
    prefix: 'ion.

      Disadvantages of B-Trees

      - '
    suffix: '

      - Not the best for all cases.

      -'
    type: TextQuoteSelector
  snapshot_sha256: sha256:16676146810fb0eb8a30a3fadb08b27a08230ed4b540533f51130ac4a02ed3c2
- evidence_id: evidence-613b328ca2f2
  position:
    end: 7516
    start: 7489
    type: TextPositionSelector
  selector:
    exact: Not the best for all cases.
    prefix: 'd can have a high disk usage.

      - '
    suffix: '

      - For small datasets, the searc'
    type: TextQuoteSelector
  snapshot_sha256: sha256:16676146810fb0eb8a30a3fadb08b27a08230ed4b540533f51130ac4a02ed3c2
- evidence_id: evidence-76dc09ac3b6d
  position:
    end: 1116
    start: 1013
    type: TextPositionSelector
  selector:
    exact: '- All leaf nodes of a B tree are at the same level, i.e. they have the
      same depth (height of the tree).'
    prefix: 'sfies the following properties:

      '
    suffix: '

      - The keys of each node of a B '
    type: TextQuoteSelector
  snapshot_sha256: sha256:16676146810fb0eb8a30a3fadb08b27a08230ed4b540533f51130ac4a02ed3c2
- evidence_id: evidence-64ae9b2b952f
  position:
    end: 1221
    start: 1117
    type: TextPositionSelector
  selector:
    exact: '- The keys of each node of a B tree (in case of multiple keys), should
      be stored in the ascending order.'
    prefix: 'ame depth (height of the tree).

      '
    suffix: '

      - In a B tree , all non-leaf no'
    type: TextQuoteSelector
  snapshot_sha256: sha256:16676146810fb0eb8a30a3fadb08b27a08230ed4b540533f51130ac4a02ed3c2
- evidence_id: evidence-929c66dfcdfe
  position:
    end: 1309
    start: 1222
    type: TextPositionSelector
  selector:
    exact: '- In a B tree , all non-leaf nodes (except root node) should have at leastm/2
      children.'
    prefix: ' stored in the ascending order.

      '
    suffix: '

      - All nodes (except root node) '
    type: TextQuoteSelector
  snapshot_sha256: sha256:16676146810fb0eb8a30a3fadb08b27a08230ed4b540533f51130ac4a02ed3c2
- evidence_id: evidence-00006726c56b
  position:
    end: 1375
    start: 1310
    type: TextPositionSelector
  selector:
    exact: '- All nodes (except root node) should have at least m/2 - 1 keys.'
    prefix: 'ould have at leastm/2 children.

      '
    suffix: '

      - If the root node is a leaf no'
    type: TextQuoteSelector
  snapshot_sha256: sha256:16676146810fb0eb8a30a3fadb08b27a08230ed4b540533f51130ac4a02ed3c2
- evidence_id: evidence-b1b915105f64
  position:
    end: 447
    start: 304
    type: TextPositionSelector
  selector:
    exact: One of the standout features of a B-Tree is its ability to store a significant
      number of keys within a single node, including large key values.
    prefix: ' on disk block and key sizes.

      - '
    suffix: ' It significantly reduces the tr'
    type: TextQuoteSelector
  snapshot_sha256: sha256:16676146810fb0eb8a30a3fadb08b27a08230ed4b540533f51130ac4a02ed3c2
extractor: trafilatura/2.2.0
id: web-computer-science-b-tree
media_type: text/html
origin: external
raw_ref:
  path: archive/raw/3b92b8acaee5004285117dedea42ed05303d7de4783daf0cf9e9ebbc6cc7dd66.html
read_status: retrieved
retrieval:
  acquisition: fetch
  resolved_url: https://www.geeksforgeeks.org/dsa/introduction-of-b-tree-2/
  url: https://www.geeksforgeeks.org/dsa/introduction-of-b-tree-2/
schema_version: source/v1
snapshot_sha256: sha256:16676146810fb0eb8a30a3fadb08b27a08230ed4b540533f51130ac4a02ed3c2
source_type: doc
vault_id: public
---
A B-Tree is a specialized m-way tree designed to optimize data access, especially on disk-based storage systems.
- In a B-Tree of order m, each node can have up to m children and m-1 keys, allowing it to efficiently manage large datasets.
- The value of m is decided based on disk block and key sizes.
- One of the standout features of a B-Tree is its ability to store a significant number of keys within a single node, including large key values. It significantly reduces the tree’s height, hence reducing costly disk operations.
- B Trees allow faster data retrieval and updates, making them an ideal choice for systems requiring efficient and scalable data management. By maintaining a balanced structure at all times,
- B-Trees deliver consistent and efficient performance for critical operations such as search, insertion, and deletion.
Following is an example of a B-Tree of order 5 .
Properties of a B-Tree
B Tree of order m can be defined as an m-way search tree which satisfies the following properties:
- All leaf nodes of a B tree are at the same level, i.e. they have the same depth (height of the tree).
- The keys of each node of a B tree (in case of multiple keys), should be stored in the ascending order.
- In a B tree , all non-leaf nodes (except root node) should have at leastm/2 children.
- All nodes (except root node) should have at least m/2 - 1 keys.
- If the root node is a leaf node (only node in the tree), then it will have no children and will have at least one key. If the root node is a non-leaf node, then it will have at least 2 children and at least one key.
- A non-leaf node with n-1 key values should have n non NULL children.
We can see in the above diagram that all the leaf nodes are at the same level and all non-leaf nodes have no empty sub-tree and have number of keys one less than the number of their children.
Interesting Facts about B-Tree
1. Height when the B-tree is completely full (i.e., all nodes have the maximum m children):
h_{\text{min}} = \left\lceil \log_{m}(n + 1) \right\rceil - 1 
2.  Height when the B-tree is least filled (each node has the minimum t children):
h_{\text{max}} = \left\lfloor \log_{t} \left( \frac{n + 1}{2} \right) \right\rfloor 
Need of a B-Tree
The B-Tree data structure is essential for several reasons:
- Improved Performance Over M-way Trees: While M-way trees can be either balanced or skewed, B-Trees are always self-balanced. This self-balancing property ensures fewer levels in the tree, significantly reducing access time compared to M-way trees. This makes B-Trees particularly suitable for external storage systems where faster data retrieval is crucial.
- Optimized for Large Datasets: B-Trees are designed to handle millions of records efficiently. Their reduced height and balanced structure enable faster sequential access to data and simplify operations like insertion and deletion. This ensures efficient management of large datasets while maintaining an ordered structure.
Operations on B-Tree
B-Trees support various operations that make them highly efficient for managing large datasets. Below are the key operations:
Note: "n" is the total number of elements in the B-tree
Search Operation in B-Tree
Search is similar to the search in Binary Search Tree. Let the key to be searched is k.
Start from the root and recursively traverse down. 
For every visited non-leaf node 
- If the current node contains k, return the node.
- Otherwise, determine the appropriate child to traverse. This is the child just before the first key greater than k.
If we reach a leaf node and don't find k in the leaf node, then return NULL.
Searching a B-Tree is similar to searching a binary tree. The algorithm is similar and goes with recursion. At each level, the search is optimized as if the key value is not present in the range of the parent then the key is present in another branch. As these values limit the search they are also known as limiting values or separation values. If we reach a leaf node and don’t find the desired key then it will display NULL.
Input: Search 120 in the given B-Tree. 
The key 120 is located in the leaf node containing 110 and 120. The search process is complete.
Algorithm for Searching an Element in a B-Tree
struct Node {
    int n;
    int key[MAX_KEYS];
    Node* child[MAX_CHILDREN];
    bool leaf;
};
Node* BtreeSearch(Node* x, int k) {
    int i = 0;
    while (i < x->n && k > x->key[i]) {
        i++;
    }
    if (i < x->n && k == x->key[i]) {
        return x;
    }
    if (x->leaf) {
        return nullptr;
    }
    return BtreeSearch(x->child[i], k);
}
BtreeSearch(x, k)
    i = 1
    
    // n[x] means number of keys in x node
    while i ? n[x] and k ? keyi[x]
        do i = i + 1
    if i  n[x] and k = keyi[x]
        then return (x, i)   
    if leaf [x]
        then return NIL
    else
        return BtreeSearch(ci[x], k)
class Node {
    int n;
    int[] key = new int[MAX_KEYS];
    Node[] child = new Node[MAX_CHILDREN];
    boolean leaf;
}
Node BtreeSearch(Node x, int k) {
    int i = 0;
    while (i < x.n && k > x.key[i]) {
        i++;
    }
    if (i < x.n && k == x.key[i]) {
        return x;
    }
    if (x.leaf) {
        return null;
    }
    return BtreeSearch(x.child[i], k);
}
class Node:
    def __init__(self):
        self.n = 0
        self.key = [0] * MAX_KEYS
        self.child = [None] * MAX_CHILDREN
        self.leaf = True
def BtreeSearch(x, k):
    i = 0
    while i < x.n and k > x.key[i]:
        i += 1
    if i < x.n and k == x.key[i]:
        return x
    if x.leaf:
        return None
    return BtreeSearch(x.child[i], k)
class Node {
    public int n;
    public int[] key = new int[MAX_KEYS];
    public Node[] child = new Node[MAX_CHILDREN];
    public bool leaf;
}
Node BtreeSearch(Node x, int k) {
    int i = 0;
    while (i < x.n && k > x.key[i]) {
        i++;
    }
    if (i < x.n && k == x.key[i]) {
        return x;
    }
    if (x.leaf) {
        return null;
    }
    return BtreeSearch(x.child[i], k);
}
// Define a Node class with properties n, key, child, and leaf
class Node {
    constructor() {
        this.n = 0;
        this.key = new Array(MAX_KEYS);
        this.child = new Array(MAX_CHILDREN);
        this.leaf = false;
    }
}
// Define a function BtreeSearch that takes in a Node object x and an integer k
function BtreeSearch(x, k) {
    let i = 0;
    while (i < x.n && k > x.key[i]) {
        i++;
    }
    if (i < x.n && k == x.key[i]) {
        return x;
    }
    if (x.leaf) {
        return null;
    }
    return BtreeSearch(x.child[i], k);
}
Applications of B-Trees
- It is used in large databases to access data stored on the disk
- Searching for data in a data set can be achieved in significantly less time using the B-Tree
- With the indexing feature, multilevel indexing can be achieved.
- Most of the servers also use the B-tree approach.
- B-Trees are used in CAD systems to organize and search geometric data.
- B-Trees are also used in other areas such as natural language processing, computer networks, and cryptography.
Advantages of B-Trees
- B-Trees have a guaranteed time complexity of O(log n) for basic operations like insertion, deletion, and searching, which makes them suitable for large data sets and real-time applications.
- B-Trees are self-balancing.
- High-concurrency and high-throughput.
- Efficient storage utilization.
Disadvantages of B-Trees
- B-Trees are based on disk-based data structures and can have a high disk usage.
- Not the best for all cases.
- For small datasets, the search time in a B-Tree might be slower compared to a binary search tree, as each node may contain multiple keys.