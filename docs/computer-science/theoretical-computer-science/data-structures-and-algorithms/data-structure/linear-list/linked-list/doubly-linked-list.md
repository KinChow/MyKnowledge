# 双链表

## 概念

*A doubly linked list is a special type of* [**linked list**](https://www.geeksforgeeks.org/data-structures/linked-list/) *in which each node contains a pointer to the previous node as well as the next node in the structure.*



- **Dynamic size:** The size of a doubly linked list can change dynamically, meaning that nodes can be added or removed as needed.
- **Two-way navigation:** In a doubly linked list, each node contains pointers to both the previous and next elements, allowing for navigation in both forward and backward directions.
- **Memory overhead:** Each node in a doubly linked list requires memory for two pointers (previous and next), in addition to the memory required for the data stored in the node.



## 操作



## 优劣

### 好处

- **Two-way navigation:** The doubly linked list structure allows for navigation in both forward and backward directions, making it easier to traverse the list and access elements at any position.
- **Efficient insertion and deletion:** The doubly linked list structure allows for the efficient insertion and deletion of elements at any position in the list. This can be useful in situations where elements need to be added or removed frequently.
- **Versatility:** The doubly linked list can be used to implement a wide range of data structures and algorithms, making it a versatile and useful tool in computer science.



### 坏处

- **Memory overhead:** Each node in a doubly linked list requires memory for two pointers (previous and next), in addition to the memory required for the data stored in the node. This can result in a higher memory overhead compared to a singly linked list, where only one pointer is needed.
- **Slower access times:** Access times for individual elements in a doubly linked list may be slower compared to arrays, as the pointers must be followed to access a specific node.
- **Pointer manipulation:** The doubly linked list structure requires more manipulation of pointers compared to arrays, which can result in more complex code and potential bugs.



## 应用

- **Implementing a Hash Table:** Doubly linked lists can be used to implement hash tables, which are used to store and retrieve data efficiently based on a key.
- **Dynamic Memory Allocation:** In systems programming, doubly linked lists can be used to manage dynamic memory allocation, where memory blocks are allocated and deallocated as needed.
- **Reversing a List:** A doubly linked list can be used to reverse a list efficiently by swapping the previous and next pointers of each node.



## 参考

https://www.geeksforgeeks.org/doubly-linked-list-meaning-in-dsa/?ref=ml_lbp

