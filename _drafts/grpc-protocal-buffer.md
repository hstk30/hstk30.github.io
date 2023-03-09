# gRPC and Protocal Buffer


## RPC 和 HTTP


[HTTP和RPC的优缺点](https://developer.aliyun.com/article/634470) 

我能感受的应该就是字节大小的对比。HTTP 一般都用JSON，通过UTF-8 编码，再加上gzip。
对于一个浮点数，比如`1.23456789`，它的UTF-8 编码长度就是10。
但是使用二进制表示，单精度浮点数的长度只有4，这样就节省了一些存储和传输的压力。

之所以有这个体会是因为之前tf-serving 使用HTTP 传输了一个`batch_size * seq_len * vocab_size` 的浮点数据，
一个请求的数据大小大概有300MB（32(batch_size) * 64(avg_seq_len) * 20000(vocab_size) * 9(float 文本表示) = 351MB），
于是就爆炸了。


## Protocal Buffer

```
syntax = "proto3";

message SearchRequest {
    string query = 1;
    int32 page_number = 2;
    int32 result_per_page = 3;
}
```


这里的“默认值”，并不是通常意义的默认值，而是字段编号（Field Numbers)，
每个字段需要一个唯一的字段编号。而在版本更新，对这个消息的字段有更新删除后，
通过这个唯一编号保证前后消息版本的兼容。

字段编号1到15使用1字节编码（还有4bit干嘛去了？）；
16到2047使用2字节编码；
19000到19999保留。
所以给最重要的字段分配1到15的编号，不确定的分配大点的编号，从而提升一些性能。

实践中，在消息版本迭代更新中，通过声明保留字段（Reserved Fields）来要求protocal buffer compiler 进来检查。


### 字段规则

- **singular**: 默认规则。需要注意，对于标量消息字段，声明了这个规则的字段无法区分该字段值是来自默认值还是显式设置的。
- **optional**: 区别于 **singular** 的是：它能区分出该字段值是来自默认值还是显式设置的。
- **repeated**: 类似 `list` 。
- **map**: 类似 `dict` 。


### 自动生成对应语言的类

```
protoc --proto_path=IMPORT_PATH --python_out=DST_DIR --pyi_out=DST_DIR path/to/file.proto
```

生成
- `xxx_pb2.py` 通过奇怪的方式生成对应message 的类数据结构 
- `xxx_pb2.pyi` Python 用于语法提示的文件

## gRPC

```
python3 -m grpc_tools.protoc -I. --python_out=. --pyi_out=. --grpc_python_out=. message.proto
```

生成

- `xxx_pb2.py` Protocal buffer 的生成
- `xxx_pb2.pyi` Python 用于语法提示的文件
- `xxx_pb2_grpc.py` 对应服务的**Stub** 类


## 未完成

- gRPC 如何负载平衡，有注册中心(register) 吗？


[ngx grpc](http://nginx.org/en/docs/http/ngx_http_grpc_module.html)

nginx 也可以做grpc 的负载平衡


## 参考

- [grpc quickstart](https://grpc.io/docs/languages/python/quickstart/)
- [proto3 programming guides](https://protobuf.dev/programming-guides/proto3/)


