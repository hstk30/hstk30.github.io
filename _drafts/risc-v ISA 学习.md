# rCore 学习

```
qemu-system-riscv64 \
  -machine virt \
   -nographic \
   -bios ./bootloader/rustsbi-qemu.bin \
   -device loader,file=target/riscv64gc-unknown-none-elf/release/os.bin,addr=0x80200000 \
   -s -S

riscv64-unknown-elf-gdb \
    -ex 'file target/riscv64gc-unknown-none-elf/release/os' \
    -ex 'set arch riscv:rv64' \
    -ex 'target remote localhost:1234'
``` 

```
rust-objcopy --strip-all target/riscv64gc-unknown-none-elf/release/os -O binary target/riscv64gc-unknown-none-elf/release/os.bin
```

`<C-A> x` 退出`qemu`


## risc-v ISA 学习

在RV32I上进行

通过组合使用RV32I提供的基础指令来实现一些有用的扩展执行，伪指令(pseudo instructions)

## 转移控制

`call` <==> `auipc ra, 0`  <== `ra = PC + (0 << 12)`
`ret` <==> `jalr x0, ra, 0` <== `x0=PC + 4; PC=ra + 0`

## 数据传送指令


## 长整型加法

假设`long` 为64位，则两个64位的加法，可以被分解为一下基础指令
假设`l1` 的高32位存放在寄存器`a3` 中，低32位存放在`a2` 中，
`l2` 的高32位存放在寄存器`a5` 中，低32位存放在`a4` 中，
结果的高32位存放在寄存器`a1` 中，低32位存放在`a0` 。

```
add a0, a2, a4 # 低32位
sltu a2, a0, a2 # 是否进位，两个正数相加反而变小，说明进位
add a5, a3, a5 # 高32位
add a1, a2, a5 # 高32位加进位
```


## 获取pc

```
auipc a2, 0
```

`x86` 上获取的方法

```
_start:
	call next_ins
next_ins:
	pop %rax # 获取当前pc 到rax 中
```

当时不知道在哪里看到这种代码，直接傻眼了。就不能有条指令直接获取PC吗？
不过，这不就是组合使用基础指令来获取特定功能的指令吗？不就和risc-v 的伪指令差不多吗？
当然性能上可能有差距。

