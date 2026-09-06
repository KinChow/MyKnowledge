---
archive_policy: text-only
attachments:
- filename: nvidia-cuda-programming-guide-v2.html
  kind: document
  media_type: text/html
  role: original
  sha256: sha256:cf96d69dc20a22e77e9d6508f269a489fee20732635a1e41fc3bb892c3499a8f
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-b98c8e4a7b27
  position:
    end: 232
    start: 60
    type: TextPositionSelector
  quote_sha256: sha256:49efd235593e631503279aa798864883e28a6d20e8faff72775c25b51a2463b0
  selector:
    exact: CUDA is a parallel computing platform and programming model developed by
      NVIDIA that enables dramatic increases in computing performance by harnessing
      the power of the GPU.
    prefix: ' and the CUDA Programming Guide

      '
    suffix: ' It allows developers to acceler'
    type: TextQuoteSelector
  selector_sha256: sha256:2191ee7342a26c0e62e12391d42cafb27e1c772128d0c05c4236af20a9fbb8c5
  snapshot_sha256: sha256:19240c8229bdc716b8f594b5c2f02db066ff0612874556ef1e62da0fb14fd023
extractor: trafilatura/2.2.0
id: nvidia-cuda-programming-guide-v2
local:
  file_sha256: sha256:cf96d69dc20a22e77e9d6508f269a489fee20732635a1e41fc3bb892c3499a8f
  path_ref: local-sidecar:public/nvidia-cuda-programming-guide-v2
media_type: text/html
origin: external
raw_ref:
  path: archive/raw/cf96d69dc20a22e77e9d6508f269a489fee20732635a1e41fc3bb892c3499a8f.html
  sha256: sha256:cf96d69dc20a22e77e9d6508f269a489fee20732635a1e41fc3bb892c3499a8f
read_status: retrieved
retrieval:
  acquisition: local-file
  url: https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html
schema_version: source/v1
snapshot_sha256: sha256:19240c8229bdc716b8f594b5c2f02db066ff0612874556ef1e62da0fb14fd023
source_type: local-file
vault_id: public
---
CUDA Programming Guide#
CUDA and the CUDA Programming Guide
CUDA is a parallel computing platform and programming model developed by NVIDIA that enables dramatic increases in computing performance by harnessing the power of the GPU. It allows developers to accelerate compute-intensive applications and is widely used in fields such as deep learning, scientific computing, and high-performance computing (HPC).
This CUDA Programming Guide is the official, comprehensive resource on the CUDA programming model and how to write code that executes on the GPU using the CUDA platform. This guide covers everything from the CUDA programming model and the CUDA platform to the details of language extensions and covers how to make use of specific hardware and software features. This guide provides a pathway for developers to learn CUDA if they are new, and also provides an essential resource for developers as they build applications using CUDA.
Organization of This Guide
Even for developers who primarily use libraries, frameworks, or DSLs, an understanding of the CUDA programming model and how GPUs execute code is valuable in knowing what is happening behind the layers of abstraction. This guide starts with a chapter on the CUDA programming model outside of any specific programming language which is applicable to anyone interested in understanding how CUDA works, even non-developers.
The guide is broken down into five primary parts:
- Part 1: Introduction and Programming Model Abstract 
  - A language agnostic overview of the CUDA programming model as well as a brief tour of the CUDA platform.
  - This section is meant to be read by anyone wanting to understand GPUs and the concepts of executing code on GPUs, even if they are not developers.
- Part 2: Programming GPUs in CUDA 
  - The basics of programming GPUs in C++ and Python.
  - This section is meant to be read by anyone wanting to get started in GPU programming.
  - This section is meant to be instructional, not complete, and teaches the most important and common parts of CUDA programming, including some common performance considerations.
- Part 3: Advanced CUDA 
  - Introduces some more advance features of CUDA that enable both fine-grained control and more opportunities to maximize performance, including the use of multiple GPUs in a single application.
  - This section concludes with a tour of the features covered in part 4 with a brief introduction to the purpose and function of each, sorted by when and why a developer may find each feature useful.
- Part 4: CUDA Features 
  - This section contains complete coverage of specific CUDA features such as CUDA graphs, dynamic parallelism, interoperability with graphics APIs, and unified memory.
  - This section should be consulted when knowing the complete picture of a specific CUDA feature is needed. Where possible, care has been taken to introduce and motivate the features covered in this section in earlier sections.
- Part 5: Technical Appendices 
  - The technical appendices provide some reference documentation on CUDA’s C++ high-level language support, hardware-specific specifications, and other technical specifications.
  - This section is meant as technical reference for specific description of syntax, semantics, and technical behavior of elements of CUDA.
Parts 1-3 provide a guided learning experience for developers new to CUDA, though they also provide insight and updated information useful for CUDA developers of any experience level.
Parts 4 and 5 provide a wealth of information about specific features and detailed topics, and are intended to provide a curated, well-organized reference for developers needing to know more details as they write CUDA applications.