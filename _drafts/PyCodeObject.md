# PyCodeObject


```C
typedef struct {
    PyObject_HEAD
    int co_argcount;		/* Code Block 位置参数的个数 */
    int co_nlocals;		/* Code Block 中局部变量的个数，包括其位置参数的个数 */
    int co_stacksize;		/* 执行该段Code Block 需要的栈空间 */
    int co_flags;		/* CO_..., see below */
    PyObject *co_code;		/* Code Block 编译所得的字节码指令序列，PyStringObject */
    PyObject *co_consts;	/* 保存Code Block 中的所有常量，PyTupleObject */
    PyObject *co_names;		/* 保存Code Block 中的所有符号，PyTupleObject */
    PyObject *co_varnames;	/* Code Block 中局部变量名集合，PyTupleObject */
    PyObject *co_freevars;	/* 实现闭包需要用到的东西，PyTupleObject */
    PyObject *co_cellvars;      /* Code Block 中内部嵌套函数所引用的局部变量名集合 */
    /* The rest doesn't count for hash/cmp */
    PyObject *co_filename;	/* string (where it was loaded from) */
    PyObject *co_name;		/* string (name, for reference) */
    int co_firstlineno;		/* first source line number */
    PyObject *co_lnotab;	/* string (encoding addr<->lineno mapping) */
    void *co_zombieframe;     /* for optimization only (see frameobject.c) */
} PyCodeObject;
```

```
source = open('Dict.py').read()
co = compile(source, 'Dict.py', 'exec')
type(co)
co
dir(co)
co.co_argcount
co.co_cellvars
co.co_code
co.co_consts
co.co_filename
co.co_name
co.co_names
co.co_freevars
co.co_lnotab
co.co_stacksize
co.co_nlocals
```
