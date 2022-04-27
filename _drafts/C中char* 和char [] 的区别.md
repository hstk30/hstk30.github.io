# C中char* 和char [] 的区别


```
#include<stdio.h>

int main()
{
    char* s1 = "abc";
    char* s2 = "abc";
    char s3[] = "abc";
    char s4[] = "abc";

    printf("s1 addr: %p, s2 addr: %p\n", s1, s2);
    printf("s3 addr: %p, s4 addr: %p\n", s3, s4);

    return 0;
}
```

output:

```
s1 addr: 0x400620, s2 addr: 0x400620
s3 addr: 0x7ffc32eeed50, s4 addr: 0x7ffc32eeed40
```

`objdump -s main` 得到

```
Contents of section .rodata:
 400610 01000200 00000000 00000000 00000000  ................
 400620 61626300 73312061 6464723a 2025702c   abc.s1 addr: %p,
 400630 20733220 61646472 3a202570 0a007333  s2 addr: %p..s3
 400640 20616464 723a2025 702c2073 34206164   addr: %p, s4 ad
 400650 64723a20 25700a00                                dr: %p..
```

也就是说`s1、s2` 中的`"abc"` 是存放在`.rodata` 中的数据，属于真正的*字符串常量*。
而`s3、s4` 中的`"abc"` 是存放在*栈* 中的数据，在函数调用的时候才压入*栈* 中。

因此，`s3、s4` 中的数据是可以修改的，而要想通过指针操作改变`s1、s2` 中的数据则会报错(Segmentation fault，段错误)，
但编译却是能正常通过的，只有在真正执行到的时候才会报警。

如

```
    s3[1] = 'c';
    printf("%s\n", s3);
    *(s1 + 1) = 'c';  // 能正常编译，但执行时报错
    printf("%s\n", s1);  //
```


