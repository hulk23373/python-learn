"""
Python 函数全览

函数是把一段逻辑"打包"起来、起个名字、可以反复调用的工具。
Python 的函数比大多数语言灵活得多，因为它把函数本身也当成对象。

本文件覆盖：
    1. 函数基础     : def、调用、return、docstring
    2. 参数类型全览 : 位置/关键字/默认/*args/**kwargs/仅关键字/仅位置
    3. 返回值       : 单值、多值、None、卫语句
    4. 作用域       : LEGB、global、nonlocal
    5. 闭包         : 函数记住外部变量
    6. 函数是对象   : 赋值、传参、返回、存字典
    7. lambda       : 匿名函数
    8. 高阶函数     : map / filter / sorted(key=) / reduce
    9. 装饰器       : 不修改原函数就增强它
   10. 递归         : 函数调用自己
   11. 类型注解     : 写给人和 IDE 看的提示
   12. 常见陷阱     : 可变默认值、闭包晚绑定等
"""

import functools
import inspect
import time
from functools import reduce


# 模块级变量：这才是 global 关键字能改到的"全局"
_global_counter = 0


def section(title):
    """打印分节标题"""
    print(f"\n{'=' * 64}\n{title}\n{'=' * 64}")


# ============================================================
# 1. 函数基础
# ============================================================

def demo_basics():
    section("1. 函数基础")

    # ---- 最简形式 ----
    def greet():
        print("  你好")

    greet()                     # 调用：函数名 + 括号

    # ---- 带参数和返回值 ----
    def add(a, b):
        return a + b

    print(f"  add(1, 2) = {add(1, 2)}")

    # ---- 没有 return 就返回 None ----
    def no_return():
        x = 1 + 1               # 做了事，但没 return

    print(f"  no_return() = {no_return()!r}")

    # ---- 只有 return 也返回 None ----
    def bare_return():
        return

    print(f"  bare_return() = {bare_return()!r}")

    # ---- docstring：函数的第一条字符串，说明用途 ----
    def area(width, height):
        """计算矩形面积。

        参数:
            width: 宽
            height: 高
        返回:
            面积（宽 * 高）
        """
        return width * height

    print(f"  area.__doc__ 第一行: {area.__doc__.strip().splitlines()[0]!r}")
    print(f"  area(3, 4) = {area(3, 4)}")

    # ---- def 是语句，执行到它时才创建函数对象 ----
    # 所以在 def 之前不能调用
    # print(not_yet())        # ❌ NameError
    def not_yet():
        return "现在可以了"

    print(f"  {not_yet()}")

    # ---- 嵌套函数：函数里可以再定义函数 ----
    def outer():
        def inner():
            return "我是内层函数"
        return inner()

    print(f"  嵌套函数: {outer()}")

    # ---- 函数名只是一个变量，可以重新绑定 ----
    alias = add
    print(f"  别名调用 alias(5, 6) = {alias(5, 6)}")
    print(f"  alias is add -> {alias is add}")


# ============================================================
# 2. 参数类型全览（本节是重点）
# ============================================================

def demo_parameters():
    section("2. 参数类型全览")

    # ---------- 2.1 位置参数 ----------
    def power(base, exponent):
        return base ** exponent

    # 按位置传：第一个给 base，第二个给 exponent
    print(f"  位置传参 power(2, 3) = {power(2, 3)}")

    # 按关键字传：顺序可以颠倒
    print(f"  关键字传参 power(exponent=3, base=2) = {power(exponent=3, base=2)}")

    # 混用：位置参数必须写在关键字参数前面
    print(f"  混用 power(2, exponent=3) = {power(2, exponent=3)}")
    # power(base=2, 3)  ❌ SyntaxError: positional argument follows keyword argument

    # ---------- 2.2 默认参数 ----------
    def greet(name, greeting="你好"):
        return f"{greeting}，{name}"

    print(f"  {greet('张三')}")
    print(f"  {greet('张三', 'Hello')}")
    print(f"  {greet('张三', greeting='Hi')}")

    # ⚠️⚠️ 最重要的陷阱：默认值只在【定义时】求值一次
    def bad_append(item, target=[]):        # ❌ 可变默认值
        target.append(item)
        return target

    print(f"\n  ⚠️ 可变默认值陷阱：")
    print(f"    bad_append(1) = {bad_append(1)}")
    print(f"    bad_append(2) = {bad_append(2)}   ← 期望 [2]，实际 [1, 2]！")
    print(f"    bad_append(3) = {bad_append(3)}   ← 还在累积！")

    # 正确写法：默认用 None，函数内部再创建
    def good_append(item, target=None):     # ✅
        if target is None:
            target = []
        target.append(item)
        return target

    print(f"    good_append(1) = {good_append(1)}")
    print(f"    good_append(2) = {good_append(2)}   ← 正确")

    # 同样的道理：默认值是在 def 执行时算的，不是每次调用时
    def timestamp(t=time.time()):           # 记录的是【定义时刻】
        return t

    t1 = timestamp()
    time.sleep(0.01)
    t2 = timestamp()
    print(f"\n  默认参数只求值一次: t1 == t2 -> {t1 == t2}（都是定义那一刻的时间）")

    # ---------- 2.3 *args：接收任意多个位置参数 ----------
    def sum_all(*args):
        # args 是一个元组！名字叫 args 只是约定
        print(f"    args 的类型 = {type(args).__name__}, 内容 = {args}")
        return sum(args)

    print(f"\n  *args:")
    print(f"    sum_all() = {sum_all()}")
    print(f"    sum_all(1) = {sum_all(1)}")
    print(f"    sum_all(1, 2, 3, 4) = {sum_all(1, 2, 3, 4)}")

    # ---------- 2.4 **kwargs：接收任意多个关键字参数 ----------
    def show_info(**kwargs):
        # kwargs 是一个字典！名字叫 kwargs 只是约定
        print(f"    kwargs 的类型 = {type(kwargs).__name__}, 内容 = {kwargs}")
        for key, value in kwargs.items():
            print(f"      {key} = {value}")

    print(f"\n  **kwargs:")
    show_info(name="张三", age=25, city="北京")

    # ---------- 2.5 参数顺序规则 ----------
    # 完整顺序：位置参数 -> 默认参数 -> *args -> 仅关键字参数 -> **kwargs
    def full(a, b, c=3, *args, d, e=5, **kwargs):
        print(f"    a={a}, b={b}, c={c}")
        print(f"    args={args}")
        print(f"    d={d}, e={e}")
        print(f"    kwargs={kwargs}")

    print(f"\n  完整参数顺序演示:")
    full(1, 2, 3, 4, 5, d=6, e=7, f=8, g=9)

    # ---------- 2.6 仅关键字参数（* 分隔符）----------
    # 单独的 * 后面的参数，必须用关键字传
    def create_user(name, *, email, age):
        return f"{name} / {email} / {age}"

    print(f"\n  仅关键字参数: {create_user('张三', email='z@x.com', age=25)}")
    # create_user('张三', 'z@x.com', 25)   ❌ TypeError
    print("    ↑ 只能用关键字传，强制调用方写清楚每个值的含义")

    # ---------- 2.7 仅位置参数（/ 分隔符，Python 3.8+）----------
    # / 前面的参数只能用位置传，不能用关键字
    def pos_only(a, b, /, c):
        return a + b + c

    print(f"\n  仅位置参数: pos_only(1, 2, 3) = {pos_only(1, 2, 3)}")
    print(f"  后面的 c 仍可用关键字: pos_only(1, 2, c=3) = {pos_only(1, 2, c=3)}")
    # pos_only(a=1, b=2, c=3)             ❌ TypeError: a, b 是仅位置参数

    # 完整组合：/ 在前，* 在后
    def everything(a, b, /, c, d=4, *, e, f=6, **kwargs):
        return f"a={a} b={b} c={c} d={d} e={e} f={f} kwargs={kwargs}"

    print(f"  全部组合: {everything(1, 2, 3, 4, e=5)}")

    # ---------- 2.8 调用时解包 ----------
    data = [1, 2, 3]
    numbers = {"a": 1, "b": 2, "c": 3}

    def three(a, b, c):
        return a + b + c

    print(f"\n  列表解包 three(*[1,2,3]) = {three(*data)}")
    print(f"  字典解包 three(**{{...}}) = {three(**numbers)}")

    # 转发参数：装饰器里最常见的写法
    def wrapper(func, *args, **kwargs):
        return func(*args, **kwargs)

    print(f"  参数转发 wrapper(power, 2, 4) = {wrapper(power, 2, 4)}")


# ============================================================
# 3. 返回值
# ============================================================

def demo_return():
    section("3. 返回值")

    # ---- 返回单个值 ----
    def square(n):
        return n * n

    print(f"  square(5) = {square(5)}")

    # ---- 返回多个值：本质是返回一个元组 ----
    def min_max(nums):
        return min(nums), max(nums)

    result = min_max([3, 1, 4, 1, 5])
    print(f"  返回多值 result = {result!r}  type={type(result).__name__}")

    low, high = min_max([3, 1, 4, 1, 5])         # 解包接收
    print(f"  解包接收 low={low}, high={high}")

    # ---- 卫语句：提前 return，避免层层嵌套 ----
    def process(user):
        if user is None:
            return "无用户"                       # 提前退出
        if not user.get("active"):
            return "未激活"
        if not user.get("name"):
            return "缺少姓名"
        return f"处理 {user['name']}"

    print(f"\n  卫语句:")
    print(f"    {process(None)}")
    print(f"    {process({'active': False})}")
    print(f"    {process({'active': True, 'name': '张三'})}")

    # ---- return 会立刻结束函数 ----
    def early_exit():
        print("    第一行")
        return "返回了"
        print("    这一行永远不会执行")        # 不可达代码

    print(f"  {early_exit()}")


# ============================================================
# 4. 作用域：LEGB
# ============================================================

def demo_scope():
    section("4. 作用域：LEGB")

    # Python 查找变量按 L -> E -> G -> B 的顺序：
    #   L: Local          当前函数内部
    #   E: Enclosing      外层嵌套函数
    #   G: Global         模块全局
    #   B: Built-in       内置（print、len 等）

    x = "全局 x"

    def read_global():
        # 只读时，直接能找到外层的 x
        return f"读到了 {x}"

    print(f"  {read_global()}")

    # ⚠️ 函数内对变量【赋值】会创建局部变量，遮蔽外部的同名变量
    def shadow():
        x = "局部 x"                 # 这是新的局部变量，不是修改全局
        return x

    print(f"  shadow() 返回 {shadow()!r}，但外面的 x 仍是 {x!r}")

    # ---- global：声明"我要改的是【模块级】那个" ----
    # 注意：global 指向的是模块顶层，不是外层函数！
    def increment_global_counter():
        global _global_counter       # 不加这行会报 UnboundLocalError
        _global_counter += 1

    increment_global_counter()
    increment_global_counter()
    print(f"  用 global 修改后 _global_counter = {_global_counter}")

    # ⚠️ 关键区别：如果变量是"外层函数的局部变量"，global 是够不着的
    local_counter = 0               # 这是 demo_scope 的局部变量

    def bad_use_of_global():
        global local_counter        # ← 指向模块级，不是 demo_scope 的 local_counter
        # local_counter += 1        # ❌ NameError: 模块级没有这个名字
        pass

    print("  ⚠️ global 改不到外层函数的局部变量——那种情况要用 nonlocal")

    # ⚠️ 连 global 都不声明就直接赋值会怎样（下面这行不声明 global）：
    # 因为 "counter = ..." 让 Python 认为它是局部变量，
    # 而 += 需要先读，此时局部变量还不存在 -> UnboundLocalError

    # ---- nonlocal：修改外层嵌套函数的变量 ----
    def outer():
        value = 0

        def inner():
            nonlocal value           # 声明"我要改的是外层的 value"
            value += 1
            return value

        inner()
        inner()
        return value

    print(f"  用 nonlocal 修改外层变量，结果为 {outer()}")

    # ---- 对比：不声明 nonlocal ----
    def outer_broken():
        value = 0

        def inner():
            value = 99               # 这是内层自己的新变量
            return value

        inner()
        return value                 # 外层 value 还是 0

    print(f"  不声明 nonlocal 时外层不变: {outer_broken()}")

    # ---- 最佳实践：尽量少用 global / nonlocal ----
    # 优先用参数传入、用返回值传出。全局状态会让代码难以理解和测试。

    # ---- 内置作用域 ----
    print(f"  builtins 里的 len: {len([1, 2, 3])}")
    # 不要用 print/list/dict 等内置名当变量名，会遮蔽内置函数


# ============================================================
# 5. 闭包
# ============================================================

def demo_closure():
    section("5. 闭包")

    # 闭包 = 内层函数 + 它记住的外层变量
    # 外层函数返回后，内层函数依然能访问那些变量

    def make_multiplier(n):
        def multiply(x):
            return x * n             # n 来自外层，被"记住"了
        return multiply

    times2 = make_multiplier(2)
    times10 = make_multiplier(10)

    print(f"  2 倍: {times2(5)}")
    print(f"  10 倍: {times10(5)}")
    print("  ↑ 两个闭包各自记住了不同的 n，互不干扰")

    # ---- 闭包能看到"变化后"的外层变量 ----
    def make_counter():
        count = 0

        def counter():
            nonlocal count
            count += 1
            return count

        return counter

    c1 = make_counter()
    c2 = make_counter()              # 另一个独立计数器
    print(f"\n  计数器: {c1()}, {c1()}, {c1()}")
    print(f"  另一个独立计数器: {c2()}")
    print("  ↑ c1 和 c2 各有自己的 count 状态")

    # ---- 闭包能看到 __closure__ 里存的东西 ----
    print(f"\n  times2 的闭包内容: {times2.__closure__}")
    print(f"  捕获的 n 值: {times2.__closure__[0].cell_contents}")

    # ---- 用闭包实现简单配置 ----
    def make_formatter(prefix, suffix):
        def format(value):
            return f"{prefix}{value}{suffix}"
        return format

    bold = make_formatter("**", "**")
    print(f"  闭包做格式化: {bold('important')}")


# ============================================================
# 6. 函数是对象（一等公民）
# ============================================================

def demo_functions_are_objects():
    section("6. 函数是对象")

    def greet(name):
        return f"你好，{name}"

    # ---- 1. 能赋给变量 ----
    say_hello = greet
    print(f"  赋给变量: {say_hello('张三')}")

    # ---- 2. 能放进容器 ----
    operations = {
        "add": lambda a, b: a + b,
        "sub": lambda a, b: a - b,
        "mul": lambda a, b: a * b,
    }
    print(f"  存字典: operations['mul'](6, 7) = {operations['mul'](6, 7)}")

    func_list = [str, int, float]
    print(f"  存列表: {[f(3.9) for f in func_list]}")

    # ---- 3. 能当参数传（高阶函数）----
    def apply_twice(func, value):
        return func(func(value))

    print(f"  作为参数: apply_twice(lambda x: x + 3, 10) = {apply_twice(lambda x: x + 3, 10)}")

    # ---- 4. 能当返回值 ----
    def choose_operation(op):
        if op == "add":
            return lambda a, b: a + b
        return lambda a, b: a * b

    chosen = choose_operation("add")
    print(f"  作为返回值: {chosen(2, 3)}")

    # ---- 5. 函数有属性 ----
    print(f"\n  函数属性:")
    print(f"    __name__    = {greet.__name__!r}")
    print(f"    __doc__     = {greet.__doc__!r}")
    print(f"    __module__  = {greet.__module__!r}")
    print(f"    type        = {type(greet).__name__}")
    print(f"    is callable = {callable(greet)}")

    # ---- 6. 用函数本身做判断条件 ----
    print(f"  callable(len) = {callable(len)}，callable(42) = {callable(42)}")


# ============================================================
# 7. lambda 匿名函数
# ============================================================

def demo_lambda():
    section("7. lambda 匿名函数")

    # 语法：lambda 参数: 表达式
    # 只能包含【一个表达式】，不能写多条语句

    add = lambda a, b: a + b
    print(f"  lambda 加法: {add(3, 4)}")

    # 等价于：
    def add_def(a, b):
        return a + b
    print(f"  等价 def:   {add_def(3, 4)}")

    # ---- 适合：用完即丢的小函数 ----
    print(f"  排序 key: {sorted(['bbb', 'a', 'cc'], key=lambda s: len(s))}")
    print(f"  按第二个元素排序: {sorted([(1, 3), (2, 1), (3, 2)], key=lambda p: p[1])}")

    # ---- 适合：map / filter 的简短逻辑 ----
    print(f"  map: {list(map(lambda x: x * 2, [1, 2, 3]))}")
    print(f"  filter: {list(filter(lambda x: x > 1, [1, 2, 3]))}")

    # ---- 不适合：复杂逻辑 ----
    # 一旦需要 if/else 嵌套或很多步骤，就改回 def
    # lambda 里可以有三元表达式，但可读性会变差
    classify = lambda n: "正" if n > 0 else ("零" if n == 0 else "负")
    print(f"  可以但别这么写: {classify(-5)}")

    # ---- lambda 的常见坑：循环里晚绑定 ----
    print(f"\n  ⚠️ 闭包晚绑定:")
    funcs = [lambda: i for i in range(3)]
    print(f"    [lambda: i for i in range(3)] -> {[f() for f in funcs]}")
    print("    期望 [0, 1, 2]，实际全是 2 —— lambda 查 i 时循环已经结束了")

    # 修复：把 i 作为默认参数"当场固定"
    funcs_fixed = [lambda i=i: i for i in range(3)]
    print(f"    修复 [lambda i=i: i ...] -> {[f() for f in funcs_fixed]}")

    # ---- lambda 的名字是 <lambda> ----
    print(f"  lambda 的 __name__: {add.__name__!r}")
    print("  ↑ 调试时看不出是哪个函数，所以复杂逻辑别用 lambda")


# ============================================================
# 8. 高阶函数
# ============================================================

def demo_higher_order():
    section("8. 高阶函数")

    numbers = [1, 2, 3, 4, 5]

    # ---- map：对每个元素应用函数 ----
    doubled = list(map(lambda x: x * 2, numbers))
    print(f"  map 翻倍: {doubled}")

    # ---- filter：保留条件为真的元素 ----
    evens = list(filter(lambda x: x % 2 == 0, numbers))
    print(f"  filter 偶数: {evens}")

    # ---- sorted 的 key 参数（最常用）----
    words = ["banana", "apple", "cherry"]
    print(f"  按长度排序: {sorted(words, key=len)}")
    print(f"  按字母倒序: {sorted(words, reverse=True)}")

    people = [
        {"name": "张三", "age": 25},
        {"name": "李四", "age": 30},
        {"name": "王五", "age": 20},
    ]
    by_age = sorted(people, key=lambda p: p["age"])
    print(f"  按年龄排序: {[p['name'] for p in by_age]}")

    # ---- reduce：把序列压缩成一个值 ----
    total = reduce(lambda a, b: a + b, numbers)
    print(f"  reduce 求和: {total}")

    product = reduce(lambda a, b: a * b, numbers)
    print(f"  reduce 求积: {product}")

    # ---- 用生成器表达式代替 map/filter（更 Pythonic）----
    print(f"\n  更 Pythonic 的写法:")
    print(f"    [x*2 for x in numbers]        = {[x * 2 for x in numbers]}")
    print(f"    [x for x in numbers if x%2==0] = {[x for x in numbers if x % 2 == 0]}")
    print("  ↑ 列表推导式通常比 map/filter + lambda 更易读")

    # ---- 短路工具 ----
    print(f"\n  any / all:")
    print(f"    any([False, True])  = {any([False, True])}")
    print(f"    all([True, True])   = {all([True, True])}")
    print(f"    all([True, False])  = {all([True, False])}")


# ============================================================
# 9. 装饰器
# ============================================================

def demo_decorators():
    section("9. 装饰器")

    # 装饰器本质：接收一个函数，返回一个增强版函数
    # 语法 @decorator 是语法糖：func = decorator(func)

    # ---- 9.1 基础装饰器 ----
    def log_calls(func):
        @functools.wraps(func)          # 保留原函数的名字和文档
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

    # @functools.wraps 的价值
    print(f"\n  保留元信息: __name__ = {add.__name__!r}, __doc__ = {add.__doc__!r}")
    print("  ↑ 不加 @functools.wraps 的话，__name__ 会变成 'wrapper'")

    # ---- 9.2 等价的非装饰器写法 ----
    def plain_func(x):
        return x * 2

    decorated = log_calls(plain_func)
    print(f"\n  手动装饰: {decorated(5)}")

    # ---- 9.3 带参数的装饰器（三层嵌套）----
    def repeat(times):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                results = []
                for _ in range(times):
                    results.append(func(*args, **kwargs))
                return results
            return wrapper
        return decorator

    @repeat(3)
    def say_hi():
        return "Hi"

    print(f"\n  带参数装饰器 @repeat(3): {say_hi()}")

    # ---- 9.4 多重装饰器：从下往上包裹 ----
    def bold(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return f"<b>{func(*args, **kwargs)}</b>"
        return wrapper

    def italic(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return f"<i>{func(*args, **kwargs)}</i>"
        return wrapper

    @bold
    @italic
    def text():
        return "内容"

    # 等价于 text = bold(italic(text))
    # 所以先加 italic，再加 bold
    print(f"\n  多重装饰器: {text()}")
    print("  ↑ @bold 在最上面，最后包裹；@italic 先应用（从下往上读）")

    # ---- 9.5 常见内置装饰器 ----
    class Example:
        def __init__(self):
            self._value = 42

        @property                        # 把方法变成属性
        def value(self):
            return self._value

        @staticmethod                    # 不需要 self 的方法
        def helper(x):
            return x * 2

        @classmethod                     # 第一个参数是类本身
        def create(cls):
            return cls()

    e = Example()
    print(f"\n  @property:    e.value = {e.value}（像属性一样访问）")
    print(f"  @staticmethod: {Example.helper(5)}（不用实例）")
    print(f"  @classmethod:  {type(Example.create()).__name__}")

    # ---- 9.6 装饰器的典型用途 ----
    print("\n  典型用途: 日志、计时、权限校验、缓存、重试、限流")


# ============================================================
# 10. 递归
# ============================================================

def demo_recursion():
    section("10. 递归")

    # 递归 = 函数调用自己，必须有【终止条件】否则无限递归

    # ---- 阶乘 ----
    def factorial(n):
        if n <= 1:                       # 终止条件（基准情形）
            return 1
        return n * factorial(n - 1)      # 递归调用

    print(f"  5! = {factorial(5)}")

    # ---- 斐波那契：朴素版（性能差）----
    def fib_slow(n):
        if n < 2:
            return n
        return fib_slow(n - 1) + fib_slow(n - 2)

    print(f"  fib_slow(10) = {fib_slow(10)}")
    print("  ⚠️ fib_slow(40) 会非常慢，因为大量重复计算（指数级）")

    # ---- 用缓存优化（记忆化）----
    @functools.lru_cache(maxsize=None)
    def fib_fast(n):
        if n < 2:
            return n
        return fib_fast(n - 1) + fib_fast(n - 2)

    t = time.perf_counter()
    result = fib_fast(100)
    elapsed = time.perf_counter() - t
    print(f"  用 lru_cache 后 fib(100) = {result}")
    print(f"  耗时 {elapsed:.6f} 秒（朴素的算到 40 都要很久）")

    # ---- 递归遍历嵌套结构 ----
    def flatten(items):
        result = []
        for item in items:
            if isinstance(item, list):
                result.extend(flatten(item))    # 遇到子列表就递归
            else:
                result.append(item)
        return result

    print(f"\n  递归展平: {flatten([1, [2, [3, 4]], 5])}")

    # ---- 递归深度限制 ----
    import sys
    print(f"\n  递归深度上限: {sys.getrecursionlimit()}（超过会 RecursionError）")
    print("  深度很大时应改用循环，避免栈溢出")


# ============================================================
# 11. 类型注解
# ============================================================

def demo_annotations():
    section("11. 类型注解")

    # 类型注解只是"提示"，Python 运行时【不会检查】！
    # 作用是给 IDE、静态检查工具（mypy）和读代码的人看

    def add(a: int, b: int) -> int:
        return a + b

    print(f"  add(1, 2) = {add(1, 2)}")
    print(f"  注解信息: {add.__annotations__}")

    # ⚠️ 传错类型照样能跑（不会报错）
    print(f"  add('a', 'b') = {add('a', 'b')!r}   ← 类型注解没拦住！")

    # ---- 常见注解写法 ----
    def greet(name: str, times: int = 1) -> str:
        return f"你好 {name}！" * times

    print(f"\n  {greet('张三', 2)}")

    # ---- 容器类型（Python 3.9+ 可直接用内置类型）----
    def total(numbers: list[int]) -> int:
        return sum(numbers)

    def lookup(data: dict[str, int], key: str) -> int | None:
        return data.get(key)

    print(f"  total([1,2,3]) = {total([1, 2, 3])}")
    print(f"  lookup({{'a': 1}}, 'a') = {lookup({'a': 1}, 'a')}")

    # ---- 联合类型注解 ----
    def to_int(value: str | int) -> int:
        return int(value)

    print(f"  to_int('42') = {to_int('42')}, to_int(42) = {to_int(42)}")

    # ---- Optional / Union 的旧写法（了解即可）----
    # from typing import Optional, Union
    # def f(x: Optional[int]) -> None: ...


# ============================================================
# 12. 常见陷阱总结
# ============================================================

def demo_pitfalls():
    section("12. 常见陷阱总结")

    # ① 可变默认参数（最经典）——见第 2 节
    print("  ① 可变默认参数：默认值只在定义时创建一次，用 None 代替")

    # ② 闭包 / lambda 晚绑定 ——见第 7 节
    print("  ② 循环里创建 lambda：用 lambda i=i: ... 固定当前值")

    # ③ 函数内赋值会创建局部变量
    x = 10

    def shadow_demo():
        # print(x)     # ❌ UnboundLocalError（因为下面有 x = ...）
        x = 20          # 这行让 x 在整个函数内都是局部变量
        return x

    print(f"  ③ 作用域遮蔽：函数内 {shadow_demo()}，函数外 {x}")

    # ④ 忘记 return
    def forgot_return():
        result = 1 + 1

    print(f"  ④ 忘记 return 得到 {forgot_return()!r}")

    # ⑤ 修改了列表却以为函数返回了新列表
    def mutate(lst):
        lst.append(99)              # 直接修改了调用方的列表
        return lst

    original = [1, 2]
    returned = mutate(original)
    print(f"  ⑤ 原地修改：original = {original}，returned = {returned}，"
          f"是同一个对象 -> {original is returned}")

    # ⑥ 参数的默认值里调用函数/时间等"动态"内容
    print("  ⑥ 默认值在定义时求值，别把 time.time() 之类放默认值")

    # ⑦ 装饰器忘记 @functools.wraps，丢失函数元信息
    print("  ⑦ 装饰器里一律加 @functools.wraps(func)")

    # ⑧ 递归没有终止条件 -> RecursionError
    print("  ⑧ 递归必须有终止条件，深度过大改用循环")

    # ⑨ 用可变对象（list/dict/set）当参数时，注意是否想修改原对象
    print("  ⑨ 函数收到 list/dict 是引用，修改会影响调用方；需要副本就用 copy()")

    # ⑩ 参数顺序写错：位置参数不能跟在关键字参数后面
    print("  ⑩ 位置参数必须写在关键字参数前面")


# ============================================================
# 主函数
# ============================================================

def main():
    print("Python 函数全览")

    demo_basics()
    # demo_parameters()
    # demo_return()
    # demo_scope()
    # demo_closure()
    # demo_functions_are_objects()
    # demo_lambda()
    # demo_higher_order()
    # demo_decorators()
    # demo_recursion()
    # demo_annotations()
    # demo_pitfalls()

    section("演示结束")
    print("函数相关功能演示完毕。")


if __name__ == "__main__":
    main()
