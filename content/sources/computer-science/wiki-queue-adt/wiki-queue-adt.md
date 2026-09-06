---
archive_policy: text-only
attachments:
- filename: wiki-queue-adt.txt
  kind: document
  media_type: text/plain
  role: original
  sha256: sha256:59e1aece957ba5df3292e05265c2b20977be1ab8ca87c0d03b0122fd85d2abd7
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-321ef16388c5
  position:
    end: 103
    start: 0
    type: TextPositionSelector
  quote_sha256: sha256:4aef33ce74dddde869424a38af7bcfa485a731a4c4a8077638d7fcf4fb3ca4fd
  selector:
    exact: In computer science, a queue is an abstract data type that serves as an
      ordered collection of entities.
    prefix: ''
    suffix: ' By convention, the end of the q'
    type: TextQuoteSelector
  selector_sha256: sha256:8ad9da45fb704dfaf8830bde3ef4f397e8253b6f51d9ed6132d87ab773ce7627
  snapshot_sha256: sha256:59e1aece957ba5df3292e05265c2b20977be1ab8ca87c0d03b0122fd85d2abd7
- evidence_id: evidence-0b3f314368e0
  position:
    end: 302
    start: 104
    type: TextPositionSelector
  quote_sha256: sha256:bbbbd16e61f8ad119320365e3ade90b811805ebbf0675e89285b1f8877333f2c
  selector:
    exact: By convention, the end of the queue where elements are added is called
      the back, tail, or rear of the queue. The end of the queue where elements are
      removed is called the head or front of the queue.
    prefix: 'ordered collection of entities. '
    suffix: ' The name queue is an analogy to'
    type: TextQuoteSelector
  selector_sha256: sha256:b38a940fb84dec92e73a25b63d5b474e60b2206ac7aee5a822c41779cebd8741
  snapshot_sha256: sha256:59e1aece957ba5df3292e05265c2b20977be1ab8ca87c0d03b0122fd85d2abd7
- evidence_id: evidence-5fbba192da65
  position:
    end: 497
    start: 441
    type: TextPositionSelector
  quote_sha256: sha256:16c8f808981cffed38f339664b7f455c7d0c552aa1d11ddfc0d309ee14b288ac
  selector:
    exact: Enqueue, which adds one element to the rear of the queue
    prefix: 't supports two main operations.

      '
    suffix: '

      Dequeue, which removes one elem'
    type: TextQuoteSelector
  selector_sha256: sha256:f169ac9a729dd9eebd914407459e810b3d5d0a19eb4c0d449cedf163f982f27d
  snapshot_sha256: sha256:59e1aece957ba5df3292e05265c2b20977be1ab8ca87c0d03b0122fd85d2abd7
- evidence_id: evidence-63df362c3908
  position:
    end: 561
    start: 498
    type: TextPositionSelector
  quote_sha256: sha256:24238c808a084346ce1f4465b73b65a04d26c89741629c86311245b793a4080a
  selector:
    exact: Dequeue, which removes one element from the front of the queue.
    prefix: 'lement to the rear of the queue

      '
    suffix: '

      Other operations may also be al'
    type: TextQuoteSelector
  selector_sha256: sha256:ac5d81577da448d359459346eb5edb7ba94c409e5014de730ff202625701e13e
  snapshot_sha256: sha256:59e1aece957ba5df3292e05265c2b20977be1ab8ca87c0d03b0122fd85d2abd7
- evidence_id: evidence-8bb17fb652f7
  position:
    end: 721
    start: 562
    type: TextPositionSelector
  quote_sha256: sha256:967342c745cc104db471699704ffb71c075c7c37db8379f0bd83c1a8b6befcbb
  selector:
    exact: Other operations may also be allowed, often including a peek or front operation
      that returns the value of the next element to be dequeued without dequeuing
      it.
    prefix: 'nt from the front of the queue.

      '
    suffix: '

      The operations of a queue make '
    type: TextQuoteSelector
  selector_sha256: sha256:87f4fef4e04277dc323ad81e6e56ea8be52e0b52b26dee12c8f3eeceb01d2b49
  snapshot_sha256: sha256:59e1aece957ba5df3292e05265c2b20977be1ab8ca87c0d03b0122fd85d2abd7
- evidence_id: evidence-a8fcff8045f3
  position:
    end: 864
    start: 722
    type: TextPositionSelector
  quote_sha256: sha256:c04835b97af4606d52d652dafb3e2092f19957bcdfa64cf8b26a0fa16f98bdf1
  selector:
    exact: The operations of a queue make it a first-in-first-out (FIFO) data structure
      as the first element added to the queue is the first one removed.
    prefix: ' dequeued without dequeuing it.

      '
    suffix: ' This is equivalent to the requi'
    type: TextQuoteSelector
  selector_sha256: sha256:edb63c55fbcc408635f4a12ac74336649f1737102e1a617df9feb6cd6125e170
  snapshot_sha256: sha256:59e1aece957ba5df3292e05265c2b20977be1ab8ca87c0d03b0122fd85d2abd7
- evidence_id: evidence-2ae223870aea
  position:
    end: 1124
    start: 1031
    type: TextPositionSelector
  quote_sha256: sha256:eae5bb9821bd9a633d25d4f576938774b54c75af33567c75a3e161559c16b3ea
  selector:
    exact: A queue is an example of a linear data structure, or more abstractly a
      sequential collection.
    prefix: 'the new element can be removed. '
    suffix: '

      Queues are common in computer p'
    type: TextQuoteSelector
  selector_sha256: sha256:f4cba435da62baca98c7e7cbc9c0f434dd478ce1428343474ea6c2cc6c13bb39
  snapshot_sha256: sha256:59e1aece957ba5df3292e05265c2b20977be1ab8ca87c0d03b0122fd85d2abd7
- evidence_id: evidence-2bcf59757f6a
  position:
    end: 1436
    start: 1315
    type: TextPositionSelector
  quote_sha256: sha256:c27c9531de3b544639e3f52c5fe06f9523633efbc9f73cb7027a5389be3ccd16
  selector:
    exact: A queue may be implemented as circular buffers and linked lists, or by
      using both the stack pointer and the base pointer.
    prefix: '-oriented languages as classes. '
    suffix: '

      Time complexity in big O notati'
    type: TextQuoteSelector
  selector_sha256: sha256:44730e07b299ecfa1f08ccf7c93816792e2209e7e73aca0ba540e622d7e87b6d
  snapshot_sha256: sha256:59e1aece957ba5df3292e05265c2b20977be1ab8ca87c0d03b0122fd85d2abd7
- evidence_id: evidence-4db305b3ca1c
  position:
    end: 1681
    start: 1619
    type: TextPositionSelector
  quote_sha256: sha256:9367d1c9a287c2f730fdaff53656172fb24562629eddc23f494b927f78c70ade
  selector:
    exact: A bounded queue is a queue limited to a fixed number of items.
    prefix: 't case. Space complexity: O(n).

      '
    suffix: '

      There are several efficient imp'
    type: TextQuoteSelector
  selector_sha256: sha256:f363ea68ca9523dba2fdb69226666e5a320ef5288cdf2fd4b42da955d52dff48
  snapshot_sha256: sha256:59e1aece957ba5df3292e05265c2b20977be1ab8ca87c0d03b0122fd85d2abd7
- evidence_id: evidence-55c74d7a1fd6
  position:
    end: 1848
    start: 1682
    type: TextPositionSelector
  quote_sha256: sha256:7e50b91d323b3cb94c3cb6908b72e6d863cd116bfac47b268c4741c0b97de448
  selector:
    exact: There are several efficient implementations of FIFO queues. An efficient
      implementation is one that can perform the operations—en-queuing and de-queuing—in
      O(1) time.
    prefix: 'ted to a fixed number of items.

      '
    suffix: '

      A doubly linked list has O(1) i'
    type: TextQuoteSelector
  selector_sha256: sha256:c57a6caef3662fd09eba3b08681275bd2841f9362de32b8302acd2f3a9b9ccff
  snapshot_sha256: sha256:59e1aece957ba5df3292e05265c2b20977be1ab8ca87c0d03b0122fd85d2abd7
- evidence_id: evidence-01e0dc35da5b
  position:
    end: 1953
    start: 1849
    type: TextPositionSelector
  quote_sha256: sha256:56989b37b3d453224596914829ae4f915481757dcbce6500066d0637b772a5a2
  selector:
    exact: A doubly linked list has O(1) insertion and deletion at both ends, so it
      is a natural choice for queues.
    prefix: 'ng and de-queuing—in O(1) time.

      '
    suffix: '

      A regular singly linked list on'
    type: TextQuoteSelector
  selector_sha256: sha256:ebfa968cb442b2b2cd3eb63d5ac45a50efeab1a09bbad618a000b6542754ad91
  snapshot_sha256: sha256:59e1aece957ba5df3292e05265c2b20977be1ab8ca87c0d03b0122fd85d2abd7
- evidence_id: evidence-98db9ed161b0
  position:
    end: 2178
    start: 1954
    type: TextPositionSelector
  quote_sha256: sha256:b6d4e21f18f8d36254fdce4ea617294d9daedbf4b8d627f9642990b5b8f1c2b0
  selector:
    exact: A regular singly linked list only has efficient insertion and deletion
      at one end. However, a small modification—keeping a pointer to the last node
      in addition to the first one—will enable it to implement an efficient queue.
    prefix: 'is a natural choice for queues.

      '
    suffix: '

      A deque implemented using a mod'
    type: TextQuoteSelector
  selector_sha256: sha256:52cdd4e64f437d53f44a681ed26c708442c4c2d3567af74389eb41f208096b00
  snapshot_sha256: sha256:59e1aece957ba5df3292e05265c2b20977be1ab8ca87c0d03b0122fd85d2abd7
- evidence_id: evidence-a6281e47fc6b
  position:
    end: 2229
    start: 2179
    type: TextPositionSelector
  quote_sha256: sha256:22d0a44812c50943735866afe0ebc86cf2a47a2b8eb1df474fdd224642e7314c
  selector:
    exact: A deque implemented using a modified dynamic array
    prefix: 'o implement an efficient queue.

      '
    suffix: '

      '
    type: TextQuoteSelector
  selector_sha256: sha256:3cb003a8e0784c2aab1e5795d26852546f77ef813ce77b7ff47946e41f73bba5
  snapshot_sha256: sha256:59e1aece957ba5df3292e05265c2b20977be1ab8ca87c0d03b0122fd85d2abd7
- evidence_id: evidence-8d8f51a56142
  position:
    end: 1030
    start: 865
    type: TextPositionSelector
  quote_sha256: sha256:72cc665fc5e28a7885bf3ce0b0a5380ee81f875f0c41628a392411eb3b265486
  selector:
    exact: This is equivalent to the requirement that once a new element is added,
      all elements that were added before have to be removed before the new element
      can be removed.
    prefix: 'queue is the first one removed. '
    suffix: ' A queue is an example of a line'
    type: TextQuoteSelector
  selector_sha256: sha256:cb48f5a21b1a5b9500eb0f661667a0465937c95ff7ddf97546ba744f9fa5ba33
  snapshot_sha256: sha256:59e1aece957ba5df3292e05265c2b20977be1ab8ca87c0d03b0122fd85d2abd7
- evidence_id: evidence-3612bdfaecca
  position:
    end: 864
    start: 748
    type: TextPositionSelector
  quote_sha256: sha256:2da52dcbeda3a3ee1a553a974f389efe1960543986d43f483dcdf8fee6684d35
  selector:
    exact: make it a first-in-first-out (FIFO) data structure as the first element
      added to the queue is the first one removed.
    prefix: 'g it.

      The operations of a queue '
    suffix: ' This is equivalent to the requi'
    type: TextQuoteSelector
  selector_sha256: sha256:98f42b4e9e2b1ecfa3d4e545fa2ae947189b02725c8a2665ffc3876f8ea6089d
  snapshot_sha256: sha256:59e1aece957ba5df3292e05265c2b20977be1ab8ca87c0d03b0122fd85d2abd7
extractor: utf8/1
id: wiki-queue-adt
local:
  file_sha256: sha256:59e1aece957ba5df3292e05265c2b20977be1ab8ca87c0d03b0122fd85d2abd7
  path_ref: local-sidecar:public/wiki-queue-adt
media_type: text/plain
origin: external
raw_ref:
  path: archive/raw/59e1aece957ba5df3292e05265c2b20977be1ab8ca87c0d03b0122fd85d2abd7.txt
  sha256: sha256:59e1aece957ba5df3292e05265c2b20977be1ab8ca87c0d03b0122fd85d2abd7
read_status: retrieved
retrieval:
  acquisition: local-file
schema_version: source/v1
snapshot_sha256: sha256:59e1aece957ba5df3292e05265c2b20977be1ab8ca87c0d03b0122fd85d2abd7
source_type: local-file
vault_id: public
---
In computer science, a queue is an abstract data type that serves as an ordered collection of entities. By convention, the end of the queue where elements are added is called the back, tail, or rear of the queue. The end of the queue where elements are removed is called the head or front of the queue. The name queue is an analogy to the words used to describe people in line to wait for goods or services. It supports two main operations.
Enqueue, which adds one element to the rear of the queue
Dequeue, which removes one element from the front of the queue.
Other operations may also be allowed, often including a peek or front operation that returns the value of the next element to be dequeued without dequeuing it.
The operations of a queue make it a first-in-first-out (FIFO) data structure as the first element added to the queue is the first one removed. This is equivalent to the requirement that once a new element is added, all elements that were added before have to be removed before the new element can be removed. A queue is an example of a linear data structure, or more abstractly a sequential collection.
Queues are common in computer programs, where they are implemented as data structures coupled with access routines, as an abstract data structure or in object-oriented languages as classes. A queue may be implemented as circular buffers and linked lists, or by using both the stack pointer and the base pointer.
Time complexity in big O notation: Search O(n) average and O(n) worst case; Insert O(1) average and O(1) worst case; Delete O(1) average and O(1) worst case. Space complexity: O(n).
A bounded queue is a queue limited to a fixed number of items.
There are several efficient implementations of FIFO queues. An efficient implementation is one that can perform the operations—en-queuing and de-queuing—in O(1) time.
A doubly linked list has O(1) insertion and deletion at both ends, so it is a natural choice for queues.
A regular singly linked list only has efficient insertion and deletion at one end. However, a small modification—keeping a pointer to the last node in addition to the first one—will enable it to implement an efficient queue.
A deque implemented using a modified dynamic array
