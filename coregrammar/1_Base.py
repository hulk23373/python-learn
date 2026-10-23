"""
Python 基础数据类型全览与演示

Python 的内置数据类型大致分为以下几类：
    1. 数字类型   : int, float, complex, bool
    2. 序列类型   : str, list, tuple, range, bytes, bytearray
    3. 集合类型   : set, frozenset
    4. 映射类型   : dict
    5. 二进制类型 : bytes, bytearray, memoryview
    6. 特殊类型   : NoneType, 以及各类可调用/模块对象

本文件通过大量变量声明和实际使用，演示这些类型的基本用法。
"""

import sys
import decimal
import fractions
import datetime
from collections import namedtuple, OrderedDict, defaultdict, Counter, deque


def section(title):
    """打印分节标题，方便阅读输出"""
    print(f"\n{'=' * 60}\n{title}\n{'=' * 60}")


# ============================================================
# 1. 数字类型 (Numeric Types)
# ============================================================

def demo_numbers():
    section("1. 数字类型")

    # bool 是 int 的子类，先声明后面会用到
    is_student = True          # bool：布尔型（注意大写 True/False）
    is_graduated = False

    # int：整数，Python 3 中 int 没有大小限制（任意精度）
    age = 25
    temperature = -40
    big_number = 123_456_789_012_345_678_901_234_567_890  # 下划线只是可读性分隔符
    binary_num = 0b1010        # 二进制 -> 10
    octal_num = 0o17           # 八进制 -> 15
    hex_num = 0xFF             # 十六进制 -> 255

    # float：浮点数，双精度 64 位，存在精度问题
    height = 1.75
    pi = 3.141592653589793
    scientific = 6.02e23       # 科学计数法：6.02 * 10^23
    infinity = float("inf")    # 正无穷
    not_a_number = float("nan")  # 非数字 NaN

    # complex：复数（实部 + 虚部，虚部用 j 表示）
    z1 = 3 + 4j
    z2 = complex(2, -5)

    print(f"is_student      = {is_student!r:>10}  type={type(is_student).__name__}")
    print(f"is_graduated    = {is_graduated!r:>10}  type={type(is_graduated).__name__}")
    print(f"age             = {age!r:>10}  type={type(age).__name__}")
    print(f"temperature     = {temperature!r:>10}")
    print(f"big_number      = {big_number!r}")
    print(f"binary/octal/hex= {binary_num} / {octal_num} / {hex_num}")
    print(f"height          = {height!r:>10}")
    print(f"pi              = {pi!r}")
    print(f"scientific      = {scientific!r}")
    print(f"infinity        = {infinity!r}")
    print(f"not_a_number    = {not_a_number!r}")
    print(f"z1              = {z1!r}  real={z1.real}, imag={z1.imag}")
    print(f"z2              = {z2!r}  |z2|={abs(z2):.4f}")

    # 数值运算
    print(f"\n整数除法 7 // 2 = {7 // 2}（向下取整）")
    print(f"真除法   7 / 2  = {7 / 2}（结果永远是 float）")
    print(f"取模     7 % 3  = {7 % 3}")
    print(f"幂运算   2 ** 10 = {2 ** 10}")
    print(f"科学计数输入 6.02e23 实际存储 = {scientific}")
    print(f"0.1 + 0.2 = {0.1 + 0.2!r}  ← 浮点精度问题")
    print(f"用 decimal 解决: {decimal.Decimal('0.1') + decimal.Decimal('0.2')!r}")
    print(f"用 fractions 表示 1/3: {fractions.Fraction(1, 3)!r}")

    # 类型转换
    print(f"\nint('42')      = {int('42')!r}")
    print(f"int(3.99)      = {int(3.99)!r}（截断，非四舍五入）")
    print(f"float('1.5')   = {float('1.5')!r}")
    print(f"bool('')       = {bool('')!r}，bool('a') = {bool('a')!r}")
    print(f"complex(1, 2)  = {complex(1, 2)!r}")


# ============================================================
# 2. 字符串 (str) 与二进制序列 (bytes / bytearray)
# ============================================================

def demo_strings_and_bytes():
    section("2. 字符串与二进制序列")

    # str：不可变的 Unicode 字符序列
    age = 25
    name = "张三"
    greeting = 'Hello, World!'
    multiline = """这是
多行
字符串"""
    raw_string = r"C:\Users\name\Desktop"   # 原始字符串，反斜杠不转义
    escaped = "第一行\n第二行\t制表符\\反斜杠"
    repeated = "ab" * 3
    concatenated = "Hello" + ", " + "Python"
    formatted = f"我叫{name}，今年{age}岁"   # f-string 格式化

    print(f"name            = {name!r}")
    print(f"greeting        = {greeting!r}")
    print(f"multiline       = {multiline!r}")
    print(f"raw_string      = {raw_string!r}")
    print(f"escaped         = {escaped!r}")
    print(f"repeated        = {repeated!r}")
    print(f"concatenated    = {concatenated!r}")
    print(f"formatted       = {formatted!r}")

    # 索引与切片：索引从 0 开始，负数从末尾算
    s = "Python"
    print(f"\n")
    print(f"s = {s!r}")
    print(f"s[0]={s[0]!r}  s[-1]={s[-1]!r}  s[1:4]={s[1:4]!r}  s[::-1]={s[::-1]!r}")

    # 常用方法
    text = "  Hello Python World  "
    print(f"\nstrip()       = {text.strip()!r}")
    print(f"upper()       = {text.upper()!r}")
    print(f"lower()       = {text.lower()!r}")
    print(f"split()       = {text.strip().split()!r}")
    print(f"replace()     = {text.strip().replace('Python', 'Java')!r}")
    print(f"find('Python')= {text.find('Python')}")
    print(f"startswith()  = {text.strip().startswith('Hello')}")
    print(f"join()        = {'-'.join(['a', 'b', 'c'])!r}")
    print(f"len()         = {len(text)}")
    print(f"isdigit()     = {'123'.isdigit()}，isalpha() = {'abc'.isalpha()}")
    print(f"zfill()       = {'42'.zfill(5)!r}")
    print(f"格式化         = {'{}-{:.3f}'.format('pi', 3.14159)!r}")

    # bytes：不可变字节序列；bytearray：可变字节序列
    raw_bytes = b"hello"                       # bytes 字面量
    encoded = "中文".encode("utf-8")            # 字符串编码为 bytes
    from_hex = bytes.fromhex("48656c6c6f")     # 从十六进制构造
    mutable_bytes = bytearray(b"hello")        # 可变版本

    print(f"\nraw_bytes       = {raw_bytes!r}  type={type(raw_bytes).__name__}")
    print(f"encoded         = {encoded!r}（'中文' UTF-8 编码，共 {len(encoded)} 字节）")
    print(f"from_hex        = {from_hex!r}")
    print(f"decode 回来      = {encoded.decode('utf-8')!r}")
    print(f"mutable_bytes   = {mutable_bytes!r}")
    mutable_bytes[0] = ord("H")                # bytearray 可以原地修改
    print(f"修改后           = {mutable_bytes!r}")

    # memoryview：无需拷贝地访问二进制数据的缓冲区
    mv = memoryview(raw_bytes)
    print(f"memoryview      = {mv!r}  mv[0]={mv[0]}（'h' 的 ASCII 码）")



# ============================================================
# 3. 序列类型：list / tuple / range
# ============================================================

def demo_sequences():
    section("3. 序列类型：list / tuple / range")

    # list：可变、有序、可重复、可混合类型
    fruits = ["apple", "banana", "cherry"]
    numbers = [1, 2, 3, 4, 5]
    mixed = [1, "two", 3.0, True, None, [1, 2], {"k": "v"}]   # 可以放任意类型
    nested = [[1, 2], [3, 4], [5, 6]]
    empty_list = []
    from_range = list(range(5))
    squares = [x ** 2 for x in range(6)]            # 列表推导式
    evens = [x for x in range(10) if x % 2 == 0]    # 带条件的推导式
    from_string = [x for x in "python"]             # 从字符串

    events2 = [x for x in range(20) if x % 3 == 1]

    print(f"fruits        = {fruits}")
    print(f"numbers       = {numbers}")
    print(f"mixed         = {mixed}")
    print(f"nested        = {nested}")
    print(f"empty_list    = {empty_list}")
    print(f"from_range    = {from_range}")
    print(f"squares       = {squares}")
    print(f"evens         = {evens}")
    print(f"from_string     = {from_string}")
    print(f"events2       = {events2}")

    # 增删改查
    fruits.append("date")           # 尾部追加
    fruits.insert(0, "avocado")     # 指定位置插入
    fruits.remove("banana")         # 按值删除
    popped = fruits.pop()           # 弹出末尾
    fruits[0] = "pear"              # 按下标修改
    fruits.extend(["elderberry"])   # 批量追加
    print(f"\n操作后 fruits  = {fruits}（pop 出 {popped!r}）")
    print(f"fruits[1:3]   = {fruits[1:3]}")
    print(f"len/sorted    = {len(fruits)} / {sorted(fruits)}")
    print(f"'pear' in     = {'pear' in fruits}，index = {fruits.index('pear')}")
    print(f"count('x')    = {fruits.count('pear')}")
    fruits.sort(reverse=True)
    print(f"原地倒序排序   = {fruits}")
    fruits.reverse()
    print(f"reverse()     = {fruits}")
    print(f"嵌套访问       = {nested[1][1]}")

    # tuple：不可变、有序，可作字典的键；常用来表示固定结构
    point = (3, 4)
    rgb = (255, 128, 0)
    single_tuple = (42,)            # 单元素元组必须带逗号！
    empty_tuple = ()
    packed = 1, 2, 3                # 括号可省略
    x, y, z = packed                # 解包
    a, *rest = packed               # 星号解包
    tuple_from_list = tuple([1, 2, 3])

    print(f"\npoint         = {point}, rgb = {rgb}")
    print(f"single_tuple  = {single_tuple!r}（注意逗号）")
    print(f"empty_tuple   = {empty_tuple!r}")
    print(f"packed/解包    = {packed} -> x={x}, y={y}, z={z}")
    print(f"星号解包       = a={a}, rest={rest}")
    print(f"tuple列表      = {tuple_from_list}")
    print(f"索引/切片      = {point[0]} / {packed[1:]}")
    print(f"tuple 可哈希   = {hash(point) != 0}")

    # range：惰性的等差数列，常用于循环
    r1 = range(5)           # 0..4
    r2 = range(2, 10)       # 2..9
    r3 = range(0, 10, 3)    # 0,3,6,9
    r4 = range(10, 0, -2)   # 10,8,6,4,2
    print(f"\nrange(5)         = {list(r1)}")
    print(f"range(2, 10)     = {list(r2)}")
    print(f"range(0, 10, 3)  = {list(r3)}")
    print(f"range(10, 0, -2) = {list(r4)}")
    print(f"range 是最省内存的: {sys.getsizeof(range(10**6))} 字节 "
          f"vs list: {sys.getsizeof(list(range(1000)))} 字节（1000 个元素）")


# ============================================================
# 4. 集合类型：set / frozenset
# ============================================================

def demo_sets():
    section("4. 集合类型：set / frozenset")

    # set：可变、无序、不重复
    unique_nums = {1, 2, 3, 4, 5}
    duplicates_removed = {1, 1, 2, 2, 3}          # 自动去重
    from_list = set([1, 2, 2, 3, 3, 3])
    empty_set = set()                              # 注意 {} 是空字典，不是空集合
    letters = set("hello")                         # 从字符串构造

    print(f"unique_nums       = {unique_nums}")
    print(f"duplicates_removed= {duplicates_removed}（自动去重）")
    print(f"from_list         = {from_list}")
    print(f"empty_set         = {empty_set!r}")
    print(f"letters           = {letters}（'hello' 去重）")

    # 增删
    unique_nums.add(6)
    unique_nums.discard(1)     # 不存在也不报错
    unique_nums.remove(2)      # 不存在会报错
    print(f"\nadd/discard 后     = {unique_nums}")
    print(f"remove(2) 会抛异常，discard 不会")

    # 集合运算
    A = {1, 2, 3, 4}
    B = {3, 4, 5, 6}
    print(f"\nA = {A}, B = {B}")
    print(f"并集 A | B        = {A | B}   (union)")
    print(f"交集 A & B        = {A & B}   (intersection)")
    print(f"差集 A - B        = {A - B}   (difference)")
    print(f"对称差 A ^ B      = {A ^ B}   (symmetric_difference)")
    print(f"子集 A <= B       = {A <= B}")
    print(f"超集 A >= {{1,2}}  = {A >= {1, 2}}")
    print(f"是否不相交         = {A.isdisjoint({7, 8})}")

    # set 的典型用途：去重 和 成员测试（O(1)）
    data = [1, 2, 2, 3, 3, 3, 4]
    print(f"\n列表去重           = {list(set(data))}")
    print(f"'x' in {{...}} 是 O(1) 平均复杂度")

    # frozenset：不可变集合，可哈希，能作为字典的键或放进 set
    fs = frozenset([1, 2, 3])
    fs2 = frozenset("abc")
    set_of_sets = {frozenset([1, 2]), frozenset([3, 4])}   # set 里不能放 set，但能放 frozenset
    dict_with_fs_key = {fs: "frozen 集合作为键"}
    print(f"\nfrozenset([1,2,3])       = {fs}")
    print(f"frozenset('abc')         = {fs2}")
    print(f"set 中的 frozenset        = {set_of_sets}")
    print(f"frozenset 作字典键         = {dict_with_fs_key[fs]!r}")
    print(f"不可变所以可哈希           = {hash(fs) != 0}")


# ============================================================
# 5. 映射类型：dict
# ============================================================

def demo_dicts():
    section("5. 映射类型：dict")

    # dict：键值对，键必须可哈希，Python 3.7+ 保持插入顺序
    person = {"name": "张三", "age": 25, "city": "北京"}
    empty_dict = {}
    from_pairs = dict([("a", 1), ("b", 2)])
    from_kwargs = dict(name="李四", age=30)
    nested_dict = {"user": {"id": 1, "tags": ["a", "b"]}}
    comprehension = {x: x ** 2 for x in range(5)}          # 字典推导式
    dict_from_keys = dict.fromkeys(["x", "y", "z"], 0)     # 统一初始化

    print(f"person        = {person}")
    print(f"empty_dict    = {empty_dict}")
    print(f"from_pairs    = {from_pairs}")
    print(f"from_kwargs   = {from_kwargs}")
    print(f"nested_dict   = {nested_dict}")
    print(f"comprehension = {comprehension}")
    print(f"from_keys     = {dict_from_keys}")

    # 访问
    print(f"\nperson['name']        = {person['name']}")
    print(f"person.get('phone')   = {person.get('phone')}（不存在返回 None，不报错）")
    print(f"person.get('phone','无') = {person.get('phone', '无')}")
    print(f"'age' in person       = {'age' in person}")
    print(f"keys()                = {list(person.keys())}")
    print(f"values()              = {list(person.values())}")
    print(f"items()               = {list(person.items())}")
    print(f"嵌套访问               = {nested_dict['user']['tags'][0]!r}")

    # 增删改
    person["email"] = "zhangsan@example.com"    # 新增
    person["age"] = 26                          # 修改
    person.setdefault("country", "中国")         # 不存在才设置
    person.update({"gender": "男", "age": 27})   # 批量更新
    removed = person.pop("email")               # 删除并返回值
    del person["gender"]                        # 删除
    print(f"\n操作后 person   = {person}")
    print(f"pop 出          = {removed!r}")

    # 遍历
    print("\n遍历 items():")
    for key, value in person.items():
        print(f"    {key}: {value}")

    # 合并（Python 3.9+ 的 | 运算符）
    merged = {"a": 1, "b": 2} | {"b": 3, "c": 4}
    print(f"\n字典合并  | 运算符 = {merged}（右边覆盖左边）")
    print(f"counter 计数示例   = {Counter('abracadabra')}")
    print(f"defaultdict 示例   = {defaultdict(list, {'a': [1]})['b']}")
    print(f"OrderedDict 示例   = {OrderedDict([('one', 1), ('two', 2)])}")

    # namedtuple：带字段名的元组（属于 tuple 的子类，但常与 dict 对比使用）
    Point = namedtuple("Point", ["x", "y"])
    p = Point(10, 20)
    print(f"\nnamedtuple      = {p}  p.x={p.x}, p.y={p.y}（可读性比普通 tuple 好）")

    # deque：双端队列（可变序列）
    dq = deque([1, 2, 3])
    dq.appendleft(0)
    dq.append(4)
    print(f"deque           = {dq}（两端 O(1) 插入/删除）")


# ============================================================
# 6. 布尔与 None
# ============================================================

def demo_bool_and_none():
    section("6. 布尔类型与 None")

    flag_true = True
    flag_false = False
    nothing = None                      # NoneType，只有一个实例

    # 各类型的“假值”（falsy）
    falsy_values = [False, None, 0, 0.0, 0j, "", [], (), {}, set(), range(0)]
    print("以下值在布尔上下文中均为 False：")
    for v in falsy_values:
        print(f"    {v!r:>10}  ->  bool = {bool(v)}")

    # 其余都为 True
    truthy_values = [True, 1, -1, 0.1, "a", " ", [0], (0,), {"k": 0}, {0}]
    print("\n以下值均为 True（注意 [0] 和 \" \" 也是真值）：")
    for v in truthy_values:
        print(f"    {v!r:>10}  ->  bool = {bool(v)}")

    # 布尔运算
    print(f"\nTrue and False = {flag_true and flag_false}")
    print(f"True or False  = {flag_true or flag_false}")
    print(f"not True       = {not flag_true}")
    print(f"短路求值        = {0 or 'default'}（0 为假，返回右边）")
    print(f"短路求值        = {'value' and 'next'}（左边为真，返回右边）")

    # None 的使用
    print(f"\nNone is None            = {nothing is None}（判断 None 永远用 is）")
    print(f"type(None).__name__     = {type(None).__name__}")
    print(f"bool(None)              = {bool(None)}")
    print(f"None 是单例              = {None is None}，id 相同")
    print(f"函数无返回值时默认返回     = {demo_returns_nothing()!r}")


def demo_returns_nothing():
    """没有 return 语句的函数，默认返回 None"""
    pass


# ============================================================
# 7. 类型检查与类型信息
# ============================================================

def demo_type_introspection():
    section("7. 类型检查与类型信息")

    samples = [
        ("int", 42),
        ("float", 3.14),
        ("complex", 1 + 2j),
        ("bool", True),
        ("str", "hello"),
        ("bytes", b"hello"),
        ("bytearray", bytearray(b"hi")),
        ("memoryview", memoryview(b"hi")),
        ("list", [1, 2]),
        ("tuple", (1, 2)),
        ("range", range(3)),
        ("set", {1, 2}),
        ("frozenset", frozenset([1, 2])),
        ("dict", {"a": 1}),
        ("NoneType", None),
    ]

    print(f"{'值':<20} {'type()':<25} {'isinstance 其他':<20}")
    print("-" * 70)
    for label, value in samples:
        t = type(value).__name__
        extra = ""
        if isinstance(value, int) and not isinstance(value, bool):
            extra = "int 是 numbers.Integral"
        elif isinstance(value, bool):
            extra = "bool 是 int 的子类"
        elif isinstance(value, (list, tuple, range)):
            extra = "Sequence"
        elif isinstance(value, (set, frozenset)):
            extra = "Set"
        elif isinstance(value, dict):
            extra = "Mapping"
        print(f"{label:<20} {t:<25} {extra:<20}")

    # isinstance 与 type 的区别
    print(f"\ntype(True) is int        -> {type(True) is int}（bool 是 int 子类，但 type 判定严格）")
    print(f"isinstance(True, int)    -> {isinstance(True, int)}（会考虑继承关系）")
    print(f"isinstance(1, (str, int))-> {isinstance(1, (str, int))}（可传元组批量判断）")

    # 可变 vs 不可变
    immutable = (int, float, complex, bool, str, bytes, tuple, frozenset, range, type(None))
    mutable = (list, dict, set, bytearray)
    print(f"\n不可变类型（可作为 dict 的键）: {', '.join(t.__name__ for t in immutable)}")
    print(f"可变类型（不能作 dict 的键）  : {', '.join(t.__name__ for t in mutable)}")

    # 其他常用内置类型
    other_types = {
        "function": demo_numbers,
        "module": sys,
        "class/type": int,
        "method": "abc".upper,
        "generator": (x for x in range(3)),
        "range iterator": iter(range(3)),
        "zip": zip([1], [2]),
        "map": map(str, [1, 2]),
        "filter": filter(None, [1, 0, 2]),
        "enumerate": enumerate(["a"]),
        "slice": slice(1, 5, 2),
        "ellipsis": ...,
        "datetime": datetime.datetime.now(),
    }
    print("\n其他常见内置对象类型：")
    for label, obj in other_types.items():
        print(f"    {label:<16} -> {type(obj).__name__}")


# ============================================================
# 主函数
# ============================================================

def main():
    print(f"Python 版本: {sys.version.split()[0]}")
    print(f"整数最大值信息: sys.maxsize = {sys.maxsize}（仅表示指针大小，Python int 本身无上限）")

    # demo_numbers()
    # demo_strings_and_bytes()
    # demo_sequences()
    # demo_sets()
    # demo_dicts()
    # demo_bool_and_none()
    demo_type_introspection()

    section("演示结束")
    print("所有内置数据类型演示完毕。")


if __name__ == "__main__":
    main()
