---
layout:     post
title:      "深度学习初体验的感受"
subtitle:  "深度学习深度学习一个月的一些感受和吐槽"
date:       2021-6-20
author:     "hstk30"
tags:
    - Deep Learning
---

# 深度学习一个月初体验的感受

刚入职一个月，本来面试的是`Python` 开发工程师，结果入职说是做深度学习相关的。秉持着**试一试** 的生活态度，就当公费学习新技能吧。  

## 入职前对深度学习的想法

之前公司其实也是做人工智能相关的，我们部门也会对接人工智能小组，处理一些输出的数据。人工智能对我来说就是个黑盒，作为一个“称职” 的码农，当然不需要去关心这些东西。对于从事深度学习的人，还是有一小点崇拜的，毕竟**算法工程师** 这称号还是比**CURD后端开发** 听着要高端一点。当然，在真正接触深度学习前我也看过别人写的一些算法代码，嗯，以我对`Python` 的了解，我明白，**算法工程师** 确实只关注算法本身。。。

## 炼丹师入门



### overfitting

在*训练数据* 上效果在变好，但在*验证数据* 上效果在变差。


#### 解决方法

1. 增加训练数据
2. Less parameters, sharing parameters
3. Less features
4. Early stopping
5. Regularization
6. Dropout

### optimization issue 

> If deeper networks do not obtain smaller loss on *training data*, then there is optimization issue
