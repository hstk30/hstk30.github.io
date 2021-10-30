---
layout:     post
title:      "抛砖引玉--unittest 编写举例"
date:       2021-10-30
header-img:	"img/accompany-2.jpeg"
author:     "hstk30"
tags:
    - 单元测试
---


## 需求说明
说，有一个需求：

- *输入*:  一个字符串，存在各种特殊字符
- *输出*:  
	1. 一个字符串：过滤掉了输入字符串里面的`http url`、`不可打印字符`（就用[str.isprintable](https://docs.python.org/zh-cn/3.6/library/stdtypes.html#str.isprintable)来判断就行），将剩下的文本重新拼接成一个字符串，并去掉两头的空格(`str.strip` 即可) ，
	2. 一个字典，记录返回的这个字符串中每个字符的位置和输入字符串中对应字符位置的映射关系

note: 现在已经有一个方法可以从一个字符串中提取出不同类型的字符串，如

```
class Entity:
    def __init__(self, content, category='NormalText' , start_idx=-1, end_idx=-1):
        self.content = content
        self.category = category
        self.start_idx = start_idx
        self.end_idx = end_idx

def extract_entity(input_str) -> List[Entity] :
	pass
```

所以，只需要关注`category='NormalText' ` 的`Entity` 即可。

例：

```
input_str = 'http://example.org  前面有空格，一个空格 ，\001一个不可打印字符'

output_str, pos_map = get_norm_text_and_pos_map(input_str)
assert output_str == '前面有空格，一个空格 ，一个不可打印字符'
assert pos_map == {0: 20, 1: 21, 2: 22, 3: 23, 4: 24, 5: 25, 6: 26, 7: 27, 8: 28, 9: 29, 10: 30, 11: 31, 
				   12: 33, 13: 34, 14: 35, 15: 36, 16: 37, 17: 38, 18: 39, 19: 40}
```
中间缺少的位置32 上的字符`\001` 是个`不可打印字符`，因此去掉。

## coding

#### 第一个unittest

先写一个最简单的单元测试，需要编写对应的函数`get_norm_text_and_pos_map` 来通过这个单元测试。

```
# test_norm_text.py
import unittest

from extract_entity import Entity
from norm_text import get_norm_text_and_pos_map


class TestCase(unittest.TestCase):

    def test_1(self, mock_extract_entity):
        input_str = '一个简单的文本'
        output_str, pos_map = get_norm_text_and_pos_map(input_str)

        self.assertEqual(output_str, '一个简单的文本')
        self.assertEqual(pos_map, {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6})
```

```
# norm_text.py
from extract_entity import extract_entity

def get_norm_text_and_pos_map(input_str):
    char_list = []
    pos_map = {}
    norm_idx = 0

    for entity in extract_entity(input_str):
        if entity.category == 'NormalText':
            for ch in entity.content:
                if ch.isprintable():
                    char_list.append(ch)
                    pos_map[norm_idx] = norm_idx
                    norm_idx += 1

    return ''.join(char_list), pos_map
```

顺利通过。

#### 提前改进下

上面我们并没有给出`extract_entity` 的具体实现，它可能是简单的正则代码，或者是通过一个`http` 去请求的其他服务，又或者是由`nlp` 提取出来的实体。不管怎么说，我们的代码`get_norm_text_and_pos_map` 是`依赖` 于 `extract_entity` 的，所以改进下。
[mock.patch](https://docs.python.org/zh-cn/3.6/library/unittest.mock.html#unittest.mock.patch)

```
# test_norm_text.py
import unittest
from unittest.mock import patch

from extract_entity import Entity
from norm_text import get_norm_text_and_pos_map


class TestCase(unittest.TestCase):

    @patch('norm_text.extract_entity')
    def test_1(self, mock_extract_entity):
        input_str = '一个简单的文本'
        mock_extract_entity.return_value = [Entity(content=input_str, start_idx=0, end_idx=len(input_str))]
        output_str, pos_map = get_norm_text_and_pos_map(input_str)

        self.assertEqual(output_str, '一个简单的文本')
        self.assertEqual(pos_map, {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6})
```

好了，这下我们的这个unittest 不管在哪里都可以跑了，不管是不是断网，有没有`GPU` 资源。

#### 第二个单元测试

前面是最简单的情况，根据需求，直接想到如果有`url` 会怎么样，所以有下面的unitest

```
    @patch('norm_text.extract_entity')
    def test_2(self, mock_extract_entity):
        input_str = 'http://example.org前面有个url链接'
        mock_extract_entity.return_value = [
            Entity(content='http://example.org', category='Url', start_idx=0, end_idx=18),
            Entity(content='前面有个url链接', start_idx=18, end_idx=len(input_str))
        ]
        output_str, pos_map = get_norm_text_and_pos_map(input_str)

        self.assertEqual(output_str, '前面有个url链接')
        self.assertEqual(pos_map, {0: 18, 1: 19, 2: 20, 3: 21, 4: 22, 5: 23, 6: 24, 7: 25, 8: 26})
```

都不用跑就知道可能失败，所以改进下`get_norm_text_and_pos_map` 代码

```
def get_norm_text_and_pos_map(input_str):
    char_list = []
    pos_map = {}
    norm_idx = 0

    for entity in extract_entity(input_str):
        if entity.category == 'NormalText':
            start_idx = entity.start_idx
            for i, ch in enumerate(entity.content):
                if ch.isprintable():
                    char_list.append(ch)
                    pos_map[norm_idx] = start_idx + i
                    norm_idx += 1

    return ''.join(char_list), pos_map
```
跑一下前面两个unittest，都顺利通过。

#### 第三个

那如果有不可打印字符呢

```
    @patch('norm_text.extract_entity')
    def test_3(self, mock_extract_entity):
        input_str = '一个不\001可打印字符'
        mock_extract_entity.return_value = [
            Entity(content='一个不\001可打印字符', start_idx=0, end_idx=len(input_str))
        ]
        output_str, pos_map = get_norm_text_and_pos_map(input_str)

        self.assertEqual(output_str, '一个不可打印字符')
        self.assertEqual(pos_map, {0: 0, 1: 1, 2: 2, 3: 4, 4: 5, 5: 6, 6: 7, 7: 8})
```

因为，我们提前使用`ch.isprintable`，所以这个unittest 顺利通过。

#### 第四个

需求又说，要将去掉两头的空格(`str.strip()`)， 所以，再试下前面有空格的情况

```
    @patch('norm_text.extract_entity')
    def test_4(self, mock_extract_entity):
        input_str = '  前面有空格'
        mock_extract_entity.return_value = [
            Entity(content=input_str, start_idx=0, end_idx=len(input_str))
        ]
        output_str, pos_map = get_norm_text_and_pos_map(input_str)

        self.assertEqual(output_str, '前面有空格')
        self.assertEqual(pos_map, {0: 2, 1: 3, 2: 4, 3: 5, 4: 6})
```

失败，因为，我们根本就没使用`strip()`， 简单的使用`strip()` 如

```
    return ''.join(char_list).strip(), pos_map
```

还是失败，因为句首的空格影响了`pos_map` 的映射，因此，改进下

```
def get_norm_text_and_pos_map(input_str):
    char_list = []
    pos_map = {}
    norm_idx = 0

    for entity in extract_entity(input_str):
        if entity.category == 'NormalText':
            start_idx = entity.start_idx
            for i, ch in enumerate(entity.content):
                if ch.isprintable():
                    char_list.append(ch)
                    pos_map[norm_idx] = start_idx + i
                    norm_idx += 1

    joined_str = ''.join(char_list)
    head_space_num = len(joined_str) - len(joined_str.lstrip())
    if head_space_num:
        pos_map = {i - head_space_num: j for i, j in pos_map.items() if i >= head_space_num}

    return joined_str.strip(), pos_map
```

简单的计算出句首的空格数，然后重新构造`pos_map`即可。虽然，丑了点，但是顺利通过。

#### 第五个

前面只有一个`url` 试试多个`url` 的情况

```
    @patch('norm_text.extract_entity')
    def test_5(self, mock_extract_entity):
        input_str = 'http://example.org前后都有链接http://example.org'
        mock_extract_entity.return_value = [
            Entity(content='http://example.org', category='Url', start_idx=0, end_idx=18),
            Entity(content='前后都有链接', start_idx=18, end_idx=24),
            Entity(content='http://example.org', category='Url', start_idx=24, end_idx=len(input_str)),
        ]
        output_str, pos_map = get_norm_text_and_pos_map(input_str)

        self.assertEqual(output_str, '前后都有链接')
        self.assertEqual(pos_map, {0: 18, 1: 19, 2: 20, 3: 21, 4: 22, 5: 23})
```

顺利通过。简单的想一下就知道，再多的链接应该都是可以的了。

#### 第六个

居然试了多个`url` 的情况，那就再试试多个`不可打印字符` 吧

```
    @patch('norm_text.extract_entity')
    def test_6(self, mock_extract_entity):
        input_str = '\x01SOH-\x10SO-\x1fUS'
        mock_extract_entity.return_value = [
            Entity(content=input_str, start_idx=0, end_idx=len(input_str)),
        ]
        output_str, pos_map = get_norm_text_and_pos_map(input_str)

        self.assertEqual(output_str, 'SOH-SO-US')
        self.assertEqual(pos_map, {0: 1, 1: 2, 2: 3, 3: 4, 4: 6, 5: 7, 6: 8, 7: 10, 8: 11})
```

顺利通过。看来多个`不可打印字符`  应该也不是问题。

#### 第七个

试试考虑`url` `不可打印字符` 前置`空格` 等情况综合在一起的情况，甚至再加个`Emoji` 表情进去

```
    @patch('norm_text.extract_entity')
    def test_7(self, mock_extract_entity):
        input_str = 'http://example.org 前置空格\031加入不可打印字符，\U0001F609一个emoji'
        mock_extract_entity.return_value = [
            Entity(content='http://example.org', category='Url', start_idx=0, end_idx=18),
            Entity(content=' 前置空格\031加入不可打印字符，', start_idx=18, end_idx=33),
            Entity(content='\U0001F609', category='Emoji', start_idx=33, end_idx=34),
            Entity(content='一个emoji', start_idx=34, end_idx=len(input_str)),
        ]
        output_str, pos_map = get_norm_text_and_pos_map(input_str)

        self.assertEqual(output_str, '前置空格加入不可打印字符，一个emoji')
        self.assertEqual(pos_map, {0: 19, 1: 20, 2: 21, 3: 22,
                                   4: 24, 5: 25, 6: 26, 7: 27, 8: 28, 9: 29, 10: 30, 11: 31, 12: 32,
                                   13: 34, 14: 35, 15: 36, 16: 37, 17: 38, 18: 39, 19: 40})
```

顺利通过。算是挺复杂的了，没什么问题😉，那上面的例子中的字符串应该不用验证了，肯定可以通过。

#### 最后一个

再来个极端情况的，如果输入是个空格

```
    @patch('norm_text.extract_entity')
    def test_8(self, mock_extract_entity):
        input_str = ' '
        mock_extract_entity.return_value = [
            Entity(content=' ', start_idx=0, end_idx=1),
        ]
        output_str, pos_map = get_norm_text_and_pos_map(input_str)

        self.assertEqual(output_str, '')
        print(pos_map)
        self.assertEqual(pos_map, {})
```
顺利通过。

## 结尾

一个简单的函数，一口气写了8个unittest，其实思路还是很顺畅的。最后实在不想再写下去了，就不写了。

这个例子，到了第四个unittest 代码其实已经满足需求了（虽然，丑了点）。其中，进行了3 次代码逻辑的改动和1 次`mock` 的对unittest 本身的改动，后面的unittest 基本都是复制粘贴，修改对应的输入和输出，大致的结构都是一致。

## 真的是最后一个吗

几个月后，可能你同事在家跑你的这段unittest， 但是他家的猫在他键盘上按住了空格键，结果第一个unittest 的输入变成了下面那样。他想应该也不是问题，不管怎样，先不跑一下再说

```
    @patch('norm_text.extract_entity')
    def test_1(self, mock_extract_entity):
        input_str = '一个简单的文本             '
        mock_extract_entity.return_value = [Entity(content=input_str, start_idx=0, end_idx=len(input_str))]
        output_str, pos_map = get_norm_text_and_pos_map(input_str)

        self.assertEqual(output_str, '一个简单的文本')
        self.assertEqual(pos_map, {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6})
```

失败。报错

```
{0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6} != {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10, 11: 11, 12: 12, 13: 13, 14: 14, 15: 15, 16: 16, 17: 17, 18: 18, 19: 19} 
```

你同事`blame` 一下，想顺着网线过来打你一顿。但是跑了几个月的代码，一直没有出问题，肯定也有原因。因为这个`pos_map`，最后是为了找出输出字符串某个字符的位置在输入字符串中的位置。而这个`pos_map` 其实已经记录了输出字符串的所有位置，只是多记录了句尾的空格。所以，其实也可以睁一只眼，闭一只眼。居然没人提出来，也就算了。

真的能忍吗？ 他觉得忍不了，看了下对应的函数，虽然丑了点，但是还能读懂，并且还有8个unittest，瞬间就有了改老代码的底气。


