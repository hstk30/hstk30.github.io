# 垃圾回收机制


## 理论知识

垃圾收集器(garbage collector)将内存视为一张有向可达图(reachability graph)，其形式如下图

![directed-graph](/img/in-post/Python-Source-Code/directed-graph.png)

将节点分为根节点(root node) 和堆节点(heap node)。堆节点对应于在堆中的一个已分配块。有向边`p -> q` 表示`p` 有对`q` 的引用。
根节点持有对堆节点内存块的引用，这些根节点可以是寄存器、栈里的变量，或者是虚拟内存中读写数据区域内的全局变量。

当存在一条从任意根节点出发并到达`p` 的有向路径时，我们说节点`p` 是**可达的(reachable)**。在任何时刻，不可达节点对应于垃圾，
是不能被应用再次使用的。垃圾收集器的角色是维护可达图的某种表示，并通过释放不可达节点且将它们返回给内存管理器(不管是应用的还是系统的)，
来定期地回收它们。

综上，垃圾收集器(只针对**Mark&Sweep(标记&清除)算法**)需要维护一个已分配的内存块的有向图，收集操作由**标记(mark)** 阶段和**清除(sweep)** 阶段组成。

- **标记**阶段：
	- 遍历节点，找出所有根节点
	- 顺着根节点标记出可达的节点。
- **清除**阶段：释放每个未被标记为可达的节点。

## Python 的垃圾回收机制

Python 使用

- 引用计数
- 分代回收(Generational garbage collector)

两种技术来实现垃圾回收

### 引用计数

每个Python 对象都有一个`ob_refcnt` 属性，用来记录引用这个对象的次数，当一个对象的引用被创建或复制时，引用计数加1；当一个对象的引用被销毁时，引用计数减1。
Python 通过以下的两个*宏* 来实现增减引用次数，并在引用次数为零时，调用这个对象的类型对象的析构函数`dealloc` 进行释放。

```
#define Py_INCREF(op) (             \
   (op)->ob_refcnt++)

#define Py_DECREF(op)                   \
   if (--(op)->ob_refcnt != 0)         \
       _Py_CHECK_REFCNT(op)            \
   else                        \
       _Py_Dealloc((PyObject *)(op))
```

这非常简单，但也带来几个问题：

- 每个对象都多了一个`ob_refcnt` 属性来占用内存(小问题)
- 性能与引用计数的变动次数成正比，每次赋值都需要`++` 操作(小问题)，引用次数为0时，对于`List` `Dict` 等对象要遍历所包含的元素，逐个释放（Python 使用了大量内存池机制来弥补）
- 直接导致全局解释锁(GIL, Global Interpreter Lock)，因为当多线程对同一个全局对象进行增减引用次数并不是原子操作，导致`ob_refcnt` 结果不正确。
- 循环引用(大问题，需要解决)

当然，也是有优点的：

- 简单，真的很简单
- 实时，引用计数为0就释放。而不是等到内存不够了或时间片用完了，这个时候内存中有大量的已分配对象需要遍历，往往导致程序短暂的停顿。

### 循环引用

```
In [1]: l1 = []
In [2]: l2 = []
In [3]: l3 = []
In [4]: l1.append(l2)
In [5]: l2.append(l3)
In [6]: l3.append(l1)
```

这样就直接导致循环引用，`l1.ob_refcnt == 1` `l2.ob_refcnt == 1` `l3.ob_refcnt == 1` 而没有其他变量对这3个对象的引用，所以引用计数在这种情况下失效了，因为显然这两个对象是垃圾(garbage)，应该被释放才对。

#### 解决方法

导致这样的主要原因是这3个变量各自的引用计数没有展示出我们希望表现的样子，我们希望这个引用计数应该记录来自外部的引用。
我们希望达到下图的效果：

![remove-ring](/img/in-post/Python-Source-Code/remove-ring.png)

达到这个效果的思路就是：*解铃还须系铃人*。既然计数是因为引用才增加的，那么让它再因引用而减少吧。
图的上面那部分中，本来各自的引用计数都为1，遍历container 对象内的引用，使遍历到的对象的引用计数相应减少1。
因此，最后都变成了0。此时，可以将上面三个变量标记为**不可达的**。

而图的下面那部分中，因为有一个来自外部的引用，因此在经过一轮container 对象内的引用遍历后，上顶角的对象的引用计数为1
(外部的引用在对象内遍历不到)，因此可以暂时把两个底角上的对象标记为**不可达的**，而顶角的对象依旧是**可达的**。

这样我们就将一个有向图中的所有节点分成**可达的** 和**不可达的** 两类。而对于**可达的** 对象，它所引用的对象也应该是**可达的**，
对应图的下半部分中，虽然底角的对象被标记为**不可达的**，但是因为有**可达的** 对象的引用，因此，还需要再遍历一遍**可达的** 对象所引用的对象，将它们都设置为**可达的**。

综上，总结为以下几步：

1. 遍历所有节点，对每个节点，使这个节点所引用对象的引用次数减1
2. 再遍历一遍所有节点，根据节点的引用次数将这些节点分为**可达的** 和**不可达的** 两类

伪代码如下：

```
for node in {n0, n1, n2...}:
    for element in node:
         element.ob_refcnt -= 1
      
for node in {n0, n1, n2...}:
    if node.ob_refcnt == 0 and node not mark reachable:
        mark node as unreachable

    if node.ob_refcnt > 0:
        mark node as reachable
        for element in node:
            mark element as reachable
```

标记阶段结束后，就可以对**不可达的** 对象集合进行清除了，**可达的** 对象保留即可。


### 分代回收(Generational garbage collector)

> Given a realistic amount of memory, efficiency of simple copying garbage collection is limited by the fact that the system must copy all live data at a collection. In most programs in variety of languages, most objects live a very short time, while a small percentage of then live much longer. While figures vary from language to language and program to program,usually between 80 and 98 precent of all newly-allocated heap objects die within a few million instructions, or before another megabyte has been allocated; the majority of objects die even more quickly, within tens of kilobytes of allocation.

上面是说：大多数对象的寿命都很短，只有一小部分的对象寿命比较长，通常在所有新分配的对象中，有80%到98%在几百万条指令内就死亡(成为垃圾)了。
这也是很直观的，在函数调用中，除了出、入参数外，大部分的局部变量、临时变量都可以在这次调用后被销毁、回收。
而那些在主函数中声明的变量、全局变量的生命周期往往和程序相同。

分代回收机制正是基于上面的事实。其总体思想是：将系统中的所有内存块根据其存活时间划分为不同的集合，每一个集合称为一个“代”，
垃圾回收的频率随着“代”的存活时间的增大而减小，也就是说，活得越长的对象，就越不可能是垃圾，就应该越少去收集。


## 源码分析

### 维护一个有向图

无非就是链表、双向链表或者树的结构，Python 实现中使用的双向链表。

```
 typedef union _gc_head {
     struct {
         union _gc_head *gc_next;
         union _gc_head *gc_prev;
         Py_ssize_t gc_refs;
     } gc;
     long double dummy;  /* force worst-case alignment */
 } PyGC_Head;
```

因为这个机制是只针对循环引用的，而循环引用只发生在**container** 容器对象，如`List` `Dict` `class`等中，而`int` `str` 等对象是不可能发生循环引用的。
因此，上面结构只需要给container对象加上即可。如图：

![gc-object](/img/in-post/Python-Source-Code/gc-object.png)

在原来的基础上带了个`gc head` 的*帽子*，表示这是一个需要gc 监控的container 对象。

在创建每个container 对象时，Python 使用`PyObject_GC_New`，而创建非container 对象时则使用`PyObject_Malloc`。

```
PyObject *
_PyObject_GC_Malloc(size_t basicsize)
{
 PyObject *op;
 PyGC_Head *g = (PyGC_Head *)PyObject_MALLOC(sizeof(PyGC_Head) + basicsize);
 g->gc.gc_refs = GC_UNTRACKED;
 ...
 return op;
}

PyObject *
_PyObject_GC_New(PyTypeObject *tp)
{
 PyObject *op = _PyObject_GC_Malloc(_PyObject_SIZE(tp));
 if (op != NULL)
     op = PyObject_INIT(op, tp);
 return op;
}
```

`PyObject_GC_New` 只是调用`PyObject_Malloc` 多分配一个`PyGC_Head` 结构大小的内存。

```
 /* Get an object's GC head */
 #define AS_GC(o) ((PyGC_Head *)(o)-1)  

 /* Get the object given the GC head */
 #define FROM_GC(g) ((PyObject *)(((PyGC_Head *)g)+1))
```

这两个*宏* 通过加减一个`PyGC_Head` 结构大小来实现`PyObject` 和`PyGC_Head` 之间的切换。

```
struct gc_generation {
 PyGC_Head head;
 int threshold; /* 这一“代”的最大阈值，当count >= threshold 时就对这“代”进行垃圾回收 */
 int count; /* 对于第0代而言，count 表示进行分配的次数,而对于更高的代来说,表示的是在这代上进行collect(i) 的次数 */
};

#define NUM_GENERATIONS 3
#define GEN_HEAD(n) (&generations[n].head)

static struct gc_generation generations[NUM_GENERATIONS] = {
 {{{GEN_HEAD(0), GEN_HEAD(0), 0}},   700,        0},  /* 称为“青生代” */
 {{{GEN_HEAD(1), GEN_HEAD(1), 0}},   10,     0},  /* 称为“中生代” */
 {{{GEN_HEAD(2), GEN_HEAD(2), 0}},   10,     0},  /* 称为“老生代” */
};

PyGC_Head *_PyGC_generation0 = GEN_HEAD(0);
```

这就是“有向图”的结构，也是其称为分代回收的原因。从上面代码上可以看出它分为3代。每一代都是一个双向链表的结构。
它的初始状态，如图：

![generator-init](/img/in-post/Python-Source-Code/generator-init.png)

```
/* 简单的双向列表操作，将对象`o` 加入到`_PyGC_generation0` “青生代”中*/
 #define _PyObject_GC_TRACK(o) do { \
     PyGC_Head *g = _Py_AS_GC(o); \
     g->gc.gc_refs = _PyGC_REFS_REACHABLE; \
     g->gc.gc_next = _PyGC_generation0; \
     g->gc.gc_prev = _PyGC_generation0->gc.gc_prev; \
     g->gc.gc_prev->gc.gc_next = g; \
     _PyGC_generation0->gc.gc_prev = g; \
     } while (0);
```

加入若干container 对象后，“有向图”可能长这样：

![generator-grow](/img/in-post/Python-Source-Code/generator-grow.png)

随着不断的创建container 对象，

```
 PyObject *
_PyObject_GC_Malloc(size_t basicsize)
{
 PyObject *op;
 PyGC_Head *g = (PyGC_Head *)PyObject_MALLOC(sizeof(PyGC_Head) + basicsize);
 g->gc.gc_refs = GC_UNTRACKED;
 generations[0].count++; /* number of allocated GC objects */
 if (generations[0].count > generations[0].threshold &&
     enabled &&
     generations[0].threshold &&
     !collecting &&
     !PyErr_Occurred()) {
     collecting = 1;
     collect_generations();  /* 进行垃圾回收 */
     collecting = 0;
 }
 op = FROM_GC(g);
 return op;
}
```

可以看到，当`generations[0].count > generations[0].threshold` 的时候，就调用`collect_generations()`进行垃圾回收。


### 标记阶段

```
static Py_ssize_t
collect_generations(void)
{
 int i;
 Py_ssize_t n = 0;
 /* 从最老的“代”开始重新判断要从哪个代开始回收 */
 for (i = NUM_GENERATIONS-1; i >= 0; i--) {
     if (generations[i].count > generations[i].threshold) {
         n = collect(i);
         break;
     }
 }
 return n;
}
```

上面的函数找出满足count 值越界的最“老”的那一“代”，对这“代”进行收集(`collect`)操作。


下面的函数即是垃圾回收的主函数。

```
static Py_ssize_t
collect(int generation)
{
	int i;
	PyGC_Head *young; /* the generation we are examining */
	PyGC_Head *old; /* next older generation */
	PyGC_Head unreachable; /* non-problematic unreachable trash */
	PyGC_Head *gc;
			
	/* update collection and allocation counters */
	/* 这里的count 记录的并不是在这个“代”的双向链表中链接了多少个对象(这通过gc_list_size得到)，
	* 而是这个“代”经历了多少次的分配，而对于第0“代”而言，这个count*/
		
	/* (700, 10, 10) 意味着每进行700次的分配就进行一次collect(0) 使得第一代的count+=1,
	* 每进行700*10 次分配就进行一次collect(1)使得第二代的count+=1
	* 每进行700*10*10 次分配进行一次collect(2)，将所有代的重新置零*/
	if (generation+1 < NUM_GENERATIONS)
	    generations[generation+1].count += 1;
	for (i = 0; i <= generation; i++)
	    generations[i].count = 0;
		
	/* merge younger generations with one we are currently collecting */
	for (i = 0; i < generation; i++) {
	    gc_list_merge(GEN_HEAD(i), GEN_HEAD(generation));
	}
		
	/* handy references */
	young = GEN_HEAD(generation);
	if (generation < NUM_GENERATIONS-1)
	    old = GEN_HEAD(generation+1);
	else
	    old = young;
	...
	delete_garbage(&unreachable, old);
	...
}
```



源码文件：

- `Include/object.h`
- `Include/objimpl.h`
- `Modules/gcmodule.c`

[Garbage Collection for Python](http://www.arctrix.com/nas/python/gc/)