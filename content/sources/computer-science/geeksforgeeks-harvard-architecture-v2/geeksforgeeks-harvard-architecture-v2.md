---
archive_policy: text-only
attachments:
- filename: geeksforgeeks-harvard-architecture-v2.html
  kind: document
  media_type: text/html
  role: original
  sha256: sha256:1831f0be079f6d493ef00bdab912cb1d24c1b1e00f48f28f4a1b060ce20ae5bd
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-714c76f0e212
  position:
    end: 164
    start: 0
    type: TextPositionSelector
  quote_sha256: sha256:21e936887782ad902a3be64d1ac259db9e9df7968d7794072cae818adcca4f95
  selector:
    exact: Harvard architecture is a computer design model where program instructions
      and data are stored in separate memory units that are accessed through independent
      buses.
    prefix: ''
    suffix: ' This separation allows the proc'
    type: TextQuoteSelector
  selector_sha256: sha256:4308a64e2815792871d5c422a8b7b2883064a189ad3d9d9935354f40c9c417bf
  snapshot_sha256: sha256:d3e824b788d7572bdf12e205dfeb67b027e4e40e571b7157bb1c6999a7dcc79f
extractor: trafilatura/2.2.0
id: geeksforgeeks-harvard-architecture-v2
local:
  file_sha256: sha256:1831f0be079f6d493ef00bdab912cb1d24c1b1e00f48f28f4a1b060ce20ae5bd
  path_ref: local-sidecar:public/geeksforgeeks-harvard-architecture-v2
media_type: text/html
origin: external
raw_ref:
  path: archive/raw/1831f0be079f6d493ef00bdab912cb1d24c1b1e00f48f28f4a1b060ce20ae5bd.html
  sha256: sha256:1831f0be079f6d493ef00bdab912cb1d24c1b1e00f48f28f4a1b060ce20ae5bd
read_status: retrieved
retrieval:
  acquisition: local-file
  url: https://www.geeksforgeeks.org/computer-organization-architecture/harvard-architecture/
schema_version: source/v1
snapshot_sha256: sha256:d3e824b788d7572bdf12e205dfeb67b027e4e40e571b7157bb1c6999a7dcc79f
source_type: local-file
vault_id: public
---
Harvard architecture is a computer design model where program instructions and data are stored in separate memory units that are accessed through independent buses. This separation allows the processor to fetch instructions and access data simultaneously, which helps avoid the bottleneck present in traditional Von Neumann systems.
- Eliminates the Von Neumann bottleneck.
- Faster and predictable performance (suitable for real-time systems).
- Parallel access to both instructions and data.
Working Principle
In Harvard Architecture, fetching an instruction from instruction memory and reading/writing data from/to data memory happen at the same time without waiting for one to finish. Separate buses prevent the bottleneck that occurs when data and instructions share a path. For example, while an instruction is being executed, the next instruction can be fetched simultaneously, speeding up processing.
Buses
Buses are used as signal pathways. In Harvard architecture, there are separate buses for both instruction and data. Types of Buses:
- Data Bus: It carries data among the main memory system, processor, and I/O devices.
- Data Address Bus: It carries the address of data from the processor to the main memory system.
- Instruction Bus: It carries instructions among the main memory system, processor, and I/O devices.
- Instruction Address Bus: It carries the address of instructions from the processor to the main memory system.
Components of Harvard Architecture
Harvard architecture is designed with specific components that handle instruction execution, control, and data communication.
- Arithmetic and Logic Unit: The arithmetic logic unit is part of the CPU that operates all the calculations needed. It performs addition, subtraction, comparison, logical Operations, bit Shifting Operations, and various arithmetic operations.
- Control Unit: The Control Unit is the part of the CPU that operates all processor control signals. It controls the input and output devices and also controls the movement of instructions and data within the system.
- The Input/Output (I/O) system enables communication between the computer and external devices. Input devices provide data and instructions to the system. Output devices display or deliver the processed results to the user.
Application of Harvard Architecture
Harvard architecture is a type of computer design where the memory for instructions and data are kept separate. Here are the some applications:
Digital Signal Processors (DSPs):
- Audio and video processing, telecommunications, radar systems, and image processing.
- Texas Instruments TMS320 for hearing aids.
Microcontrollers (MCUs):
- Embedded systems in consumer electronics, automotive systems, IoT devices, and industrial automation.
- PIC in automotive ABS
Network Processors:
- Routers, switches, and network security appliances.
- Broadcom StrataXGS
Automotive Systems:
- Engine control units (ECUs), advanced driver-assistance systems (ADAS), and infotainment systems.
- NXP S32K for engine control