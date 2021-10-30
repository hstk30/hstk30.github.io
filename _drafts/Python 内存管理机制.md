# Python 内存管理机制


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
 
/* Array of objects used to track chunks of memory (arenas). */
static struct arena_object* arenas = NULL;
/* The head of the singly-linked, NULL-terminated list of available
* arena_objects.
*/
static struct arena_object* unused_arena_objects = NULL;
 
/* The head of the doubly-linked, NULL-terminated at each end, list of
* arena_objects associated with arenas that have pools available.
*/
static struct arena_object* usable_arenas = NULL;
 
```




[Improving Python's Memory Allocator](https://www.evanjones.ca/memoryallocator/)