---
archive_policy: text-only
attachments:
- filename: web-computer-science-generic-tree.html
  kind: document
  media_type: text/html
  role: original
  sha256: sha256:3047ffce3756c6a36565a9d627ff564f6d5410f0f332b0dbc1994c9bda1f0c21
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-b72ffbcde843
  position:
    end: 488
    start: 0
    type: TextPositionSelector
  selector:
    exact: 'Generic trees are a collection of nodes where each node is a data structure
      that consists of records and a list of references to its children(duplicate
      references are not allowed). Unlike the linked list, each node stores the address
      of multiple nodes. Every node stores address of its children and the very first
      node''s address will be stored in a separate pointer called root.

      The Generic trees are the N-ary trees which have the following properties:

      1. Many children at every node.

      2.'
    prefix: ''
    suffix: ' The number of nodes for each no'
    type: TextQuoteSelector
  snapshot_sha256: sha256:2f6ca2fb708ccd4b5d294ba561743bc1a89e533c185412f4188879fe28c7a51f
- evidence_id: evidence-4438e87e99f1
  position:
    end: 252
    start: 0
    type: TextPositionSelector
  selector:
    exact: Generic trees are a collection of nodes where each node is a data structure
      that consists of records and a list of references to its children(duplicate
      references are not allowed). Unlike the linked list, each node stores the address
      of multiple nodes.
    prefix: ''
    suffix: ' Every node stores address of it'
    type: TextQuoteSelector
  snapshot_sha256: sha256:2f6ca2fb708ccd4b5d294ba561743bc1a89e533c185412f4188879fe28c7a51f
- evidence_id: evidence-5263a6f6a6ac
  position:
    end: 453
    start: 379
    type: TextPositionSelector
  selector:
    exact: 'The Generic trees are the N-ary trees which have the following properties:'
    prefix: 'a separate pointer called root.

      '
    suffix: '

      1. Many children at every node.'
    type: TextQuoteSelector
  snapshot_sha256: sha256:2f6ca2fb708ccd4b5d294ba561743bc1a89e533c185412f4188879fe28c7a51f
- evidence_id: evidence-fa4db717e798
  position:
    end: 485
    start: 457
    type: TextPositionSelector
  selector:
    exact: Many children at every node.
    prefix: 've the following properties:

      1. '
    suffix: '

      2. The number of nodes for each'
    type: TextQuoteSelector
  snapshot_sha256: sha256:2f6ca2fb708ccd4b5d294ba561743bc1a89e533c185412f4188879fe28c7a51f
- evidence_id: evidence-58d6bbdb5a2e
  position:
    end: 547
    start: 489
    type: TextPositionSelector
  selector:
    exact: The number of nodes for each node is not known in advance.
    prefix: 'Many children at every node.

      2. '
    suffix: '

      Example: 

       

      To represent the ab'
    type: TextQuoteSelector
  snapshot_sha256: sha256:2f6ca2fb708ccd4b5d294ba561743bc1a89e533c185412f4188879fe28c7a51f
- evidence_id: evidence-5e89cf9c3624
  position:
    end: 2416
    start: 2309
    type: TextPositionSelector
  selector:
    exact: Memory Wastage - All the pointers are not required in all the cases. Hence,
      there is lot of memory wastage.
    prefix: 'the above representation are:

      - '
    suffix: '

      - Unknown number of children - '
    type: TextQuoteSelector
  snapshot_sha256: sha256:2f6ca2fb708ccd4b5d294ba561743bc1a89e533c185412f4188879fe28c7a51f
- evidence_id: evidence-519b571cd237
  position:
    end: 2509
    start: 2419
    type: TextPositionSelector
  selector:
    exact: Unknown number of children - The number of children for each node is not
      known in advance.
    prefix: 'ere is lot of memory wastage.

      - '
    suffix: '

      Simple Approach:

      For storing th'
    type: TextQuoteSelector
  snapshot_sha256: sha256:2f6ca2fb708ccd4b5d294ba561743bc1a89e533c185412f4188879fe28c7a51f
- evidence_id: evidence-83dfa21cbba1
  position:
    end: 2747
    start: 2659
    type: TextPositionSelector
  selector:
    exact: In Linked list, we can not randomly access any child's address. So it will
      be expensive.
    prefix: 'ome issues with both of them.

      - '
    suffix: '

      - In array, we can randomly acc'
    type: TextQuoteSelector
  snapshot_sha256: sha256:2f6ca2fb708ccd4b5d294ba561743bc1a89e533c185412f4188879fe28c7a51f
- evidence_id: evidence-befe247be0b1
  position:
    end: 2874
    start: 2750
    type: TextPositionSelector
  selector:
    exact: In array, we can randomly access the address of any child, but we can store
      only fixed number of children's addresses in it.
    prefix: 'ess. So it will be expensive.

      - '
    suffix: '

      Better Approach:

      We can use Dyn'
    type: TextQuoteSelector
  snapshot_sha256: sha256:2f6ca2fb708ccd4b5d294ba561743bc1a89e533c185412f4188879fe28c7a51f
- evidence_id: evidence-18a3b8828169
  position:
    end: 3043
    start: 2892
    type: TextPositionSelector
  selector:
    exact: We can use Dynamic Arrays for storing the address of children. We can randomly
      access any child's address and the size of the vector is also not fixed.
    prefix: 'dresses in it.

      Better Approach:

      '
    suffix: '

      #include <vector>

      class Node {

      '
    type: TextQuoteSelector
  snapshot_sha256: sha256:2f6ca2fb708ccd4b5d294ba561743bc1a89e533c185412f4188879fe28c7a51f
- evidence_id: evidence-e5dcfc7cecfe
  position:
    end: 4069
    start: 4001
    type: TextPositionSelector
  selector:
    exact: 'In the first child/next sibling representation, the steps taken are:'
    prefix: 'd / Next sibling representation

      '
    suffix: '

      At each node-link the children '
    type: TextQuoteSelector
  snapshot_sha256: sha256:2f6ca2fb708ccd4b5d294ba561743bc1a89e533c185412f4188879fe28c7a51f
- evidence_id: evidence-dc543a38b4da
  position:
    end: 4149
    start: 4070
    type: TextPositionSelector
  selector:
    exact: At each node-link the children of the same parent(siblings) from left to
      right.
    prefix: 'sentation, the steps taken are:

      '
    suffix: '

      - Remove the links from parent '
    type: TextQuoteSelector
  snapshot_sha256: sha256:2f6ca2fb708ccd4b5d294ba561743bc1a89e533c185412f4188879fe28c7a51f
- evidence_id: evidence-9b50296a1951
  position:
    end: 4220
    start: 4152
    type: TextPositionSelector
  selector:
    exact: Remove the links from parent to all children except the first child.
    prefix: 'siblings) from left to right.

      - '
    suffix: '

      Since we have a link between ch'
    type: TextQuoteSelector
  snapshot_sha256: sha256:2f6ca2fb708ccd4b5d294ba561743bc1a89e533c185412f4188879fe28c7a51f
- evidence_id: evidence-24f1ad12af22
  position:
    end: 5396
    start: 5317
    type: TextPositionSelector
  selector:
    exact: Memory efficient - No extra links are required, hence a lot of memory is
      saved.
    prefix: "g = null;\n    }\n}\nAdvantages:\n- "
    suffix: '

      - Treated as binary trees - Sin'
    type: TextQuoteSelector
  snapshot_sha256: sha256:2f6ca2fb708ccd4b5d294ba561743bc1a89e533c185412f4188879fe28c7a51f
- evidence_id: evidence-e4d90aa02a5b
  position:
    end: 5591
    start: 5399
    type: TextPositionSelector
  selector:
    exact: Treated as binary trees - Since we are able to convert any generic tree
      to binary representation, we can treat all generic trees with a first child/next
      sibling representation as binary trees.
    prefix: 'nce a lot of memory is saved.

      - '
    suffix: ' Instead of left and right point'
    type: TextQuoteSelector
  snapshot_sha256: sha256:2f6ca2fb708ccd4b5d294ba561743bc1a89e533c185412f4188879fe28c7a51f
- evidence_id: evidence-f08329fa0d14
  position:
    end: 5748
    start: 5670
    type: TextPositionSelector
  selector:
    exact: Many algorithms can be expressed more easily because it is just a binary
      tree.
    prefix: 'e firstChild and nextSibling.

      - '
    suffix: '

      - Each node is of fixed size ,s'
    type: TextQuoteSelector
  snapshot_sha256: sha256:2f6ca2fb708ccd4b5d294ba561743bc1a89e533c185412f4188879fe28c7a51f
- evidence_id: evidence-8266d22eb01e
  position:
    end: 5823
    start: 5751
    type: TextPositionSelector
  selector:
    exact: Each node is of fixed size ,so no auxiliary array or vector is required.
    prefix: 'use it is just a binary tree.

      - '
    suffix: '

      Height of generic tree from par'
    type: TextQuoteSelector
  snapshot_sha256: sha256:2f6ca2fb708ccd4b5d294ba561743bc1a89e533c185412f4188879fe28c7a51f
- evidence_id: evidence-f9bac1c8c445
  position:
    end: 180
    start: 0
    type: TextPositionSelector
  selector:
    exact: Generic trees are a collection of nodes where each node is a data structure
      that consists of records and a list of references to its children(duplicate
      references are not allowed).
    prefix: ''
    suffix: ' Unlike the linked list, each no'
    type: TextQuoteSelector
  snapshot_sha256: sha256:2f6ca2fb708ccd4b5d294ba561743bc1a89e533c185412f4188879fe28c7a51f
- evidence_id: evidence-46c603cf9e8c
  position:
    end: 252
    start: 181
    type: TextPositionSelector
  selector:
    exact: Unlike the linked list, each node stores the address of multiple nodes.
    prefix: 'te references are not allowed). '
    suffix: ' Every node stores address of it'
    type: TextQuoteSelector
  snapshot_sha256: sha256:2f6ca2fb708ccd4b5d294ba561743bc1a89e533c185412f4188879fe28c7a51f
- evidence_id: evidence-62968fd58026
  position:
    end: 378
    start: 253
    type: TextPositionSelector
  selector:
    exact: Every node stores address of its children and the very first node's address
      will be stored in a separate pointer called root.
    prefix: ' the address of multiple nodes. '
    suffix: '

      The Generic trees are the N-ary'
    type: TextQuoteSelector
  snapshot_sha256: sha256:2f6ca2fb708ccd4b5d294ba561743bc1a89e533c185412f4188879fe28c7a51f
extractor: trafilatura/2.2.0
id: web-computer-science-generic-tree
media_type: text/html
origin: external
raw_ref:
  path: archive/raw/3047ffce3756c6a36565a9d627ff564f6d5410f0f332b0dbc1994c9bda1f0c21.html
read_status: retrieved
retrieval:
  acquisition: fetch
  resolved_url: https://www.geeksforgeeks.org/dsa/generic-treesn-array-trees/
  url: https://www.geeksforgeeks.org/dsa/generic-treesn-array-trees/
schema_version: source/v1
snapshot_sha256: sha256:2f6ca2fb708ccd4b5d294ba561743bc1a89e533c185412f4188879fe28c7a51f
source_type: doc
vault_id: public
---
Generic trees are a collection of nodes where each node is a data structure that consists of records and a list of references to its children(duplicate references are not allowed). Unlike the linked list, each node stores the address of multiple nodes. Every node stores address of its children and the very first node's address will be stored in a separate pointer called root.
The Generic trees are the N-ary trees which have the following properties:
1. Many children at every node.
2. The number of nodes for each node is not known in advance.
Example: 
 
To represent the above tree, we have to consider the worst case, that is the node with maximum children (in above example, 6 children) and allocate that many pointers for each node.
The node representation based on this method can be written as:
 
// Node declaration
struct Node{
   int data;
   Node *firstchild;
   Node *secondchild;
   Node *thirdchild;
   Node *fourthchild;
   Node *fifthchild;
   Node *sixthchild;
};
//Node declaration
struct Node{
   int data;
   struct Node *firstchild;
   struct Node *secondchild;
   struct Node *thirdchild;
   struct Node *fourthchild;
   struct Node *fifthchild;
   struct Node *sixthchild;
}
// Java code for above approach
public class Node {
    int data;
    Node firstchild;
    Node secondchild;
    Node thirdchild;
    Node fourthchild;
    Node fifthchild;
    Node sixthchild;
}
class Node:
    def __init__(self, data):
        self.data = data
        self.firstchild = None
        self.secondchild = None
        self.thirdchild = None
        self.fourthchild = None
        self.fifthchild = None
        self.sixthchild = None
public class Node
{
    public int Data { get; set; }
    public Node Firstchild { get; set; }
    public Node Secondchild { get; set; }
    public Node Thirdchild { get; set; }
    public Node Fourthchild { get; set; }
    public Node Fifthchild { get; set; }
    public Node Sixthchild { get; set; }
}
// Javascript code for above approach
class Node {
    constructor(data) {
        this.data = data;
        this.firstchild = null;
        this.secondchild = null;
        this.thirdchild = null;
        this.fourthchild = null;
        this.fifthchild = null;
        this.sixthchild = null;
    }
}
Disadvantages of the above representation are:
- Memory Wastage - All the pointers are not required in all the cases. Hence, there is lot of memory wastage.
- Unknown number of children - The number of children for each node is not known in advance.
Simple Approach:
For storing the address of children in a node we can use an array or linked list. But we will face some issues with both of them.
- In Linked list, we can not randomly access any child's address. So it will be expensive.
- In array, we can randomly access the address of any child, but we can store only fixed number of children's addresses in it.
Better Approach:
We can use Dynamic Arrays for storing the address of children. We can randomly access any child's address and the size of the vector is also not fixed.
#include <vector>
class Node {
public:
    int data;
    std::vector<Node*> children;
    Node(int data)
    {
        this->data = data;
    }
};
//Node declaration
struct Node{
    int data;
  
    // A dynamic array of children
    struct Node **children; 
}
import java.util.ArrayList;
class Node {
    int data;
    ArrayList<Node> children;
    Node(int data)
    {
        this.data = data;
        this.children = new ArrayList<Node>();
    }
}
class Node:
    
    def __init__(self,data):
        self.data = data
        self.children = []
using System.Collections.Generic;
class Node {
    public int data;
    public List<Node> children;
    public Node(int data)
    {
        this.data = data;
        this.children = new List<Node>();
    }
}
// This code is contributed by adityamaharshi21.
class Node {
  constructor(data) {
    this.data = data;
    this.children = [];
  }
}
Efficient Approach:
First child / Next sibling representation
In the first child/next sibling representation, the steps taken are:
At each node-link the children of the same parent(siblings) from left to right.
- Remove the links from parent to all children except the first child.
Since we have a link between children, we do not need extra links from parents to all the children. This representation allows us to traverse all the elements by starting at the first child of the parent.
 
The node declaration for first child / next sibling representation can be written as: 
 
struct Node {
    int data;
    Node *firstChild;
    Node *nextSibling;
};
//Node declaration
struct Node{
    int data;
    struct Node *firstChild;
    struct Node *nextSibling;
}
class Node {
    int data;
    Node firstChild;
    Node nextSibling;
}
class Node:
    def __init__(self, data):
        self.data = data
        self.firstChild = None
        self.nextSibling = None
        # This code is contributed by aadityamaharshi
public class Node {
    public int Data
    {
        get;
        set;
    }
    public Node FirstChild
    {
        get;
        set;
    }
    public Node NextSibling
    {
        get;
        set;
    }
}
class Node {
    constructor(data) {
        this.data = data;
        this.firstChild = null;
        this.nextSibling = null;
    }
}
Advantages:
- Memory efficient - No extra links are required, hence a lot of memory is saved.
- Treated as binary trees - Since we are able to convert any generic tree to binary representation, we can treat all generic trees with a first child/next sibling representation as binary trees. Instead of left and right pointers, we just use firstChild and nextSibling.
- Many algorithms can be expressed more easily because it is just a binary tree.
- Each node is of fixed size ,so no auxiliary array or vector is required.
Height of generic tree from parent array 
Generic tree - level order traversal