# 队列

## 概念

*A* **queue** *is a* [linear data structure](https://www.geeksforgeeks.org/introduction-to-linear-data-structures/) *that is open at both ends and the operations are performed in* [First In First Out (FIFO)](https://www.geeksforgeeks.org/fifo-first-in-first-out-approach-in-programming/) *order.*



- **Simple Queue:** Simple queue also known as a linear queue is the most basic version of a queue. Here, insertion of an element i.e. the Enqueue operation takes place at the rear end and removal of an element i.e. the Dequeue operation takes place at the front end. Here problem is that if we pop some item from front and then rear reach to the capacity of the queue and although there are empty spaces before front means the queue is not full but as per condition in isFull() function, it will show that the queue is full then. To solve this problem we use [circular queue](https://www.geeksforgeeks.org/introduction-and-array-implementation-of-circular-queue/#:~:text=A Circular Queue is a,also called 'Ring Buffer'.).
- [**Circular Queue**](https://www.geeksforgeeks.org/introduction-and-array-implementation-of-circular-queue/#:~:text=A Circular Queue is a,also called 'Ring Buffer'.)**:**  In a circular queue, the element of the queue act as a circular ring. The working of a circular queue is similar to the linear queue except for the fact that the last element is connected to the first element. Its advantage is that the memory is utilized in a better way. This is because if there is an empty space i.e. if no element is present at a certain position in the queue, then an element can be easily added at that position using modulo capacity(*%n*).
- [**Priority Queue**](https://www.geeksforgeeks.org/priority-queue-set-1-introduction/)**:** This queue is a special type of queue. Its specialty is that it arranges the elements in a queue based on some priority. The priority can be something where the element with the highest value has the priority so it creates a queue with decreasing order of values. The priority can also be such that the element with the lowest value gets the highest priority so in turn it creates a queue with increasing order of values. In pre-define priority queue, C++ gives priority to highest value whereas Java gives priority to lowest value.
- [**Dequeue**](https://www.geeksforgeeks.org/deque-set-1-introduction-applications/)**:** Dequeue is also known as Double Ended Queue. As the name suggests double ended, it means that an element can be inserted or removed from both ends of the queue, unlike the other queues in which it can be done only from one end. Because of this property, it may not obey the First In First Out property. 



## 操作

- **enqueue():** Inserts an element at the end of the queue i.e. at the rear end.
- **dequeue():** This operation removes and returns an element that is at the front end of the queue.
- **front():** This operation returns the element at the front end without removing it.
- **rear():** This operation returns the element at the rear end without removing it.
- **isEmpty():** This operation indicates whether the queue is empty or not.
- **isFull():** This operation indicates whether the queue is full or not.
- **size():** This operation returns the size of the queue i.e. the total number of elements it contains.  



## 优劣

### 好处

- Easy to implement.
- A large amount of data can be managed efficiently with ease.
- Operations such as insertion and deletion can be performed with ease as it follows the first in first out rule.



- A large amount of data can be managed efficiently with ease.
- Operations such as insertion and deletion can be performed with ease as it follows the first in first out rule.
- Queues are useful when a particular service is used by multiple consumers.
- Queues are fast in speed for data inter-process communication.
- Queues can be used in the implementation of other data structures.



### 坏处

- Static Data Structure, fixed size.
- If the queue has a large number of enqueue and dequeue operations, at some point (in case of linear increment of front and rear indexes) we may not be able to insert elements in the queue even if the queue is empty (this problem is avoided by using circular queue).
- Maximum size of a queue must be defined prior.



- The operations such as insertion and deletion of elements from the middle are time consuming.
- Limited Space.
- In a classical queue, a new element can only be inserted when the existing elements are deleted from the queue.
- Searching an element takes O(N) time.
- Maximum size of a queue must be defined prior.



## 应用

- It has a single resource and multiple consumers.
- It synchronizes between slow and fast devices.
- In a network, a queue is used in devices such as a router/switch and mail queue.
- Variations: dequeue, priority queue and double-ended priority queue.



- When a resource is shared among multiple consumers. Examples include CPU scheduling, Disk Scheduling. 
-  When data is transferred asynchronously (data not necessarily received at same rate as sent) between two processes. Examples include IO Buffers, pipes, file IO, etc. 
-  Queue can be used as an essential component in various other data structures.



- **Multi programming:** Multi programming means when multiple programs are running in the main memory. It is essential to organize these multiple programs and these multiple programs are organized as queues. 
- **Network:** In a network, a queue is used in devices such as a router or a switch. another application of a queue is a mail queue which is a directory that stores data and controls files for mail messages.
- **Job Scheduling:** The computer has a task to execute a particular number of jobs that are scheduled to be executed one after another. These jobs are assigned to the processor one by one which is organized using a queue.
- **Shared resources:** Queues are used as waiting lists for a single shared resource.