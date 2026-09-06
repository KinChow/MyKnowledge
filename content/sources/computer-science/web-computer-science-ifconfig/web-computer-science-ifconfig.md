---
archive_policy: text-only
attachments:
- filename: web-computer-science-ifconfig.html
  kind: document
  media_type: text/html
  role: original
  sha256: sha256:f27d2e5bb91ba46fca6411933e56963bd0392c0547f57114691eb698483226f4
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-5f0b8d621c23
  position:
    end: 471
    start: 0
    type: TextPositionSelector
  quote_sha256: sha256:598ef0e973c196fa4cf6d84fb10b6ff41835fd6890bb946fe07454f1fb175c87
  selector:
    exact: "IFCONFIG(8)        Linux System Administrator's Manual        IFCONFIG(8)\n
      \      ifconfig - configure a network interface\n       ifconfig [-v] [-a] [-s]
      [interface]\n       ifconfig [-v] interface [aftype] options | address ...\n
      \      Ifconfig is used to configure the kernel-resident network\n       interfaces.
      \ It is used at boot time to set up interfaces as\n       necessary.  After
      that, it is usually only needed when debugging\n       or when system tuning
      is needed."
    prefix: ''
    suffix: "\n       If no arguments are give"
    type: TextQuoteSelector
  selector_sha256: sha256:48b4c712414791146c9bd954b7277dda346a73503b714f6b9bd8f7c0f738b70c
  snapshot_sha256: sha256:ad6fa4ac495fec0ee1ed0fa58ef35013f442db3c4cb4e91cbf27aff251c62f5a
extractor: trafilatura/2.2.0
id: web-computer-science-ifconfig
media_type: text/html
origin: external
raw_ref:
  path: archive/raw/f27d2e5bb91ba46fca6411933e56963bd0392c0547f57114691eb698483226f4.html
  sha256: sha256:f27d2e5bb91ba46fca6411933e56963bd0392c0547f57114691eb698483226f4
read_status: retrieved
retrieval:
  acquisition: fetch
  resolved_url: https://man7.org/linux/man-pages/man8/ifconfig.8.html
  url: https://man7.org/linux/man-pages/man8/ifconfig.8.html
schema_version: source/v1
snapshot_sha256: sha256:ad6fa4ac495fec0ee1ed0fa58ef35013f442db3c4cb4e91cbf27aff251c62f5a
source_type: doc
vault_id: public
---
IFCONFIG(8)        Linux System Administrator's Manual        IFCONFIG(8)
       ifconfig - configure a network interface
       ifconfig [-v] [-a] [-s] [interface]
       ifconfig [-v] interface [aftype] options | address ...
       Ifconfig is used to configure the kernel-resident network
       interfaces.  It is used at boot time to set up interfaces as
       necessary.  After that, it is usually only needed when debugging
       or when system tuning is needed.
       If no arguments are given, ifconfig displays the status of the
       currently active interfaces.  If a single interface argument is
       given, it displays the status of the given interface only; if a
       single -a argument is given, it displays the status of all
       interfaces, even those that are down.  Otherwise, it configures an
       interface.
   Address Families
       If the first argument aftype after the interface name is
       recognized as the name of a supported address family, that address
       family is used for decoding and displaying all protocol addresses.
       Currently supported address families include inet (TCP/IP,
       default), inet6 (IPv6), ax25 (AMPR Packet Radio), ddp (Appletalk
       Phase 2), ipx (Novell IPX) and netrom (AMPR Packet radio).
       All numbers supplied as parts in IPv4 dotted decimal notation may
       be decimal, octal, or hexadecimal, as specified in the ISO C
       standard (that is, a leading '0x' or '0X' implies hexadecimal;
       otherwise, a leading '0' implies octal; otherwise, the number is
       interpreted as decimal).  Use of hexadecimal and octal numbers is
       not RFC-compliant and therefore its use is discouraged.
       -a     display all interfaces which are currently available, even
              if down
       -s     display a short list (like netstat -i)
       -v     be more verbose for some error conditions
       interface
              The name of the interface.  This is usually a driver name
              followed by a unit number, for example eth0 for the first
              Ethernet interface. If your kernel supports alias
              interfaces, you can specify them with syntax like eth0:0
              for the first alias of eth0. You can use them to assign
              more addresses. To delete an alias interface use ifconfig
              eth0:0 down.  Note: for every scope (i.e. same net with
              address/netmask combination) all aliases are deleted, if
              you delete the first (primary).
       up     This flag causes the interface to be activated.  It is
              implicitly specified if an address is assigned to the
              interface; you can suppress this behavior when using an
              alias interface by appending an - to the alias (e.g.
              eth0:0-).  It is also suppressed when using the IPv4
              0.0.0.0 address as the kernel will use this to implicitly
              delete alias interfaces.
       down   This flag causes the driver for this interface to be shut
              down.
       [-]arp Enable or disable the use of the ARP protocol on this
              interface.
       [-]promisc
              Enable or disable the promiscuous mode of the interface.
              If selected, all packets on the network will be received by
              the interface.
       [-]allmulti
              Enable or disable all-multicast mode.  If selected, all
              multicast packets on the network will be received by the
              interface.
       mtu M  This parameter sets the Maximum Transfer Unit (MTU) of an
              interface to M bytes.
       dstaddr addr
              Set the remote IP address for a point-to-point link (such
              as PPP).  This keyword is now obsolete; use the pointopoint
              keyword instead.
       netmask addr
              Set the IP network mask for this interface.  This value
              defaults to the usual class A, B or C network mask (as
              derived from the interface IP address), but it can be set
              to any value.
       add addr/prefixlen
              Add an address to an interface.
       del addr/prefixlen
              Remove an address from an interface.
       tunnel ::aa.bb.cc.dd
              Create a new SIT (IPv6-in-IPv4) device, tunnelling to the
              given destination.
       irq I  Set the interrupt line used by this device.  Not all
              devices can dynamically change their IRQ setting.
       io_addr Mem
              Set the start address in I/O space for this device.  Only a
              few old devices need this.
       mem_start Mem
              Set the start address for shared memory used by this
              device.  Only a few old devices need this.
       media type
              Set the physical port or medium type to be used by the
              device.  Not all devices can change this setting, and those
              that can vary in what values they support.  Typical values
              for type are 10base2 (thin Ethernet), 10baseT (twisted-pair
              10Mbps Ethernet), AUI (external transceiver) and so on.
              The special medium type of auto can be used to tell the
              driver to auto-sense the media.  Again, not all drivers can
              do this.
       [-]broadcast [addr]
              If the address argument is given, set the protocol
              broadcast address for this interface.  Otherwise, set (or
              clear) the IFF_BROADCAST flag for the interface.
       [-]pointopoint [addr]
              This keyword enables the point-to-point mode of an
              interface, meaning that it is a direct link between two
              machines with nobody else listening on it.
              If the address argument is also given, set the protocol
              address of the other side of the link, just like the
              obsolete dstaddr keyword does.  Otherwise, set or clear the
              IFF_POINTOPOINT flag for the interface.
       hw hwclass hwaddr
              Set the hardware address of this interface, if the device
              driver supports this operation.  The keyword must be
              followed by the name of the hardware class hwclass  and the
              printable ASCII equivalent of the hardware address.
              Hardware classes currently supported include ether
              (Ethernet), ax25 (AMPR AX.25), ARCnet and netrom (AMPR
              NET/ROM).
       multicast
              Set the multicast flag on the interface. This should not
              normally be needed as the drivers set the flag correctly
              themselves.
       txqueuelen length
              Set the length of the transmit queue of the device. It is
              useful to set this to small values for slower devices with
              a high latency (modem links, ISDN) to prevent fast bulk
              transfers from disturbing interactive traffic like telnet
              too much.
       name newname
              Change the name of this interface to newname.  The
              interface must be shut down first.
       address
              The IP address to be assigned to this interface.
   Interface Statistics Table (-s)
       The table lists active (default) or all known (-a) kernel
       interfaces.  With the -s option it is the same output as netstat
       -i.
       > ifconfig -s enp2s0f0
       Iface     MTU    RX-OK RX-ERR RX-DRP RX-OVR  TX-OK TX-ERR TX-DRP TX-OVR Flg
       enp2s0f0 1500 18668761      0   1318 0    26038367      0      0      0 BMRU
       The result table shows the following columns:
       Iface  Name and alias prefix of the network interface.
       MTU    The maximum transfer unit in bytes of this interface.
       RX-OK  Number of successfully received packets since interface
              statistic was reset.
       RX-ERR Total count of receive errors since statistic reset.  This
              includes: rx_errors (general receive errors), rx_crc_errors
              (packets received with a CRC checksum failure),
              rx_frame_errors (frame alignment errors, corrupted).
       RX-DRP Number of incoming packets that were dropped before
              reaching the protocol stack.  Common causes: no buffer
              space in the driver, congestion, or resource limitations.
       RX-OVR Number of packets dropped due to FIFO buffer overflows in
              the NIC or driver.  Common causes: the hardware could not
              push frames fast enough to the system.
       TX-OK  Number of packets  successfully transmitted since interface
              statistic was reset.
       TX-ERR Number of transmit errors.  Includes collisions, carrier
              loss, and other transmission failures.
       TX-DRP Number of packets dropped by the driver before being sent
              (e.g., due to congestion or lack of buffer space).
       TX-OVR Number of packets lost due to transmit FIFO overflows in
              the hardware.
       Flg    The flags for this interface, as listed below.
   Interface Flags
       The list of interface flags used in the short and detailed
       interface output.  The names of the bit flag constants of the
       SIOCGIFFLAGS control are listed in netdevice(7).
       A, ALLMULTI
              Accepts all multicast packets (IFF_ALLMULTI).
       B, BROADCAST
              Interface supports broadcast communication (IFF_BROADCAST).
       D, DEBUG
              Internal debugging for the interface enabled (IFF_DEBUG).
       L, LOOPBACK
              Interface is a loopback device (IFF_LOOPBACK).
       M, MULTICAST
              Interface supports multicast communication (IFF_MULTICAST).
       d, DYNAMIC
              Address is dynamically set (e.g. by DHCP) (IFF_DYNAMIC).
       P, PROMISC
              Interface is in promiscuous mode (captures all packets)
              (IFF_PROMISC).  This flag might not reliably show promisc
              mode.
       N, NOTRAILERS
              Avoid use of trailers in packets (IFF_NOTRAILERS).
       O, NOARP
              Interface does not use ARP (IFF_NOARP).
       p, POINTOPOINT
              Interface is point-to-point (has a peer instead of
              broadcast) (IFF_POINTOPOINT).
       s, SLAVE
              Interface is part of a bonded device (IFF_SLAVE).
       m, MASTER
              Interface controls a bonded device (IFF_MASTER).
       R, RUNNING
              Interface is operational and resources are allocated
              (IFF_RUNNING).
       U, UP  Interface is administratively up (IFF_UP).
       [NO FLAGS], <>
              If the bitmask for the interface status is 0.
   Interface Details
       Sample output for the details of a single interface:
       > ifconfig enp2s0f0
       enp2s0f0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
               inet 203.0.113.9  netmask 255.255.255.0  broadcast 203.0.113.255
               inet6 fe80::a8bb:ccff:fedd:eeff  prefixlen 64  scopeid 0x20<link>
               inet6 2001:db8::a8bb:ccff:fedd:eeff  prefixlen 64  scopeid 0x0<global>
               ether aa:bb:cc:dd:ee:ff  txqueuelen 1000  (Ethernet)
               RX packets 18668507  bytes 9459465501 (8.8 GiB)
               RX compressed 0
               RX errors 0  dropped 1318  overruns 0  frame 0
               TX packets 26038199  bytes 16983080620 (15.8 GiB)
               TX compressed 0
               TX errors 0  dropped 0  overruns 0  carrier 0  collisions 0
               device interrupt 30
       The output of the interface list is the same as netstat -i -e.
       For each interface there is a block starting with the interface
       name the flags and the mtu, optional outfil and keepalive.
       Then one line for each address, prefixed with the address type and
       its type specifc details.
              In the example is one IPv4 (inet) address.  it specifies
              netmask, optional broadcast.  If the point-to-point flag is
              set if will show destination address.
              The example follows with two IPv6 (inet6) addresses.  Such
              a line specifies addresss, prefixlen, and scopeid:
              compat IPv4 compatibility address.
              global A Global Unicast Address (UGA).
              site   A site-unique address.
              link   A link-local address.
              host   A loopback address.
       This is followed with a line for the hardware address family
       (ether in this case).  This line contains txqueuelen if available.
       If the device is configured for port selection, it has a media
       line.
       After that the packets statistics for transmit (TX) and receive
       (RX) are shown (same as in the short format above, but the
       different error counters are shown seperate).  Additionally the
       total number of bytes (frame sizes total) are shown (with a human
       friendly formatting as comment).  The compressed packet counter
       lines are optional.
       The final device line lists optional driver details, with some of
       the following keywords: interrupt, base, memory, and dma.
       Since kernel release 2.2 there are no explicit interface
       statistics for alias interfaces anymore. The statistics printed
       for the original address are shared with all alias addresses on
       the same device. If you want per-address statistics you should add
       explicit accounting rules for the address using the iptables(8)
       command.
       Since net-tools 1.60-4 ifconfig is printing byte counters and
       human readable counters with IEC 60027-2 units. So 1 KiB are 2^10
       byte. Note, the numbers are truncated to one decimal (which can by
       quite a large error if you consider 0.1 PiB is 112.589.990.684.262
       bytes :)
       Interrupt problems with Ethernet device drivers fail with EAGAIN
       (SIOCSIIFLAGS: Resource temporarily unavailable) it is most likely
       a interrupt conflict.
       /proc/net/dev /proc/net/if_inet6
       Ifconfig uses the ioctl access method to get the full address
       information, which limits hardware addresses to 8 bytes.  Because
       Infiniband hardware address has 20 bytes, only the first 8 bytes
       are displayed correctly.  Please use ip link command from iproute2
       package to display link layer informations including the hardware
       address.
       While appletalk DDP and IPX addresses will be displayed they
       cannot be altered by this command.
       Homepage of the net-tools project: 
       ⟨https://net-tools.sourceforge.io⟩
       Prefixes for binary multiples (NIST): 
       ⟨https://physics.nist.gov/cuu/Units/binary.html⟩
       route(8), netstat(8), arp(8), ip-link(8), iptables(8)
       interfaces(5), ip(7), netdevice(7)
       Fred N. van Kempen <waltje@uwalt.nl.mugnet.org>,
       Alan Cox <Alan.Cox@linux.org>, Andi Kleen,
       Phil Blundell <Philip.Blundell@pobox.com>,
       Bernd Eckenfels <net-tools@lina.inka.de>.
       This page is part of the net-tools (networking utilities) project.
       Information about the project can be found at 
       ⟨http://net-tools.sourceforge.net/⟩.  If you have a bug report for
       this manual page, see ⟨http://net-tools.sourceforge.net/⟩.  This
       page was obtained from the project's upstream Git repository
       ⟨git://git.code.sf.net/p/net-tools/code⟩ on 2026-05-24.  (At that
       time, the date of the most recent commit that was found in the
       repository was 2026-05-12.)  If you discover any rendering
       problems in this HTML version of the page, or you believe there is
       a better or more up-to-date source for the page, or you have
       corrections or improvements to the information in this COLOPHON
       (which is not part of the original manual page), send a mail to
       man-pages@man7.org
net-tools                       2025-09-10                    IFCONFIG(8)
Pages that refer to this page: getifaddrs(3), if_nameindex(3), if_nametoindex(3), sk98lin(4), wavelan(4), proc(5), proc_pid_net(5), arp(8), nameif(8), netstat(8), plipconfig(8), rarp(8), route(8)