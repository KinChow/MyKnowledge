# AVL 树

## 概念

*A binary tree is a tree data structure in which each node can have at most two children, which are referred to as the left child and the right child.* 



## 操作

- Inserting an element.
- Removing an element.
- Searching for an element.
- Deletion for an element.
- Traversing an element. There are four (mainly three) types of traversals in a binary tree which will be discussed ahead.
  - Depth-First Search (DFS) Algorithms
    - **Preorder Traversal (current-left-right):** Visit the current node before visiting any nodes inside the left or right subtrees. Here, the traversal is root – left child – right child. It means that the root node is traversed first then its left child and finally the right child.
    - **Inorder Traversal (left-current-right):** Visit the current node after visiting all nodes inside the left subtree but before visiting any node within the right subtree. Here, the traversal is left child – root – right child.  It means that the left child is traversed first then its root node and finally the right child.
    - **Postorder Traversal (left-right-current):** Visit the current node after visiting all the nodes of the left and right subtrees. Here, the traversal is left child – right child – root.  It means that the left child has traversed first then the right child and finally its root node.
  - Breadth-First Search (BFS) Algorithms
    - **Level Order Traversal:** Visit nodes level-by-level and left-to-right fashion at the same level. Here, the traversal is level-wise. It means that the most left child has traversed first and then the other children of the same level from left to right have traversed. 
- Finding the height of the tree
- Find the level of the tree
- Finding the size of the entire tree.





## 优劣

### 优点

- **Efficient searching**: Binary trees are particularly efficient when searching for a specific element, as each node has at most two child nodes, allowing for binary search algorithms to be used. This means that search operations can be performed in O(log n) time complexity.
- **Ordered traversal:** The structure of binary trees enables them to be traversed in a specific order, such as in-order, pre-order, and post-order. This allows for operations to be performed on the nodes in a specific order, such as printing the nodes in sorted order.
- **Memory efficient**: Compared to other tree structures, binary trees are relatively memory-efficient because they only require two child pointers per node. This means that they can be used to store large amounts of data in memory while still maintaining efficient search operations.
- **Fast insertion and deletion:** Binary trees can be used to perform insertions and deletions in O(log n) time complexity. This makes them a good choice for applications that require dynamic data structures, such as database systems.
- **Easy to implement:** Binary trees are relatively easy to implement and understand, making them a popular choice for a wide range of applications.
- **Useful for sorting:** Binary trees can be used to implement efficient sorting algorithms, such as heap sort and binary search tree sort.



### 缺点

- **Limited structure:** Binary trees are limited to two child nodes per node, which can limit their usefulness in certain applications. For example, if a tree requires more than two child nodes per node, a different tree structure may be more suitable.
- **Unbalanced trees:** Unbalanced binary trees, where one subtree is significantly larger than the other, can lead to inefficient search operations. This can occur if the tree is not properly balanced or if data is inserted in a non-random order.
- **Space inefficiency:** Binary trees can be space inefficient when compared to other data structures. This is because each node requires two child pointers, which can be a significant amount of memory overhead for large trees.
- **Slow performance in worst-case scenarios:** In the worst-case scenario, a binary tree can become degenerate, meaning that each node has only one child. In this case, search operations can degrade to O(n) time complexity, where n is the number of nodes in the tree.
- **Complex balancing algorithms:** To ensure that binary trees remain balanced, various balancing algorithms can be used, such as AVL trees and red-black trees. These algorithms can be complex to implement and require additional overhead, making them less suitable for some applications.





## 应用

- In compilers, Expression Trees are used which is an application of binary trees.
- Huffman coding trees are used in data compression algorithms.
- Priority Queue is another application of binary tree that is used for searching maximum or minimum in O(1) time complexity.
- Represent hierarchical data.
- Used in editing software like Microsoft Excel and spreadsheets.
- Useful for indexing segmented at the database is useful in storing cache in the system,
- Syntax trees are used for most famous compilers for programming like GCC, and AOCL to perform arithmetic operations.
- For implementing priority queues.
- Used to find elements in less time (binary search tree)
- Used to enable fast memory allocation in computers. 
- Used to perform encoding and decoding operations.
- Binary trees can be used to organize and retrieve information from large datasets, such as in inverted index and k-d trees.
- Binary trees can be used to represent the decision-making process of computer-controlled characters in games, such as in decision trees.
-  Binary trees can be used to implement searching algorithms, such as in binary search trees which can be used to quickly find an element in a sorted list.
- Binary trees can be used to implement sorting algorithms, such as in heap sort which uses a binary heap to sort elements efficiently.





- **Search algorithms:** Binary search algorithms use the structure of binary trees to efficiently search for a specific element. The search can be performed in O(log n) time complexity, where n is the number of nodes in the tree.
- **Sorting algorithms:** Binary trees can be used to implement efficient sorting algorithms, such as binary search tree sort and heap sort.
- **Database systems:** Binary trees can be used to store data in a database system, with each node representing a record. This allows for efficient search operations and enables the database system to handle large amounts of data.
- **File systems:** Binary trees can be used to implement file systems, where each node represents a directory or file. This allows for efficient navigation and searching of the file system.
- **Compression algorithms:** Binary trees can be used to implement Huffman coding, a compression algorithm that assigns variable-length codes to characters based on their frequency of occurrence in the input data.
- **Decision trees:** Binary trees can be used to implement decision trees, a type of machine learning algorithm used for classification and regression analysis.
- **Game AI**: Binary trees can be used to implement game AI, where each node represents a possible move in the game. The AI algorithm can search the tree to find the best possible move.



- DOM in HTML.
- File explorer.
- Used as the basic data structure in Microsoft Excel and spreadsheets.
- Editor tool: Microsoft Excel and spreadsheets.
- Evaluate an expression
- Routing Algorithms 



## 参考

