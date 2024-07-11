# 2-openclash安装

## toc

1. [2-openclash安装](#2-openclash安装)
    1. [toc](#toc)
    2. [关于安装](#关于安装)

## 关于安装

git 发布页

[git发布页](https://github.com/vernesong/OpenClash/releases)

安装依赖

```bash
#iptables
opkg update
opkg install coreutils-nohup bash iptables dnsmasq-full curl ca-certificates ipset ip-full iptables-mod-tproxy iptables-mod-extra libcap libcap-bin ruby ruby-yaml kmod-tun kmod-inet-diag unzip luci-compat luci luci-base
```

然后在路由器的软件包里进行直接安装ipk  (我是把文件下载到pscly.cn 中转了一下的)

<CommentService/>
