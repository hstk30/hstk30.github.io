# Rust 学习

## 字符串

`Python` 中的`str`是可变长的不可变对象，经典的问题就是多个字符串变量通过`+` 相加，
因为`str` 不可变，因此每次`+` 操作都申请内存创建一个新的中间变量字符串。

而`Rust` 提供了两种字符串对象

- `str`： 不可变，可能存在`.rodata` 中
- `String`: 可变的，在堆中进行分配，动态扩张结构。

DST(dynamically sized types)

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

函数调用的参数为值传递。
相比于`C` ，`Rust` 在退出作用域后会清理一波分配了堆内存的对象，然后栈指针`sp` 指回帧指针`fp` 。

### 引用和借用

> We call the action of creating a reference borrowing. 

借用的东西不能乱修改，除非加上`mut`。

> Mutable references have one big restriction: you can have only one mutable reference to a particular piece of data at a time.

对一个对象的引用，如果有可变引用，那么在作用域内就只能有这个引用，连不可变引用都不能存在。

> Rust enforces a similar rule for combining mutable and immutable references.

> - Two or more pointers access the same data at the same time.
> - At least one of the pointers is being used to write to the data.
> - There’s no mechanism being used to synchronize access to the data.

为了数据安全，避免程序运行时才会暴露的内存错误和一些奇奇怪怪的问题，
增加了这些限制使得这些问题在编译时就能暴露出来。

> References must always be valid.

避免了`C` 经典错误: 悬空指针。


`index out of bounds` 无法在编译时避免


## 泛型的实现

在编译的时候遍历所有用到的具体类型，并相应的创建对应具体类型的类型再进行编译。


[泛型的性能](https://course.rs/basic/trait/generic.html#泛型的性能)


## 闭包

`Fn`、`FnMut`、`FnOnce`

当编译器推导出一种类型后，它就会一直使用该类型

Rust 内部会使用结构体表示闭包，它会根据闭包捕获的变量创建对应的结构体，并为该结构体实现最合适的特征。

```
let mut i: i32 = 0;

let mut f = || {
    i += 1;
};
```

```
struct MyClosure {
    i: &mut i32
}

impl FnMut for MyClosure {
    fn call_mut(&mut self) {
        *self.i += 1;
    }
}
```


## 参考

[可视化 Rust 各数据类型的内存布局](https://github.com/rustlang-cn/Rustt/blob/main/Articles/%5B2022-05-04%5D%20%E5%8F%AF%E8%A7%86%E5%8C%96%20Rust%20%E5%90%84%E6%95%B0%E6%8D%AE%E7%B1%BB%E5%9E%8B%E7%9A%84%E5%86%85%E5%AD%98%E5%B8%83%E5%B1%80.md)