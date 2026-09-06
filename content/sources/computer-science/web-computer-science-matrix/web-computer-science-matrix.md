---
archive_policy: text-only
attachments:
- filename: web-computer-science-matrix.html
  kind: document
  media_type: text/html
  role: original
  sha256: sha256:d7ab66f96f19eae59f8625af7b9ff91bcb1dd5b64d8bd785ba3f0e74cc1bc793
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-3e7ac52db165
  position:
    end: 418
    start: 0
    type: TextPositionSelector
  quote_sha256: sha256:e979635168a2b4e4efa6bce5f4dc59f630bba6b8aac34e340e443a1b7917e2af
  selector:
    exact: 'numpy.ndarray#

      - class numpy.ndarray(shape, dtype=np.float64, buffer=None, offset=0, strides=None,
      order=None)[source]#

      - An array object represents a multidimensional, homogeneous array of fixed-size
      items. An associated data-type object describes the format of each element in
      the array (its byte-order, how many bytes it occupies in memory, whether it
      is an integer, a floating point number, or something else, etc.'
    prefix: ''
    suffix: ) Arrays should be constructed u
    type: TextQuoteSelector
  selector_sha256: sha256:a014249b799d8d7134e5786f0f0bfb1d36cfc5a0dcb30ee27c220671162eb91e
  snapshot_sha256: sha256:52eeaf5c207d5bd55831cceec188a7b6c3d8854a48c0e754e8ac958a6068c15e
extractor: trafilatura/2.2.0
id: web-computer-science-matrix
media_type: text/html
origin: external
raw_ref:
  path: archive/raw/d7ab66f96f19eae59f8625af7b9ff91bcb1dd5b64d8bd785ba3f0e74cc1bc793.html
  sha256: sha256:d7ab66f96f19eae59f8625af7b9ff91bcb1dd5b64d8bd785ba3f0e74cc1bc793
read_status: retrieved
retrieval:
  acquisition: fetch
  resolved_url: https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html
  url: https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html
schema_version: source/v1
snapshot_sha256: sha256:52eeaf5c207d5bd55831cceec188a7b6c3d8854a48c0e754e8ac958a6068c15e
source_type: doc
vault_id: public
---
numpy.ndarray#
- class numpy.ndarray(shape, dtype=np.float64, buffer=None, offset=0, strides=None, order=None)[source]#
- An array object represents a multidimensional, homogeneous array of fixed-size items. An associated data-type object describes the format of each element in the array (its byte-order, how many bytes it occupies in memory, whether it is an integer, a floating point number, or something else, etc.) Arrays should be constructed using array ,zeros orempty (refer
to the See Also section below).  The parameters given here refer to
a low-level method (ndarray(…)) for instantiating an array.For more information, refer to the numpy module and examine the
methods and attributes of an array.
  - Parameters:
    - (for the __new__ method; see Notes below)
    - shapetuple of ints
    - Shape of created array.
    - dtypedata-type, optional
    - Any object that can be interpreted as a numpy data type. Default is numpy.float64 .
    - bufferobject exposing buffer interface, optional
    - Used to fill the array with data.
    - offsetint, optional
    - Offset of array data in buffer.
    - stridestuple of ints, optional
    - Strides of data in memory.
    - order{‘C’, ‘F’}, optional
    - Row-major (C-style) or column-major (Fortran-style) order.
  - Attributes:
    - T ndarray
    - View of the transposed array.
    - data buffer
    - Python buffer object pointing to the start of the array’s data.
    - dtype dtype object
    - Data-type of the array’s elements.
    - flags dict
    - Information about the memory layout of the array.
    - flat numpy.flatiter object
    - A 1-D iterator over the array.
    - imag ndarray
    - The imaginary part of the array.
    - real ndarray
    - The real part of the array.
    - size int
    - Number of elements in the array.
    - itemsize int
    - Length of one array element in bytes.
    - nbytes int
    - Total bytes consumed by the elements of the array.
    - ndim int
    - Number of array dimensions.
    - shape tuple of ints
    - Tuple of array dimensions.
    - strides tuple of ints
    - Tuple of bytes to step in each dimension when traversing an array.
    - ctypes ctypes object
    - An object to simplify the interaction of the array with the ctypes module.
    - base ndarray
    - Base object if memory is from some other object.
 Methods See also 
  - array
  - Construct an array.
  - zeros
  - Create an array, each element of which is zero.
  - empty
  - Create an array, but leave its allocated memory unchanged (i.e., it contains “garbage”).
  - dtype
  - Create a data-type.
  - numpy.typing.NDArray
  - An ndarray alias generic w.r.t. its dtype.type .
 Notes There are two modes of creating an array using __new__ :
  - If buffer is None, then only shape ,dtype , and order
are used.
  - If buffer is an object exposing the buffer interface, then all keywords are interpreted.
 No __init__ method is needed because the array is fully initialized
after the__new__ method.Examples These examples illustrate the low-level ndarray constructor.  Refer
to the See Also section above for easier ways of constructing an
ndarray.First mode, buffer is None: >>> import numpy as np >>> np.ndarray(shape=(2,2), dtype=np.float64, order='F') array([[0.0e+000, 0.0e+000], # random [ nan, 2.5e-323]]) Second mode: >>> np.ndarray((2,), buffer=np.array([1,2,3]), ... offset=np.int_().itemsize, ... dtype=np.int_) # offset = 1*itemsize, i.e. skip first element array([2, 3])