---
archive_policy: text-only
attachments:
- filename: android-dumpsys-v2.txt
  kind: document
  media_type: text/plain
  role: original
  sha256: sha256:e86ac672adbf214253697c26e7e424508ffa3c00ee059c228b46e1ffb8345f93
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-e9bbe59eef86
  position:
    end: 94
    start: 0
    type: TextPositionSelector
  quote_sha256: sha256:b98b5cbccbf4150febc799842cecfe0805a28720786717060f52b6d15b4ee634
  selector:
    exact: dumpsys is a tool that runs on Android devices and provides information
      about system services.
    prefix: ''
    suffix: ' Call dumpsys from the command l'
    type: TextQuoteSelector
  selector_sha256: sha256:74ee00e1ea503cd051b10ffc1d3da5bddd731324f88b03f8d42d90f9964e398c
  snapshot_sha256: sha256:e86ac672adbf214253697c26e7e424508ffa3c00ee059c228b46e1ffb8345f93
extractor: utf8/1
id: android-dumpsys-v2
local:
  file_sha256: sha256:e86ac672adbf214253697c26e7e424508ffa3c00ee059c228b46e1ffb8345f93
  path_ref: local-sidecar:public/android-dumpsys-v2
media_type: text/plain
origin: external
raw_ref:
  path: archive/raw/e86ac672adbf214253697c26e7e424508ffa3c00ee059c228b46e1ffb8345f93.txt
  sha256: sha256:e86ac672adbf214253697c26e7e424508ffa3c00ee059c228b46e1ffb8345f93
read_status: retrieved
retrieval:
  acquisition: local-file
  url: https://developer.android.com/tools/dumpsys?hl=en
schema_version: source/v1
snapshot_sha256: sha256:e86ac672adbf214253697c26e7e424508ffa3c00ee059c228b46e1ffb8345f93
source_type: local-file
vault_id: public
---
dumpsys is a tool that runs on Android devices and provides information about system services. Call dumpsys from the command line using the Android Debug Bridge (ADB) to get diagnostic output for all system services running on a connected device.

The general syntax for using dumpsys is as follows:
adb shell dumpsys [-t timeout] [--help | -l | --skip services | service [ arguments ] | -c | -h]

To get a diagnostic output for all system services for your connected device, run adb shell dumpsys. For more manageable output, specify the service you want to examine by including it in the command.
