---
domain: tools
legacy_first_commit_at: '2025-07-06T20:30:14+08:00'
legacy_path: docs/tools/code-server/code-server.md
snapshot_sha256: sha256:65102567541d98f456c1e74d0bccb6f1094675e9d37fab903b4fc422dce9cf34
title: code-server
---
# code-server

## 安装

```shell
curl -fsSL https://code-server.dev/install.sh | sh
```



如果遇到以下报错

```shell
curl: (7) Failed to connect to raw.githubusercontent.com port 443: Connection refused
```

参考解决办法修改hosts，https://github.com/hawtim/hawtim.github.io/issues/10

```shell
vim etc/hosts
===============
199.232.68.133 raw.githubusercontent.com
199.232.68.133 user-images.githubusercontent.com
199.232.68.133 avatars2.githubusercontent.com
199.232.68.133 avatars1.githubusercontent.com
```





## 配置

输入命令行输入`code-server`, 会生成一个本地配置文件，ctrl+C关闭，再去改配置文件：

```shell
vim ~/.config/code-server/config.yaml
===============
bind-addr: 0.0.0.0:8080 # 如果没域名需要改成这个
auth: password
password: 123456
cert: false
===============
code-server
```





## 参考

https://zhuanlan.zhihu.com/p/539902333