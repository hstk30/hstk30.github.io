---
layout:     post
title:      "Python对象机制基石——PyObject"
date:       2021-07-03
author:     "hstk30"
header-img: "img/meet.jpg"
description: "不识庐山真面目，只缘身在此山中。"
tags:
    - Python
---

# Python 对象机制基石


![object-h-struct](/img/in-post/Python-Source-Code/object-h-struct.png)    

上图是`Include/object.h` ，也是整个**cPython** 中的最重要的结构体和它们的关系。

**note**： 这个图并不是*UML* 中的类图哦，只是用来表示这些结构体之间的关系，毕竟**c语言** 中并没有什么对象。箭头表示*引用* 或*依赖* 关系。


## PyObject 和PyVarObject

可以看到`PyObject` 只有两个字段（下面我们称名为`Py{type}Object` 的结构体为`{type}对象`）：  
- `ob_refcnt`： 引用计数字段，众所周知，Python的垃圾回收机制主要就是引用计数，因此，这个字段是所有的对象都有的。  
- `ob_type`: 指明该对象是什么*类型* 的，这里指向的是一个*Type对象* 。  

而`PyVarObject` 只比`PyObject` 多一个`ob_size` 字段，用来指明这个*Var(变长)对象* 的长度。

不只是`PyVarObject`， Python 中的所有对象都是对`PyObject` 的一个扩展。换句话说，在Python 内部，每一个对象都拥有相同的对象头部，这就使得对对象的引用变得非常的统一，我们只需要用一个 `PyObject *` 指针就可以引用任意一个对象，而不论该对象实际是什么对象。

用面向对象的角度看，就是说`PyObject` 是Python 中所有对象的基类。

## 类型对象 PyTypeObject

`PyObject` 中的`ob_type` 字段指向`PyTypeObject`, 这个`PyTypeObject` 就是用来指明这个对象到底是用来干什么的，这个结构体里包含一个初始化对象、分配内存大小的信息：`tp_basicsize, tp_itemsize`， 和一堆函数指针表明该对象相应的操作。  
就像：

```Python
In [1]: dir(type)
Out[1]:
['__abstractmethods__', '__base__', '__bases__', '__basicsize__', '__call__', '__class__', '__delattr__', '__dict__', '__dictoffset__', '__dir__', '__doc__', '__eq__', '__flags__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__instancecheck__', '__itemsize__', '__le__', '__lt__', '__module__', '__mro__', '__name__', '__ne__', '__new__', '__prepare__', '__qualname__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasscheck__', '__subclasses__', '__subclasshook__', '__text_signature__', '__weakrefoffset__', 'mro']
```

不出意外，这个`PyTypeObject` 也是一个对象。所以这个*类型对象* 也应该有它的*类型* ，这就是图上`PyTypeObjecct` 自己指向自己的原因：*类型对象* 的*类型* 是它自己（嗯，套娃了）。 

就像：

```
In [2]: class A(object):
   ...:     pass
   ...:

In [3]: A.__class__
Out[3]: type

In [4]: type.__class__
Out[4]: type

In [5]: int.__class__
Out[5]: type
```

## 对象的表现行为 Py{type}Methods

`PyNumberMethods`，`PySequenceMethods`，`PyMappingMethods` 这三个结构体就像面向对象里的*接口* 或者是*重载操作符*。例如，你为某个对象实现了`PyNumberMethods` 的`nb_add` 方法（其他方法默认），那么这个对象就能表现的像*数值对象*，尤其在遇到`+` 操作符时，就会调用你实现的`nb_add` 方法。


## 总结

上面就是Python 对象机制的结构，知道了上面这些，就可以去看`Include` 和 `Objects` 下的具体内建类型的代码了。这些内建类型代码遵循固定的结构：  
1. 在`Include/{type}object.h` 下定义相应的`Py{type}Object`。  
2. 在`Object/{type}object.c` 下实现这个对象支持的操作，用这些函数初始化这个对象的*类型对象*, 和这个对象的表现行为。 
