# virtual machine interpreters: Stack base vs Register base


感觉最主要的问题还是分支预测，由于引入流水线，导致分支跳转命令成为影响性能的瓶颈？


## papaer

[Threaded code| Bell 1973](https://dl.acm.org/doi/abs/10.1145/362248.362270)
[Virtual Machine Showdown: Stack Versus Registers](https://dl.acm.org/doi/10.1145/1328195.1328197)
[Optimizing direct threaded code by selective inlining](https://dl.acm.org/doi/abs/10.1145/277650.277743)


## 参考

[threaded-code](http://www.complang.tuwien.ac.at/forth/threaded-code.html)
[threaded-code | 译](https://www.yhspy.com/2020/08/21/Threaded-Code/)

