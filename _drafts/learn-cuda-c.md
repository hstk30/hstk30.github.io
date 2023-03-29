# CUDA C 学习

- [Professional CUDA C Programming](https://www.cs.utexas.edu/~rossbach/cs380p/papers/cuda-programming.pdf)
- [CUDA syntax](https://icl.utk.edu/~mgates3/docs/cuda.html)


## Hello World

```
// hello.cu
#include <stdio.h>


__global__ void hello_from_GPU(void)
{
    printf("Hello World from GPU%d!\n", threadIdx.x);
}

int main(void)
{
    printf("Hello World from CPU!\n");
    hello_from_GPU <<<1, 10>>>();
    cudaDeviceReset();
    return 0;
}
```

编译：`nvcc hello.cu -o hello`

- `__global__` 指明该函数会从CPU中调用，然后在GPU上执行。这种函数成为核(kernal)函数。
- `<<<1, 10>>>` `<<<grid, block>>>` 运算符内是核函数的执行配置
- `threadIdx.x`
- `cudaDeviceReset` 显式地释放和清空当前进程中与当前设备有关的所有资源。


## CUDA 编程结构

1. 分配GPU内存。
2. 从CPU内存中拷贝数据到GPU内存。
3. 调用CUDA核函数来完成程序指定的运算。
4. 将数据从GPU拷回CPU内存。
5. 释放GPU内存空间。


## 内存管理

GPU内存分配函数

    cudaError_t cudaMalloc(void **devPtr, size_t size)

相比C中的内存分配函数

    void *malloc(size_t size)

返回GPU的返回指针是 `void **`

GPU数据移动函数

    cudaError_t cudaMemcpy(void *dst, const void *src, size_t count, cudaMemcpyKind kind)

    cudaMemcpyKind: 
    - cudaMemcpyHostToHost
    - cudaMemcpyHostToDevice
    - cudaMemcpyDeviceToHost
    - cudaMemcpyDeviceToDevice


## 网格grid 和线程块block

一个网格包含多个线程块，一个线程块包含多个线程。

- `uint3` 不是`uint32`，应该相当于`struct uint3 { unsigned int x, y, z; }`
- `dim3` 类似


### 内置变量

- `blockIdx`: 线程块在网格内的索引
- `threadIdx`: 线程块内的线程索引
- `blockDim`: 线程块的维度，用每个线程块中的线程数来表示
- `gridDim`: 网格的维度，用每个网格中的线程数来表示


## 编写核函数

核函数就是在设备端（GPU）上执行的代码。

### 函数类型限定符

- `__global__` 可从主机端调用，在设备端执行
- `__device__` 仅能在设备端调用，在设备端执行
- `__host__` 默认省略，即正常的C函数


### 核函数的限制

- 只能访问设备内存
- 必须具有 `void` 返回类型
- 不支持可变数量的参数
- 不支持静态变量
- Exhibit an asynchronous behavior


