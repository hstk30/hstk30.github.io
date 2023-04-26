---
layout:     post
title:      "torch 中的 CrossEntropyLoss 和 NLLLoss"
date:       2023-04-25
header-img: "img/confuse.png"
author:     "hstk30"
description: "小舟从此逝，江海寄余生。"
tags:
    - 深度学习
---

# torch 中的 CrossEntropyLoss 和 NLLLoss


**CrossEntropyLoss == NLLLoss + LogSoftmax == NLLLoss + Log + Softmax**


```python
>>> import torch
>>> from torch import nn
>>> x = torch.randn(3, 3)
>>> x
tensor([[-1.3006, -1.2822, -0.8243],
        [ 0.2941,  1.8343, -1.3450],
        [-0.1628, -0.0365,  0.9028]])
>>> y = torch.tensor([0, 2, 1])
>>> y
tensor([0, 2, 1])

>>> cross_loss = nn.CrossEntropyLoss()
>>> cross_loss(x, y)
tensor(2.0622)

>>> log_softmax = nn.LogSoftmax(dim=1)
>>> nll_loss(log_softmax(x), y)
tensor(2.0622)

>>> nll_loss = nn.NLLLoss()
>>> softmax = nn.Softmax(dim=1)
>>> nll_loss(torch.log(softmax(x)), y)
tensor(2.0622)
```

**torch** 主打一个灵活，所以对基础的知识要求也更高。

网上大部分讲的都是前两种，第三种属于拼凑型。但是有时候我们希望模型的输出是 **softmax** 后的值，
也就是一个概率分布。这个时候就需要在 **train** 的时候

```
loss = NLLLoss()

...

prob = model(x)
loss(torch.log(prob), y)
loss.backward()
```

如果直接使用 **CrossEntropyLoss** ，则模型层的输出可能是 **dense** 层的输出，

```
loss = CrossEntropyLoss()

...

logits = model(x)
loss(logits, y)
loss.backward()
```


看似微小的差别，其实可能有以下几点问题：


- 模型结构不同，导致后续需要转 **onnx** 的时候出来的模型也是不同的
- 前者在预测的时候不需要再 **softmax** ，而后者需要再 **softmax**
- 一致性上，个人感觉前者更好，对于一个分类任务，我们肯定希望模型的输出是一个概率分布


当然，缺点是前者不能一眼看出来使用的是交叉熵损失。但是我觉得这个问题应该怪 **torch**，
谁叫你把 **softmax** 加到 **CrossEntropyLoss** 里了。网上搜”pytorch 有哪些坑“ 里面，
这个问题也属于 *top* 级别。

