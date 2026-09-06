---
archive_policy: text-only
attachments:
- filename: wiki-linked-list.txt
  kind: document
  media_type: text/plain
  role: original
  sha256: sha256:43199aaeea1c5cf30104d7fdc33c9e672b28c33687d3c92dd9f3bb2b4db37b8c
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-fbc7b862da58
  position:
    end: 276
    start: 0
    type: TextPositionSelector
  quote_sha256: sha256:0985234b7ace1ae6cfc1e28b1cca3aa9b2987e5e6ad76ec666bfd247dc3d1e16
  selector:
    exact: In computer science, a linked list is a linear collection of data elements
      whose order is not given by their physical placement in memory. Instead, each
      element points to the next. It is a data structure consisting of a collection
      of nodes which together represent a sequence.
    prefix: ''
    suffix: '

      In its most basic form, each no'
    type: TextQuoteSelector
  selector_sha256: sha256:0f8144c8561a21955f75e0b90bcfe1628d9c8167bf1101df8ce5e4152b433633
  snapshot_sha256: sha256:43199aaeea1c5cf30104d7fdc33c9e672b28c33687d3c92dd9f3bb2b4db37b8c
- evidence_id: evidence-6f9055c4a223
  position:
    end: 521
    start: 277
    type: TextPositionSelector
  quote_sha256: sha256:7950ce9f1ed365b6083c00a2cde92398eff3e5d1e3095c0c38e11910221c1091
  selector:
    exact: In its most basic form, each node contains data, and a reference (in other
      words, a link) to the next node in the sequence. This structure allows for efficient
      insertion or removal of elements from any position in the sequence during iteration.
    prefix: ' together represent a sequence.

      '
    suffix: '

      A drawback of linked lists is t'
    type: TextQuoteSelector
  selector_sha256: sha256:67ba0a01a0e9b50e28a8656464dd56312d655419f11fbe75f69f772d2f16ef7c
  snapshot_sha256: sha256:43199aaeea1c5cf30104d7fdc33c9e672b28c33687d3c92dd9f3bb2b4db37b8c
- evidence_id: evidence-e1c0317667fd
  position:
    end: 632
    start: 522
    type: TextPositionSelector
  quote_sha256: sha256:555d98030056401f83b336ad4044655967d8c22576c62f58906f7f44d0184b76
  selector:
    exact: A drawback of linked lists is that data access time is linear with respect
      to the number of nodes in the list.
    prefix: ' the sequence during iteration.

      '
    suffix: ' Because nodes are serially link'
    type: TextQuoteSelector
  selector_sha256: sha256:e13af57ee0dd3217e7a8221f4655f0169f20500297e3ea50169d9bb5461efdc2
  snapshot_sha256: sha256:43199aaeea1c5cf30104d7fdc33c9e672b28c33687d3c92dd9f3bb2b4db37b8c
- evidence_id: evidence-debf304f8906
  position:
    end: 856
    start: 633
    type: TextPositionSelector
  quote_sha256: sha256:22730fc44f84589c8024a14dbad68bd51cd50eac601113ba6369d2cb93025be0
  selector:
    exact: Because nodes are serially linked, accessing any node requires that the
      prior node be accessed beforehand (which introduces difficulties in pipelining).
      Faster access, such as random access (direct access), is not possible.
    prefix: 'he number of nodes in the list. '
    suffix: '

      Arrays have better cache locali'
    type: TextQuoteSelector
  selector_sha256: sha256:90c21c08a5900790edefb75ff705f4b1d555616120af6ef151a038625634c516
  snapshot_sha256: sha256:43199aaeea1c5cf30104d7fdc33c9e672b28c33687d3c92dd9f3bb2b4db37b8c
- evidence_id: evidence-5f4608cd28e0
  position:
    end: 916
    start: 857
    type: TextPositionSelector
  quote_sha256: sha256:1f00e98ca67d075278f9b8b707549626ae477aecb4f2513779cf2c8029d88849
  selector:
    exact: Arrays have better cache locality compared to linked lists.
    prefix: 'irect access), is not possible.

      '
    suffix: '

      The principal benefit of a link'
    type: TextQuoteSelector
  selector_sha256: sha256:63b9e19c53d4ac2494c8593309c99600fc61535a8611a544e03a71251e040e42
  snapshot_sha256: sha256:43199aaeea1c5cf30104d7fdc33c9e672b28c33687d3c92dd9f3bb2b4db37b8c
- evidence_id: evidence-816e76e0295f
  position:
    end: 1264
    start: 917
    type: TextPositionSelector
  quote_sha256: sha256:5a3880538965c5cd027bd2d28221ac1505374e659130dfeb25b2c251defbfee4
  selector:
    exact: The principal benefit of a linked list over a conventional array is that
      the list elements can be easily inserted or removed without reallocation or
      reorganization of the entire structure because the data items do not need to
      be stored contiguously in memory or on disk, while restructuring an array at
      run-time is a much more expensive operation.
    prefix: 'ality compared to linked lists.

      '
    suffix: '

      In a doubly linked list, each n'
    type: TextQuoteSelector
  selector_sha256: sha256:1bfe49c34f2e1e1c9e5b8d75ea287f67b1be01a570aa0ee727aaad86c4ef8350
  snapshot_sha256: sha256:43199aaeea1c5cf30104d7fdc33c9e672b28c33687d3c92dd9f3bb2b4db37b8c
- evidence_id: evidence-b70e16480b71
  position:
    end: 1411
    start: 1265
    type: TextPositionSelector
  quote_sha256: sha256:ccf9d121da6b945cf06dacf348f889daca91f6999b8cb1d3d4e58c2c4c546d19
  selector:
    exact: In a doubly linked list, each node contains, besides the link to the next
      node, a second link field pointing to the previous node in the sequence.
    prefix: ' much more expensive operation.

      '
    suffix: ' The two links may be called for'
    type: TextQuoteSelector
  selector_sha256: sha256:6895b3c0e4070040cdfea025c2fe8bb2c4253357bf687a4a81f4bd87c06471d0
  snapshot_sha256: sha256:43199aaeea1c5cf30104d7fdc33c9e672b28c33687d3c92dd9f3bb2b4db37b8c
- evidence_id: evidence-662ca96b80b6
  position:
    end: 1835
    start: 1492
    type: TextPositionSelector
  quote_sha256: sha256:eaaae69a76568ff33d4210408b057e411084f11ad6c892d825e996fbb0d22c1c
  selector:
    exact: In a circularly linked list, all nodes are linked in a continuous circle,
      without using null. For lists with a front and a back (such as a queue), one
      stores a reference to the last node in the list. The next node after the last
      node is the first node. Elements can be added to the back of the list and removed
      from the front in constant time.
    prefix: 's, or next and prev (previous).

      '
    suffix: '

      Circularly linked lists can be '
    type: TextQuoteSelector
  selector_sha256: sha256:a83efaf72d3d5c297b768ccd96485ee90e4998df139383fb2df23cd6ab12dccb
  snapshot_sha256: sha256:43199aaeea1c5cf30104d7fdc33c9e672b28c33687d3c92dd9f3bb2b4db37b8c
- evidence_id: evidence-3ac0049e1914
  position:
    end: 1898
    start: 1836
    type: TextPositionSelector
  quote_sha256: sha256:2ce319d204a35164abf5eae14ea358f19fa9d211af6a323eca45728830ac6329
  selector:
    exact: Circularly linked lists can be either singly or doubly linked.
    prefix: 'rom the front in constant time.

      '
    suffix: '

      With a circular list, a pointer'
    type: TextQuoteSelector
  selector_sha256: sha256:5315be3b3ad387478ed26222f9be923db05bb192e3fd0e2acbecbb12591cce0d
  snapshot_sha256: sha256:43199aaeea1c5cf30104d7fdc33c9e672b28c33687d3c92dd9f3bb2b4db37b8c
- evidence_id: evidence-d0a6e5f269a8
  position:
    end: 2214
    start: 1899
    type: TextPositionSelector
  quote_sha256: sha256:e7d5bbf84837011fe4bb91159d49d53a39fb79891ccaead86ba8ff05f10edf1a
  selector:
    exact: With a circular list, a pointer to the last node gives easy access also
      to the first node, by following one link. Thus, in applications that require
      access to both ends of the list (e.g., in the implementation of a queue), a
      circular structure allows one to handle the structure by a single pointer, instead
      of two.
    prefix: 'either singly or doubly linked.

      '
    suffix: '

      A circularly linked list may be'
    type: TextQuoteSelector
  selector_sha256: sha256:9ce4975d427b922d9b66f4433c1da722b7104b2a920ee27ab1615115dd32a1e5
  snapshot_sha256: sha256:43199aaeea1c5cf30104d7fdc33c9e672b28c33687d3c92dd9f3bb2b4db37b8c
- evidence_id: evidence-2a0d730d509f
  position:
    end: 2496
    start: 2215
    type: TextPositionSelector
  quote_sha256: sha256:c2c397d17ea0b2814b4ed81eebfba9803e7b539677473d060969d0bb78a0b802
  selector:
    exact: A circularly linked list may be a natural option to represent arrays that
      are naturally circular, e.g. the corners of a polygon, a pool of buffers that
      are used and released in FIFO (first in, first out) order, or a set of processes
      that should be time-shared in round-robin order.
    prefix: 'single pointer, instead of two.

      '
    suffix: '

      Double-linked lists require mor'
    type: TextQuoteSelector
  selector_sha256: sha256:9c8ef987ab8f72bc19a13accf98476960d7dd5c9eceaa753cdb17c6cd1d573a8
  snapshot_sha256: sha256:43199aaeea1c5cf30104d7fdc33c9e672b28c33687d3c92dd9f3bb2b4db37b8c
- evidence_id: evidence-9ef0e141f101
  position:
    end: 2750
    start: 2497
    type: TextPositionSelector
  quote_sha256: sha256:852b22c41b713d4836bd93bfe4a4c465a71f1b1dc63d877557a94af68b805a4f
  selector:
    exact: Double-linked lists require more space per node (unless one uses XOR-linking),
      and their elementary operations are more expensive; but they are often easier
      to manipulate because they allow fast and easy sequential access to the list
      in both directions.
    prefix: 'me-shared in round-robin order.

      '
    suffix: '

      In a doubly linked list, one ca'
    type: TextQuoteSelector
  selector_sha256: sha256:a223cb9fab1aa27189a416d673554e7994e00b7f9c993551a415ef5e7ae33092
  snapshot_sha256: sha256:43199aaeea1c5cf30104d7fdc33c9e672b28c33687d3c92dd9f3bb2b4db37b8c
- evidence_id: evidence-8c7e9f4376d8
  position:
    end: 3083
    start: 2751
    type: TextPositionSelector
  quote_sha256: sha256:12f93124960424a3b929d123ddfeb3fb2e714bf8358bd7749523efb4aeca7d9e
  selector:
    exact: In a doubly linked list, one can insert or delete a node in a constant
      number of operations given only that node's address. To do the same in a singly
      linked list, one must have the address of the pointer to that node, which is
      either the handle for the whole list (in case of the first node) or the link
      field in the previous node.
    prefix: 'to the list in both directions.

      '
    suffix: '

      Some algorithms require access '
    type: TextQuoteSelector
  selector_sha256: sha256:2abf200acc2c173bc3237df889ed87d5322a5d7605ae374c54a34a9b5e0b3a62
  snapshot_sha256: sha256:43199aaeea1c5cf30104d7fdc33c9e672b28c33687d3c92dd9f3bb2b4db37b8c
- evidence_id: evidence-5d91e2bb22e8
  position:
    end: 3134
    start: 3084
    type: TextPositionSelector
  quote_sha256: sha256:613d912175776cd6997705746400392739be4c9750450a8e367d376ab1e3bfae
  selector:
    exact: Some algorithms require access in both directions.
    prefix: 'ink field in the previous node.

      '
    suffix: '

      '
    type: TextQuoteSelector
  selector_sha256: sha256:5bb4be3ed66efa2c5ad0e19bbf86d92aad329de8260b2217b7af0e923fc427cf
  snapshot_sha256: sha256:43199aaeea1c5cf30104d7fdc33c9e672b28c33687d3c92dd9f3bb2b4db37b8c
extractor: utf8/1
id: wiki-linked-list
local:
  file_sha256: sha256:43199aaeea1c5cf30104d7fdc33c9e672b28c33687d3c92dd9f3bb2b4db37b8c
  path_ref: local-sidecar:public/wiki-linked-list
media_type: text/plain
origin: external
raw_ref:
  path: archive/raw/43199aaeea1c5cf30104d7fdc33c9e672b28c33687d3c92dd9f3bb2b4db37b8c.txt
  sha256: sha256:43199aaeea1c5cf30104d7fdc33c9e672b28c33687d3c92dd9f3bb2b4db37b8c
read_status: retrieved
retrieval:
  acquisition: local-file
schema_version: source/v1
snapshot_sha256: sha256:43199aaeea1c5cf30104d7fdc33c9e672b28c33687d3c92dd9f3bb2b4db37b8c
source_type: local-file
vault_id: public
---
In computer science, a linked list is a linear collection of data elements whose order is not given by their physical placement in memory. Instead, each element points to the next. It is a data structure consisting of a collection of nodes which together represent a sequence.
In its most basic form, each node contains data, and a reference (in other words, a link) to the next node in the sequence. This structure allows for efficient insertion or removal of elements from any position in the sequence during iteration.
A drawback of linked lists is that data access time is linear with respect to the number of nodes in the list. Because nodes are serially linked, accessing any node requires that the prior node be accessed beforehand (which introduces difficulties in pipelining). Faster access, such as random access (direct access), is not possible.
Arrays have better cache locality compared to linked lists.
The principal benefit of a linked list over a conventional array is that the list elements can be easily inserted or removed without reallocation or reorganization of the entire structure because the data items do not need to be stored contiguously in memory or on disk, while restructuring an array at run-time is a much more expensive operation.
In a doubly linked list, each node contains, besides the link to the next node, a second link field pointing to the previous node in the sequence. The two links may be called forward and backwards, or next and prev (previous).
In a circularly linked list, all nodes are linked in a continuous circle, without using null. For lists with a front and a back (such as a queue), one stores a reference to the last node in the list. The next node after the last node is the first node. Elements can be added to the back of the list and removed from the front in constant time.
Circularly linked lists can be either singly or doubly linked.
With a circular list, a pointer to the last node gives easy access also to the first node, by following one link. Thus, in applications that require access to both ends of the list (e.g., in the implementation of a queue), a circular structure allows one to handle the structure by a single pointer, instead of two.
A circularly linked list may be a natural option to represent arrays that are naturally circular, e.g. the corners of a polygon, a pool of buffers that are used and released in FIFO (first in, first out) order, or a set of processes that should be time-shared in round-robin order.
Double-linked lists require more space per node (unless one uses XOR-linking), and their elementary operations are more expensive; but they are often easier to manipulate because they allow fast and easy sequential access to the list in both directions.
In a doubly linked list, one can insert or delete a node in a constant number of operations given only that node's address. To do the same in a singly linked list, one must have the address of the pointer to that node, which is either the handle for the whole list (in case of the first node) or the link field in the previous node.
Some algorithms require access in both directions.
