---
layout:     post
title:      "Fluent Python 小记"
date:       2018-10-31
author:     "hstk30"
tags:
    - Python
---

忘了是什么时候写下的`note`了， 先放在这里凑个数吧。


## 目录
{: .no_toc}

* 目录
{:toc}

# 2 序列

## 2.5 对序列使用+和*

- +和*不修改原来的操作对象，而是构建一个全新的序列。
- 如果a*n中，序列a里的元素是对其他可变对象的引用的话，需要格外注意

```python
a = [1, 2, 3]
aa = [a] * 3  # aa = [[1, 2, 3], [1, 2, 3], [1, 2, 3]]
a[1] = 3
aa
>>> [[1, 3, 3], [1, 3, 3], [1, 3, 3]]

```

## 关于+=的谜题

```python
t = (1, 2, [30, 40])
t[2] += [50, 60]
```
- 猜想执行的结果。  
- 查看`s[a] += b` 的`Python` 字节码。
- 不要把可变对象放在元组中。
- 增量赋值不是原子操作。

## 数组array.array

- 数据背后存的并不是float对象， 而是数字的机器翻译，即字节表示

```python
from array import array
from random import random
floats = array('d', (random() for i in range(10**7)))  # 'd'=>double, 'b'=>signed char
fp = open('float.bin', 'wb')
floats.tofile(fp)
fp.close()
floats2 = array('d')
fp = open('float.bin', 'rb')
floats2.fromfile(fp, 10**7)
fp.close()
floats == floats2
>>> True
```

## memoryview内存视图

像操作c语言数据那样操作python数据

## struct Format Characters

 Format 	| C Type 	    | Python type	| Standard size |
----------|-------------|---------------|---------------|
x			| pad byte    | no value      |               |  
c			| char		    | bytes of length 1 | 1         |  
b			| signed char	 | integer       | 1             |  
B			| unsigned char | integer     |    1          |
?	       | _Bool	    |   bool	       | 1             |
h	       | short	    | integer       | 2             |
H         | unsigned short	| integer	   | 2             |
i         | int         | integer      | 4              |
I         | unsigned int |	integer | 4 |
l | long | integer | 4 |
L | unsigned long | integer | 4 |
q | long long | integer | 8 |
Q | unsigned long long | integer | 8 |
n | ssize_t | integer | 
N | size_t | integer |
e |  | float | 2 |
f | float | float | 4 |
d | double | float | 8 |
s | char[] | bytes |
p | char[] | bytes |
P | void * | integer |

# 4.文本和字节序列

## 字符、码位、字节

Unicode标准把字符的标识和具体的字节表述进行了如下的明确区分:


- 字符的标识，即码位，是0~1，114，111的数字（十进制），在Unicode标准中以4~6个十六进制数字标识，而且加前缀“U+”。例如，字母A的码位是U+0041，欧元符号的码位是U+20AC，高音谱号的码位是U+1D11E。在Unicode6.3中（这是python3.4使用的标准），约10%的有效码位有对应的字符。
- 字符的具体表述取决于所用的编码。编码是在码位和字节序列之间转换时使用的算法。在UTF-8编码中，A（U+0041）的码位编码成单个字节\x41，为在UTF-16LE编码中编码成两个字节\x41\x00。再举个例子，欧元符号（U+20AC）在UTF-8编码中是三个字节--\xe2\x82\xac，而在UTF-16LE中编码成两个字节：\xac\x20。

把码位转换为字节序列的过程是编码；把字节序列转换成码位的过程是解码。

```python
s = 'café'  
len(s)
>>> 4
b = s.encode('utf8')
b
>>> b'caf\xc3\xa9'  # 字节序列
len(b)
>>> 5
b.decode('utf8')
>>> café
```

# 特殊方法

- 使用`__setitem__`方法支持`v[0] = 1.1`这样的赋值
- 使用`__setattr__`方法支持`v.x = 1.1`这样的赋值
- `__hash__`建议使用`^`（异或）运算符计算对象各属性的散列值，like`v[0] ^ v[1]`
- 序列协议要求实现`__len__`和`__getitem__`方法
- 标准的迭代器接口有两个方法，`__next__`和`__iter__`。
- 可迭代的对象一定不能是自身的迭代器。也就是说，可迭代的对象必须实现`__iter__`方法，但不能实现`__next__`方法。
- 可迭代对象和迭代器之间的区别：Python从可迭代的对象中获取迭代器。
- 构建*可迭代的对象*和*迭代器*时经常会出现错误，原因是混淆了两者。要知道，可迭代的对象有个`__iter__`方法，每次都实例化一个新的*迭代器*；而迭代器要实现`__next__`方法，返回单个元素，此外还要实现`__iter__`方法，返回迭代器本身。



# 可迭代对象和迭代器实例

```python
import re
import reprlib

RE_WORD = re.compile('\w+')

class Sentence:
	"""Sentence是一个可迭代对象，因为实现了__iter__方法,
	但是不是一个迭代器，因为没有实现__next__方法
	"""
	def __init__(self, text):
		self.text = text
		self.words = RE_WORD.findall(text)
	
	def __repr__(self):
		pass
	
	def __iter__(self):
		"""返回一个迭代器，
		"""
		return iter(self.words)
```


# 处理多重继承

1. 把接口继承和实现继承分开  
	使用多重继承时，一定要明确一开始为什么创建子类
	- 继承接口，创建子类型，实现“是什么”关系
	- 继承实现，通过重用避免代码重复

	其实这两条经常同时出现，不过只要可能，一定要明确意图，通过继承重用代码是实现细节，通过可以换用组合和委托模式。而接口继承则是框架的支柱。
2. 通过mixin重用代码
	如果一个类的作用是为多个不相关的子类提供方法实现，从而实现重用，但不体现“是什么”关系，应该把那个类明确地定义为混入类（mixin class）。从概念上讲，混入不定义新类型，只是打包方法，便于重用。混入类绝对不能实例化，而且具体类不能只继承混入类。混入类应该提供某方面的特定行为，只实现少量关系密切的方法。
3. 在名称中明确指明混入，加入后缀Mixin
4. 不要子类化多个具体类
	具体类可以没有，或最多只有一个具体超类。也就是说，具体类的超类中除了这一个具体超类之外，其余的都是抽象基类或混入。如下，Alpha为一个具体类，Beta和Gamma为抽象基类或混入。
	
	```python
	class MyConcreteClass(Alpha, Beta, Gamma):
		"""这个一个具体类，可以实例化"""
		# 更多代码
	```
5. 为用户提供聚合类
	如果抽象基类或混入的组合对客户代码非常有用，那就提供一个类，使用易于理解的方式把它们组合起来。Grady Booch把这种类称为聚合类（aggregate class）。
	
	```Python
	class Widget(BaseWidget, Pack, Place, Grid):
		"""Internal class
		
		Base class for widget which can be positioned with the
		geometry managers Pack, Place or Grid.
		"""
		pass
		
	```
6. 优先使用对象组合，而不是类继承

# 重载运算符

- 实现一元运算符和中缀运算符的特殊方法一定不能修改操作数。使用这些运算符的表达式期待结果是新的对象。增量赋值表达式除外。

## 中缀运算符的特殊分派机制

对表达式`a+b`而言，解释器会执行以下几步操作。


1. 如果a有`__add__`方法，而且返回值不是`NotImplemented`，调用`a.__add__(b)`，然后返回结果
2. 如果a没有`__add__`方法，或者调用`__add__`方法返回`NotImplemented`，检查b有没有`__radd__`方法，如果有，而且没有返回`NotImplemented`，调用`b.__radd__(a)`，然后返回结果
3. 如果都没有，则抛出`TypeError`

##  比较运算符

- 正向和反向调用使用的是同一系列方法
- 对`==`和`！=`来说，如果反向调用失败，Python会比较对象的ID，而不抛出`TypeError`

# 注意点

- 别把`NotImplemented`和`NotImplementedError`搞混。前者是特殊的单例值，如果中缀运算符特殊方法不能处理给定的操作数，那么要把它返回给解释器。而`NotImplementedError`是一种异常，抽象类中的占位方法把它抛出，提醒子类必须覆盖。

# 词汇表

- *EAFP*
	取得原谅比获得许可容易（easier to ask for forgiveness than permission)。这是一种常见的Python编程风格，先假定存在有效的键或属性，如果假定不成立，那么捕获异常。这种风格简单明快，特点是代码中有很多try和except语句。与其他语言一样（如C语言），这种风格的对立面是LBYL风格。
- *LBYL*
	三思而后行（look before you leap)。这种编程风格在调用函数或查找属性或键之前显示测试前提条件。与EAFP风格相反，这种风格的特点是代码中有很多的if语句。在多线程环境中，LBYL风格可能会在“检查”和“行事”的空当引入条件竞争。例如，对`if key in mapping: return mapping[key]`这段代码来说，如果在测试之后，但在查找之前，另一个线程从映射中删除了那个键，那么这段代码就会失败。这个问题可以使用锁或者EAFP风格解决。
- 

# 并发和并行

- 并发是指一次处理多件事（concurrency）
- 并行是指一次做多件事(parallelism)

真正的并行需要多个核心。现代的笔记本电脑有4个CPU核心，但是经常不经意间就有超过100个进程同时运行。因此，实际上大多数过程都是并发处理的，而不是并行处理。计算机始终运行着100多个进程，确保每个进程都有机会取得进展，不过CPU本身同时做的事情不能超过四件。十年前使用的设备也能并发处理100个进程，不过都在同一核心里。
