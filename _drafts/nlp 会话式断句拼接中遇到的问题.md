# nlp 会话式断句拼接中遇到的问题

后面的消息用来纠正前面的错别字、词。

case 1:
```
- 一个星期了，快递怎么一直听在
- 停
```

case 2:
```
- 还会伤心
- 上新
```

case 3:
```
- 能用揪心
- 就行
```

单句的查看消息，除了case 1，就算是人也不能看出是否正确。
结合上下文，则是需要使用下文的字、词来替换当前消息相应位置上的字、词。

不过，现在的研究方向好像都是只使用上文的信息来补全当前的消息。

- [Conversational Query Rewriting with Self-supervised Learning](https://arxiv.org/abs/2102.04708)
- [Improving Open-Domain Dialogue Systems via Multi-Turn Incomplete Utterance Restoration](https://ai.tencent.com/ailab/nlp/dialogue/papers/EMNLP_zhufengpan.pdf)


