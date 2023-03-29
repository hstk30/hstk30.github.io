---
layout:     post
title:      "Shell 问题记录"
date:       2022-12-05
header-img: "img/confuse.png"
author:     "hstk30"
description: "急来拖佛脚，闲时不烧香。"
tags:
    - Shell
    - 编程问题记录
---

# shell 问题记录

> You can't connect the dots looking forward; you can only connect them looking backwards. 
> So you have to trust that the dots will somehow connect in your future.
> You have to trust in something - your gut, destiny, life, karma, whatever. 
> This approach has never let me down, and it has made all the difference in my life.
> --jobs


## 使用哪个 *Shell*

*Shell* 有多种实现，`bash`, `dash`, `zsh`，各有各的特性，非常不兼容。
用 `sh xx.sh` 执行脚本的时候需要确定这个 *sh* 具体链接的是哪个

```
ls -l /bin/sh
```

在 `docker` 内执行脚本经常遇到这个问题。

避免的方法：

1. 手动指定特定 *Shell* ，`/bin/bash xx.sh`
2. `./xx.sh`, 使用文件头中的 *Sha-Bang* ，`#!/bin/bash`
3. 自己控制 `docker` 的制作


## 没有二维数组

[How to declare 2D array in bash](https://stackoverflow.com/questions/16487258/how-to-declare-2d-array-in-bash)

需要模拟下标，狗都不用。


## 读文件只读到第一行

[While loop stops reading after the first line in Bash](https://stackoverflow.com/questions/13800225/while-loop-stops-reading-after-the-first-line-in-bash)

有 `config.csv` 文件如下

```
hstk,10/24/1995,111-555,8888-444
hstk30,8/24/1995,222-6666,8888-333
hw,01/10/1960,333-7777,8888-222
```

```sh
#!/bin/bash
CONFIG_FILE=${1}

count=0
OLDIFS=$IFS
IFS=','
while read name date phone1 phone2 ; do
   let count++
   echo $count
   echo $name
   echo $date
   echo $phone1
   echo $phone2
   # cat  # 可以是其他会读入stdin 的命令
done < $CONFIG_FILE
IFS=$OLDIFS
```

输出为

```
1
hstk
10/24/1995
111-555
8888-444
hstk30,8/24/1995,222-6666,8888-333
hw,01/10/1960,333-7777,8888-222
```

可以看到 `while` 循环只跑了1次，期望是3次，因为后面的输入被 `cat` 吃掉了

出现这个问题的原因应该是，`< $CONFIG_FILE` 以后 `stdin` 指向了这个文件， 
*Shell* 执行命令的逻辑是 `fork + exec` , `fork` 的时候复制了文件描述符表，
因此 `cat` 的 `stdin` 指向的也是 `$CONFIG_FILE`, 所以把这个文件的内容都读完了。

同理，类似 `cat` 的会从 `stdin` 读取数据的命令都会导致这个问题，如 `ssh`。

避免的方法：
1. 对于 `ssh` 添加 `-n` 参数可避免 
    > ssh -n      Redirects stdin from /dev/null (actually, prevents reading from stdin).  This must be used when ssh is run in the background.  A common trick is to use this to run X11 programs on a remote machine.  For example, ssh -n shadows.cs.hut.fi emacs & will start an emacs on shadows.cs.hut.fi, and the X11 connection will be automatically forwarded over an encrypted channel.  The ssh program will be put in the background.  (This does not work if ssh needs to ask for a password or passphrase; see also the -f option.)  Refer to the description of StdinNull in ssh_config(5) for details
2. 指定读入文件描述符，`9< $CONFIG_FILE` ，选一个没有用过的文件描述符（小脚本可适用），
    `Linux` 分配的文件描述符从当前最大的已分配文件描述符开始递增（我记得是这样的？）
3. 手动设置执行命令的 `stdin` 为 `/dev/null`， `< /dev/null`
