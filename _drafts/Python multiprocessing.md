# Python multiprocessing

- 将对象的绑定方法作为子进程任务，将使得整个对象被 pickle 序列化传给子进程， 所以一种经验法则是使用 `@staticmethod` 或直接传一个函数

> Once our object IntToBitarrayConverter is created, the object is bound to the method convert(...). This means when we pass our method to Pool.map(...), we are implicitly passing a reference to the object as well.




[Multiprocessing.Pool() - Stuck in a Pickle](https://thelaziestprogrammer.com/python/a-multiprocessing-pool-pickle)


[2017-pybay Concurrency](https://pybay.com/site_media/slides/raymond2017-keynote/intro.html)

