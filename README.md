# fedora-rpm-p7zip

p7zip for fedora with rar support

# why this repo exists?

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
