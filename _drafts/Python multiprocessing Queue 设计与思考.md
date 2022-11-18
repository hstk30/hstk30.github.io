# Python multiprocessing Queue 设计与思考

Queue 使用了Pipe 进行同步，而Pipe 是基于文件的

要想控制两个进程，就需要进程之外的结构进行同步


多进程同步原语。

(multiprocessing-logging)[https://github.com/jruere/multiprocessing-logging]

(Linux 管道pipe的实现原理)[https://segmentfault.com/a/1190000009528245]
(concurrent.futures.ProcessPoolExecutor unpickle)[https://bugs.python.org/issue29423]

