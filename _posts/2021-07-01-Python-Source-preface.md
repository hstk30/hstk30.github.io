---
layout:     post
title:      "Python源码阅读前言"
date:       2021-07-01
author:     "hstk30"
header-img: "img/prospect.jpg"
description: "欲穷千里目，更上一层楼。"
tags:
    - Python
---

> 用c 思考，用Python 实现。

其实在大四的时候就有幸看到 **《Python源码剖析》** 这本书，在实习的时候午睡前还会看一会儿再睡，
写的实在是好，使得我的c 语言能力也大有长进。最近有空再复习一下，
会更新一些Python源码相关的文章，主要讲Python 内建对象：`int, string, list, dict`的实现，
内存管理机制，可能会讲多线程机制。


# Python源码阅读前言

参考的Python 源码版本是 [Python 2.5.1](https://www.python.org/downloads/release/python-251/)。

它的目录组织结构如下：

目录 			  | 描述
-------------  | -------------
Include		  	  |  c语言头文件，可以找到所有**Py{type}Object** 对象的定义和相应方法的声明
Object			  | 对应**Py{type}Object** 对象方法的实现，并初始化相应的**Py{type}_Type**类型
Python 		       |  Python 解释器的*Compiler* 和执行引擎（`ceval.c`）部分，是Python 运行的核心
Modules			| 用c语言实现的底层库
Lib				| Python 实现的标准库
Parser			|  Python解释器词法分析和语法分析

其他的目录我也说不清楚到底是干嘛的，就不写了。。。  

当然，如果是要看Python 的底层实现，我觉得看`Include`, `Object`, `Python` 目录下的文件就行了。

![img](/img/in-post/Python-arch.png)

上面的图就是Python 的总体架构，我们可以把代码阅读的关注点放在 *Compiler* 后的事情， *Compiler* 就相当于使用Python的 
[dis库](https://docs.python.org/3.6/library/dis.html) 将我们写的Python 代码转换成了指令集合--Python 字节码（byte code），
然后这些字节码会进入 *Code Evauator* 中，也就是`Python/ceval.c` 中的一个2000 多行的函数。
这个函数就叫做Python 的虚拟机，其实就是一个`for` 无限循环加上`switch: case:`，处理定义的所有字节码操作。（嗯，并不是什么魔法嘛）

### 参考

**《Python源码剖析》** : 强烈推荐  
[CPython internals](https://www.youtube.com/playlist?list=PLzV58Zm8FuBL6OAv1Yu6AwXZrnsFbbR0S) 

