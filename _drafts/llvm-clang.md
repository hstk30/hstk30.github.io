## llvm clang 初学记录


### 编译

```
cmake -G "Unix Makefiles" -DLLVM_ENABLE_PROJECTS="clang" -DCMAKE_BUILD_TYPE=Release -DLLVM_TARGETS_TO_BUILD="AArch64" -DBUILD_SHARED_LIBS=On ../llvm
make
```

```
cmake -G "Ninja" -DLLVM_ENABLE_PROJECTS="clang" -DCMAKE_BUILD_TYPE=Release -DLLVM_TARGETS_TO_BUILD="AArch64" -DBUILD_SHARED_LIBS=On ../llvm
ninja
```


Mac 上编译出现

```
fatal error: 'stdio.h' file not found
```

尝试加入 `-isysroot` 选项，使用 `clang -### ...` 去获取，我的是 `/Library/Developer/CommandLineTools/SDKs/MacOSX.sdk`


### 名称概念

- 命令行上的 `clang` ，称为 `Clang Driver` ，是个驱动，一个包含变异全部阶段的驱动
- 命令行上的 `clang -cc1` 称为 `Clang 编译器` 
- `Clang 前端`


通过命令 `clang -### main.c -o main` ，加入 `-###` 显示打印 `Clang Driver` 驱动实际执行了哪些命令。

[参考：Clang编译器的简单分析](https://zhuanlan.zhihu.com/p/26443002)

## 模块化工具

### 代码 -> .ll (LLVM IR Human Readable)

    clang -emit-llvm -S main.c -o main.ll

### .ll -> .bc (LLVM IR Bitcode)

    llvm-as main.ll -o main.bc

### .bc -> .ll

    llvm-dis main.bc -o main.ll

### .bc -> .s (target machine Assembly language)

    llc main.bc -o main.s


#### 有用的选项

- `-run-pass=<pass-name>` Run compiler only for specified passes (comma separated list)
- `-stop-after=<pass-name>` `-stop-before=<pass-name>` `-start-before` `-start-after`



### link .bc like ld

    llvm-link a.bc b.bc -o c.bc

### opt LLVM IR

    opt a.ll -o b.ll


## clang 常用选项

### 调试

- `-mllvm -debug-pass=Arguments` `-mllvm -debug-pass=Structure` 打印使用的优化Pass


## TableGen 配置选项解析

[llvm TableGen](https://llvm.org/docs/TableGen/)

一句话概括：读取 `.td` 文件中的配置信息，解析为 `C++` 代码在llvm项目中使用。

`grep "TableGen\'erated file" -r .` 查看自动生成的 `.inc` 文件。

`class xx is not defined` 缺啥就 `find` 加入对应的 `-I` (难搞)


### 一些配置文件

- `*InstrInfo.td` , like `AArch64InstrInfo.td`
- `*RegisterInfo.td` , like `AArch64RegisterInfo.td`

## FileCheck 测试工具

[llvm FileCheck](https://llvm.org/docs/CommandGuide/FileCheck.html)

一句话概括：用于测试llvm工具集的输出与期望是否相同，测试代码和期望结果在同一文件里。

### 有用的指令

- `CHECK-LABEL:` 分隔测试代码块，防止跨越不同代码块的测试代码
- `CHECK:`
- `CHECK-NOT:`
- `CHECK-NEXT:`: 要求检查的指令连续
- `CHECK-SAME:`: **same line** 同一行内检查
- `COM:`: **comment** 注释

## 写Pass

[WritingAnLLVMPass](https://llvm.org/docs/WritingAnLLVMPass.html)

[WritingAnLLVMNewPMPass](https://llvm.org/docs/WritingAnLLVMNewPMPass.html)


### 使用 *gdb* 调试的注意事项

- 用 *gdb* 调试动态加载的 pass 时，先把断点设在 `break llvm::PassManager::run` 。
- 内联函数有错误的堆栈信息
- `run` 后 Pass 内设置的断点失效


## LLVM Program Structure 

| C/C++ Source | LLVM IR |
| -- | -- | 
| Source file | **Module** contains **Function** and **Global Variables** |
| Function | **Function** contains **Basic Blocks** and **Arguments** |
| Code Block | **Basic Blocks**  contains a list of **Instructions** |
| Statement | **Instruction** is an **Opcode** plus vector of **Operands** |


## User-Use-Usee

- `Value(Usee)` : keep track of a list of **Users** that are using this **Value**
- `Instruction(User)` : keep track of a list of **Values** that it is using as **Operands**

```
%2 = add %1, 10
```

Think this way: "%2 is the Value Representation of Instruction add %1, 10" 

## 指令选择

[GlobalISel](https://llvm.org/docs/GlobalISel/index.html)

- **FastISel**
- **SelectionDAGISel**
- **GlobalISel**

LLVM IR -> target-specific Machine IR (MIR).

> SelectionDAG and FastISel operate on individual basic blocks, GlobalISel operates on the whole function.

## 大端问题

问题一大堆

- [BigEndianNEON](https://llvm.org/docs/BigEndianNEON.html)
- [issues-34708](https://github.com/llvm/llvm-project/issues/34708)


