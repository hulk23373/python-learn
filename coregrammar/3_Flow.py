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


def section(title):
    """打印分节标题"""
    print(f"\n{'=' * 64}\n{title}\n{'=' * 64}")


# ============================================================
# 1. if / elif / else —— 条件分支
# ============================================================

def demo_if_elif_else():
    section("1. if / elif / else")

    score = 85

    # 基本形式：if 后面跟条件表达式，冒号结尾，代码块靠【缩进】划分
    # Python 没有大括号！缩进就是语法，4 个空格是社区标准
    if score >= 90:
        print("优秀")
    elif score >= 80:          # 注意是 elif，不是 else if
        print("良好")
    elif score >= 60:
        print("及格")
    else:                       # else 不需要条件
        print("不及格")

    # ---- 条件里可以写什么 ----
    age = 25
    name = "张三"
    tags = ["vip", "new"]

    if age >= 18:                      # 比较运算
        print(f"{name} 已成年")

    if name and age > 0:               # 逻辑运算 and / or / not
        print("逻辑与：都成立")

    if "vip" in tags:                  # 成员运算
        print("是 VIP")

    if name is not None:               # 身份运算（判断 None 永远用 is）
        print("name 不是 None")

    # ---- Python 独有的链式比较 ----
    x = 5
    if 0 < x < 10:                     # 等价于 (0 < x) and (x < 10)
        print(f"{x} 在 0 和 10 之间（链式比较）")

    # ---- 真值测试：不必写 == True 或 == [] ----
    items = [1, 2, 3]
    if items:                          # 非空即为真
        print("items 非空")

    empty = []
    if not empty:                      # 空列表为假
        print("empty 是空的")

    # 记住假值清单：False None 0 0.0 0j "" [] () {} set() range(0)

    # ---- 嵌套与扁平化 ----
    # 不好的写法：层层嵌套
    a, b, c = 1, 0, 1
    if a:
        if b:
            if c:
                print("嵌套三层")

    # 好的写法：用 and 压平
    if a and b and c:
        print("这一行等价于上面三层嵌套，但可读性好得多")

    # ---- 单个语句可以写在同一行（不推荐，但要知道是合法的）----
    if score > 60: print("单行 if 是合法的")

    # ---- 多个条件分支用字典分派（比长 if-elif 链更好）----
    def handle_create():
        return "创建"

    def handle_delete():
        return "删除"

    action = "create"
    handlers = {"create": handle_create, "delete": handle_delete}
    print(f"字典分派: {handlers.get(action, lambda: '未知')()}")


# ============================================================
# 2. 三元表达式（条件表达式）
# ============================================================

def demo_ternary():
    section("2. 三元表达式")

    age = 20

    # 语法：  A if 条件 else B
    # 注意顺序和 C/Java 的  条件 ? A : B  不同！Python 把结果写在前面
    status = "成年" if age >= 18 else "未成年"
    print(f"status = {status!r}")

    # C/Java 写法对比（Python 里这样写是语法错误）：
    #   status = age >= 18 ? "成年" : "未成年"     ❌

    # 常见用法：给默认值
    username = ""
    display = username if username else "匿名用户"
    print(f"display = {display!r}")

    # 嵌套三元（超过两层就该改成 if-else 了，可读性会崩）
    score = 85
    grade = "A" if score >= 90 else ("B" if score >= 80 else "C")
    print(f"嵌套三元: {grade}")

    # 与推导式结合很常见
    numbers = [1, 2, 3, 4, 5]
    labels = ["奇" if n % 2 else "偶" for n in numbers]
    print(f"推导式 + 三元: {labels}")

    # 注意：条件为真时返回前面的值，为假时返回 else 后面的值
    # 而且只会求值其中一个分支（惰性）
    def side_effect(tag):
        print(f"  [求值了 {tag}]")
        return tag

    _ = side_effect("A") if True else side_effect("B")
    print("↑ 只看到 A 被求值，B 分支没有执行")


# ============================================================
# 3. for 循环
# ============================================================

def demo_for():
    section("3. for 循环")

    # Python 的 for 是【遍历】循环，不是 C 那种三段式 for
    # 语法：for 变量 in 可迭代对象:
    for fruit in ["apple", "banana", "cherry"]:
        print(f"  {fruit}")

    # C 风格的 for(int i=0; i<5; i++) 在 Python 里写 for i in range(5)
    print("range(5):", end=" ")
    for i in range(5):
        print(i, end=" ")
    print()

    # range 的三种形式
    print("range(2, 6):", list(range(2, 6)))          # 2,3,4,5
    print("range(0, 10, 3):", list(range(0, 10, 3)))  # 0,3,6,9
    print("range(10, 0, -2):", list(range(10, 0, -2)))

    # 遍历字符串（逐字符）
    for ch in "abc":
        print(f"  字符 {ch!r}")

    # 遍历元组、集合
    for v in (10, 20):
        print(f"  元组元素 {v}")

    for v in {1, 2, 3}:           # set 无序，输出顺序不保证
        print(f"  集合元素 {v}")

    # ---- 遍历字典的三种方式 ----
    person = {"name": "张三", "age": 25}

    for key in person:                       # 默认遍历键
        print(f"  键: {key}")

    for value in person.values():            # 遍历值
        print(f"  值: {value}")

    for key, value in person.items():        # 同时取键值（最常用）
        print(f"  {key} = {value}")

    # ---- 解包遍历：元素本身是元组时 ----
    pairs = [("a", 1), ("b", 2)]
    for letter, number in pairs:
        print(f"  {letter} -> {number}")

    # ---- 遍历多个序列：zip 并排走 ----
    names = ["张三", "李四", "王五"]
    ages = [25, 30, 35]
    for name, age in zip(names, ages):
        print(f"  {name} 今年 {age} 岁")

    # ⚠️ zip 会在最短的那个序列用完时停下（静默截断，不报错）
    for a, b in zip([1, 2, 3], [10, 20]):
        print(f"  zip 截断演示: {a}, {b}")      # 只跑两次

    # ---- 需要下标时用 enumerate，不要用 range(len(...)) ----
    fruits = ["apple", "banana", "cherry"]
    for i, fruit in enumerate(fruits):
        print(f"  {i}: {fruit}")

    for i, fruit in enumerate(fruits, start=1):   # 指定起始编号
        print(f"  第 {i} 个: {fruit}")

    # ---- 倒序遍历 ----
    for x in reversed([1, 2, 3]):
        print(f"  reversed: {x}")

    # ---- 遍历时排序（sorted 返回新列表，不改原列表）----
    for x in sorted([3, 1, 2]):
        print(f"  sorted: {x}")

    # ⚠️⚠️ 最重要的陷阱：不要在遍历 list 的同时增删它
    # 这会导致跳过元素，行为难以预测
    nums = [1, 2, 3, 4]
    broken = []
    # 错误示范（不要运行）：
    # for n in nums:
    #     if n % 2 == 0:
    #         nums.remove(n)      # ← 边遍历边改，会漏掉元素
    # 正确做法：遍历副本，或生成新列表
    for n in nums[:]:                   # 遍历副本
        if n % 2 == 0:
            nums.remove(n)
    print(f"  安全地删除偶数后: {nums}")

    # 或者干脆用推导式造新列表（推荐）
    nums2 = [1, 2, 3, 4, 5, 6]
    odd = [n for n in nums2 if n % 2]
    print(f"  推导式过滤出奇数: {odd}")


# ============================================================
# 4. while 循环
# ============================================================

def demo_while():
    section("4. while 循环")

    # while 条件为真时反复执行，适合"不知道要循环几次"的场景
    count = 0
    while count < 3:
        print(f"  count = {count}")
        count += 1                  # ⚠️ 忘写这句就是死循环

    # Python 没有 ++ / -- 运算符！要写 count += 1
    # count++ 在 Python 里是语法错误

    # ---- 最常见的范式：while True + break ----
    n = 0
    while True:
        n += 1
        if n >= 3:
            break                   # 用 break 跳出
        print(f"  while True 第 {n} 轮")

    # ---- while 处理"消费队列"型逻辑 ----
    queue = [1, 2, 3]
    while queue:
        item = queue.pop(0)
        print(f"  处理 {item}，剩余 {len(queue)}")

    # ---- 与 for 的选择原则 ----
    # 已知次数 / 有明确可遍历对象 -> for
    # 条件驱动、次数不确定     -> while


# ============================================================
# 5. break / continue
# ============================================================

def demo_break_continue():
    section("5. break / continue")

    # break：立即跳出【当前这一层】循环
    for i in range(10):
        if i == 3:
            break
        print(f"  break 演示 {i}")

    print("  ↑ 到 3 就停了")

    # continue：跳过本次剩余代码，直接进入下一次
    for i in range(6):
        if i % 2 == 0:
            continue                # 偶数跳过
        print(f"  continue 跳过偶数 -> {i}")

    # ---- break 只跳出最内层 ----
    print("  嵌套中的 break：")
    for i in range(3):
        for j in range(3):
            if j == 1:
                break               # 只跳出内层 for j
            print(f"    i={i}, j={j}")
    # 外层继续跑，所以 i 会走完 0,1,2

    # ---- 想跳出多层：用标志位或函数 return ----
    print("  用函数 return 跳出多层：")

    def find_pair():
        for i in range(3):
            for j in range(3):
                if i + j == 3:
                    return (i, j)   # 直接退出整个函数
        return None

    print(f"    找到 {find_pair()}")

    # 或者用循环的 else 子句（下一节）
    # Python 没有 goto，也没有带标签的 break（Java 的 break outer;）


# ============================================================
# 6. 循环的 else 子句 —— Python 独有
# ============================================================

def demo_loop_else():
    section("6. 循环的 else 子句（Python 独有）")

    # 规则：【没有 break 过】循环正常结束时执行 else
    # 换句话说：else 是"没被 break 打断"的意思
    # 它不是"否则"——叫 else 是 Python 的历史包袱，理解成 no-break 更准

    print("  情况 A：正常结束，没 break -> else 会执行")
    for i in range(3):
        print(f"    i={i}")
    else:
        print("    ✅ else 执行了")

    print("  情况 B：中途 break -> else 跳过")
    for i in range(10):
        if i == 2:
            print(f"    break at {i}")
            break
    else:
        print("    ❌ 这行不会打印")

    # ---- 典型用途：查找未找到时给出提示 ----
    def search(target, items):
        for item in items:
            if item == target:
                print(f"    找到了 {target}")
                break
        else:
            print(f"    没找到 {target}")

    search(3, [1, 2, 3, 4])
    search(9, [1, 2, 3, 4])

    # 等价写法对比（不用 else 得引入标志位，更啰嗦）
    found = False
    for item in [1, 2, 3]:
        if item == 9:
            found = True
            break
    if not found:
        print("    标志位写法（等价的，但更啰嗦）")

    # ---- while 也有 else ----
    n = 0
    while n < 3:
        n += 1
    else:
        print(f"    while 正常结束，n={n}")

    # ---- 空可迭代对象：循环一次都不跑，但 else 仍会执行 ----
    for _ in []:
        pass
    else:
        print("    空循环也会执行 else（因为没有 break）")


# ============================================================
# 7. pass 与 ...
# ============================================================

def demo_pass():
    section("7. pass 与 ...")

    # pass 是【空语句】，什么都不做，但语法上必须有个东西占位
    x = 5
    if x > 0:
        pass                    # 先占位，以后再写
    else:
        print("负数")

    # 类/函数体不能为空，用 pass 占位
    class Empty:
        pass

    def not_implemented():
        pass

    print(f"  空类实例: {Empty()}")
    print(f"空函数返回: {not_implemented()!r}")

    # ...（Ellipsis）也能占位，语义上更强调"待实现"
    def todo():
        ...

    print(f"用 ... 占位的函数返回: {todo()!r}")
    print("  区别：pass 是语句，... 是表达式（是个真对象，类型 ellipsis）")

    # 循环中过滤掉某些分支时也常用
    for i in range(5):
        if i % 2 == 0:
            pass                # 偶数什么也不做
        else:
            print(f"  奇数 {i}")


# ============================================================
# 8. 推导式 —— 用表达式代替循环
# ============================================================

def demo_comprehensions():
    section("8. 推导式（循环的表达式化写法）")

    # 列表推导式：[表达式 for 变量 in 可迭代对象 if 条件]
    squares = [n ** 2 for n in range(6)]
    print(f"  列表推导式: {squares}")

    evens = [n for n in range(10) if n % 2 == 0]
    print(f"  带过滤: {evens}")

    pairs = [(x, y) for x in range(2) for y in range(2)]
    print(f"  双层循环: {pairs}")     # 相当于两层 for 嵌套

    # 嵌套推导式的顺序：外层 for 写前面，和普通 for 的书写顺序一致
    matrix = [[1, 2, 3], [4, 5, 6]]
    flat = [n for row in matrix for n in row]
    print(f"  展平矩阵: {flat}")

    # 字典推导式
    square_map = {n: n ** 2 for n in range(4)}
    print(f"  字典推导式: {square_map}")

    # 键值互换
    original = {"a": 1, "b": 2}
    swapped = {v: k for k, v in original.items()}
    print(f"  键值互换: {swapped}")

    # 集合推导式
    unique_lens = {len(w) for w in ["a", "bb", "cc", "ddd"]}
    print(f"  集合推导式: {unique_lens}")

    # 生成器表达式：用圆括号，惰性求值，省内存
    gen = (n ** 2 for n in range(10 ** 6))
    print(f"  生成器对象: {gen}")
    print(f"  取前 5 个: {[next(gen) for _ in range(5)]}")
    print("  ↑ 生成器不会一次算完，用多少算多少")

    # ⚠️ 推导式里的变量不会泄漏到外部（Python 3 的行为）
    n = 999
    _ = [n for n in range(3)]
    print(f"  推导式外部的 n 仍是 {n}")

    # ⚠️ 推导式适合简单逻辑；太复杂就该写回普通 for，可读性优先


# ============================================================
# 9. match / case —— 结构化模式匹配（Python 3.10+）
# ============================================================

def demo_match_case():
    section("9. match / case（Python 3.10+）")

    # match 不是 switch！它是【模式匹配】，能力远超 switch
    # 语法：match 值: 然后 case 模式:
    # 每个 case 自上而下匹配，匹配到第一个就停（不需要 break）

    def describe(value):
        match value:
            case 0:
                return "零"
            case 1 | 2 | 3:                # 或模式：匹配其中一个
                return "小数字"
            case int(n) if n < 0:          # 带守卫条件 if
                return f"负数 {n}"
            case int(n):                   # 捕获模式：把值绑定到 n
                return f"整数 {n}"
            case str(s) if len(s) > 5:
                return f"长字符串 {s!r}"
            case str(s):
                return f"短字符串 {s!r}"
            case [x, y]:                   # 序列模式：正好两个元素
                return f"二元组/列表 ({x}, {y})"
            case [x, *rest]:               # 星号模式：至少一个元素
                return f"非空序列，头={x}，余={rest}"
            case []:
                return "空序列"
            case {"type": "user", "name": name}:   # 映射模式
                return f"用户 {name}"
            case _:                        # 通配符：相当于 default
                return "其它"

    samples = [0, 2, -5, 42, "hi", "verylong", (1, 2), [1, 2, 3], [],
               {"type": "user", "name": "张三", "extra": 1}, None]
    for s in samples:
        print(f"  {s!r:>32} -> {describe(s)}")

    # ---- 字面量模式 / 常量 ----
    def classify(code):
        match code:
            case 200:
                return "OK"
            case 404:
                return "Not Found"
            case _:
                return "Other"

    print(f"  classify(200) = {classify(200)}")
    print(f"  classify(500) = {classify(500)}")

    # ---- 类模式：匹配对象的类型和属性 ----
    class Point:
        __match_args__ = ("x", "y")        # 允许位置参数匹配

        def __init__(self, x, y):
            self.x = x
            self.y = y

        def __repr__(self):
            return f"Point({self.x}, {self.y})"

    def locate(p):
        match p:
            case Point(0, 0):
                return "原点"
            case Point(x, 0):
                return f"X 轴上的点，x={x}"
            case Point(0, y):
                return f"Y 轴上的点，y={y}"
            case Point(x, y) if x == y:
                return f"对角线上的点 {x}"
            case Point(x, y):
                return f"普通点 ({x}, {y})"
            case _:
                return "不是点"

    for p in [Point(0, 0), Point(5, 0), Point(0, 3), Point(4, 4), Point(4, 7), "x"]:
        print(f"  {p!r:>14} -> {locate(p)}")

    # ⚠️ 几个必须知道的点：
    # 1. 没有 case 匹配上时，什么也不发生（不会报错）——建议总是写 case _:
    # 2. case 不会贯穿（不需要 break），和 C 的 switch 不同
    # 3. case 里捕获的变量会留在【当前作用域】：函数内是局部变量，模块级则泄漏到模块
    # 4. 想匹配"变量"必须用限定名（如 Color.RED），裸名字会被当作捕获模式！

    # 演示这个陷阱：裸变量名会被当成"捕获模式"而不是"常量比较"
    RED = "red"

    def match_bare_name(value):
        match value:
            case RED:                  # ⚠️ 不是和 "red" 比！这是【捕获模式】
                return f"匹配了一切；函数内的 RED 被绑定成 {RED!r}"
        return "永远到不了这里"

    print(f"  ⚠️ 裸变量名陷阱: match_bare_name('blue') -> {match_bare_name('blue')}")
    print("  ⚠️ 传的是 'blue' 却匹配成功，证明裸名字不是常量比较")
    print(f"  ✅ 函数外的 RED 不受影响，仍是 {RED!r}（捕获绑定在函数局部作用域）")

    # 正确写法：用【点号限定名】，Python 才会把它当常量
    class Color:
        RED = "red"

    def match_dotted_name(value):
        match value:
            case Color.RED:            # ✅ 点号限定名 -> 常量比较
                return "是红色"
            case _:
                return "不是红色"

    print(f"  ✅ 点号限定名: match_dotted_name('red')  -> {match_dotted_name('red')}")
    print(f"  ✅ 点号限定名: match_dotted_name('blue') -> {match_dotted_name('blue')}")
    print(f"  ✅ Color.RED 没有被覆盖: {Color.RED!r}")


# ============================================================
# 10. try / except / else / finally —— 异常流程
# ============================================================

def demo_try_except():
    section("10. try / except / else / finally")

    # 基本形式
    try:
        result = 10 / 0
    except ZeroDivisionError as e:       # as 把异常对象绑定给 e
        print(f"  捕获到: {type(e).__name__}: {e}")

    # ---- 捕获多种异常 ----
    for value in ["abc", None]:
        try:
            print(f"  int({value!r}) = {int(value)}")
        except (ValueError, TypeError) as e:    # 用元组并列多种类型
            print(f"  {value!r} 失败: {type(e).__name__}")

    # ---- 分开处理不同异常（按顺序匹配，先匹配先执行）----
    def safe_div(a, b):
        try:
            return a / b
        except ZeroDivisionError:
            print("    除数为零")
            return None
        except TypeError:
            print("    类型不对")
            return None

    safe_div(1, 0)
    safe_div("a", 1)

    # ---- else：try 里【没有发生异常】才执行 ----
    # 用途：把"可能出错的代码"和"出错后才不该跑的逻辑"分开
    try:
        value = int("42")
    except ValueError:
        print("  转换失败")
    else:
        print(f"  ✅ 没有异常，else 执行，value={value}")
    finally:
        print("  finally 无论如何都执行")

    # ---- finally：不管有没有异常、有没有 return 都执行 ----
    def with_finally():
        try:
            return "try 里的返回值"
        finally:
            print("  finally 在 return 之后、返回之前执行")

    print(f"  {with_finally()}")

    # ⚠️ finally 里的 return 会覆盖 try 里的 return（极危险，别这么写）
    def dangerous():
        try:
            return "try"
        finally:
            return "finally"        # ← 吞掉了 try 的返回值，还会吞掉异常

    print(f"  ⚠️ finally 里 return: {dangerous()}")

    # ---- 执行顺序总览 ----
    # 正常：      try 全部 -> else -> finally
    # 有异常：    try 中断 -> except -> finally
    # 未捕获：    try 中断 -> finally -> 异常继续往上抛
    # 有 return：try -> finally -> 真正返回

    # ---- 不要裸 except ----
    # except:                 ❌ 会吞掉 KeyboardInterrupt、SystemExit 等
    # except Exception:       ✅ 想兜底就用这个
    try:
        raise RuntimeError("示例异常")
    except Exception as e:
        print(f"  兜底捕获: {e}")

    # ---- 自定义异常 ----
    class MyError(Exception):
        pass

    try:
        raise MyError("我自己的错误")
    except MyError as e:
        print(f"  自定义异常: {e}")

    # ---- 异常链：raise ... from ... ----
    try:
        try:
            raise ValueError("底层原因")
        except ValueError as e:
            raise RuntimeError("上层包装") from e
    except RuntimeError as e:
        print(f"  异常链: {e}，原因: {e.__cause__}")


# ============================================================
# 11. raise —— 主动抛出异常
# ============================================================

def demo_raise():
    section("11. raise")

    # 抛出内置异常
    try:
        raise ValueError("值不合法")
    except ValueError as e:
        print(f"  {e}")

    # 抛出时不写异常类举例
    try:
        age = -1
        if age < 0:
            raise ValueError(f"年龄不能为负: {age}")
    except ValueError as e:
        print(f"  {e}")

    # ---- 裸 raise：重新抛出当前异常（常用于记录日志后继续抛）----
    try:
        try:
            raise KeyError("原始错误")
        except KeyError:
            print("  先记录一下，再原样抛出")
            raise
    except KeyError as e:
        print(f"  重新捕获: {e}")


# ============================================================
# 12. with —— 上下文管理器
# ============================================================

def demo_with():
    section("12. with 上下文管理器")

    # with 保证【无论如何都会执行清理】，比 try/finally 更简洁
    # 典型场景：文件、锁、数据库连接、网络会话

    # 文件操作的标准写法
    fake_file = io.StringIO("第一行\n第二行\n")
    with fake_file as f:
        content = f.read()
    print(f"  with 读文件: {content!r}")
    print(f"  退出 with 后文件已自动关闭: {f.closed}")

    # 等价于：
    # f = open(...)
    # try:
    #     ...
    # finally:
    #     f.close()

    # ---- 同时管理多个资源 ----
    with io.StringIO("a") as f1, io.StringIO("b") as f2:
        print(f"  两个资源: {f1.read()} / {f2.read()}")

    # ---- 自定义上下文管理器（类形式）----
    class Timer:
        def __enter__(self):
            print("    进入 with")
            return self                 # as 后面拿到的是 __enter__ 的返回值

        def __exit__(self, exc_type, exc_val, exc_tb):
            print("    退出 with")
            return False                # 返回 True 会吞掉异常，通常返回 False

    with Timer() as t:
        print("    正在执行")

    # ---- 自定义上下文管理器（生成器形式，更简洁）----
    @contextlib.contextmanager
    def tag(name):
        print(f"    <{name}>")
        try:
            yield name                  # yield 之前 = __enter__
        finally:
            print(f"    </{name}>")      # yield 之后 = __exit__

    with tag("div") as t:
        print("    内容")


# ============================================================
# 13. assert —— 断言
# ============================================================

def demo_assert():
    section("13. assert 断言")

    # assert 条件, 提示信息
    # 条件为假时抛 AssertionError
    x = 5
    assert x > 0, "x 必须为正数"
    print("  assert 通过了")

    try:
        assert x > 10, f"x 应该大于 10，实际是 {x}"
    except AssertionError as e:
        print(f"  断言失败: {e}")

    # ⚠️ 重要：用 python -O 运行时，assert 会被【整个删除】
    # 所以【绝不能用 assert 做输入校验】！它只用于开发期的内部不变量检查
    # 校验用户输入请用 if + raise


# ============================================================
# 14. return / yield —— 函数级流程控制
# ============================================================

def demo_return_yield():
    section("14. return / yield")

    # return：结束函数并返回值（不写则返回 None）
    def add(a, b):
        return a + b

    print(f"  add(1, 2) = {add(1, 2)}")

    # 返回多个值 = 返回元组
    def min_max(nums):
        return min(nums), max(nums)

    lo, hi = min_max([3, 1, 4, 1, 5])
    print(f"  多返回值: lo={lo}, hi={hi}")

    # return 可以提前退出，避免深层嵌套（叫"卫语句"）
    def process(user):
        if user is None:
            return "无用户"              # 提前返回
        if not user.get("active"):
            return "未激活"
        return "处理成功"

    print(f"  {process(None)} / {process({'active': True})}")

    # ---- yield：把函数变成生成器，可以"暂停"执行 ----
    def count_up(n):
        i = 0
        while i < n:
            yield i                     # 暂停在这里，把值交出去
            i += 1                      # 下次 next() 从这里继续

    gen = count_up(3)
    print(f"  生成器对象: {gen}")
    print(f"  逐个取出: {list(gen)}")

    # yield 的价值：惰性求值，处理大数据不占内存
    def read_lines(lines):
        for line in lines:
            yield line.strip()

    print(f"  生成器过滤: {list(read_lines(['  a  ', ' b ']))}")

    # ---- yield from：委托给另一个生成器 ----
    def chain():
        yield 1
        yield from [2, 3, 4]            # 把另一个可迭代对象的值逐个交出
        yield 5

    print(f"  yield from: {list(chain())}")


# ============================================================
# 15. 海象运算符 := （Python 3.8+）
# ============================================================

def demo_walrus():
    section("15. 海象运算符 :=")

    # 作用：在表达式内部【同时赋值和使用】，减少重复计算

    # 不用的写法：计算两次
    data = "hello world"
    if len(data) > 5:
        print(f"  长度 {len(data)}")      # len() 调了两次

    # 用海象：只算一次
    if (n := len(data)) > 5:
        print(f"  长度 {n}（只算了一次）")

    # 在 while 中读取（常见于读文件/读输入）
    lines = io.StringIO("a\nb\nc\n")
    while (line := lines.readline()):
        print(f"  读到: {line.strip()!r}")

    # 在推导式中过滤并复用
    values = ["1", "2", "x", "4"]
    valid = [v for item in values if (v := item).isdigit()]
    print(f"  推导式中的海象: {valid}")

    # ⚠️ 必须加括号：if n := len(data) 是语法错误


# ============================================================
# 16. 常见陷阱总结
# ============================================================

def demo_pitfalls():
    section("16. 常见陷阱总结")

    # ① 缩进错误：Python 靠缩进划分代码块
    x = 1
    if x:
        print("  正确缩进")
    # print("错误缩进")   # ← 去掉注释会导致 IndentationError

    # ② 混用 tab 和空格 -> TabError，统一用 4 空格

    # ③ if 后面忘写冒号 -> SyntaxError

    # ④ = 和 == 混淆
    # if x = 1: 是语法错误，应为 x == 1

    # ⑤ 循环中修改被遍历的列表（见第 3 节）

    # ⑥ while 忘写改变条件的语句 -> 死循环

    # ⑦ 裸 except 吞掉一切（含 Ctrl+C）

    # ⑧ 用 assert 做输入校验（-O 会删掉）

    # ⑨ 浮点数比较用 ==
    print(f"  0.1 + 0.2 == 0.3 ? {0.1 + 0.2 == 0.3}")
    print(f"  正确写法: {abs((0.1 + 0.2) - 0.3) < 1e-9}")

    # ⑩ 链式比较不能写成 C 风格
    # if x > 0 && x < 10:  ❌ Python 用 and，或者直接 0 < x < 10

    # ⑪ 修改集合时遍历它
    s = {1, 2, 3}
    # for v in s:
    #     s.remove(v)        # RuntimeError: Set changed size during iteration
    # 正确做法
    for v in list(s):
        print(f"  安全遍历集合副本: {v}")


# ============================================================
# 主函数
# ============================================================

def main():
    print(f"Python 流程控制语法全览")

    # demo_if_elif_else()
    # demo_ternary()
    # demo_for()
    # demo_while()
    # demo_break_continue()
    # demo_loop_else()
    # demo_pass()
    # demo_comprehensions()
    # demo_match_case()
    # demo_try_except()
    # demo_raise()
    # demo_with()
    # demo_assert()
    demo_return_yield()
    # demo_walrus()
    # demo_pitfalls()

    section("演示结束")
    print("流程控制语法演示完毕。")


if __name__ == "__main__":
    main()
