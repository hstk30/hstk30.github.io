# nginx reload 客户端依然报错

虽然NGINX 是平滑重启的，但是没有和客户端保持一致。这有点像*软件工程* 里的**沟通** 问题。

`connection reset `

客户端重试的机制没有跟上对应的接口，因此出错。

[探究 Nginx 中 reload 流程的真相](https://cloud.tencent.com/developer/article/1555933)

[Nginx Connection Reset 问题排查](https://segmentfault.com/a/1190000038463522)