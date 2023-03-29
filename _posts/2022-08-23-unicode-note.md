---
layout:     post
title:      "Unicode 中遇到的一些问题和一些必知必会"
date:       2022-08-28
header-img: "img/confuse.png"
author:     "hstk30"
description: "死去元知万事空，但悲不见九州同。"
tags:
    - Python
    - Unicode
---


# Unicode 一些知识和遇到的错误

bytes.decode -> str 将存在文件里的二进制byte **解码** 为我们能看的文本

str.encode -> bytes 将我们能看的文本 **编码** 为存在文件中的二进制byte

`utf-8` 与字节顺序无关。

大概有1.1M 码点（code point），也就是说大概21位就可以表示所有的码点，
Unicode 编码的字符一般以`wchar_t` 类型存储，`wchar_t` 一般实现为32位。


## 最常见的错误

```
In [1]: b'\x80'.decode('utf-8')
---------------------------------------------------------------------------
UnicodeDecodeError                        Traceback (most recent call last)
Input In [15], in <cell line: 1>()
----> 1 b'\x80'.decode('utf-8')

UnicodeDecodeError: 'utf-8' codec can't decode byte 0x80 in position 0: invalid start byte
```

即根据`utf-8` 算法，不能将`0x80` 转换为一个Unicode 中的码点。

```
In [2]: '\x80'.encode()
Out[2]: b'\xc2\x80'
In [3]: bin(0xc280)
Out[3]: '0b1100001010000000'
```

`0b1100, 0010, 1000, 0000` 根据`utf-8` 算法，就能转换为对应的Unicode的码点`0x80`

| 字节数 |  Unicode  | UTF-8编码 |
|:-------------:|:---------------:|:-------------|
| 1 | 000000-00007F | 0xxxxxxx |
| 2 | 000080-0007FF | 110xxxxx 10xxxxxx |
| 3 | 000800-00FFFF | 1110xxxx 10xxxxxx 10xxxxxx  |
| 4 | 010000-10FFFF  | 11110xxx 10xxxxxx 10xxxxxx 10xxxxxx |


## 冷知识

###  某些字符能够用多个合法的编码表示

在Unicode中，某些字符能够用多个合法的编码表示。比如
[Python CookBook normalize_unicode](https://python3-cookbook.readthedocs.io/zh_CN/latest/c02/p09_normalize_unicode_text_to_regexp.html)

里提到的例子:

```
In [1]: s1 = 'Spicy Jalape\u00f1o'

In [2]: s2 = 'Spicy Jalapen\u0303o'

In [3]: s1
Out[3]: 'Spicy Jalapeño'

In [4]: s2
Out[4]: 'Spicy Jalapeño'

In [5]: s1 == s2
Out[5]: False

In [6]: len(s1)
Out[6]: 14

In [7]: len(s2)
Out[7]: 15
```

[unicode 组合字符](https://zh.wikipedia.org/zh-cn/%E7%B5%84%E5%90%88%E5%AD%97%E7%AC%A6)


### 大小写转换后字符串长度会改变

[The Unicode® Standard Version 14.0 – Core Specification](https://www.unicode.org/versions/Unicode14.0.0/ch05.pdf)

`5.18 Case Mappings` 中的`Complications for Case Mapping`, 就讲到了`Change in Length`.

虽然
[Python Doc: str.lower()](https://docs.python.org/3.6/library/stdtypes.html#str.lower) 
中确实提到了`lowercasing algorithm`，但是谁能想到一个简简单单的`大小写转换` 居然还会改变长度!


```
In [1]: s = 'İ'

In [2]: s
Out[2]: 'İ'

In [3]: len(s)
Out[3]: 1

In [4]: s.lower()
Out[4]: 'i̇'

In [5]: len(s.lower())
Out[5]: 2
```

```
In [2]: s = '\u0390'

In [3]: s
Out[3]: 'ΐ'

In [4]: len(s)
Out[4]: 1

In [5]: s.upper()
Out[5]: 'Ϊ́'

In [6]: len(s.upper())
Out[6]: 3
```

我对`大小写转换` 的算法还停留在`c语言` 里的 


```c
char l_letter = u_letter + 'a' - 'A';
```

不过这样反而能满足中文NLP 的需要。


## 参考

- [Must Know About Unicode and Character Sets](https://www.joelonsoftware.com/2003/10/08/the-absolute-minimum-every-software-developer-absolutely-positively-must-know-about-unicode-and-character-sets-no-excuses/)
- [Pragmatic Unicode](https://nedbatchelder.com/text/unipain.html)
- [stackoverflow unicode-lowercase](https://stackoverflow.com/questions/3522387/what-is-the-standard-algorithm-for-converting-unicode-characters-into-lowercase)
- [Python CookBook normalize_unicode](https://python3-cookbook.readthedocs.io/zh_CN/latest/c02/p09_normalize_unicode_text_to_regexp.html)

