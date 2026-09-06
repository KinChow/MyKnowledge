---
archive_policy: text-only
attachments:
- filename: web-computer-science-c-class-and-raii.html
  kind: document
  media_type: text/html
  role: original
  sha256: sha256:de9324c60d732a47e77eef1e8327a001ce956f8580ff8b3752fb81b71ef48c88
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-ba1aae8c21d5
  position:
    end: 348
    start: 0
    type: TextPositionSelector
  quote_sha256: sha256:dedfa059d5bd1210ad24fd9dafabf512c2d2196839c0473e23dcae4e8d36caf4
  selector:
    exact: 'RAII

      Resource Acquisition Is Initialization or RAII, is a C++ programming technique[1][2]
      which binds the life cycle of a resource that must be acquired before use (allocated
      heap memory, thread of execution, open socket, open file, locked mutex, disk
      space, database connection—anything that exists in limited supply) to the lifetime
      of an object.'
    prefix: ''
    suffix: '

      RAII guarantees that the resour'
    type: TextQuoteSelector
  selector_sha256: sha256:03f52960ec9df6ffa23fb7252ea709d5246b9c08217a7e9d72c6c4c1d144efcc
  snapshot_sha256: sha256:359ff95622ed2db2f75e0df801a22e1fbf41ec2ffb2f415a3cd7587f67d5da30
extractor: trafilatura/2.2.0
id: web-computer-science-c-class-and-raii
media_type: text/html
origin: external
raw_ref:
  path: archive/raw/de9324c60d732a47e77eef1e8327a001ce956f8580ff8b3752fb81b71ef48c88.html
  sha256: sha256:de9324c60d732a47e77eef1e8327a001ce956f8580ff8b3752fb81b71ef48c88
read_status: retrieved
retrieval:
  acquisition: fetch
  resolved_url: https://en.cppreference.com/cpp/language/raii
  url: https://en.cppreference.com/w/cpp/language/raii
schema_version: source/v1
snapshot_sha256: sha256:359ff95622ed2db2f75e0df801a22e1fbf41ec2ffb2f415a3cd7587f67d5da30
source_type: doc
vault_id: public
---
RAII
Resource Acquisition Is Initialization or RAII, is a C++ programming technique[1][2] which binds the life cycle of a resource that must be acquired before use (allocated heap memory, thread of execution, open socket, open file, locked mutex, disk space, database connection—anything that exists in limited supply) to the lifetime of an object.
RAII guarantees that the resource is available to any function that may access the object (resource availability is a class invariant, eliminating redundant runtime tests). It also guarantees that all resources are released when the lifetime of their controlling object ends, in reverse order of acquisition. Likewise, if resource acquisition fails (the constructor exits with an exception), all resources acquired by every fully-constructed member and base subobject are released in reverse order of initialization. This leverages the core language features (object lifetime, scope exit, order of initialization and stack unwinding) to eliminate resource leaks and guarantee exception safety. Another name for this technique is Scope-Bound Resource Management (SBRM), after the basic use case where the lifetime of an RAII object ends due to scope exit.
RAII can be summarized as follows:
- encapsulate each resource into a class, where
  - the constructor acquires the resource and establishes all class invariants or throws an exception if that cannot be done,
  - the destructor releases the resource and never throws exceptions;
- always use the resource via an instance of a RAII-class that either
  - has automatic storage duration or temporary lifetime itself, or
  - has lifetime that is bounded by the lifetime of an automatic or temporary object.
Move semantics enable the transfer of resources and ownership between objects, inside and outside containers, and across threads, while ensuring resource safety.
Classes with open()/close(), lock()/unlock(), or init()/copyFrom()/destroy() member functions are typical examples of non-RAII classes:
std::mutex m;
void bad() 
{
    m.lock();             // acquire the mutex
    f();                  // if f() throws an exception, the mutex is never released
    if (!everything_ok())
        return;           // early return, the mutex is never released
    m.unlock();           // if bad() reaches this statement, the mutex is released
}
void good()
{
    std::lock_guard<std::mutex> lk(m); // RAII class: mutex acquisition is initialization
    f();                               // if f() throws an exception, the mutex is released
    if (!everything_ok())
        return;                        // early return, the mutex is released
}                                      // if good() returns normally, the mutex is released
The standard library
The C++ library classes that manage their own resources follow RAII: std::string, std::vector, std::jthread(since C++20), and many others acquire their resources in constructors (which throw exceptions on errors), release them in their destructors (which never throw), and don't require explicit cleanup.
In addition, the standard library offers several RAII wrappers to manage user-provided resources:
- std::unique_ptr and std::shared_ptr through std::make_unique and std::make_shared to manage dynamically-allocated memory;
- std::lock_guard, std::unique_lock, std::shared_lock to manage mutexes.
Notes
RAII does not apply to the management of the resources that are not acquired before use: CPU time, core availability, cache capacity, entropy pool capacity, network bandwidth, electric power consumption, stack memory. For such resources, a C++ class constructor cannot guarantee resource availability for the duration of object lifetime, and other means of resource management have to be used.