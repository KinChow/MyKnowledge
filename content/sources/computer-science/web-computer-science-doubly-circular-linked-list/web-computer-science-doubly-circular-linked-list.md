---
archive_policy: text-only
attachments:
- filename: web-computer-science-doubly-circular-linked-list.html
  kind: document
  media_type: text/html
  role: original
  sha256: sha256:b36957d5615919653ccdbf8e381814eae8a25bcc9aca79d50d1c555a19f14f95
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-f9a479499eee
  position:
    end: 475
    start: 0
    type: TextPositionSelector
  quote_sha256: sha256:b96fada67e66c427156bbb2bc99468fa0f58b6ec42bbb719aa84bef3c69301fd
  selector:
    exact: 'A circular linked list is a data structure where the last node points
      back to the first node, forming a closed loop.

      - Structure: All nodes are connected in a circle, enabling continuous traversal
      without encountering NULL .

      - Difference from Regular Linked List: In a regular linked list, the last node
      points to NULL , whereas in a circular linked list, it points to the first node.

      - Uses: Ideal for tasks like scheduling and managing playlists, where smooth
      and repeated.'
    prefix: ''
    suffix: '

      Types of Circular Linked Lists

      '
    type: TextQuoteSelector
  selector_sha256: sha256:792ff3b4b0b1e3e7715f7d55c0f9dd36b5c0e8b0afcb3fa582bca47ccc74c971
  snapshot_sha256: sha256:2962ff2a04f3a4e867cc2ed3671d54dff23ec5788223fd64c2e47b0953b49785
- evidence_id: evidence-355e5aff8fbb
  position:
    end: 116
    start: 0
    type: TextPositionSelector
  quote_sha256: sha256:465a59183bfe2d5d4b876eb9a44a4cb62c2cdd2ac9a63451c11afa2a0afe1f4d
  selector:
    exact: A circular linked list is a data structure where the last node points back
      to the first node, forming a closed loop.
    prefix: ''
    suffix: '

      - Structure: All nodes are conn'
    type: TextQuoteSelector
  selector_sha256: sha256:6414abf6d9f57fff2fd49299b7664aa72ee6665db05099ab688b72852d83c5e4
  snapshot_sha256: sha256:2962ff2a04f3a4e867cc2ed3671d54dff23ec5788223fd64c2e47b0953b49785
- evidence_id: evidence-b089d48016e4
  position:
    end: 1093
    start: 989
    type: TextPositionSelector
  quote_sha256: sha256:5d51e60703332d785537afa12735be04a7a4fb03ad566b0e157bdeb1b987bad3
  selector:
    exact: In circular doubly linked list, each node has two pointers prev and next,
      similar to doubly linked list.
    prefix: '2. Circular Doubly Linked List:

      '
    suffix: ' The prev pointer points to the '
    type: TextQuoteSelector
  selector_sha256: sha256:86d0a236bec4d18d74a3f2bde42b4e94ce7143e2d4756ca458d4b6bced4de2ff
  snapshot_sha256: sha256:2962ff2a04f3a4e867cc2ed3671d54dff23ec5788223fd64c2e47b0953b49785
- evidence_id: evidence-0348bb935fa5
  position:
    end: 1311
    start: 1177
    type: TextPositionSelector
  quote_sha256: sha256:faac88ccd3d36e61a65387235c51c399e429e2d4f7b04f6981783032a659dab2
  selector:
    exact: Here, in addition to the last node storing the address of the first node,
      the first node will also store the address of the last node.
    prefix: 'e next points to the next node. '
    suffix: '

      Note: Here, we will use the sin'
    type: TextQuoteSelector
  selector_sha256: sha256:1d24429e7ddddb5b2c95a3d6ddf036b40356843b19076f512123615420d04d76
  snapshot_sha256: sha256:2962ff2a04f3a4e867cc2ed3671d54dff23ec5788223fd64c2e47b0953b49785
extractor: trafilatura/2.2.0
id: web-computer-science-doubly-circular-linked-list
media_type: text/html
origin: external
raw_ref:
  path: archive/raw/b36957d5615919653ccdbf8e381814eae8a25bcc9aca79d50d1c555a19f14f95.html
  sha256: sha256:b36957d5615919653ccdbf8e381814eae8a25bcc9aca79d50d1c555a19f14f95
read_status: retrieved
retrieval:
  acquisition: fetch
  resolved_url: https://www.geeksforgeeks.org/dsa/circular-linked-list/
  url: https://www.geeksforgeeks.org/circular-linked-list/
schema_version: source/v1
snapshot_sha256: sha256:2962ff2a04f3a4e867cc2ed3671d54dff23ec5788223fd64c2e47b0953b49785
source_type: doc
vault_id: public
---
A circular linked list is a data structure where the last node points back to the first node, forming a closed loop.
- Structure: All nodes are connected in a circle, enabling continuous traversal without encountering NULL .
- Difference from Regular Linked List: In a regular linked list, the last node points to NULL , whereas in a circular linked list, it points to the first node.
- Uses: Ideal for tasks like scheduling and managing playlists, where smooth and repeated.
Types of Circular Linked Lists
We can create a circular linked list from both singly linked lists and doubly linked lists. So, circular linked lists are basically of two types:
1. Circular Singly Linked List
In Circular Singly Linked List, each node has just one pointer called the "next" pointer. The next pointer of the last node points back to the first node and this results in forming a circle. In this type of Linked list, we can only move through the list in one direction.
2. Circular Doubly Linked List:
In circular doubly linked list, each node has two pointers prev and next, similar to doubly linked list. The prev pointer points to the previous node and the next points to the next node. Here, in addition to the last node storing the address of the first node, the first node will also store the address of the last node.
Note: Here, we will use the singly linked list to explain the working of circular linked lists.
Representation of a Circular Singly Linked List
Let's take a look on the structure of a circular linked list.
Create/Declare a Node of Circular Linked List
class Node {
public:
    int data;
    Node* next;
    // Constructor
    Node(int value) {
        data = value;
        next = nullptr;
    }
};
class Node {
    int data;
    Node next;
    Node(int data){
        this.data = data;
        this.next = null;
    }
}
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
class Node {
    public int data;
    public Node next;
    public Node(int data){
        this.data = data;
        this.next = null;
    }
}
class Node {
    constructor(data){
        this.data = data;
        this.next = null;
    }
}
In the code above, each node has data and a pointer to the next node. When we create multiple nodes for a circular linked list, we only need to connect the last node back to the first one.
Example of Creating a Circular Linked List
Here’s an example of creating a circular linked list with three nodes (10, 20, 30, 40, 50):
Why have we taken a pointer that points to the last node instead of the first node?
For the insertion of a node at the beginning, we need to traverse the whole list. Also, for insertion at the end, the whole list has to be traversed. If instead of the start pointer, we take a pointer to the last node, then in both cases there won't be any need to traverse the whole list. So insertion at the beginning or at the end takes constant time, irrespective of the length of the list.
Application of Linked List
Advantage of Circular Linked List
- Efficient Traversal
- No Null Pointers / References
- Useful for Repetitive Tasks
- Insertion at Beginning or End is O(1)
- Uniform Traversal
- Efficient Memory Utilization
Disadvantage of Circular Linked List
- Complex Implementation
- Infinite Loop Risk
- Harder to Debug
- Deletion Complexity
- Memory Overhead (for Doubly Circular LL)
- Not Cache Friendly
Operations on the Circular Linked List
- Insertion : At the Beginning, At the End and At a Specific Position
- Deletion : Removal from different positions