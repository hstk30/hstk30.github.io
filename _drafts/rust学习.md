# Rust 学习

## 字符串

`Python` 中的`str`是可变长的不可变对象，经典的问题就是多个字符串变量通过`+` 相加，
因为`str` 不可变，因此每次`+` 操作都申请内存创建一个新的中间变量字符串。

而`Rust` 提供了两种字符串对象

- `str`： 不可变，可能存在`.rodata` 中
- `String`: 可变的，在堆中进行分配，动态扩张结构。


## 所有权

### 基本原则

> 1. Each value in Rust has a variable that’s called its owner.
> 2. There can only be one owner at a time.
> 3. When the owner goes out of scope, the value will be dropped.

第二条规则暗示当有变量赋值操作时，其实是在进行拷贝操作或者被编译器禁止。

> Rust will never automatically create “deep” copies of your data.

```
    let s1 = String::from("hello");
    let s2 = s1;

    println!("{}, world!", s1);
```

所以对于这个例子，`浅拷贝` 的话违背了原则`2` ，`深拷贝` 也违背了上面提到的不会自动`深拷贝`。
因此，`Rust` 在语言层面禁止了上面操作，认为：`s1` 在进行赋值操作以后不再有效，
后续如果有对`s1` 的操作就在编译时报错。很霸道啊！不过，考虑到实际的使用情况，
我们在赋值字符串的时候到底想要做什么？

- 通过获取字符串指针，进行双指针操作？
- 保留原来字符串，在拷贝的副本上进行增删改操作？（手动深拷贝的情况）
- ...



## 泛型的实现

在编译的时候遍历所有用到的具体类型，并相应的创建对应具体类型的类型再进行编译。


[泛型的性能](https://course.rs/basic/trait/generic.html#泛型的性能)


## 闭包

当编译器推导出一种类型后，它就会一直使用该类型

