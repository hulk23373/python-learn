
# 3. list/tuple/range

# 列表，有序，可变，什么都能放
def test_list():
    l1 = [1, 2, "3"]
    print(l1)
    l2 = [x * 2 for x in range(6) if x // 3 == 1]
    print(l2)
    a = 2
    print(f"{a in l1}")
    print(f"{a not in l2}")

# 元组，有序，不可变
def test_tuple():
    t1 = (3, 4)
    # 省略括号
    t2 = 1, 3, 5
    # 解包
    x, y, z = t2
    a, *b = t2
    print(f"{x, y, z}")
    print(f"{a, b}")

# 懒生成数列
def test_range():
    a = range(10)
    b = range(2, 10)
    c = range(1, 10, 3)
    print(f"{[x for x in a]}")
    print(f"{[x for x in b]}")
    print(f"{[x for x in c]}")

# set/frozenset，无序，不重复，哈希表
def test_set():
    s1 = {1, 1, 2, 3}
    print(s1)
    # 空set
    s2 = set()
    s2.add(1)
    print(s2)
    # 不可变
    s3 = frozenset([1, 2, 3, 3, 3, 4])
    print(s3)

# dict，键值对，可变，hash
def test_dict():
    person = {"name": "张三", "age": 25, "city": "北京"}
    person.setdefault("sex", "男")
    name = person.get("name")
    print(person)
    print(f"name={name}")
    # items吐出元组，然后解包
    for key, value in person.items():
        print(key, value)

# boolean/none
def test_none_boolean():
    x = "123"
    # None 是单例，is判断是否是同一个对象，==判断值是否相等
    if x is not None:
        print(f"{x}")
        print(f"{x!r}")
    # 空的东西是假的
    print(f"{0 or 'default'}")

# type/isinstance：类型检查
def test_type():
    x = "123"
    print(f"{type(x).__name__}")
    print(f"{type(x) is str}")
    # 严格类型检查
    print(f"{type(True) is int}")
    # 考虑继承关系
    print(isinstance(True, int))

# 哪些类型支持切片
# 切片是**序列（sequence）**的通用能力，不是 list 专属：
#
# 类型	切片结果
# list	新 list
# str	新 str（字符串"复制"没意义，因为不可变）
# tuple	新 tuple
# bytes / bytearray	同类型
# range	新 range（range(10)[2:5] → range(2, 5)）
# dict / set	❌ 不支持（无序，没有"第几个"的概念）
def test_slice():
    a = "abcdefg "
    print(f"{a[:]!r}")  # 复制整个列表（浅拷贝）
    print(f"{a[::-1]!r}")  # 反转
    print(f"{a[-3:]!r}")  # 最后三个
    print(f"{a[:-1]!r}")  # 去掉最后一个
    print(f"{a[1:]!r}")  # 去掉第一个
    print(f"{a[::2]!r}")  # 取偶数位置
    print(f"{a[1::2]!r}")  # 取奇数位置
    print(f"{a[1:8:2]!r}")  # 切片
    print(f"{a.strip()!r}")  # （字符串常用）不是切片，别混

# 类型转换
def test_exchange():
    str = "3"
    i = int(str)
    f = float(str)
    print(i)
    print(f)

def main():
    print(f"{'=' * 20}")
    # test_list()
    # test_tuple()
    # test_range()
    # test_set()
    # test_dict()
    # test_none_boolean()
    # test_type()
    test_slice()
    test_exchange()

if __name__ == "__main__":
    main()