---
archive_policy: text-only
attachments:
- filename: web-computer-science-fastboot.html
  kind: document
  media_type: text/html
  role: original
  sha256: sha256:7fa0a7c5152915ce4b40c2828e111293419c170e9e7a2f0e0fb85b8c50fa10dc
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-19a7d5bbd3c0
  position:
    end: 427
    start: 0
    type: TextPositionSelector
  quote_sha256: sha256:1c63c1fcaed6c9f713ab07e203e37fbb32c544e91b0d9104090dd85941c9a601
  selector:
    exact: 'fastboot常用命令

      显示fastboot设备：fastboot devices

      获取手机相关信息：fastboot getvar all

      重启手机：fastboot reboot

      重启到bootloader：fastboot reboot-bootloader

      擦除分区：fastboot erase (分区名)

      例：清除system分区：fastboot erase system

      刷入分区：fastboot flash (分区名) (分区镜像)

      例：将boot镜像 “boot.img” 刷入boot分区：fastboot flash boot boot.img

      引导启动镜像：fastboot boot (分区镜像)

      例：启动到recovery分区：fastboot boot recovery.img

      刷入ROM：fastboot update (刷机包)

      例：将 update.zip 刷入：fastboot update update.'
    prefix: ''
    suffix: 'zip

      解锁Bootloader：fastboot oem un'
    type: TextQuoteSelector
  selector_sha256: sha256:eff70449cfcda9819018f6bc75238f9dc7809eadb6e6f2c15c015cc9536d966a
  snapshot_sha256: sha256:d892e5ed148e58381caddb84f39400ac0770d9ff976afe93e1af6c273a8b53db
extractor: trafilatura/2.2.0
id: web-computer-science-fastboot
media_type: text/html
origin: external
raw_ref:
  path: archive/raw/7fa0a7c5152915ce4b40c2828e111293419c170e9e7a2f0e0fb85b8c50fa10dc.html
  sha256: sha256:7fa0a7c5152915ce4b40c2828e111293419c170e9e7a2f0e0fb85b8c50fa10dc
read_status: retrieved
retrieval:
  acquisition: fetch
  resolved_url: https://blog.csdn.net/m0_66587877/article/details/134807972
  url: https://blog.csdn.net/m0_66587877/article/details/134807972
schema_version: source/v1
snapshot_sha256: sha256:d892e5ed148e58381caddb84f39400ac0770d9ff976afe93e1af6c273a8b53db
source_type: doc
vault_id: public
---
fastboot常用命令
显示fastboot设备：fastboot devices
获取手机相关信息：fastboot getvar all
重启手机：fastboot reboot
重启到bootloader：fastboot reboot-bootloader
擦除分区：fastboot erase (分区名)
例：清除system分区：fastboot erase system
刷入分区：fastboot flash (分区名) (分区镜像)
例：将boot镜像 “boot.img” 刷入boot分区：fastboot flash boot boot.img
引导启动镜像：fastboot boot (分区镜像)
例：启动到recovery分区：fastboot boot recovery.img
刷入ROM：fastboot update (刷机包)
例：将 update.zip 刷入：fastboot update update.zip
解锁Bootloader：fastboot oem unlock (参数见视频，视机型而定)
多设备使用：fastboot -s (命令)
通过fastboot devices获取序列号，控制多设备中的一个
例：清除序列号为’abc’设备的system分区：fastboot -s abc erase system