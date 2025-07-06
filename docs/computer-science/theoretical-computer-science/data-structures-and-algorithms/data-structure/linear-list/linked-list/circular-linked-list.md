# 循环链表

## 概念

*A* [**circular linked list**](https://www.geeksforgeeks.org/circular-linked-list/) *is a special type of* [**linked list**](https://www.geeksforgeeks.org/data-structures/linked-list/) *in which the last node is connected to the first node, creating a continuous loop. In a circular linked list, each node has a reference to the next node in the sequence, just like in a regular linked list, but the last node’s reference points back to the first node.*



- The last node in the list points back to the first node.
- Unlike a regular linked list, which ends with a null reference, a circular linked list has no end, as the last node points back to the first node.
- Circular linked lists can grow or shrink dynamically as elements are added or removed.



## 操作



## 优劣

### 好处

- **Dynamic size:** Circular linked lists can grow or shrink dynamically as elements are added or removed.
- **Applications in various fields:** Circular linked lists have various applications in fields such as operating systems, game development, music and video playback, buffer management, and LRU Cache, among others.
- **Memory utilization:** Circular linked lists are useful in cases where memory utilization is an important consideration, as they allow for the efficient utilization of memory.



- **Efficient operations:** Since the last node of the list points back to the first node, circular linked lists can be traversed quickly and efficiently. This makes them useful for applications that require frequent traversal, such as queue and hash table implementations.
- **Space** **efficiency**: Circular linked lists can be more space-efficient than other types of linked lists because they do not require a separate pointer to keep track of the end of the list. This means that circular linked lists can be more compact and take up less memory than other types of linked lists.
- **Flexibility**: The circular structure of the list allows for greater flexibility in certain applications. For example, a circular linked list can be used to represent a ring or circular buffer, where new elements can be added and old elements can be removed without having to shift the entire list.
- **Dynamic** **size**: Circular linked lists can be dynamically sized, which means that nodes can be added or removed from the list as needed. This makes them useful for applications where the size of the list may change frequently, such as memory allocation and music or media players.
- **Ease** **of** **implementation**: Implementing circular linked lists is often simpler than implementing other types of linked lists. This is because circular linked lists have a simple, circular structure that is easy to understand and implement.



### 坏处

- **Complexity:** As compared to arrays, the implementation of circular linked lists can be more complex, as each node requires a reference to the next node in the sequence.
- **Memory overhead:** Circular linked lists require more memory as compared to arrays, as each node requires a reference to the next node in addition to the data stored in the node.
- **Debugging:** Debugging circular linked lists can be more challenging as compared to arrays, as the circular reference can make it difficult to track the flow of data through the list.



- **Complexity**: Circular linked lists can be more complex than other types of linked lists, especially when it comes to algorithms for insertion and deletion operations. For example, determining the correct position for a new node can be more difficult in a circular linked list than in a linear linked list.
- **Memory** **leaks**: If the pointers in a circular linked list are not managed properly, memory leaks can occur. This happens when a node is removed from the list but its memory is not freed, leading to a buildup of unused memory over time.
- **Traversal can be more difficult:** While traversal of a circular linked list can be efficient, it can also be more difficult than linear traversal, especially if the circular list has a complex structure. Traversing a circular linked list requires careful management of the pointers to ensure that each node is visited exactly once.
- **Lack** **of a natural end:** The circular structure of the list can make it difficult to determine when the end of the list has been reached. This can be a problem in certain applications, such as when processing a list of data in a linear fashion.



## 应用

- **Resource allocation:** In operating systems, circular linked lists are used to implement round-robin scheduling, where processes are given equal time slices in a cyclic fashion.
- **Music and video playback:** Circular linked lists can be used to implement continuous playback of songs or videos.
- **Buffer management:** Circular linked lists can be used to implement circular buffers, which are fixed-size data structures that hold a limited number of elements and overwrite old elements when full.
- **Circular Queues:** Circular linked lists can be used to implement circular queues.



- **Implementation of a Queue:** A circular linked list can be used to implement a queue, where the front and rear of the queue are the first and last nodes of the list, respectively. In this implementation, when an element is enqueued, it is added to the rear of the list and when an element is dequeued, it is removed from the front of the list.
- **Music or Media Player:** Circular linked lists can be used to create a playlist for a music or media player. The playlist can be represented as a circular linked list, where each node contains information about a song or media item, and the next node points to the next song in the playlist. This allows for continuous playback of the playlist.
- **Hash table implementation:** Circular linked lists can be used to implement a hash table, where each index in the table is a circular linked list. This is a form of collision resolution, where when two keys hash to the same index, the nodes are added to the circular linked list at that index.
- **Memory allocation**: In computer memory management, circular linked lists can be used to keep track of allocated and free blocks of memory. Each node in the list represents a block of memory and its status, with the next node pointing to the next block of memory. When a block of memory is freed, it can be added back to the circular linked list.
- **Navigation systems:** Circular linked lists can be used to model the movements of vehicles on a circular route, such as buses, trains or planes that travel in a loop or circular route. Each node in the list represents the location of the vehicle on the route, with the next node pointing to the next location on the route.



- **Music and Media Players:** Circular linked lists can be used to implement playlists in music and media players. Each node in the list can represent a song or media item, and the “next” pointer can point to the next song in the playlist. When the end of the playlist is reached, the pointer can be set to the beginning of the list, creating a circular structure that allows for continuous playback.
- **Task** **Scheduling**: Circular linked lists can be used to implement task scheduling algorithms, where each node in the list represents a task and its priority. The “next” pointer can point to the next task in the queue, with the end of the queue pointing back to the beginning to create a circular structure. This allows for a continuous loop of task scheduling, where tasks are added and removed from the queue based on their priority.
- **Cache Management**: Circular linked lists can be used in cache management algorithms to manage the replacement of cache entries. Each node in the list can represent a cache entry, with the “next” pointer pointing to the next entry in the list. When the end of the list is reached, the pointer can be set to the beginning of the list, creating a circular structure that allows for the replacement of older entries with newer ones.
- **File System Management**: Circular linked lists can be used in file system management to track the allocation of disk space. Each node in the list can represent a block of disk space, with the “next” pointer pointing to the next available block. When the end of the list is reached, the pointer can be set to the beginning of the list, creating a circular structure that allows for the allocation and deallocation of disk space.



## 参考

https://www.geeksforgeeks.org/circular-linked-list-meaning-in-dsa/?ref=ml_lbp

https://www.geeksforgeeks.org/applications-advantages-and-disadvantages-of-circular-linked-list/?ref=ml_lbp