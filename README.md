# fedora-rpm-p7zip

p7zip for fedora with rar support

## installation

download the rpm files at https://github.com/ttys3/fedora-rpm-p7zip/releases

```bash
sudo dnf install -y p7zip-plugins p7zip
sudo dnf reinstall -y ./p7zip-*
```

and edit `/etc/dnf/dnf.conf`, add p7zip to dnf ignore:
```diff
--- /etc/dnf/dnf.conf.orig	2019-12-21 14:28:11.962944715 +0800
+++ /etc/dnf/dnf.conf	2019-12-21 14:28:58.361615505 +0800
@@ -4,3 +4,4 @@ installonly_limit=3
 clean_requirements_on_remove=True
 best=False
 skip_if_unavailable=True
+exclude=p7zip p7zip-plugins
```

## how to build

```shell
sudo dnf builddep -y ./p7zip.spec

export VERSION=16.02
curl -LO http://downloads.sf.net/p7zip/p7zip_${VERSION}_src_all.tar.bz2
mv p7zip_${VERSION}_src_all.tar.bz2 $HOME/rpmbuild/SOURCES/p7zip_16.02_src_all-norar.tar.bz2
cp -v *.patch $HOME/rpmbuild/SOUR
rpmbuild -bb ./p7zip.spec
```

## why this repo exists?

according to Igor Pavlov ( https://sourceforge.net/p/sevenzip/discussion/45798/thread/dc2d0438/#8f9f ):

>fedora/centos have removed 7-zip's unrar code as non-free code.
Maybe you can use p7zip compiled for another linux systems with 7-zip's unrar plugin:
p7zip-full and p7zip-rar

>RAR code is divided into two parts in p7zip:
>1) free part of unrar (in p7zip-full)
>2) non-free part of unrar (p7zip-rar)

>But fedora have removed both parts of unrar code.

this repo is fork from `https://src.fedoraproject.org/rpms/p7zip.git` and added rar support back.

see more details at https://src.fedoraproject.org/rpms/p7zip/tree/f31
