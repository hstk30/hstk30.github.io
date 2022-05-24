# rCore 学习

```
qemu-system-riscv64 \
  -machine virt \
   -nographic \
   -bios ./bootloader/rustsbi-qemu.bin \
   -device loader,file=target/riscv64gc-unknown-none-elf/release/os.bin,addr=0x80200000 \
   -s -S

riscv64-unknown-elf-gdb \
    -ex 'file target/riscv64gc-unknown-none-elf/release/os' \
    -ex 'set arch riscv:rv64' \
    -ex 'target remote localhost:1234'
``` 

```
rust-objcopy --strip-all target/riscv64gc-unknown-none-elf/release/os -O binary target/riscv64gc-unknown-none-elf/release/os.bin
```

`<C-A> x` 退出`qemu`


## 编写OS 需要的重要功能

- 设置trap 入口stvec, trap 的时候上下文保存和恢复，地址空间切换
- 每个进程一个页表、内核栈
- 不同应用的内核栈之间差一个Guard Page 在栈溢出的时候硬件报错，而不是覆盖之前的数据
- 内核需要一个虚拟内存地址到物理内存地址的恒等映射的页表，内核页表
- 建立用于内核地址空间与应用地址空间相互切换所需的跳板空间？  内核和应用vpn共同映射的一块公共物理地址，用于执行trap操作，使得切换地址空间的指令控制流仍能连续执行
- 设置`satp` 内核空间、用户空间切换
- 页面置换算法，纯软件的实现性能不行，需要硬件上的支持。
	- Clock置换策略（工程上的妥协），硬件提供PTE 的`A` Access `D` Dirty 位。软硬件约定：每当页被引用（即读或写）时，处理器硬件将把对应该页的页表项的使用位设置为1。但是，硬件不会清除该位（即将其设置为0），而这是由操作系统来负责的。
	- LRU置换策略
	- 工作集置换策略
	- 缺页率置换策略


- waitpid 系统调用：子进程不能自己回收自己的资源，需要父进程调用waitpid才行，因为子进程需要通过内核栈进行系统调用，因此子进程不能自己回收自己的内核栈页帧


## 一些可以决策的地方

### 内存分配算法

- buddy system alloc  ✅
- bitmap, 
- free list

评价指标：性能，内外内存碎片
 
### 内核与应用空间的隔离

- 内核和应用有各自的虚拟内存空间。Trap 的时候需要进行地址空间的切换（设置页表基址寄存器），任务切换的时候无需进行（因为这个过程全程在内核内完成）。但需要一个*跳板机制* ，来保证切换地址空间的执行控制流能连续执行
- 每个应用的页表都映射一遍内核的逻辑段，没有一个单独的内核地址空间。Trap 的时候无需切换地址空间，但任务切换的时候仍然需要（每个应用一个页表，因此是必须的）。优点：1. 易实现 2. 避免了系统调用Trap 时的地址空间切换。 缺点： 1. 每个应用的页表多了内核的映射页表带来内存的消耗 2. 侧信道攻击，熔断 (Meltdown) 漏洞 ，应用能看到内核中的数据（？？）


### 页面置换算法

- 全局页面置换策略： 每个应用的物理页数量可以动态调整。 ✅
- 局部页面置换策略： 每个应用的物理页数量固定，在应用内部置换

硬件支持：硬件提供PTE 的`A` Access `D` Dirty 位。软硬件约定：每当页被引用（即读或写）时，处理器硬件将把对应该页的页表项的使用位设置为1。但是，硬件不会清除该位（即将其设置为0），而这是由操作系统来负责的。

* Clock置换策略 ✅
* LRU置换策略
* 工作集置换策略
* 缺页率置换策略

评价指标： 访存命中率

### 任务调度算法

* 协作式 yield
* 抢占式

- 时间片的 Round-Robin， 10ms? 30ms?
- 优先级调度
- Round-Robin with multiple feedback
- 彩票调度（Lottery Scheduling）
- 步长调度（Stride Scheduling）

评价指标： 公平性，cpu和IO设备的使用率，响应时间，周转时间


#### 多核调度

多核的负载平衡，处理器亲和性，Cache 一致性，共享数据的同步互斥机制


### 文件系统

UNIX 文件只是一个字节序列。文件内容的任何结构或组织仅由处理它的程序决定。

> 基于路径的索引难以并行或分布式化，因为我们总是需要查到一级目录的底层编号才能查到下一级，这是一个天然串行的过程

需要辨别哪些数据结构是存放的磁盘上的，哪些是存放的内存中的。


## a fork() is in the road


[原文](https://www.microsoft.com/en-us/research/uploads/prod/2019/04/fork-hotos19.pdf)

[中文翻译（不全）](https://github.com/YdrMaster/notebook/blob/main/rCore3.0/20220330-get-fork-out-of-my-os.md)

> Intuitively, the way to make a system scale is to avoid needless sharing.

没太懂，不过这老哥的语气是很强硬。是说`fork + exec` 不好，`exec` 只是一个附带品，主要还是说`fork` 不好，过于集中化，
不能compose等等缺点。`fork` 之后需要手动关闭一些文件、管道、`socket`，设置`close_on_exec` 我还有点感知，
但是那些安全问题我确是一无所知。
 
推荐使用`多线程` 来替代传统的使用`fork` 来进行并发的方式？ 使用`posix_spawn` 替换`fork + exec` ? 不过好像有点像推销`Windows` 的
`CreateProcess()` 实现（一堆参数!）。将`copy-on-write` 独立出来作为单独的`API` 。


## risc-v ISA 学习

在RV32I上进行

通过组合使用RV32I提供的基础指令来实现一些有用的扩展执行，伪指令(pseudo instructions)

## 转移控制

`call` <==> `auipc ra, 0`  <== `ra = PC + (0 << 12)`
`ret` <==> `jalr x0, ra, 0` <== `x0=PC + 4; PC=ra + 0`

## 数据传送指令


## 长整型加法

假设`long` 为64位，则两个64位的加法，可以被分解为一下基础指令
假设`l1` 的高32位存放在寄存器`a3` 中，低32位存放在`a2` 中，
`l2` 的高32位存放在寄存器`a5` 中，低32位存放在`a4` 中，
结果的高32位存放在寄存器`a1` 中，低32位存放在`a0` 。

```
add a0, a2, a4 # 低32位
sltu a2, a0, a2 # 是否进位，两个正数相加反而变小，说明进位
add a5, a3, a5 # 高32位
add a1, a2, a5 # 高32位加进位
```


## 获取pc

```
auipc a2, 0
```

`x86` 上获取的方法

```
_start:
	call next_ins
next_ins:
	pop %rax # 获取当前pc 到rax 中
```

当时不知道在哪里看到这种代码，直接傻眼了。就不能有条指令直接获取PC吗？
不过，这不就是组合使用基础指令来获取特定功能的指令吗？不就和risc-v 的伪指令差不多吗？
当然性能上可能有差距。

