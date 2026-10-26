"""
Python 流程控制语法全览

流程控制 = 决定"哪些代码执行"、"执行几次"、"按什么顺序执行"的语法。

Python 的流程控制大致分为五类：
    1. 条件分支 : if / elif / else、三元表达式、match / case
    2. 循环     : for、while、break、continue、循环的 else 子句
    3. 空语句   : pass、...
    4. 异常流程 : try / except / else / finally、raise
    5. 其它     : with（上下文管理）、assert（断言）、return / yield

本文件每一节都用可运行的代码演示，并标注常见陷阱。
"""

import io
import contextlib

# 条件分支
def demo_if_else():
    x = 80
    if x >= 90:
        print(f"成绩优秀")
    elif x >=80:
        print(f"成绩良好")
    else:
        print(f"成绩一般")

    # 三元运算
    print(f"{'优秀' if x >= 90 else '良好'}")

# match/case
def demo_match_case():
    samples = [0, 2, -5, 42, "hi", "verylong", (1, 2), [1, 2, 3], [],
               {"type": "user", "name": "张三", "extra": 1}, None]
    # match case
    def demo_describe(value):
        match value:
            case int(x):
                return f"整数{x}"
            case _:  # default
                return f"其他"
    for value in samples:
        t = demo_describe(value)
        print(f"{t}")

# 循环，for/while/break/continue/else
def demo_for():
    # for
    for x in range(1, 10, 2):
        print(f"{x}")
    # while
    x = 1
    while x <= 10:
        x += 1
        if x == 8:
            break
        print(f"{x}")
    else:
        # 如果有break，则不输出
        print("xxxx")

# 空语句，pass
def demo_pass():
    x = 10
    if x < 20:
        pass  # 什么都不做
    else:
        print(f"{x}")

# 异常处理
def demo_exception():
    try:
        try:
            x = 10 / 0
        except ZeroDivisionError as e:
            print(f"  捕获到: {type(e).__name__}: {e}")
            raise
    except Exception as e:
        print(f"重新捕获异常：{e}")
    finally:
        print(f"finally无论如何都会执行")

# with上下文管理
def demo_with():
    # with 保证【无论如何都会执行清理】，比 try/finally 更简洁
    # 典型场景：文件、锁、数据库连接、网络会话
    file = io.StringIO("第一行\n第二行\n")
    with file as f:
        content = f.read()
        print(f"{content}")

    with io.StringIO("啦啦啦啦") as file2:
        content = file2.read()
        print(f"{content}")

# assert 断言
def demo_assert():
    x = 11
    assert x > 10, f"x必须大于10，x当前的值为：{x}"
    print(f"{x}")

# yield
def demo_yield():
    def count_up(n):
        x = 3
        while x < n:
            yield x
            x += 1
    # 创建生成器对象
    count = count_up(10)
    print(f"生成器对象：{count}")
    y = next(count)
    print(f"逐个取出：{y}")
    print(f"逐个取出：{list(count)}")


def main():
    print(f"{'=' * 60!r}")
    # demo_if_else()
    # demo_match_case()
    # demo_for()
    # demo_pass()
    # demo_exception()
    # demo_with()
    # demo_assert()
    demo_yield()

if __name__ == "__main__":
    main()