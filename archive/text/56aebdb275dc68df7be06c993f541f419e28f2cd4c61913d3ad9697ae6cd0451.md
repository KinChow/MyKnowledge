# Git配置

## 概念

### 系统配置（对所有用户使用）

存放在Git安装目录下：`%Git%/etc/gitconfig`。

使用`git config`时用`--system`选项，例如：

```shell
git config --system core.autocrlf
```



### 用户配置（只适用于当前用户）

存放在用户目录下。

使用`git config`时用`--global`选项，例如：

```shell
git config --global user.name
```



### 仓库配置（只对当前项目）

存放在工作目录的`./git/config`。

使用`git config`时用`--local`选项，例如：

```shell
git config --local remote.origin.url
```





## 配置个人身份

```shell
git config --global user.name "XXX"
git config --global user.email "xxx@xxx.com"
```

这些配置信息会在git仓库提交修改信息中体现，与git服务器认证使用的密码或公钥密码无关。





## 文本换行符配置

windows使用回车(CR)和换行(LF)两个字符结束一行，而mac或linux只是用换行(LF)一个字符。



提交时自动地把行结束符CRLF转换成LF，而签出代码时把LF转换成CRLF：

```shell
git config --global core.autocrlf true
```



提交时自动地把行结束符CRLF转换成LF，而签出时不转换：

```shell
git config --global core.autocrlf input
```





## 文本编码配置

* i18n.commitEncoding 选项：git commit log存储时采用的编码
* i18n.logOutputEncoding 选项：查看git log时，显示采用的编码

```shell
# 中文编码支持
git config --global gui.encoding utf-8
git config --global i18n.commitEncoding utf-8
git config --global i18n.logOutputEncoding utf-8

# 显示路径中的中文
git config --global core.quotepath false
```





## 与服务器的认证配置

### 常见的两种协议认证方式

#### http/https 协议认证

设置口令缓存：

```shell
git config --global credential.helper store
```



添加https证书信任：

```shell
git config --global http.sslverify false
```





#### ssh 协议认证

使用公钥认证，无需输入密码，加密传输，操作便利又保证安全。



过程：

1. 生成公钥：

```shell
ssh-keygen -t ed25519 -C "xxx@xxx.com"
```

2. 添加公钥到代码平台。