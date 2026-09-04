---
archive_policy: text-only
attachments:
- filename: adb-man-page.html
  kind: document
  media_type: text/html
  role: original
  sha256: sha256:840ae95020ad4d1f896bc41f54c1c926abca1664a00d6900fba62c91c01fada9
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-13340361505e
  position:
    end: 938
    start: 796
    type: TextPositionSelector
  quote_sha256: sha256:ea04468846430ecbeb619e37d502e5f299d464bf6f9eea6d55146942705dbff2
  selector:
    exact: Connects to the ADB Server via its smart socket interface. Allows sending
      requests, receives responses and manages lifecycle of the adb server
    prefix: 'd [COMMAND_OPTIONS]

      Description

      '
    suffix: '.

      Tasks are performed via comman'
    type: TextQuoteSelector
  selector_sha256: sha256:1517f55c839e9f442ff0e3ea2f6837a01230e36be35ebb2d5e1bffa591915679
  snapshot_sha256: sha256:1fbdfbfc4a3140d02abe4c978f650427bfd4a6ce7cdd2703bc209eb8bcf0b66d
- evidence_id: evidence-f54fa20e67c1
  position:
    end: 1103
    start: 974
    type: TextPositionSelector
  quote_sha256: sha256:7431c98beadb9b01590e04fcda779f032848f3ee3dc33af6dfcc2ac7366f532b
  selector:
    exact: Some commands are fulfilled directly by the server while others are “forwarded
      over to the adbd(ADB daemon) running on the device
    prefix: 'sks are performed via commands. '
    suffix: '.

      Global Options

      - -a

      - Listen o'
    type: TextQuoteSelector
  selector_sha256: sha256:189940a78b27b9bd45a0d1d4c43cd11281903fb44ac117d88bcb9cda3e7278ba
  snapshot_sha256: sha256:1fbdfbfc4a3140d02abe4c978f650427bfd4a6ce7cdd2703bc209eb8bcf0b66d
- evidence_id: evidence-fc90a2d45789
  position:
    end: 1904
    start: 1869
    type: TextPositionSelector
  quote_sha256: sha256:e3b241e4cafe17bf9432af908bd008e31f2a679c911dd518d0d99f5215ffe394
  selector:
    exact: devices [-l] List connected devices
    prefix: 'out is closed.

      General Commands

      '
    suffix: '.

      -l Use long output.

      track-devi'
    type: TextQuoteSelector
  selector_sha256: sha256:5fcc5cb35c3dc2641a6c44a1a91986dc04fb458a17812614672063eab60c5c7e
  snapshot_sha256: sha256:1fbdfbfc4a3140d02abe4c978f650427bfd4a6ce7cdd2703bc209eb8bcf0b66d
- evidence_id: evidence-ffe377f53faf
  position:
    end: 4026
    start: 3939
    type: TextPositionSelector
  quote_sha256: sha256:7681e1b50d0fd71afa2e2ab174c2a03d08031f24a67f0de75b89abc0e00d9a11
  selector:
    exact: push [–sync] [-z ALGORITHM] [-Z] LOCAL... REMOTE Copy local files/directories
      to device
    prefix: ' “–proto-binary”.

      File Transfer

      '
    suffix: '.

      –sync Only push files that are'
    type: TextQuoteSelector
  selector_sha256: sha256:b1695f807f08e9db0b3805598c61325fdb46b65685a72afe395052906c068fdc
  snapshot_sha256: sha256:1fbdfbfc4a3140d02abe4c978f650427bfd4a6ce7cdd2703bc209eb8bcf0b66d
- evidence_id: evidence-ac9d97596664
  position:
    end: 4336
    start: 4263
    type: TextPositionSelector
  quote_sha256: sha256:619be0416199ede1a85e524a3351d1bca5f037e641bcae87944bb99e392cea06
  selector:
    exact: pull [-a] [-z ALGORITHM] [-Z] REMOTE... LOCAL Copy files/dirs from device
    prefix: '/zstd).

      -Z Disable compression.

      '
    suffix: '

      -a preserve file timestamp and '
    type: TextQuoteSelector
  selector_sha256: sha256:25b1187a9ac15f70be6105e4d8fb3f69031d0ad9af035b23a26a815d1af31754
  snapshot_sha256: sha256:1fbdfbfc4a3140d02abe4c978f650427bfd4a6ce7cdd2703bc209eb8bcf0b66d
- evidence_id: evidence-a45ee5354880
  position:
    end: 5381
    start: 5294
    type: TextPositionSelector
  quote_sha256: sha256:c95a6292682948c1214fd487ba98371da17cf2a42eb629d5376cd0775ec3be7d
  selector:
    exact: install [-lrtsdg] [–instant] PACKAGE Push a single package to the device
      and install it
    prefix: 'so adb shell cmd package help):

      '
    suffix: '

      install-multiple [-lrtsdpg] [–i'
    type: TextQuoteSelector
  selector_sha256: sha256:c7d3814f3b7833e9b6e54f09d862d92b4d2dc43bd0186be770639770bc27ad55
  snapshot_sha256: sha256:1fbdfbfc4a3140d02abe4c978f650427bfd4a6ce7cdd2703bc209eb8bcf0b66d
- evidence_id: evidence-a5342d654f4e
  position:
    end: 1384
    start: 1315
    type: TextPositionSelector
  quote_sha256: sha256:d6e1211e17e235fe0ebf98b74d38671a461e11cb19fec5a114fac18dd368f619
  selector:
    exact: '-s SERIAL

      - Use device with given SERIAL (overrides $ANDROID_SERIAL).'
    prefix: 'le TCP/IP devices available).

      - '
    suffix: '

      - -t ID

      - Use device with given'
    type: TextQuoteSelector
  selector_sha256: sha256:35fc581e9b602164c5b4d2b3eda27fea504963b8cf6e1d0da509ec9fc9bc8b04
  snapshot_sha256: sha256:1fbdfbfc4a3140d02abe4c978f650427bfd4a6ce7cdd2703bc209eb8bcf0b66d
- evidence_id: evidence-89d257d47bde
  position:
    end: 1545
    start: 1498
    type: TextPositionSelector
  quote_sha256: sha256:2f4b981ccabbfae03681b3a6618ec2197aa5d9cdeddc46529050ee1ae763506b
  selector:
    exact: Smart socket PORT of adb server [default=5037].
    prefix: 'ault=localhost].

      - -P

      - **PORT* '
    suffix: '

      - -L SOCKET

      - Listen on given s'
    type: TextQuoteSelector
  selector_sha256: sha256:764ce4158ec832bd522ca1e63bfce3a77df97c17c423ca8ffaad74ab0864d3dd
  snapshot_sha256: sha256:1fbdfbfc4a3140d02abe4c978f650427bfd4a6ce7cdd2703bc209eb8bcf0b66d
- evidence_id: evidence-a6e6d0e8e1a3
  position:
    end: 5659
    start: 5626
    type: TextPositionSelector
  quote_sha256: sha256:9963bf4a0dc7490af1c1fd9208bbe0001e7f2b9a2ff7f38f5ee2286b727cde04
  selector:
    exact: '-r: Replace existing application.'
    prefix: 'ice and install them atomically

      '
    suffix: '

      -t Allow test packages.

      -d Allo'
    type: TextQuoteSelector
  selector_sha256: sha256:c691bfbef04c0f0d0346546c1fe9b529ba10ea066967f024065ea5708f35569b
  snapshot_sha256: sha256:1fbdfbfc4a3140d02abe4c978f650427bfd4a6ce7cdd2703bc209eb8bcf0b66d
extractor: trafilatura/2.2.0
id: adb-man-page
media_type: text/html
origin: external
raw_ref:
  path: archive/raw/840ae95020ad4d1f896bc41f54c1c926abca1664a00d6900fba62c91c01fada9.html
  sha256: sha256:840ae95020ad4d1f896bc41f54c1c926abca1664a00d6900fba62c91c01fada9
read_status: retrieved
retrieval:
  acquisition: fetch
  resolved_url: https://www.mankier.com/1/adb
  url: https://www.mankier.com/1/adb
schema_version: source/v1
snapshot_sha256: sha256:1fbdfbfc4a3140d02abe4c978f650427bfd4a6ce7cdd2703bc209eb8bcf0b66d
source_type: doc
vault_id: public
---
Examples (TL;DR)
- Check whether the adb server process is running and start it: adb start-server
- Terminate the adb server process: adb kill-server
- Start a remote shell in the target emulator/device instance: adb shell
- Push an Android application to an emulator/device: adb install -r path/to/file.apk
- Copy a file/directory from the target device: adb pull path/to/device_file_or_directory path/to/local_destination_directory
- Copy a file/directory to the target device: adb push path/to/local_file_or_directory path/to/device_destination_directory
- List all connected devices: adb devices
- Specify which device to send commands to if there are multiple devices: adb -s device_id shell
Adb(1) Man Page
Version
1.0.41
Synopsis
adb [GLOBAL_OPTIONS] command [COMMAND_OPTIONS]
Description
Connects to the ADB Server via its smart socket interface. Allows sending requests, receives responses and manages lifecycle of the adb server.
Tasks are performed via commands. Some commands are fulfilled directly by the server while others are “forwarded over to the adbd(ADB daemon) running on the device.
Global Options
- -a
- Listen on all network interfaces, not just localhost.
- -d
- Use USB device (error if multiple devices connected).
- -e
- Use TCP/IP device (error if multiple TCP/IP devices available).
- -s SERIAL
- Use device with given SERIAL (overrides $ANDROID_SERIAL).
- -t ID
- Use device with given transport ID.
- -H
- Name of adb server host [default=localhost].
- -P
- **PORT* Smart socket PORT of adb server [default=5037].
- -L SOCKET
- Listen on given socket for adb server [default=tcp:localhost:5037].
- --one-device SERIAL|USB
- Server will only connect to one USB device, specified by a SERIAL number or USB device address (only with `start-server' or `server nodaemon').
- --exit-on-write-error
- Exit if stdout is closed.
General Commands
devices [-l] List connected devices.
-l Use long output.
track-devices [-l][–proto-text][–proto-binary] Same as the `device' command, but does not return. It sends updates when the list of devices changes.
-l Use legacy long output.
-proto-text Use protobuf output.
-proto-binary Use binary protobuf output.
help Show this help message.
version Show version number.
Networking
connect HOST[:PORT] Connect to a device via TCP/IP [default PORT=5555].
disconnect [HOST[:PORT]] Disconnect from given TCP/IP device [default PORT=5555], or all.
pair HOST[:PORT] [PAIRING_CODE] Pair with a device for secure TCP/IP communication.
forward --list | [–no-rebind] LOCAL_REMOTE | --remove LOCAL | --remove-all
--list List all forward socket connections.
[–no-rebind] LOCAL_REMOTE Forward socket connection using one of the followings.
tcp:PORT (local may be “tcp:0” to pick any open port. localreserved:UNIX_DOMAIN_SOCKET_NAME. localfilesystem:UNIX_DOMAIN_SOCKET_NAME. jdwp:PROCESS PID (remote only). vsock:CID:PORT (remote only). acceptfd:FD (listen only). dev:DEVICE_NAME. dev-raw:DEVICE_NAME. (open device in raw mode)**.
--remove LOCAL Remove specific forward socket connection.
--remove-all Remove all forward socket connections.
reverse --list | [--no-rebind] REMOTE LOCAL | --remove REMOTE | --remove-all
--list List all reverse socket connections from device.
[--no-rebind] REMOTE LOCAL Reverse socket connection using one of the following.
tcp:PORT (REMOTE may be “tcp:0” to pick any open port). localabstract:UNIX_DOMAIN_SOCKET_NAME. localreserved:UNIX_DOMAIN_SOCKET_NAME. localfilesystem:UNIX_DOMAIN_SOCKET_NAME.
--remove REMOTE Remove specific reverse socket connection.
--remove-all Remove all reverse socket connections from device.
mdns check | services Perform mDNS subcommands.
check Check if mdns discovery is available.
services List all discovered services.
track-services Stream discovered services. Supports flags “–proto-text” and “–proto-binary”.
list-known-hosts Show ADB Wifi paired devices. Supports flags “–proto-text” and “–proto-binary”.
File Transfer
push [–sync] [-z ALGORITHM] [-Z] LOCAL... REMOTE Copy local files/directories to device.
–sync Only push files that are newer on the host than the device.
-n Dry run, push files to device without storing to the filesystem.
-z enable compression with a specified algorithm (any/none/brotli/lz4/zstd).
-Z Disable compression.
pull [-a] [-z ALGORITHM] [-Z] REMOTE... LOCAL Copy files/dirs from device
-a preserve file timestamp and mode.
-z enable compression with a specified algorithm (any/none/brotli/lz4/zstd)
-Z disable compression
sync [-l] [-z ALGORITHM] [-Z] [all|data|odm|oem|product|system|system_ext|vendor] Sync a local build from $ANDROID_PRODUCT_OUT to the device (default all)
-n Dry run. Push files to device without storing to the filesystem.
-l List files that would be copied, but don’t copy them.
-z Enable compression with a specified algorithm (any/none/brotli/lz4/zstd)
-Z Disable compression.
Shell
shell [-e ESCAPE] [-n] [-Tt] [-x] [COMMAND...] Run remote shell command (interactive shell if no command given).
-e Choose escape character, or “none”; default `~'.
-n Don’t read from stdin.
-T: Disable pty allocation.
-t: Allocate a pty if on a tty (-tt: force pty allocation).
-x Disable remote exit codes and stdout/stderr separation.
emu COMMAND Run emulator console COMMAND
App Installation
(see also adb shell cmd package help):
install [-lrtsdg] [–instant] PACKAGE Push a single package to the device and install it
install-multiple [-lrtsdpg] [–instant] PACKAGE... Push multiple APKs to the device for a single package and install them
install-multi-package [-lrtsdpg] [–instant] PACKAGE... Push one or more packages to the device and install them atomically
-r: Replace existing application.
-t Allow test packages.
-d Allow version code downgrade (debuggable packages only).
-p Partial application install (install-multiple only).
-g Grant all runtime permissions.
--abi ABI Override platform’s default ABI.
--instant Cause the app to be installed as an ephemeral install app.
--no-streaming Always push APK to device and invoke Package Manager as separate steps.
--streaming Force streaming APK directly into Package Manager.
--fastdeploy Use fast deploy.
-no-fastdeploy Prevent use of fast deploy.
-force-agent Force update of deployment agent when using fast deploy.
-date-check-agent Update deployment agent when local version is newer and using fast deploy.
--version-check-agent Update deployment agent when local version has different version code and using fast deploy.
--local-agent     Locate agent files from local source build (instead of SDK location). See also adb shell pm help for more options.
uninstall [-k] APPLICATION_ID Remove this APPLICATION_ID from the device.
-k Keep the data and cache directories.
Debugging
bugreport [PATH] Write bugreport to given PATH [default=bugreport.zip]; if PATH is a directory, the bug report is saved in that directory. devices that don’t support zipped bug reports output to stdout.
jdwp List pids of processes hosting a JDWP transport.
logcat Show device log (logcat –help for more).
server-status Display server configuration (USB backend, mDNS backend, log location, binary path. See adb_host.proto (AdbServerStatus) for details.
Security
disable-verity Disable dm-verity checking on userdebug builds.
enable-verity Re-enable dm-verity checking on userdebug builds.
keygen FILE Generate adb public/private key; private key stored in FILE.
Scripting
wait-for [-TRANSPORT] -STATE... Wait for device to be in a given state.
STATE: device, recovery, rescue, sideload, bootloader, or disconnect. TRANSPORT: usb, local, or any [default=any].
get-state Print offline | bootloader | device.
get-serialno Print SERIAL_NUMBER.
get-devpath Print DEVICE_PATH.
remount [-R] Remount partitions read-write.
-R Automatically reboot the device.
reboot [bootloader|recovery|sideload|sideload-auto-reboot] Reboot the device; defaults to booting system image but supports bootloader and recovery too.
sideload Reboots into recovery and automatically starts sideload mode.
sideload-auto-reboot Same as sideload but reboots after sideloading.
sideload OTAPACKAGE Sideload the given full OTA package OTAPACKAGE.
root Restart adbd with root permissions.
unroot Restart adbd without root permissions.
usb Restart adbd listening on USB.
tcpip PORT Restart adbd listening on TCP on PORT.
Internal Debugging
start-server Ensure that there is a server running.
kill-server Kill the server if it is running.
reconnect Close connection from host side to force reconnect.
reconnect device Close connection from device side to force reconnect.
reconnect offline Reset offline/unauthorized devices to force reconnect.
USB
Only valid when running with libusb backend.
attach SERIAL Attach a detached USB device identified by its SERIAL number.
detach SERIAL Detach from a USB device identified by its SERIAL to allow use by other processes.
Features
host-features
list features supported by adb server.
features
list features supported by both adb server and device.
Environment Variables
$ADB_TRACE Comma (or space) separated list of debug info to log: all,adb,sockets,packets,rwx,usb,sync,sysdeps,transport,jdwp,services,auth,fdevent,shell,incremental,mdns,mdns-stack.
$ADB_VENDOR_KEYS Colon-separated list of keys (files or directories).
$ANDROID_SERIAL Serial number to connect to (see -s).
$ANDROID_LOG_TAGS Tags to be used by logcat (see logcat –help).
$ADB_LOCAL_TRANSPORT_MAX_PORT Max emulator scan port (default 5585, 16 emulators).
$ADB_MDNS_AUTO_CONNECT Comma-separated list of mdns services to allow auto-connect (default adb-tls-connect).
$ADB_MDNS_OPENSCREEN The default mDNS-SD backend is Bonjour (mdnsResponder). For machines where Bonjour is not installed, adb can spawn its own, embedded, mDNS-SD back end, openscreen. If set to “1”, this env variable forces mDNS backend to openscreen.
$ADB_LIBUSB     ADB has its own USB backend implementation but can also employ libusb. use adb devices -l (usb: prefix is omitted for libusb) or adb host-features (look for libusb in the output list) to identify which is in use. To override the default for your OS, set ADB_LIBUSB to “1” to enable libusb, or “0” to enable the ADB backend implementation.
Bugs
See Issue Tracker: here (https://issuetracker.google.com/issues/new?component=192795&template=1310483).
Authors
See OWNERS file in ADB AOSP repo.