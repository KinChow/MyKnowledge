---
archive_policy: text-only
attachments:
- filename: web-computer-science-queue.html
  kind: document
  media_type: text/html
  role: original
  sha256: sha256:2ede4dc52ae3d89c237eaf0ad74f532e157aa2db0c64422a8af9d2f18899c2db
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-53caeacfb415
  position:
    end: 196
    start: 0
    type: TextPositionSelector
  quote_sha256: sha256:77893bead1a3c620ea50bb284e7d3130a6d2a50f1518aea63b1a9804fb9e125a
  selector:
    exact: 'FIFO is an abbreviation for first in, first out. It is a method for handling
      data structures where the first element is processed first and the newest element
      is processed last.

      Real-life example:'
    prefix: ''
    suffix: '

       

      In this example, following th'
    type: TextQuoteSelector
  selector_sha256: sha256:d302b3c8a4d5162dcc0f801b2c62235ced317298801dd8e65f6d740ff396cd9b
  snapshot_sha256: sha256:94fd1cbaeabf32db07a479884495c724dc7832e5913b3b701ed68ba94aac7477
- evidence_id: evidence-8ff2ed221c43
  position:
    end: 177
    start: 0
    type: TextPositionSelector
  quote_sha256: sha256:8743d4ddda183683be0dcdd52cabca2c13c5a4c9487de3f3da0fe139259c3f1b
  selector:
    exact: FIFO is an abbreviation for first in, first out. It is a method for handling
      data structures where the first element is processed first and the newest element
      is processed last.
    prefix: ''
    suffix: '

      Real-life example:

       

      In this ex'
    type: TextQuoteSelector
  selector_sha256: sha256:e4263a6e70aab4005df07812114ad85cc6cf6c00349ad1916e3dc7bd58374e71
  snapshot_sha256: sha256:94fd1cbaeabf32db07a479884495c724dc7832e5913b3b701ed68ba94aac7477
- evidence_id: evidence-9dee8b7f3fce
  position:
    end: 985
    start: 883
    type: TextPositionSelector
  quote_sha256: sha256:8e77fd6a420df8aebb5c60bf4d63c1b52a9fd16a952ec573029a760bc3967f17
  selector:
    exact: Certain data structures like Queue and other variants of Queue uses FIFO
      approach for processing data.
    prefix: "FO used:\n- Data Structures:\n  - "
    suffix: "\n- Disk scheduling:\n  - Disk con"
    type: TextQuoteSelector
  selector_sha256: sha256:2e718a9ca6681d347ed96070862d953d296cf390d386dc2a415030d43dca7864
  snapshot_sha256: sha256:94fd1cbaeabf32db07a479884495c724dc7832e5913b3b701ed68ba94aac7477
- evidence_id: evidence-5a69eff1293e
  position:
    end: 1135
    start: 1009
    type: TextPositionSelector
  quote_sha256: sha256:fe4f6d8c6a127082a4b0f1a034a6b083435aeb6908633fe40b963d72d546f44e
  selector:
    exact: Disk controllers can use the FIFO as a disk scheduling algorithm to determine
      the order in which to service disk I/O requests.
    prefix: "ng data.\n- Disk scheduling:\n  - "
    suffix: '

      - Communications and networking'
    type: TextQuoteSelector
  selector_sha256: sha256:989c3402ec061303ce13cca813a43cd334da5dc5cea527caf76d3963838b68ae
  snapshot_sha256: sha256:94fd1cbaeabf32db07a479884495c724dc7832e5913b3b701ed68ba94aac7477
- evidence_id: evidence-e63039c54202
  position:
    end: 1317
    start: 1173
    type: TextPositionSelector
  quote_sha256: sha256:5d03445fb5683cd64c1c317330cf1750a2f24676f9785a3474d315b548cba83a
  selector:
    exact: Communication network bridges, switches and routers used in computer networks
      use FIFOs to hold data packets en route to their next destination.
    prefix: "munications and networking\"\n  - "
    suffix: '

      Program Examples for FIFO

      Progr'
    type: TextQuoteSelector
  selector_sha256: sha256:5226eb9ce242ad9708ed695374f230f2180e45daf844985d4718dda8816cd68f
  snapshot_sha256: sha256:94fd1cbaeabf32db07a479884495c724dc7832e5913b3b701ed68ba94aac7477
extractor: trafilatura/2.2.0
id: web-computer-science-queue
media_type: text/html
origin: external
raw_ref:
  path: archive/raw/2ede4dc52ae3d89c237eaf0ad74f532e157aa2db0c64422a8af9d2f18899c2db.html
  sha256: sha256:2ede4dc52ae3d89c237eaf0ad74f532e157aa2db0c64422a8af9d2f18899c2db
read_status: retrieved
retrieval:
  acquisition: fetch
  resolved_url: https://www.geeksforgeeks.org/dsa/fifo-first-in-first-out-approach-in-programming/
  url: https://www.geeksforgeeks.org/fifo-first-in-first-out-approach-in-programming/
schema_version: source/v1
snapshot_sha256: sha256:94fd1cbaeabf32db07a479884495c724dc7832e5913b3b701ed68ba94aac7477
source_type: doc
vault_id: public
---
FIFO is an abbreviation for first in, first out. It is a method for handling data structures where the first element is processed first and the newest element is processed last.
Real-life example:
 
In this example, following things are to be considered:
- There is a ticket counter where people come, take tickets and go.
- People enter a line (queue) to get to the Ticket Counter in an organized manner.
- The person to enter the queue first, will get the ticket first and leave the queue.
- The person entering the queue next will get the ticket after the person in front of him
- In this way, the person entering the queue last will the tickets last
- Therefore, the First person to enter the queue gets the ticket first and the Last person to enter the queue gets the ticket last.
This is known as First-In-First-Out approach or FIFO.
Where is FIFO used:
- Data Structures:
  - Certain data structures like Queue and other variants of Queue uses FIFO approach for processing data.
- Disk scheduling:
  - Disk controllers can use the FIFO as a disk scheduling algorithm to determine the order in which to service disk I/O requests.
- Communications and networking"
  - Communication network bridges, switches and routers used in computer networks use FIFOs to hold data packets en route to their next destination.
Program Examples for FIFO
Program 1: Queue
// C++ program to demonstrate 
// working of FIFO 
// using Queue interface in C++
#include<bits/stdc++.h>
using namespace std;
// print the elements of queue
void print_queue(queue<int> q)
{
    while (!q.empty())
    {
        cout << q.front() << " ";
        q.pop();
    }
    cout << endl;
}
// Driver code
int main() 
{ 
    queue<int> q ;
    // Adds elements {0, 1, 2, 3, 4} to queue 
    for (int i = 0; i < 5; i++) 
        q.push(i); 
    // Display contents of the queue. 
    cout << "Elements of queue-";
        
    print_queue(q);
    // To remove the head of queue. 
    // In this the oldest element '0' will be removed 
    int removedele = q.front();
    q.pop();
    cout << "removed element-" << removedele << endl; 
    print_queue(q);
    // To view the head of queue 
    int head = q.front(); 
    cout << "head of queue-" << head << endl; 
    // Rest all methods of collection interface, 
    // Like size and contains can be used with this 
    // implementation. 
    int size = q.size(); 
    cout << "Size of queue-" << size;
        
    return 0;
} 
// This code is contributed by Arnab Kundu
// Java program to demonstrate
// working of FIFO
// using Queue interface in Java
import java.util.LinkedList;
import java.util.Queue;
public class QueueExample {
    public static void main(String[] args)
    {
        Queue<Integer> q = new LinkedList<>();
        // Adds elements {0, 1, 2, 3, 4} to queue
        for (int i = 0; i < 5; i++)
            q.add(i);
        // Display contents of the queue.
        System.out.println("Elements of queue-" + q);
        // To remove the head of queue.
        // In this the oldest element '0' will be removed
        int removedele = q.remove();
        System.out.println("removed element-" + removedele);
        System.out.println(q);
        // To view the head of queue
        int head = q.peek();
        System.out.println("head of queue-" + head);
        // Rest all methods of collection interface,
        // Like size and contains can be used with this
        // implementation.
        int size = q.size();
        System.out.println("Size of queue-" + size);
    }
}
# Python program to demonstrate
# working of FIFO
# using Queue interface in Python
q = []
# Adds elements {0, 1, 2, 3, 4} to queue
for i in range(5):
    q.append(i)
# Display contents of the queue.
print("Elements of queue-" , q)
# To remove the head of queue.
# In this the oldest element '0' will be removed
removedele = q.pop(0)
print("removed element-" , removedele)
print(q)
# To view the head of queue
head = q[0]
print("head of queue-" , head)
# Rest all methods of collection interface,
# Like size and contains can be used with this
# implementation.
size = len(q)
print("Size of queue-" , size)
# This code is contributed by patel2127.
// C# program to demonstrate 
// working of FIFO 
using System;
using System.Collections.Generic;
public class QueueExample 
{ 
    public static void Main(String[] args) 
    { 
        Queue<int> q = new Queue<int>(); 
        // Adds elements {0, 1, 2, 3, 4} to queue 
        for (int i = 0; i < 5; i++) 
            q.Enqueue(i); 
        // Display contents of the queue. 
        Console.Write("Elements of queue-"); 
        foreach(int s in q) 
                Console.Write(s + " "); 
        // To remove the head of queue. 
        // In this the oldest element '0' will be removed 
        int removedele = q.Dequeue(); 
        Console.Write("\nremoved element-" + removedele + "\n"); 
        foreach(int s in q) 
                Console.Write(s + " "); 
        // To view the head of queue 
        int head = q.Peek(); 
        Console.Write("\nhead of queue-" + head); 
        // Rest all methods of collection interface, 
        // Like size and contains can be used with this 
        // implementation. 
        int size = q.Count; 
        Console.WriteLine("\nSize of queue-" + size); 
    } 
} 
// This code has been contributed by 29AjayKumar
<script>
// JavaScript program to demonstrate
// working of FIFO
// using Queue interface in Java
let q = [];
// Adds elements {0, 1, 2, 3, 4} to queue
for (let i = 0; i < 5; i++)
    q.push(i);
// Display contents of the queue.
document.write("Elements of queue-[" + q.join(", ")+"]<br>");
// To remove the head of queue.
// In this the oldest element '0' will be removed
let removedele = q.shift();
document.write("removed element-" + removedele+"<br>");
document.write("["+q.join(", ")+"]<br>");
// To view the head of queue
let head = q[0];
document.write("head of queue-" + head+"<br>");
// Rest all methods of collection interface,
// Like size and contains can be used with this
// implementation.
let size = q.length;
document.write("Size of queue-" + size+"<br>");
// This code is contributed by avanitrachhadiya2155
</script>
Output
Elements of queue-0 1 2 3 4 
removed element-0
1 2 3 4 
head of queue-1
Size of queue-4
Complexities Analysis:
- Time Complexity: O(N)
- Space Complexity: O(N)