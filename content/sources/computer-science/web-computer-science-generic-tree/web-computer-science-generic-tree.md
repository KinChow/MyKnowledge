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
  quote_sha256: sha256:0fbc2e48d51e8ba42b1499ae3cba1e69e162519dcded4fe61152a075c156696b
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
  selector_sha256: sha256:97f94363ff48a4fd5b18ee65a6317ac13bf034fb285896e4a7e0242a3d1ad5ef
  snapshot_sha256: sha256:2f6ca2fb708ccd4b5d294ba561743bc1a89e533c185412f4188879fe28c7a51f
- evidence_id: evidence-4438e87e99f1
  position:
    end: 252
    start: 0
    type: TextPositionSelector
  quote_sha256: sha256:df2fba1dc8eeb0c28d995718276cb7910349edaf88ccb92c81d0d08ac9be0a7c
  selector:
    exact: Generic trees are a collection of nodes where each node is a data structure
      that consists of records and a list of references to its children(duplicate
      references are not allowed). Unlike the linked list, each node stores the address
      of multiple nodes.
    prefix: ''
    suffix: ' Every node stores address of it'
    type: TextQuoteSelector
  selector_sha256: sha256:252fdf772650a8c2e1e0c015619856cf993f38ccd3e65bfb213e79be77e030a1
  snapshot_sha256: sha256:2f6ca2fb708ccd4b5d294ba561743bc1a89e533c185412f4188879fe28c7a51f
- evidence_id: evidence-5263a6f6a6ac
  position:
    end: 453
    start: 379
    type: TextPositionSelector
  quote_sha256: sha256:ab5e599c94b9eb2fa5a107326eefc153d874ab19f0feeebfa6cdb70e5e4e3e0d
  selector:
    exact: 'The Generic trees are the N-ary trees which have the following properties:'
    prefix: 'a separate pointer called root.

      '
    suffix: '

      1. Many children at every node.'
    type: TextQuoteSelector
  selector_sha256: sha256:470f05c5053aa2fa05d1e2144396a945e609c6e2095286e18d3b5bf66b34974c
  snapshot_sha256: sha256:2f6ca2fb708ccd4b5d294ba561743bc1a89e533c185412f4188879fe28c7a51f
- evidence_id: evidence-fa4db717e798
  position:
    end: 485
    start: 457
    type: TextPositionSelector
  quote_sha256: sha256:702c4b1f3a1fb947b166be385a6b0b315f2a1033b1a5eacce7b8bbc8b3e6eaca
  selector:
    exact: Many children at every node.
    prefix: 've the following properties:

      1. '
    suffix: '

      2. The number of nodes for each'
    type: TextQuoteSelector
  selector_sha256: sha256:716e602b1e8ed9ff64239104592b1cf408915e0875545f0295802ff2b4564677
  snapshot_sha256: sha256:2f6ca2fb708ccd4b5d294ba561743bc1a89e533c185412f4188879fe28c7a51f
- evidence_id: evidence-58d6bbdb5a2e
  position:
    end: 547
    start: 489
    type: TextPositionSelector
  quote_sha256: sha256:624c3d2c6fd6d36446adc7bb24a2fa279a68de54da03e6267b7dc4ba135cde83
  selector:
    exact: The number of nodes for each node is not known in advance.
    prefix: 'Many children at every node.

      2. '
    suffix: '

      Example: 

       

      To represent the ab'
    type: TextQuoteSelector
  selector_sha256: sha256:63ba9b05ebbc5289f9c5cf62b90cf177fec954d8232ad212dcd6c138f1f1d384
  snapshot_sha256: sha256:2f6ca2fb708ccd4b5d294ba561743bc1a89e533c185412f4188879fe28c7a51f
- evidence_id: evidence-5e89cf9c3624
  position:
    end: 2416
    start: 2309
    type: TextPositionSelector
  quote_sha256: sha256:a8e91053e278150fb3b9ceb6a75ffcf3e12a46b20305d89e892e3831c99d9475
  selector:
    exact: Memory Wastage - All the pointers are not required in all the cases. Hence,
      there is lot of memory wastage.
    prefix: 'the above representation are:

      - '
    suffix: '

      - Unknown number of children - '
    type: TextQuoteSelector
  selector_sha256: sha256:e03c0f0da7b5c87e6b2827ceef7a80c43fe934f3889547b274dd96131574fb27
  snapshot_sha256: sha256:2f6ca2fb708ccd4b5d294ba561743bc1a89e533c185412f4188879fe28c7a51f
- evidence_id: evidence-519b571cd237
  position:
    end: 2509
    start: 2419
    type: TextPositionSelector
  quote_sha256: sha256:b755a826eb0d8adf660b7bc615326ee8dc9dbbacdcbe094095cd6a4bde33a6a8
  selector:
    exact: Unknown number of children - The number of children for each node is not
      known in advance.
    prefix: 'ere is lot of memory wastage.

      - '
    suffix: '

      Simple Approach:

      For storing th'
    type: TextQuoteSelector
  selector_sha256: sha256:8c15672ca68ac355bb5e0fc33e7f06816bdd3445ec5c0b6a564b3dc0e07153e9
  snapshot_sha256: sha256:2f6ca2fb708ccd4b5d294ba561743bc1a89e533c185412f4188879fe28c7a51f
- evidence_id: evidence-83dfa21cbba1
  position:
    end: 2747
    start: 2659
    type: TextPositionSelector
  quote_sha256: sha256:5c7792526c84e7f922e31e91e1e58bb5e552f09693fa0e04d350136464162416
  selector:
    exact: In Linked list, we can not randomly access any child's address. So it will
      be expensive.
    prefix: 'ome issues with both of them.

      - '
    suffix: '

      - In array, we can randomly acc'
    type: TextQuoteSelector
  selector_sha256: sha256:cb305c617287bc15746630780700615b6c4eff50717f74679b5d00498bc7226e
  snapshot_sha256: sha256:2f6ca2fb708ccd4b5d294ba561743bc1a89e533c185412f4188879fe28c7a51f
- evidence_id: evidence-befe247be0b1
  position:
    end: 2874
    start: 2750
    type: TextPositionSelector
  quote_sha256: sha256:559cd7cd98f4827d2fa3f7612007cd1047af9bb49e4008f7bc6169ec5c9cc764
  selector:
    exact: In array, we can randomly access the address of any child, but we can store
      only fixed number of children's addresses in it.
    prefix: 'ess. So it will be expensive.

      - '
    suffix: '

      Better Approach:

      We can use Dyn'
    type: TextQuoteSelector
  selector_sha256: sha256:b370105709dd5f2a99cdd3cd40d96cff11d441877d63a8420aa5bd5e8d9daa54
  snapshot_sha256: sha256:2f6ca2fb708ccd4b5d294ba561743bc1a89e533c185412f4188879fe28c7a51f
- evidence_id: evidence-18a3b8828169
  position:
    end: 3043
    start: 2892
    type: TextPositionSelector
  quote_sha256: sha256:8ab23c8696197398bcfc036a1efc0c61ccea53cad90dd8bb98fb29e86819b871
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
  selector_sha256: sha256:4d73a2da569187e3d7499e11dfb8f2a3d14f241402c122a18b6f4a839eaa5ec0
  snapshot_sha256: sha256:2f6ca2fb708ccd4b5d294ba561743bc1a89e533c185412f4188879fe28c7a51f
- evidence_id: evidence-e5dcfc7cecfe
  position:
    end: 4069
    start: 4001
    type: TextPositionSelector
  quote_sha256: sha256:ca6e5d25497669b9fa05c303f87ad9c34ee342a3384c57afe91bf1ed260de84a
  selector:
    exact: 'In the first child/next sibling representation, the steps taken are:'
    prefix: 'd / Next sibling representation

      '
    suffix: '

      At each node-link the children '
    type: TextQuoteSelector
  selector_sha256: sha256:9f6462484f2758d30e89a9a1de67fe9e58bbcc8c4af80c0dc031da7e63fcd73c
  snapshot_sha256: sha256:2f6ca2fb708ccd4b5d294ba561743bc1a89e533c185412f4188879fe28c7a51f
- evidence_id: evidence-dc543a38b4da
  position:
    end: 4149
    start: 4070
    type: TextPositionSelector
  quote_sha256: sha256:3a2959f3811b32e191b8cabec2df519b445fdbc92b3b7fcb31e8ea1ade6d0b59
  selector:
    exact: At each node-link the children of the same parent(siblings) from left to
      right.
    prefix: 'sentation, the steps taken are:

      '
    suffix: '

      - Remove the links from parent '
    type: TextQuoteSelector
  selector_sha256: sha256:5839350308f7d9c7892e257392ff467ccf41e250471db014cef33709d8785e6c
  snapshot_sha256: sha256:2f6ca2fb708ccd4b5d294ba561743bc1a89e533c185412f4188879fe28c7a51f
- evidence_id: evidence-9b50296a1951
  position:
    end: 4220
    start: 4152
    type: TextPositionSelector
  quote_sha256: sha256:4064b3027deee4917e4128864b75847060bebdfce657620ba6f4ea67c46c5343
  selector:
    exact: Remove the links from parent to all children except the first child.
    prefix: 'siblings) from left to right.

      - '
    suffix: '

      Since we have a link between ch'
    type: TextQuoteSelector
  selector_sha256: sha256:b60d11cbbac16ef48a30fbfeeb86cecc9e94c30881ed5d89a1094ed4f9195064
  snapshot_sha256: sha256:2f6ca2fb708ccd4b5d294ba561743bc1a89e533c185412f4188879fe28c7a51f
- evidence_id: evidence-24f1ad12af22
  position:
    end: 5396
    start: 5317
    type: TextPositionSelector
  quote_sha256: sha256:8f999f0f6aa698b1da251c70c2b28e6b621a526721b9de3190d37f9eda5e3503
  selector:
    exact: Memory efficient - No extra links are required, hence a lot of memory is
      saved.
    prefix: "g = null;\n    }\n}\nAdvantages:\n- "
    suffix: '

      - Treated as binary trees - Sin'
    type: TextQuoteSelector
  selector_sha256: sha256:59eaf5aa25c617cabe411465eda25d04e6eabefea8659e82b865aaab5a2e92f8
  snapshot_sha256: sha256:2f6ca2fb708ccd4b5d294ba561743bc1a89e533c185412f4188879fe28c7a51f
- evidence_id: evidence-e4d90aa02a5b
  position:
    end: 5591
    start: 5399
    type: TextPositionSelector
  quote_sha256: sha256:c93a1cc9e66f7d2a4a6cff20ed3eadfc850523725a5a9d196bb33d9310e1223b
  selector:
    exact: Treated as binary trees - Since we are able to convert any generic tree
      to binary representation, we can treat all generic trees with a first child/next
      sibling representation as binary trees.
    prefix: 'nce a lot of memory is saved.

      - '
    suffix: ' Instead of left and right point'
    type: TextQuoteSelector
  selector_sha256: sha256:108eb90ee50d79a5c1589e3f9e7a965d9c5a35a8055af2649d32fa4acd09ae6d
  snapshot_sha256: sha256:2f6ca2fb708ccd4b5d294ba561743bc1a89e533c185412f4188879fe28c7a51f
- evidence_id: evidence-f08329fa0d14
  position:
    end: 5748
    start: 5670
    type: TextPositionSelector
  quote_sha256: sha256:f8f60e9be85b64b31cb181c835c1729ba256091e6c7430d8fe650984ced63bcc
  selector:
    exact: Many algorithms can be expressed more easily because it is just a binary
      tree.
    prefix: 'e firstChild and nextSibling.

      - '
    suffix: '

      - Each node is of fixed size ,s'
    type: TextQuoteSelector
  selector_sha256: sha256:0baced8d371c4f7916d39e786a48108a4aeca687d40b5c7c788c8ea000f8dd0b
  snapshot_sha256: sha256:2f6ca2fb708ccd4b5d294ba561743bc1a89e533c185412f4188879fe28c7a51f
- evidence_id: evidence-8266d22eb01e
  position:
    end: 5823
    start: 5751
    type: TextPositionSelector
  quote_sha256: sha256:10c60d8d8636976ffa7c0272f23a0fd928c428fa63e561f986454e2a2a245323
  selector:
    exact: Each node is of fixed size ,so no auxiliary array or vector is required.
    prefix: 'use it is just a binary tree.

      - '
    suffix: '

      Height of generic tree from par'
    type: TextQuoteSelector
  selector_sha256: sha256:6793304d214506cf9d500be6cfe1189bf8ad047d97efd2b2678708a2997ffd20
  snapshot_sha256: sha256:2f6ca2fb708ccd4b5d294ba561743bc1a89e533c185412f4188879fe28c7a51f
- evidence_id: evidence-f9bac1c8c445
  position:
    end: 180
    start: 0
    type: TextPositionSelector
  quote_sha256: sha256:40875c681f5bce9850d5b3f592ce0c165f6ef7887a4e1970a35e3478321c7f8f
  selector:
    exact: Generic trees are a collection of nodes where each node is a data structure
      that consists of records and a list of references to its children(duplicate
      references are not allowed).
    prefix: ''
    suffix: ' Unlike the linked list, each no'
    type: TextQuoteSelector
  selector_sha256: sha256:1a2e2c5f823af8242d8c8a37185da3b3d67dacdf36cf8d9847ad24fc9bce7111
  snapshot_sha256: sha256:2f6ca2fb708ccd4b5d294ba561743bc1a89e533c185412f4188879fe28c7a51f
- evidence_id: evidence-46c603cf9e8c
  position:
    end: 252
    start: 181
    type: TextPositionSelector
  quote_sha256: sha256:cd2d6bb9192edb879e173378f67a753487c45f5840906b485e15f3cf50a42810
  selector:
    exact: Unlike the linked list, each node stores the address of multiple nodes.
    prefix: 'te references are not allowed). '
    suffix: ' Every node stores address of it'
    type: TextQuoteSelector
  selector_sha256: sha256:c339f41a2195ee0df9fa17660c6e43d800decaf51c50847926ddef3b4a37baeb
  snapshot_sha256: sha256:2f6ca2fb708ccd4b5d294ba561743bc1a89e533c185412f4188879fe28c7a51f
- evidence_id: evidence-62968fd58026
  position:
    end: 378
    start: 253
    type: TextPositionSelector
  quote_sha256: sha256:964c6cf807d0fca6a9c28ff2a652d083bca5de798e6adefdd078e634bad03e8b
  selector:
    exact: Every node stores address of its children and the very first node's address
      will be stored in a separate pointer called root.
    prefix: ' the address of multiple nodes. '
    suffix: '

      The Generic trees are the N-ary'
    type: TextQuoteSelector
  selector_sha256: sha256:fc3a48dc16ac1d5168da589eb8f2f9f93847773d8870c47963dd7cbb4469eb15
  snapshot_sha256: sha256:2f6ca2fb708ccd4b5d294ba561743bc1a89e533c185412f4188879fe28c7a51f
extractor: trafilatura/2.2.0
id: web-computer-science-generic-tree
media_type: text/html
origin: external
raw_ref:
  path: archive/raw/3047ffce3756c6a36565a9d627ff564f6d5410f0f332b0dbc1994c9bda1f0c21.html
  sha256: sha256:3047ffce3756c6a36565a9d627ff564f6d5410f0f332b0dbc1994c9bda1f0c21
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