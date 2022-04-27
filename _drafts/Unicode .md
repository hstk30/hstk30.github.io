# Unicode 


bytes.decode -> str 将存在文件里的二进制byte **解码** 为我们能看的文本

str.encode -> bytes 将我们能看的文本**编码** 为存在文件中的二进制byte

`utf-8` 与字节顺序无关。

最常见的错误

```
In [1]: b'\x80'.decode('utf-8')
---------------------------------------------------------------------------
UnicodeDecodeError                        Traceback (most recent call last)
Input In [15], in <cell line: 1>()
----> 1 b'\x80'.decode('utf-8')

UnicodeDecodeError: 'utf-8' codec can't decode byte 0x80 in position 0: invalid start byte
```

即根据`utf-8` 算法，不能将`0x80` 转换为一个Unicode 中的码位。

```
In [2]: '\x80'.encode()
Out[2]: b'\xc2\x80'
In [3]: bin(0xc280)
Out[3]: '0b1100001010000000'
```

`0b1100, 0010, 1000, 0000` 根据`utf-8` 算法，就能转换为对应的Unicode的码位（Code Point）`0x80`

| 字节数 |  Unicode  | UTF-8编码 |
|:-------------:|:---------------:|:-------------|
| 1 | 000000-00007F | 0xxxxxxx |
| 2 | 000080-0007FF | 110xxxxx 10xxxxxx |
| 3 | 000800-00FFFF | 1110xxxx 10xxxxxx 10xxxxxx  |
| 4 | 010000-10FFFF  | 11110xxx 10xxxxxx 10xxxxxx 10xxxxxx |



- Python3 字符串使用utf-8，但是`utf-8` 表示不同码位的长度是不一样的，所以s[x] 还是O(1) 的复杂度吗？

```
In [1]: '\x80'
Out[1]: '\x80'

In [2]: '\x80'.encode()
Out[2]: b'\xc2\x80'

In [3]: len('\x80'.encode())
Out[3]: 2

In [4]: ? len
Signature:  len(obj, /)
Docstring: Return the number of items in a container.
Type:      builtin_function_or_method

In [5]: len('\x80')
Out[5]: 1
```


布隆过滤器：可以判断一个元素是否在一个集合中，对于不在是肯定的，对于在需要进一步判断。


[细说：Unicode, UTF-8, UTF-16, UTF-32, UCS-2, UCS-4](https://www.cnblogs.com/malecrab/p/5300503.html)
