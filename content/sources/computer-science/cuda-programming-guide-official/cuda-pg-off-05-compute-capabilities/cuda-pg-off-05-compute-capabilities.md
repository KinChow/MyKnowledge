---
archive_policy: text-only
attachments:
- filename: cuda-pg-off-05-compute-capabilities.html
  kind: document
  media_type: text/html
  role: original
  sha256: sha256:c2a0bb13e405a112cce52d1240fe0e0547c010c7dd5407c2832d70f571a5c0ba
confidentiality: public
domain: computer-science
extractor: trafilatura/2.2.0
id: cuda-pg-off-05-compute-capabilities
media_type: text/html
origin: external
raw_ref:
  path: archive/raw/c2a0bb13e405a112cce52d1240fe0e0547c010c7dd5407c2832d70f571a5c0ba.html
  sha256: sha256:c2a0bb13e405a112cce52d1240fe0e0547c010c7dd5407c2832d70f571a5c0ba
read_status: retrieved
retrieval:
  acquisition: fetch
  resolved_url: https://docs.nvidia.com/cuda/cuda-programming-guide/05-appendices/compute-capabilities.html
  url: https://docs.nvidia.com/cuda/cuda-programming-guide/05-appendices/compute-capabilities.html
schema_version: source/v1
snapshot_sha256: sha256:e7cc3d592b336c7f6cd1f9ffab600a4d03cc620383d84ad417f8434b1e3ca6f3
source_type: doc
vault_id: public
---
5.1. Compute Capabilities#
The general specifications and features of a compute device depend on its compute capability (see Compute Capability and Streaming Multiprocessor Versions).
Table 29, Table 30, and Table 31 show the features and technical specifications associated with each compute capability that is currently supported.
All NVIDIA GPU architectures use a little-endian representation.
5.1.1. Obtain the GPU Compute Capability#
The CUDA GPU Compute Capability page provides a comprehensive mapping from NVIDIA GPU models to their compute capability.
Alternatively, the nvidia-smi tool, provided with the NVIDIA Driver, can be used to get the compute capability of a GPU. For example, the following command will output the GPU names and compute capabilities available on the system:
 --query-gpu=name,compute_cap
At runtime, the compute capability can be obtained using the CUDA Runtime API cudaDeviceGetAttribute() , CUDA Driver API cuDeviceGetAttribute(), or NVML API nvmlDeviceGetCudaComputeCapability():
#include <cuda_runtime_api.h>
int computeCapabilityMajor, computeCapabilityMinor;
cudaDeviceGetAttribute(&computeCapabilityMajor, cudaDevAttrComputeCapabilityMajor, device_id);
cudaDeviceGetAttribute(&computeCapabilityMinor, cudaDevAttrComputeCapabilityMinor, device_id);
#include <cuda.h>
int computeCapabilityMajor, computeCapabilityMinor;
cuDeviceGetAttribute(&computeCapabilityMajor, CU_DEVICE_ATTRIBUTE_COMPUTE_CAPABILITY_MAJOR, device_id);
cuDeviceGetAttribute(&computeCapabilityMinor, CU_DEVICE_ATTRIBUTE_COMPUTE_CAPABILITY_MINOR, device_id);
#include <nvml.h> // required linking with -lnvidia-ml
int computeCapabilityMajor, computeCapabilityMinor;
nvmlDeviceGetCudaComputeCapability(nvmlDevice, &computeCapabilityMajor, &computeCapabilityMinor);
5.1.2. Feature Availability#
Most compute features introduced with a compute architecture are intended to be available on all subsequent architectures. This is shown in Table 29 by the “yes” for availability of a feature on compute capabilities subsequent to its introduction.
5.1.2.1. Architecture-Specific Features#
Beginning with devices of Compute Capability 9.0, specialized compute features that are introduced with an architecture may not be guaranteed to be available on all subsequent compute capabilities. These features are called architecture-specific features and target acceleration of specialized operations, such as Tensor Core operations, which are not intended for all classes of compute capabilities or may significantly change in future generations. Code must be compiled with an architecture-specific compiler target (see Feature Set Compiler Targets) to enable architecture-specific features. Code compiled with an architecture-specific compiler target can only be run on the exact compute capability it was compiled for.
5.1.2.2. Family-Specific Features#
Beginning with devices of Compute Capability 10.0, some architecture-specific features are common to devices of more than one compute capability. The devices that contain these features are part of the same family and these features can also be called family-specific features. Family-specific features are guaranteed to be available on all devices in the same family. A family-specific compiler target is required to enable family-specific features. See Section 5.1.2.3. Code compiled for a family-specific target can only be run on GPUs which are members of that family.
5.1.2.3. Feature Set Compiler Targets#
There are three sets of compute features which the compiler can target:
Baseline Feature Set: The predominant set of compute features that are introduced with the intent to be available for subsequent compute architectures. These features and their availability are summarized in Table 29.
Architecture-Specific Feature Set: A small and highly specialized set of features called architecture-specific, that are introduced to accelerate specialized operations, which are not guaranteed to be available or might change significantly on subsequent compute architectures.  These features are summarized in the respective “Compute Capability #.#” subsections.  The architecture-specific feature set is a superset of the family-specific feature set.  Architecture-specific compiler targets were introduced with Compute Capability 9.0 devices and are selected by using an a suffix in the compilation target, for example by specifying compute_100a or compute_120a as the compute target.
Family-Specific Feature Set: Some architecture-specific features are common to GPUs of more than one compute capability. These features are summarized in the respective “Compute Capability #.#” subsections. With a few exceptions, later-generation devices with the same major compute capability are in the same family. Table 28 indicates the compatibility of family-specific targets with device compute capability, including exceptions. The family-specific feature set is a superset of the baseline feature set.  Family-specific compiler targets were introduced with Compute Capability 10.0 devices and are selected by using an f suffix in the compilation target, for example by specifying compute_100f or compute_120f as the compute target.
All devices starting from compute capability 9.0 have a set of features that are architecture-specific. To utilize the complete set of these features on a specific GPU, the architecture-specific compiler target with the suffix a must be used. Additionally, starting from compute capability 10.0, there are sets of features that appear in multiple devices with different minor compute capabilities. These sets of instructions are called family-specific features, and the devices which share these features are said to be part of the same family. The family-specific features are a subset of the architecture-specific features that are shared by all members of that GPU family. The family-specific compiler target with the suffix f allows the compiler to generate code that uses this common subset of architecture-specific features.
For example:
- The compute_100 compilation target does not allow the use of architecture-specific features.  This target will be compatible with all devices of compute capability 10.0 and later.
- The compute_100f family-specific compilation target allows the use of the subset of architecture-specific features that are common across the GPU family. This target will only be compatible with devices that are part of the GPU family. In this example, it is compatible with devices of Compute Capability 10.0, 10.3, and 10.7. The features available in the family-specificcompute_100f target are a superset of the features available in the baselinecompute_100 target.
- The compute_100a architecture-specific compilation target allows the use of the complete set of architecture-specific features in Compute Capability 10.0 devices. This target will only be compatible with devices of Compute Capability 10.0 and no others. The features available in thecompute_100a target form a superset of the features available in thecompute_100f target.
5.1.3. Features and Technical Specifications#
Note that the KB and K units used in the following tables correspond to 1024 bytes (i.e., a KiB) and 1024 respectively.
Non-Tensor Core throughputs. For more information on throughput see the CUDA Best Practices Guide
Kernels relying on shared memory allocations over 48 KB per block must use dynamic shared memory and require an explicit opt-in, see Configuring L1/Shared Memory Balance.
For devices of compute capability 10.7, kernels that use the 328 KB shared-memory configuration must explicitly enable cudaSharedMemoryModeAllowOversizedSharedMemory by setting either the cudaFuncAttributeSharedMemoryMode function attribute or the cudaLaunchAttributeSharedMemoryMode launch attribute.
Table 33 shows the input data types supported by Tensor Core acceleration. The Tensor Core feature set is available within the CUDA compilation toolchain through inline PTX. It is strongly recommended that applications use this feature set through CUDA-X libraries such as cuDNN, cuBLAS, and cuFFT, for example, or through CUTLASS, a collection of CUDA C++ template abstractions and Python domain-specific languages (DSLs) designed to enable high-performance matrix-matrix multiplication (GEMM) and related computations across all levels within CUDA.