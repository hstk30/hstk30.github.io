---
layout:     post
title:      "Callee-saved register meet Thread switch"
date:       2023-12-31
header-img: "img/confuse.png"
author:     "hstk30"
tags:
    - 编译原理
---

# Callee-saved registers and Thread switch

## Caller-saved registers Callee-saved registers

- *Caller-saved registers* : 保存这些寄存器的责任在调用者，也就是说被调用者（callee）可以任意修改。
    因此，又名 *volatile registers* （对于调用者而言，这些寄存器在调用过程中是 **易失的**），
    或者 *call-clobbered* （在调用过程中会被 **破坏**）。
- *Callee-saved registers* : 保存这些寄存器的责任在被调用者，调用者可以放心使用这些寄存器，即使在跳转指令后。
    因此，又名 *non-volatile registers* （对于调用者而言，这些寄存器在调用过程中是 **非易失的**），
    或者 *call-preserved* （在调用过程中会被 **保存**）。

在汇编中的表现形式 :

```
Caller:
...
str caller-saved regs
argument pass
bl Callee
handle ret
ldr caller-saved regs
...
ret

Callee:
str callee-saved regs
...
ldr callee-saved regs
ret
```

## 系统级线程

对于系统级的线程，线程切换由操作系统控制，将线程的当前状态、上下文，也就是各种寄存器的状态保存到内核的一块区域，

汇编中的表现形式（基本上也是直接写的汇编） :

```
__switch:
#__switch(current_task_kernal_stack a0, next_task_kernal_stack a1)
str current sp to a0
str all registers to a0

ldr all registers from a1
ldr sp from a1
```

## 用户级线程

对于用户级线程，则由实现定义。可能是抢占式的，也可能是非抢占式的，对于线程切换时的上下文保存也由实现而定，
这对于编译器的实现形成了挑战。

现在有一种轻量级线程（Light-Wight Thread），它是非抢占式的，调用顺序由编码者直接定义。由于是轻量级线程，
因此线程切换时也只保存通用寄存器（General-Purpose registers）和一些特殊寄存器。

## 问题

![LWT-Callee-saved-regs](/img/in-post/LWT-Callee-save-reg.png)

设置背景为 **AArach64** （`v8` 为向量寄存器，且为 *Callee-saved registers*）， 有上面的调用关系。
编译器按照 **调用规范** 正确生成汇编代码: 

- 对于 `FuncB` ，按照 *Callee-saved registers* 的原则， 在函数开始保存 `v8` 的值，在函数结束时恢复 `v8` 的值
- 对于 `FuncA` ，由于 `v8` 为 *Callee-saved registers* ，因此在 `LWT(FuncB)` 后不需要恢复就可以直接使用 `v8`

看似一切都合理，其实不然。由于这种线程模型只保存通用寄存器，未保存向量寄存器，因此在 `LWT(FuncA)` 切回
*return address* 继续执行后，它使用的 `v8` 寄存器的值其实是 `FuncB` 中的新 `v8` ，`FuncA` 真正需要的 `v8`
在 `FuncB` 的最后才会被恢复。

