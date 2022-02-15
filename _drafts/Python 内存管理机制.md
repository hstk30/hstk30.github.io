# Python 内存管理机制

Python 内存管理结构总览

![pymalloc-layout](/img/in-post/Python-Source-Code/pymalloc-layout.png)    

源码文件：`Object/obmalloc.c`

## Pool 管理

![pool-layout](/img/in-post/Python-Source-Code/pool-layout.png)    

```
typedef uchar block;  
 
struct pool_header {
	union { block *_padding;
	 uint count; } ref;  /* number of allocated blocks    */
	block *freeblock;       /* pool's free list head         */
	struct pool_header *nextpool;   /* next pool of this size class  */
	struct pool_header *prevpool;   /* previous pool       ""        */
	uint arenaindex;        /* index into arenas of base adr */
	uint szidx;         /* block size class index    */
	uint nextoffset;        /* bytes to virgin block     */
	uint maxnextoffset;     /* largest valid nextoffset  */
};
```

### 三种状态

- **可用的**(used) : 至少分配了一个`block`，并且至少还有一个`block` 没有被分配。一个`pool` 中的`block size` 相同。这些相同`size i` 的`pool` 被链接在
	`双向循环链表usedpool[i + i]` 上。如果一个`pool` 中所有的`block` 都被分配了，这个`pool` 进入**full** 状态。如果一个`pool` 中所有的`block` 都被释放
	则进入**empty** 状态。
- **满的**(full)：所有的`block` 都被分配了。当一个`pool` 进入**full** 状态，则从`usedpool[i + i]` 链表中删除这个`pool`。当其中有`block` 被释放时，重新
	链接进`usedpool[i +i]` ，即`block size` 不变。
- **空的**(empty)： 所有的`block` 都是可分配的。当一个`pool` 进入**empty** 状态，则从`usedpool[i + i]` 链表中删除这个`pool`，并且链接到
	`单向链表arena_object->freepools` 中。当一个内存申请发现对应`size i` 的`usedpool[i + i]` 是空的，则从`arena_object_freepools` 中取出第一个
	`pool`，并且将这个`pool` 初始化为对应`block size` 的。如果之前这个`pool` 就是这个`block size` 的，就可以跳过这个初始化。

## Block 管理

`单向链表pool_header->freeblock` 指向`pool` 中空闲的`block`。`pool` 的`blocks` 在一开始只是一坨未初始化的内存，并没有链接在一起。在未进行释放前，这个`pool` 的`block` 分配简单的通过:

```
bp = pool_header->freeblock;
pool_header->freeblock = (block *)pool + pool->nextoffset;  \\将freeblock 指向nextoffset
pool_header->nextoffset += block size;  \\ 将nextoffset 增加一个block size
return bp;
```

直到`nextoffset > maxnextoffset`。

而当一个`block` 被释放，这个`block` 被插入到`poolheader->freeblock` 的表头。此时，再申请内存，则从`freeblock` 中取走表头的`block` 即可。


## Arena 管理 

![arena-layout](/img/in-post/Python-Source-Code/arena-layout.png)    


```
struct arena_object {
 /* The address of the arena, as returned by malloc.  Note that 0
  * will never be returned by a successful malloc, and is used
  * here to mark an arena_object that doesn't correspond to an
  * allocated arena.
  */
	uptr address;
	
	/* Pool-aligned pointer to the next pool to be carved off. */
	block* pool_address;
	
	/* The number of available pools in the arena:  free pools + never-
	* allocated pools.
	*/
	uint nfreepools;
	
	/* The total number of pools in the arena, whether or not available. */
	uint ntotalpools;
	
	/* Singly-linked list of available pools. */
	struct pool_header* freepools;
	
	struct arena_object* nextarena;
	struct arena_object* prevarena;
};
```


```
static struct arena_object* arenas = NULL;  // 简单的arena_object 的动态数组
static struct arena_object* unused_arena_objects = NULL;  // 单向链表，链接还没有被真正分配内存的`arena`，即`.address == 0` 

/*
	双向链表，链接有`pool` 可用的`arena`。这条链按`.nfreepool` 的升序排列，使得下一次分配都从
	`.nfreepools` 最小的`arena` 进行分配。从而当用有内存释放时，使得`.nfreepools` 大的`arena` 有机会
	进入`empty`，即`arena` 中的`pool` 都为`empty`，从而使得这个`arena` 的内存可以释放回系统内存。
*/  
static struct arena_object* usable_arenas = NULL;
```


## 可用pool 缓存池--usedpools

```
#define PTA(x)  ((poolp )((uchar *)&(usedpools[2*(x)]) - 2*sizeof(block *)))
#define PT(x)   PTA(x), PTA(x)

static poolp usedpools[2 * ((NB_SMALL_SIZE_CLASSES + 7) / 8) * 8] = {
 PT(0), PT(1), PT(2), PT(3), PT(4), PT(5), PT(6), PT(7)
 , PT(8), PT(9), PT(10), PT(11), PT(12), PT(13), PT(14), PT(15)
 , PT(16), PT(17), PT(18), PT(19), PT(20), PT(21), PT(22), PT(23)
 , PT(24), PT(25), PT(26), PT(27), PT(28), PT(29), PT(30), PT(31)
 , PT(32), PT(33), PT(34), PT(35), PT(36), PT(37), PT(38), PT(39)
 , PT(40), PT(41), PT(42), PT(43), PT(44), PT(45), PT(46), PT(47)
 , PT(48), PT(49), PT(50), PT(51), PT(52), PT(53), PT(54), PT(55)
 , PT(56), PT(57), PT(58), PT(59), PT(60), PT(61), PT(62), PT(63)
};
```






[Improving Python's Memory Allocator](https://www.evanjones.ca/memoryallocator/)