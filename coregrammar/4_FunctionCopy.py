import functools
import time

from numpy.ma.mrecords import addfield


# 2. 参数类型
def demo_parameters():
    # 2.1 位置参数
    def add(a, b):
        return a + b
    # 按位置传
    print(f"  add(1, 2) = {add(1, 2)}")
    # 按关键字传
    print(f"  add(a=1, b=2) = {add(a=1, b=2)}")
    # 混用，位置参数必须写在关键字前面
    print(f"  add(1, b=2) = {add(1, b=2)}")

    # 2.2 默认参数
    def greet(name, greeting="Hello"):
        return f"{greeting} {name}"
    print(f"  greet('Alice') = {greet('Alice')}")
    print(f"  greet('Alice', 'Hi') = {greet('Alice', 'Hi')}")

    # 警惕！默认参数仅在函数定义时求值一次！
    def timestamp(t=time.time()):
        return t

    t1 = timestamp()
    print(f"  t1 = {t1}")
    time.sleep(1)
    t2 = timestamp()
    print(f"  t2 = {t2}")
    print(f"  t1 == t2 -> {t1 == t2}")

    # 接收任意多个位置的参数，类似可变参数：*args
    def all_sum(*args):
        # args是元组
        print(f"  args 的类型 = {type(args).__name__}, 内容 = {args}")
        return sum(args)
    print(f"  sum(1, 2, 3) = {all_sum(1, 2, 3)}")

    # 接收任意多个关键字参数：**keywords
    def print_info(**kwargs):
        print(f"  kwargs 的类型 = {type(kwargs).__name__}, 内容 = {kwargs}")
        for key, value in kwargs.items():
            print(f"  {key} = {value}")
    print_info(name="Alice", age=25, city="New York")

# 3. 返回值
def demo_return():
    # 3.1 单个返回值
    def add(a, b):
        return a + b
    print(f"  add(1, 2) = {add(1, 2)}")
    # 3.2 多个返回值，解包接收
    def min_max(lst):
        return min(lst), max(lst)
    # 返回值是元组，解包
    low, high = min_max([3, 1, 4, 1, 5])
    print(f"  min = {low}, max = {high}")

# 4. 作用域

# 5.闭包，一个函数 + 它随身携带的“外部变量背包”
def demo_closure():
    """
    闭包成立的三个条件：
        1. 有函数嵌套
        2. 内层函数引用了外层变量
        3. 内层函数被返回出去
    :return:
    """
    def outer(x):
        def inner(n):
            return x * n
        return inner      # 返回内层函数本身
    f = outer(2)
    print(f"{ 'f的类型：' + str(type(f).__name__)}")
    print(f"  f(3) = {f(3)}")
    print(f"  f(4) = {f(4)}")

    # 累加器
    def make_counter():
        count = 0
        def counter():
            nonlocal count
            count += 1
            return count
        return counter
    c1 = make_counter()
    print(f"{c1()}")
    print(f"{c1()}")
    print(f"{c1()}")

    # 平方函数
    def square(n):
        return n * n

    # 装饰器
    def make_cache(fun):
        # 轻量级的私有状态
        cache = {}
        def wrapper(n):
            if n in cache:
                print(f"  {n} 在缓存中，返回缓存值")
                return cache[n]
            else:
                print(f"  {n} 不在缓存中，计算并缓存结果")
                cache[n] = fun(n)
                return cache[n]
        return wrapper
    mc1 = make_cache(square)
    print(f"{mc1(3)}")
    print(f"{mc1(4)}")
    print(f"{mc1(3)}")

# 6. 函数是对象（一等公民）
def demo_function_is_object():
    # 6.1 可以放进列表
    fun_list = [str, int, float]
    print(f"{[fun(3.9) for fun in fun_list]}")

    # 6.2 当参数
    # 6.3 当返回值
    def choose_operation(op):
        if op == "add":
            return lambda x, y: x + y
        elif op == "sub":
            return lambda x, y: x - y
        else:
            return lambda x, y: x * y

# 7. 匿名函数，基本语法：lambda 参数列表 : 返回的表达式
def demo_anonymous_function():
    # 7.1 匿名函数
    add = lambda x, y: x + y
    print(f"{add(3, 4)}")

    # 7.2 循环中闭包晚绑定!!!!!!!!
    func = [lambda : i * i for i in range(5)]
    # 输出结果：[4, 4, 4, 4, 4]，期待：[0, 1, 2, 3, 4]
    print(f"{[f() for f in func]}")
    # 如何修改？
    # i=i 默认值取成外层循环的 i 现在的值
    func2 = [lambda i=i : i * i for i in range(5)]
    print(f"{[f() for f in func2]}")

# 9.1 装饰器
def demo_decorators():
    # 装饰器本质：接收一个函数，返回一个增强版函数
    # 语法 @decorator 是语法糖：func = decorator(func)

    # ---- 9.1 基础装饰器 ----
    def log_calls(func):
        # @functools.wraps(func) 会把原函数的 __name__、__doc__ 等元信息复制到 wrapper 上
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print(f"    [调用前] {func.__name__}")
            result = func(*args, **kwargs)
            print(f"    [调用后] 返回 {result!r}")
            return result
        return wrapper

    @log_calls
    def add(a, b):
        """两数相加"""
        return a + b

    print("  调用被装饰的 add(2, 3):")
    print(f"  结果: {add(2, 3)}")

# 主函数
def main():
    print(f"{'=' * 60!r}")
    # demo_parameters()
    demo_return()
    # demo_closure()
    # demo_function_is_object()
    # demo_anonymous_function()
    demo_decorators()

if __name__ == "__main__":
    main()