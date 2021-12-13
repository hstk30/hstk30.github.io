---
layout:     post
title:      "nginx 相关问题记录"
date:       2021-11-26
author:     "hstk30"
tags:
    - nginx
---

# nginx 相关问题记录

> 现在整个大地都采用一种语言，只包括为数不多的单词。
在一次从东方往西方迁徙的过程中，人们发现了苏美尔地区，并在那里定居下来。接着他们奔走相告说：“来，让我们制造砖块，并把它们烧好。”
于是，他们用砖块代替石头，用沥青代替灰泥（建造房屋）。然后，他们又说：“来，让我们建造一座带有高塔的城市，这个塔将高达云霄，也将让我们声名远扬，同时，有个这个城市，我们就可以聚居在这里，再也不会分散在广阔的大地上了。”
于是上帝决定下来看看人们建造的城市和高塔，看了以后，他说：“他们只是一个种族，使用同一种语言，如果他们一开始就能够建造城市和高塔，那以后就没有什么难得倒他们了。来，让我们下去，在他们的语言里制造些混淆，让他们相互之间不能听懂。”
这样，上帝把人们分散到世界各地，于是他们不得不停止建造那座城市。
——创世纪，11:1-8

摘录自《人月传说》第7章《为什么巴比伦塔会失败？（WHY DID THE TOWER OF BABEL FAIL？）》

## 参数解释

### `max_fails`与 `fail_timeout`

> `max_fails=number`  
> sets the number of unsuccessful attempts to communicate with the server that should happen in the duration set by the fail_timeout parameter to consider the server unavailable for a duration also set by the fail_timeout parameter. By default, the number of unsuccessful attempts is set to 1. The zero value disables the accounting of attempts. What is considered an unsuccessful attempt is defined by the `proxy_next_upstream`, `fastcgi_next_upstream`, `uwsgi_next_upstream`, `scgi_next_upstream`, `memcached_next_upstream`, and `grpc_next_upstream` directives.

> 翻译  
> 在`fail_timeout` 参数设置的持续时间内发生的与服务器通信的失败尝试次数，以确定服务器在下一个`fail_timeout` 参数设置的持续时间内是否可用。 默认情况下，不成功尝试的次数设置为 1。

>`fail_timeout=time`  
>sets  
> - the time during which the specified number of unsuccessful attempts to communicate with the server should happen to consider the server unavailable;  
> - and the period of time the server will be considered unavailable.
> By default, the parameter is set to 10 seconds.  

> 翻译  
> - 在这段时间内如果出现`max_fails` 次的与上游服务器的失败尝试，则认为这个上游服务器不可用
> - 上游服务器被认为不可用的时间
> 默认为10s

例子

```
server 192.168.1.2 max_fails=2 fail_timeout=60s；
```

表示如果60秒内`nginx`与上游`192.168.1.2` 出现了2次失败尝试，这个上游服务器就被认为`不可用`，则在下一个60s内`nginx` 不会转发请求给上游服务器`192.168.1.2`。过了这个时间后再恢复可用，进行尝试，以此循环。

一种极端情况下（如高并发下，上游响应时间过长，出现大量与上游的连接超时或读响应超时），导致所有的上游服务器都被认为`不可用`，则出现大量

```
...no live upstreams while connecting to upstream...
```

的错误日志。

一个直接的做法是，降低`fail_timeout`，提高`max_fails`，如设置为

```
server 192.168.1.2 max_fails=10 fail_timeout=30s；
```

则被认为`不可用`的时间减少到30秒，且有10次的失败尝试机会。这样在上游服务器还是健康的情况下是能减少上面的错误日志的。

### 三个超时时间

#### `proxy_connect_timeout`

> Defines a timeout for establishing a connection with a proxied server. It should be noted that this timeout cannot usually exceed 75 seconds.

> 与代理服务器建立连接的超时时间。一般不能超过75秒。

#### `proxy_read_timeout`

> Defines a timeout for reading a response from the proxied server. The timeout is set only between two successive read operations, not for the transmission of the whole response. If the proxied server does not transmit anything within this time, the connection is closed.

> 从代理服务器读取响应的超时时间。 超时仅在两次连续读取操作之间设置，而不是针对整个响应的传输。 如果代理服务器在此时间内未传输任何内容，则连接将关闭。

#### `proxy_send_timeout `

> Sets a timeout for transmitting a request to the proxied server. The timeout is set only between two successive write operations, not for the transmission of the whole request. If the proxied server does not receive anything within this time, the connection is closed.
 
> 将请求传输到代理服务器的超时时间。 超时仅设置在两次连续的写操作之间，而不是针对整个请求的传输。 如果代理服务器在这段时间内没有收到任何信息，则连接关闭

感觉是个凑数的参数，真实环境真的会出现nginx传输的出问题吗？确实没遇到过😬


这三个超时时间的设置其实更多的是不同组之间的工程沟通问题。nginx 常作为代理服务器，结构如下

```
client -> nginx -> upstream server
```

所以需要把`client` 与`nginx` 的请求超时时间、建立连接超时时间，`nginx` 与`server` 的请求超时时间、建立连接超时时间等超时时间一起考虑，这就需要不同组之间进行沟通、确认。

#### `proxy_next_stream` 和 `upstream_response_time `

> Syntax:	proxy_next_upstream error | timeout | invalid_header | http_500 | http_502 | http_503 | http_504 | http_403 | http_404 | http_429 | non_idempotent | off ...;  
> Default:	proxy_next_upstream error timeout;  
> Context:	http, server, location  
> Specifies in which cases a request should be passed to the next server

当出现声明的case 的时候就传给下一个server 去处理。比如，有以下配置

```
upstream flask-test {
	server 127.0.0.1:5000  fail_timeout=30s max_fails=20;  # server 1
	server 127.0.0.1:5001  fail_timeout=30s max_fails=20;  # server 2
}

server{
    listen 8600 default;
    server_name   0.0.0.0;
    location / {
        proxy_pass http://flask-test;
        proxy_next_upstream error timeout non_idempotent;
        proxy_read_timeout 10s;
        proxy_set_header NGINX_SEND_TIME $time_local;
    }
}
```

当一个请求先到server 1， 但是server 1 比较忙，用了11s (> `proxy_read_timeout`) 才返回，则nginx 将这个请求发给server 2继续处理。这时，同一个请求就会被上游处理两边，如果这个请求会改变*状态*，则可能出错。

> keeps time spent on receiving the response from the upstream server; the time is kept in seconds with millisecond resolution. Times of several responses are separated by commas and colons like addresses in the $upstream_addr variable.

`upstream_response_time` 记录从上游服务器接收相应所花的时间。以秒为单位，精确到毫秒。多个响应的时间用逗号分隔。

如，在`log format` 中写了`$request_time $upstream_response_time`

 则有timeout 出现时，日志可能像
 
 ```
 19.013 10.001, 9.012
 ```


## reload 客户端依然报错

虽然NGINX 是平滑重启的，但是没有和客户端保持一致。

`connection reset `

客户端重试的机制没有跟上对应的接口，因此出错。

## 未完待续


[探究 Nginx 中 reload 流程的真相](https://cloud.tencent.com/developer/article/1555933)

[Nginx Connection Reset 问题排查](https://segmentfault.com/a/1190000038463522)


