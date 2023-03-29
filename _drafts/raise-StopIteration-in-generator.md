# 如何在生成器中正常终止


## 结论

使用`return` 来终止生成器而不是通过`raise StopIteration`
（虽然感觉`raise StopIteration` 也挺合理的，我就是一开始想到用这个来终止才发现这个问题的）


具体的解释正好有

[PEP 479 – Change StopIteration handling inside generators](https://peps.python.org/pep-0479/)


## Code

```python
def stop_by_return(c):
    for i in range(c):
        yield i
        if i > 2:
            return
```

```python
def stop_by_raise(c):
    for i in range(c):
        yield i
        if i > 2:
            raise StopIteration

```

## Test


### Case1

```python
for i in stop_by_return(10):
    print(i)
```

#### In Python3.6

Output: 
```
0
1
2
3

```

#### In Python3.10

Output:
```
0
1
2
3

```
### Case2

```python
for i in stop_by_raise(10):
    print(i)
```


#### In Python3.6

Output: 

```
0
1
2
3
/Library/Frameworks/Python.framework/Versions/3.6/bin/ipython3:1: DeprecationWarning: generator 'stop_by_raise' raised StopIteration
  #!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3.6
```


#### In Python3.10

```
0
1
2
3
---------------------------------------------------------------------------
StopIteration                             Traceback (most recent call last)
Input In [2], in stop_by_raise(c)
      4 if i > 2:
----> 5     raise StopIteration

StopIteration:

The above exception was the direct cause of the following exception:

RuntimeError                              Traceback (most recent call last)
Input In [4], in <cell line: 1>()
----> 1 for i in stop_by_raise(10):
      2     print(i)

RuntimeError: generator raised StopIteration

```

