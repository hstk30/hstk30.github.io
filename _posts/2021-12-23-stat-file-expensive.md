---
layout:     post
title:      "stat 的代价很高"
date:       2021-12-23
header-img:	"img/accompany-2.jpeg"
author:     "hstk30"
description: "量大福也大，机深祸也深。"
tags:
    - 编程问题记录
---


# 一个日志引发的性能问题


```python
import os
import time

fp = open('test.txt', mode='w')

start_time = time.time()
for _ in range(100000):
	fp.write('a')
	fp.flush()
	os.stat('test.txt')
end_time = time.time()
print(f'Used time: {end_time - start_time}')
```

Used time: 37.93260073661804

```python
import os
import time

fp = open('test.txt', mode='w')

start_time = time.time()
for _ in range(100000):
	fp.write('a')
	fp.flush()
end_time = time.time()
print(f'Used time: {end_time - start_time}')
```

Used time: 0.10350179672241211

```python
import os
import time

fp = open('test.txt', mode='w')

start_time = time.time()
for _ in range(100000):
	os.stat('test.txt')
end_time = time.time()
print(f'Used time: {end_time - start_time}')
```

Used time: 0.09731388092041016

```
>>> stat test.txt
  文件："test.txt"
  大小：100000          块：200        IO 块：32768  普通文件
设备：2ah/42d   Inode：7937523     硬链接：1
权限：(0644/-rw-r--r--)  Uid：( 3011/  hanwei)   Gid：( 3999/ alg_dev)
最近访问：2021-12-23 14:58:27.833851083 +0800
最近更改：2021-12-23 14:59:40.443886325 +0800
最近改动：2021-12-23 14:59:40.443886325 +0800
创建时间：-
```


[WatchedFileHandler](https://docs.python.org/3.6/library/logging.handlers.html#watchedfilehandler)
