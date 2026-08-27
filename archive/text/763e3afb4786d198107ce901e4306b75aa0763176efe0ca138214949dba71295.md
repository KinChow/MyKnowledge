# 数组

## 概念

An array is a collection of items of same data type stored at contiguous memory locations. 



## 基本术语

* 索引
* 元素
* 长度

- ***\*Array Index:\**** In an array, elements are identified by their indexes. Array index starts from 0.
- ***\*Array element:\**** Elements are items stored in an array and can be accessed by their index.
- ***\*Array Length:\**** The length of an array is determined by the number of elements it can contain. 



## 操作

* 遍历
* 插入
* 删除
* 搜索
* 排序
* 反转
* 数组左旋转 d 个位置
* 使用递归生成子数组



- Traversal: Traverse through the elements of an array.
- Insertion: Inserting a new element in an array.
- Deletion: Deleting element from the array.
- Searching:  Search for an element in the array.
- Sorting: Maintaining the order of elements in the array.



## 优劣

### 好处

- Arrays allow random access to elements. This makes accessing elements by position faster.
- Arrays have better cache locality which makes a pretty big difference in performance.
- Arrays represent multiple data items of the same type using a single name.
- Arrays store multiple data of similar types with the same name.
- Array data structures are used to implement the other data structures like linked lists, stacks, queues, trees, graphs, etc.



- **Efficient access to elements:** Arrays provide direct and efficient access to any element in the collection. Accessing an element in an array is an O(1) operation, meaning that the time required to access an element is constant and does not depend on the size of the array.
- **Fast data retrieval:** Arrays allow for fast data retrieval because the data is stored in contiguous memory locations. This means that the data can be accessed quickly and efficiently without the need for complex data structures or algorithms.
- **Memory efficiency:** Arrays are a memory-efficient way of storing data. Because the elements of an array are stored in contiguous memory locations, the size of the array is known at compile time. This means that memory can be allocated for the entire array in one block, reducing memory fragmentation.
- **Versatility:** Arrays can be used to store a wide range of data types, including integers, floating-point numbers, characters, and even complex data structures such as objects and pointers.
- **Easy to implement:** Arrays are easy to implement and understand, making them an ideal choice for beginners learning computer programming.
- **Compatibility with hardware:** The array data structure is compatible with most hardware architectures, making it a versatile tool for programming in a wide range of environments.



### 坏处

- As arrays have a fixed size, once the memory is allocated to them, it cannot be increased or decreased, making it impossible to store extra data if required. An array of fixed size is referred to as a static array. 
- Allocating less memory than required to an array leads to loss of data.
  An array is homogeneous in nature so, a single array cannot store values of different data types. 
- Arrays store data in contiguous memory locations, which makes deletion and insertion very difficult to implement. This problem is overcome by implementing linked lists, which allow elements to be accessed sequentially.  



- **Fixed size:** Arrays have a fixed size that is determined at the time of creation. This means that if the size of the array needs to be increased, a new array must be created and the data must be copied from the old array to the new array, which can be time-consuming and memory-intensive.
- **Memory allocation issues:** Allocating a large array can be problematic, particularly in systems with limited memory. If the size of the array is too large, the system may run out of memory, which can cause the program to crash.
- **Insertion and deletion issues**: Inserting or deleting an element from an array can be inefficient and time-consuming because all the elements after the insertion or deletion point must be shifted to accommodate the change.
- **Wasted space:** If an array is not fully populated, there can be wasted space in the memory allocated for the array. This can be a concern if memory is limited.
- **Limited data type support:** Arrays have limited support for complex data types such as objects and structures, as the elements of an array must all be of the same data type.
- **Lack of flexibility:** The fixed size and limited support for complex data types can make arrays inflexible compared to other data structures such as linked lists and trees.



### 结构体 vs 数组

- The structure can store different types of data whereas an array can only store similar data types.
- Structure does not have limited size like an array.
- Structure elements may or may not be stored in contiguous locations but array elements are stored in contiguous locations.
- In structures, object instantiation is possible whereas in arrays objects are not possible.



## 应用

- They are used in the implementation of other data structures such as array lists, heaps, hash tables, vectors, and matrices.
- Database records are usually implemented as arrays.
- It is used in lookup tables by computer.
- It is used for different sorting algorithms such as bubble sort insertion sort, merge sort, and quick sort.



- **Storing and accessing data**: Arrays are used to store and retrieve data in a specific order. For example, an array can be used to store the scores of a group of students, or the temperatures recorded by a weather station.
- **Sorting:** Arrays can be used to sort data in ascending or descending order. Sorting algorithms such as bubble sort, merge sort, and quicksort rely heavily on arrays.
- **Searching**: Arrays can be searched for specific elements using algorithms such as linear search and binary search.
- **Matrices**: Arrays are used to represent matrices in mathematical computations such as matrix multiplication, linear algebra, and image processing.
- **Stacks and queues:** Arrays are used as the underlying data structure for implementing stacks and queues, which are commonly used in algorithms and data structures.
- **Graphs**: Arrays can be used to represent graphs in computer science. Each element in the array represents a node in the graph, and the relationships between the nodes are represented by the values stored in the array.
- **Dynamic programming**: Dynamic programming algorithms often use arrays to store intermediate results of subproblems in order to solve a larger problem.



**C/C++:**

- Arrays are used to implement vectors, and lists in C++ STL.
- Arrays are used as the base of all sorting algorithms.
- Arrays are used to implement other DS like a stack, queue, etc.
- Used for implementing matrices. 
- Data structures like trees also sometimes use the array implementation since arrays are easier to handle than pointers. For example, a segment tree uses array implementation.
- Binary search trees and balanced binary trees are used in data structures such as a heap, map, and set, which can be built using arrays.
- Graphs are also implemented as arrays in the form of an adjacency matrix.