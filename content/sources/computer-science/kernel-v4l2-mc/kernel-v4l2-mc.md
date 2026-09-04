---
archive_policy: text-only
attachments:
- filename: kernel-v4l2-mc.txt
  kind: document
  media_type: text/plain
  role: original
  sha256: sha256:2d76c8af4d05637a2678f0ebdc5b5383ebf7876930efd12f5da0a9cfd37cc6dd
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-d3551866bc58
  position:
    end: 347
    start: 238
    type: TextPositionSelector
  quote_sha256: sha256:b3a5c74b1d2140153fe6afb172c6e8801d0b68808a8c4961c503a853199ec795
  selector:
    exact: hardware devices are modelled as an oriented graph of building blocks called
      entities connected through pads.
    prefix: 'dia framework. To achieve this, '
    suffix: ' An entity is a basic media hard'
    type: TextQuoteSelector
  selector_sha256: sha256:fb72a6e5ba8c388222726d6385aabbcd9f2bab4413b59c93e893511ad9f38b5c
  snapshot_sha256: sha256:2d76c8af4d05637a2678f0ebdc5b5383ebf7876930efd12f5da0a9cfd37cc6dd
- evidence_id: evidence-0267a563245f
  position:
    end: 644
    start: 348
    type: TextPositionSelector
  quote_sha256: sha256:3256e5593070c6a650c56d7a16663f8311166ee5a22ee72ec3929307506e7722
  selector:
    exact: An entity is a basic media hardware building block. It can correspond to
      a large variety of logical blocks such as physical hardware devices (CMOS sensor
      for instance), logical hardware devices (a building block in a System-on-Chip
      image processing pipeline), DMA channels or physical connectors.
    prefix: 'ntities connected through pads. '
    suffix: ' A pad is a connection endpoint '
    type: TextQuoteSelector
  selector_sha256: sha256:9a23069b089e76a185f15d6c2940c30146239bc64dd408a84dc1ad994b9b14e6
  snapshot_sha256: sha256:2d76c8af4d05637a2678f0ebdc5b5383ebf7876930efd12f5da0a9cfd37cc6dd
extractor: utf8/1
id: kernel-v4l2-mc
local:
  file_sha256: sha256:2d76c8af4d05637a2678f0ebdc5b5383ebf7876930efd12f5da0a9cfd37cc6dd
  path_ref: local-sidecar:public/kernel-v4l2-mc
media_type: text/plain
origin: external
raw_ref:
  path: archive/raw/2d76c8af4d05637a2678f0ebdc5b5383ebf7876930efd12f5da0a9cfd37cc6dd.txt
  sha256: sha256:2d76c8af4d05637a2678f0ebdc5b5383ebf7876930efd12f5da0a9cfd37cc6dd
read_status: retrieved
retrieval:
  acquisition: local-file
schema_version: source/v1
snapshot_sha256: sha256:2d76c8af4d05637a2678f0ebdc5b5383ebf7876930efd12f5da0a9cfd37cc6dd
source_type: local-file
vault_id: public
---
# Source: https://docs.kernel.org/driver-api/media/mc-core.html (Media Controller, retrieved 2026-09-04)

Discovering a device internal topology, and configuring it at runtime, is one of the goals of the media framework. To achieve this, hardware devices are modelled as an oriented graph of building blocks called entities connected through pads. An entity is a basic media hardware building block. It can correspond to a large variety of logical blocks such as physical hardware devices (CMOS sensor for instance), logical hardware devices (a building block in a System-on-Chip image processing pipeline), DMA channels or physical connectors. A pad is a connection endpoint through which an entity can interact with other entities. Data (not restricted to video) produced by an entity flows from the entity’s output to one or more entity inputs. Pads should not be confused with physical pins at chip boundaries. A link is a point-to-point oriented connection between two pads, either on the same entity or on different entities. Data flows from a source pad to a sink pad.

6.1.2. Media device ¶ A media device is represented by a struct media_device instance, defined in include/media/media-device.h . Allocation of the structure is handled by the media device driver, usually by embedding the media_device instance in a larger driver-specific structure. Drivers initialise media device instances by calling media_device_init() . After initialising a media device instance, it is registered by calling __media_device_register() via the macro media_device_register() and unregistered by calling media_device_unregister() . An initialised media device must be eventually cleaned up by calling media_device_cleanup() . Note that it is not allowed to unregister a media device instance that was not previously registered, or clean up a media device instance that was not previously initialised.

6.1.3. Entities ¶ Entities are represented by a struct media_entity instance, defined in include/media/media-entity.h . The structure is usually embedded into a higher-level structure, such as v4l2_subdev or video_device instances, although drivers can allocate entities directly. Drivers initialize entity pads by calling media_entity_pads_init() . Drivers register entities with a media device by calling media_device_register_entity() and unregistered by calling media_device_unregister_entity() .

6.1.4. Interfaces ¶ Interfaces are represented by a struct media_interface instance, defined in include/media/media-entity.h . Currently, only one type of interface is defined: a device node. Such interfaces are represented by a struct media_intf_devnode . Drivers initialize and create device node interfaces by calling media_devnode_create() and remove them by calling: media_devnode_remove() .

6.1.5. Pads ¶ Pads are represented by a struct media_pad instance, defined in include/media/media-entity.h . Each entity stores its pads in a pads array managed by the entity driver. Drivers usually embed the array in a driver-specific structure. Pads are identified by their entity and their 0-based index in the pads array. Both information are stored in the struct media_pad , making the struct media_pad pointer the canonical way to store and pass link references. Pads have flags that describe the pad capabilities and state. MEDIA_PAD_FL_SINK indicates that the pad supports sinking data. MEDIA_PAD_FL_SOURCE indicates that the pad supports sourcing data.

Note One and only one of MEDIA_PAD_FL_SINK or MEDIA_PAD_FL_SOURCE must be set for each pad.

6.1.6. Links ¶ Links are represented by a struct media_link instance, defined in include/media/media-entity.h . There are two types of links: 1. pad to pad links : Associate two entities via their PADs. Each entity has a list that points to all links originating at or targeting any of its pads. A given link is thus stored twice, once in the source entity and once in the target entity. Drivers create pad to pad links by calling: media_create_pad_link() and remove with media_entity_remove_links() . 2. interface to entity links : Associate one interface to a Link. Drivers create interface to entity links by calling: media_create_intf_link() and remove with media_remove_intf_links() .

Note Links can only be created after having both ends already created.

Links have flags that describe the link capabilities and state. The valid values are described at media_create_pad_link() and media_create_intf_link() .

6.1.7. Graph traversal ¶ The media framework provides APIs to traverse media graphs, locating connected entities and links. To iterate over all entities belonging to a media device, drivers can use the media_device_for_each_entity macro, defined in include/media/media-device.h . struct media_entity * entity ;

media_device_for_each_entity ( entity , mdev ) { // entity will point to each entity in turn ... }

Helper functions can be used to find a link between two given pads, or a pad connected to another pad through an enabled link ( media_entity_find_link() , media_pad_remote_pad_first() , media_entity_remote_source_pad_unique() and media_pad_remote_pad_unique() ).

6.1.8. Use count and power handling ¶ Due to the wide differences between drivers regarding power management needs, the media controller does not implement power management. However, the struct media_entity includes a use_count field that media drivers can use to track the number of users of every entity for power management needs. The media_entity . use_count field is owned by media drivers and must not be touched by entity drivers. Access to the field must be protected by the media_device . graph_mutex lock.

6.1.9. Links setup ¶ Link properties can be modified at runtime by calling media_entity_setup_link() .

6.1.10. Pipelines and media streams ¶ A media stream is a stream of pixels or metadata originating from one or more source devices (such as a sensors) and flowing through media entity pads towards the final sinks. The stream can be modified on the route by the devices (e.g. scaling or pixel format conversions), or it can be split into mul
