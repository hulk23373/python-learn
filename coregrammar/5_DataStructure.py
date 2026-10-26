"""
Python 数据结构全览

数据结构 = 数据的组织方式。选对结构，代码又短又快；选错结构，程序会莫名变慢。

本文件覆盖：
    1. 总览与复杂度           : 先建立"什么场景选什么"的地图
    2. list  动态数组         : 栈 (Stack)
    3. deque 双端队列         : 队列 (Queue)
    4. tuple / namedtuple     : 不可变记录
    5. dict  哈希表           : 映射、计数、分组
    6. set   集合             : 去重、成员测试、集合运算
    7. heapq 堆               : 优先队列、Top-K
    8. 栈的应用               : 括号匹配、逆波兰表达式
    9. 队列的应用             : BFS 广度优先搜索
   10. 链表                   : 手写单链表
   11. 二叉树                 : 遍历、二叉搜索树
   12. 图                     : 邻接表、DFS / BFS
   13. 排序                   : 冒泡、快排、归并、内置 sorted
   14. 查找                   : 线性查找、二分查找
   15. 选择指南               : 一张表决定用什么

复杂度记号：
    O(1)    常数时间，和数据量无关
    O(log n) 对数时间，数据翻倍只多一步（二分）
    O(n)    线性时间，数据翻倍时间翻倍
    O(n log n) 排序的典型复杂度
    O(n^2)  平方时间，数据翻倍时间四倍（双层循环）
"""

import heapq
import bisect
import time
from collections import deque, Counter, defaultdict, OrderedDict, namedtuple


def section(title):
    """打印分节标题"""
    print(f"\n{'=' * 64}\n{title}\n{'=' * 64}")


# ============================================================
# 1. 总览与复杂度
# ============================================================

def demo_overview():
    section("1. 数据结构总览与复杂度")

    table = [
        # (结构, 随机访问, 查找, 头部插入, 尾部插入, 有序, 可变, 典型用途)
        ("list",  "O(1)", "O(n)",   "O(n)",   "O(1)", "是", "是", "数组、栈、有序序列"),
        ("tuple", "O(1)", "O(n)",   "—",      "—",    "是", "否", "固定记录、可作键"),
        ("deque", "O(n)", "O(n)",   "O(1)",   "O(1)", "是", "是", "队列、双端操作"),
        ("dict",  "—",    "O(1)",   "O(1)",   "O(1)", "是*", "是", "映射、计数、索引"),
        ("set",   "—",    "O(1)",   "O(1)",   "O(1)", "否", "是", "去重、成员测试"),
        ("heapq", "—",    "O(n)",   "O(log n)", "O(log n)", "否", "是", "优先队列、Top-K"),
    ]

    header = f"{'结构':<7}{'随机访问':<10}{'查找':<9}{'头部插入':<11}{'尾部插入':<11}{'有序':<6}{'可变':<6}用途"
    print("  " + header)
    print("  " + "-" * 72)
    for row in table:
        print(f"  {row[0]:<7}{row[1]:<10}{row[2]:<9}{row[3]:<11}{row[4]:<11}{row[5]:<6}{row[6]:<6}{row[7]}")

    print("\n  * dict 保持插入顺序（Python 3.7+），但不是按值排序")

    # 实测：为什么复杂度重要
    print("\n  实测：在 10 万个元素里查找 1000 次")
    data_list = list(range(100_000))
    data_set = set(data_list)
    data_dict = {x: x for x in data_list}

    for name, container in [("list", data_list), ("set", data_set), ("dict", data_dict)]:
        start = time.perf_counter()
        for _ in range(1000):
            99_999 in container
        print(f"    {name:<5} 耗时 {time.perf_counter() - start:.5f} 秒")

    # 实测：list.pop(0) 的隐藏代价
    print("\n  实测：从头部删除 1 万次")
    start = time.perf_counter()
    lst = list(range(20_000))
    while len(lst) > 10_000:
        lst.pop(0)
    print(f"    list.pop(0)     耗时 {time.perf_counter() - start:.4f} 秒  ← O(n)")

    start = time.perf_counter()
    dq = deque(range(20_000))
    while len(dq) > 10_000:
        dq.popleft()
    print(f"    deque.popleft() 耗时 {time.perf_counter() - start:.5f} 秒  ← O(1)")


# ============================================================
# 2. list：动态数组与栈
# ============================================================

def demo_list_stack():
    section("2. list 动态数组 + 栈 Stack")

    # list 底层是"动态数组"：一块连续内存，满了就扩容
    # 随机访问 arr[i] 是 O(1)，但中间插入/删除是 O(n)（要搬动后面的元素）

    arr = [10, 20, 30, 40, 50]
    print(f"  arr = {arr}")
    print(f"  arr[2]        = {arr[2]}      O(1) 随机访问")
    print(f"  arr[-1]       = {arr[-1]}")
    print(f"  arr[1:4]      = {arr[1:4]}")
    print(f"  len(arr)      = {len(arr)}")

    # 尾部操作是 O(1)（均摊），这是 list 最擅长的
    arr.append(60)
    print(f"  append(60)    = {arr}")
    print(f"  pop()         = {arr.pop()}  ← 从尾部弹出，O(1)")

    # ⚠️ 中间插入/删除是 O(n)
    arr.insert(0, 5)
    print(f"  insert(0, 5)  = {arr}  ← O(n)，要搬动所有元素")
    removed = arr.pop(0)
    print(f"  pop(0)        = {removed}   ← O(n)，不推荐")

    # ---- 栈：后进先出 LIFO ----
    # 栈就是"只在同一端进出"的列表，list 天然适合
    print("\n  栈 Stack（LIFO，后进先出）:")
    stack = []
    for x in [1, 2, 3]:
        stack.append(x)
        print(f"    push({x}) -> {stack}")

    print(f"    peek()  -> {stack[-1]}  （只看栈顶，不弹出）")
    while stack:
        print(f"    pop()   -> {stack.pop()}，剩余 {stack}")

    # 用栈的典型场景：撤销操作、函数调用栈、括号匹配

    # ---- 列表推导式与常用方法 ----
    nums = [3, 1, 4, 1, 5, 9, 2, 6]
    print(f"\n  常用操作 (nums = {nums}):")
    print(f"    sorted()      = {sorted(nums)}")
    print(f"    min/max/sum   = {min(nums)} / {max(nums)} / {sum(nums)}")
    print(f"    出现 1 的次数  = {nums.count(1)}")
    print(f"    第一个 5 的下标 = {nums.index(5)}")
    print(f"    倒序          = {nums[::-1]}")

    # ⚠️ sort() 原地排序返回 None，sorted() 返回新列表
    nums_copy = nums.copy()
    result = nums_copy.sort()
    print(f"    nums.sort() 的返回值 = {result!r}  ← 原地修改，返回 None")


# ============================================================
# 3. deque：队列
# ============================================================

def demo_queue():
    section("3. deque 双端队列 + 队列 Queue")

    # 队列：先进先出 FIFO
    # 用 list 实现队列的经典错误是 list.pop(0)，每次 O(n)
    # 正确工具是 collections.deque，两端操作都是 O(1)

    print("  deque 两端操作都是 O(1):")
    dq = deque([2, 3])
    dq.appendleft(1)          # 左端插入
    dq.append(4)              # 右端插入
    print(f"    appendleft(1), append(4) -> {dq}")
    print(f"    popleft() -> {dq.popleft()}")
    print(f"    pop()     -> {dq.pop()}")
    print(f"    剩余       -> {dq}")

    # ---- 队列：只用 append / popleft ----
    print("\n  队列 Queue（FIFO，先进先出）:")
    queue = deque()
    for name in ["任务A", "任务B", "任务C"]:
        queue.append(name)
        print(f"    enqueue({name}) -> {list(queue)}")

    while queue:
        print(f"    dequeue() -> {queue.popleft()}，剩余 {list(queue)}")

    # ---- deque 的其他实用能力 ----
    print("\n  deque 的其它用法:")
    d = deque([1, 2, 3, 4, 5], maxlen=5)     # 固定长度，满了自动挤掉另一端
    print(f"    deque(maxlen=5) = {d}")
    d.append(6)
    print(f"    append(6) 后    = {d}  ← 自动挤掉最左边的 1")
    d.extend([7, 8])
    print(f"    extend([7,8])   = {d}")
    d.rotate(2)                # 整体右移
    print(f"    rotate(2)       = {d}")
    d.rotate(-2)
    print(f"    rotate(-2)      = {d}")

    # 典型用途：滑动窗口、任务队列、BFS、撤销重做


# ============================================================
# 4. tuple / namedtuple：不可变记录
# ============================================================

def demo_tuple():
    section("4. tuple / namedtuple 不可变记录")

    # tuple 适合表示"固定结构的记录"
    point = (3, 4)
    rgb = (255, 128, 0)
    record = ("张三", 25, "北京")

    print(f"  point  = {point}")
    print(f"  rgb    = {rgb}")
    print(f"  record = {record}")

    # 解包让 tuple 很好用
    name, age, city = record
    print(f"  解包: name={name}, age={age}, city={city}")

    # 不可变 -> 可哈希 -> 能作字典的键
    distances = {
        (0, 0): "原点",
        (1, 0): "东",
        (0, 1): "北",
    }
    print(f"  tuple 作键: distances[(1, 0)] = {distances[(1, 0)]}")

    # namedtuple：给每个位置起名字，可读性比下标好得多
    Point = namedtuple("Point", ["x", "y"])
    p = Point(10, 20)
    print(f"\n  namedtuple:")
    print(f"    p        = {p}")
    print(f"    p.x      = {p.x}, p.y = {p.y}")
    print(f"    仍然能解包: x={p[0]}, y={p[1]}")
    print(f"    类型      = {type(p).__name__}")
    print(f"    仍然是 tuple: {isinstance(p, tuple)}")
    print(f"    可哈希    = {hash(p) != 0}")

    # 对比：dict 更灵活但有额外开销；namedtuple 更轻量、不可变
    print("\n  namedtuple vs dict:")
    print("    namedtuple: 轻量、不可变、可按属性访问、可作键")
    print("    dict      : 灵活、可变、键是字符串、有哈希开销")


# ============================================================
# 5. dict：哈希表
# ============================================================

def demo_dict():
    section("5. dict 哈希表")

    # dict 底层是哈希表：查找、插入、删除平均都是 O(1)
    # 代价是占内存较多，且键必须可哈希（不可变）

    # ---- 创建方式 ----
    d1 = {"a": 1, "b": 2}
    d2 = dict(a=1, b=2)
    d3 = dict([("a", 1), ("b", 2)])
    d4 = {k: v for k, v in [("a", 1), ("b", 2)]}
    d5 = dict.fromkeys(["a", "b"], 0)

    print(f"  字面量        {d1}")
    print(f"  dict(kwargs)  {d2}")
    print(f"  dict(pairs)   {d3}")
    print(f"  推导式        {d4}")
    print(f"  fromkeys      {d5}")

    # ---- 访问：优先用 get ----
    user = {"name": "张三", "age": 25}
    print(f"\n  访问:")
    print(f"    user['name']              = {user['name']}")
    print(f"    user.get('phone')         = {user.get('phone')}")
    print(f"    user.get('phone', '未填')  = {user.get('phone', '未填')}")
    print(f"    'age' in user             = {'age' in user}")

    # ---- 增删改 ----
    user["city"] = "北京"
    user.update({"age": 26, "gender": "男"})
    removed = user.pop("gender")
    print(f"\n  增删改后: {user}")
    print(f"  pop 出: {removed}")

    # ---- 遍历（三种）----
    print("\n  遍历:")
    print(f"    键:   {list(user.keys())}")
    print(f"    值:   {list(user.values())}")
    print(f"    键值: {list(user.items())}")

    # ---- 合并（Python 3.9+）----
    left = {"a": 1, "b": 2}
    right = {"b": 3, "c": 4}
    print(f"\n  合并: {left} | {right} = {left | right}  ← 右边覆盖左边")

    # ---- 用 dict 模拟二维表 / 索引 ----
    users = [
        {"id": 1, "name": "张三"},
        {"id": 2, "name": "李四"},
    ]
    by_id = {u["id"]: u for u in users}
    print(f"\n  建立索引: by_id[2] = {by_id[2]}")

    # ---- 嵌套 dict ----
    config = {
        "db": {"host": "localhost", "port": 3306},
        "cache": {"ttl": 60},
    }
    print(f"  嵌套访问: config['db']['port'] = {config['db']['port']}")

    # ⚠️ 判断键必须存在时，用 get 或 setdefault，别直接下标
    counter = {}
    for word in ["a", "b", "a"]:
        counter[word] = counter.get(word, 0) + 1
    print(f"  手写计数: {counter}")


# ============================================================
# 6. 专用字典：Counter / defaultdict / OrderedDict
# ============================================================

def demo_special_dicts():
    section("6. Counter / defaultdict / OrderedDict")

    # ---- Counter：计数器 ----
    text = "abracadabra"
    c = Counter(text)
    print(f"  Counter({text!r}) = {c}")
    print(f"  出现最多的 2 个: {c.most_common(2)}")
    print(f"  'a' 的次数: {c['a']}")
    print(f"  不存在的键返回 0: c['z'] = {c['z']}")

    # 统计词频
    words = ["apple", "banana", "apple", "cherry", "banana", "apple"]
    print(f"  词频: {Counter(words)}")

    # Counter 支持加减
    c1 = Counter(a=3, b=1)
    c2 = Counter(a=1, b=2)
    print(f"  c1 + c2 = {c1 + c2}")
    print(f"  c1 - c2 = {c1 - c2}")

    # ---- defaultdict：缺键自动创建默认值 ----
    # 分组：按首字母把单词分组
    groups = defaultdict(list)
    for word in ["apple", "avocado", "banana", "blueberry", "cherry"]:
        groups[word[0]].append(word)
    print(f"\n  defaultdict(list) 分组:")
    for key in sorted(groups):
        print(f"    {key}: {groups[key]}")

    # 计数：不用写 get(word, 0)
    count = defaultdict(int)
    for ch in "hello":
        count[ch] += 1
    print(f"  defaultdict(int) 计数: {dict(count)}")

    # 嵌套字典（树形结构）
    tree = defaultdict(dict)
    tree["root"]["child"] = 1
    print(f"  defaultdict(dict) 嵌套: {dict(tree)}")

    # ---- OrderedDict：记住插入顺序 ----
    # Python 3.7+ 普通 dict 也保序了，OrderedDict 现在主要用在需要
    # move_to_end / 显式语义 的场景
    od = OrderedDict()
    od["first"] = 1
    od["second"] = 2
    od["third"] = 3
    print(f"\n  OrderedDict = {od}")
    od.move_to_end("first")
    print(f"  move_to_end('first') = {od}")
    od.move_to_end("third", last=False)
    print(f"  move_to_end('third', last=False) = {od}")


# ============================================================
# 7. set：集合
# ============================================================

def demo_set():
    section("7. set 集合")

    # set 底层也是哈希表，查找/插入/删除 O(1)，且自动去重
    # 无序、元素必须可哈希

    nums = [1, 2, 2, 3, 3, 3, 4]
    unique = set(nums)
    print(f"  去重: set({nums}) = {unique}")

    # ---- 成员测试 O(1) ----
    print(f"  3 in unique  = {3 in unique}")
    print(f"  99 in unique = {99 in unique}")

    # ---- 集合运算 ----
    A = {1, 2, 3, 4}
    B = {3, 4, 5, 6}
    print(f"\n  A = {A}, B = {B}")
    print(f"    并集 A | B = {A | B}")
    print(f"    交集 A & B = {A & B}")
    print(f"    差集 A - B = {A - B}")
    print(f"    对称差 A ^ B = {A ^ B}")
    print(f"    A <= B     = {A <= B}")
    print(f"    A.isdisjoint({{7,8}}) = {A.isdisjoint({7, 8})}")

    # ---- 增删 ----
    s = {1, 2}
    s.add(3)
    s.discard(1)          # 不存在也不报错
    print(f"\n  add(3), discard(1) -> {s}")
    print("  remove() 不存在会抛 KeyError，discard() 不会")

    # ---- frozenset：不可变集合，可作键 ----
    fs = frozenset([1, 2, 3])
    print(f"\n  frozenset = {fs}")
    print(f"  hash(fs)  = {hash(fs) != 0}，可作字典键")
    index = {frozenset({"a", "b"}): "AB 组"}
    print(f"  用 frozenset 作键: {index[frozenset({'a', 'b'})]}")

    # ---- 典型用途 ----
    # 1) 去重且保持顺序（Python 3.7+ 的 dict 也行）
    ordered_unique = list(dict.fromkeys([3, 1, 3, 2, 1]))
    print(f"\n  去重且保序: {ordered_unique}")

    # 2) 找共同好友
    alice = {"张三", "李四", "王五"}
    bob = {"李四", "王五", "赵六"}
    print(f"  共同好友: {alice & bob}")


# ============================================================
# 8. heapq：优先队列
# ============================================================

def demo_heapq():
    section("8. heapq 优先队列")

    # 堆是一棵完全二叉树，用 list 存储
    # 最小堆：堆顶永远是最小值
    # 插入/弹出 O(log n)，取最小值 O(1)
    # Python 的 heapq 只提供【最小堆】

    nums = [5, 1, 8, 3, 9, 2]
    print(f"  原始: {nums}")

    # heapify：原地把列表变成堆，O(n)
    heap = nums.copy()
    heapq.heapify(heap)
    print(f"  heapify 后: {heap}  ← 只保证堆性质，不是完全有序")

    # heappush / heappop
    heapq.heappush(heap, 0)
    print(f"  heappush(0): {heap}")
    print(f"  heappop() -> {heapq.heappop(heap)}")
    print(f"  剩余: {heap}")

    # ---- 求最小的 3 个 ----
    data = [7, 2, 9, 1, 5, 3, 8, 4, 6]
    smallest3 = heapq.nsmallest(3, data)
    largest3 = heapq.nlargest(3, data)
    print(f"\n  nsmallest(3) = {smallest3}")
    print(f"  nlargest(3)  = {largest3}")

    # ---- 最大堆：把值取负，或存 (priority, value) ----
    # heapq 只有最小堆，要最大值就取负数
    max_heap = []
    for x in [5, 1, 8, 3]:
        heapq.heappush(max_heap, -x)
    print(f"\n  最大堆（存负数）: {max_heap}")
    print(f"  弹出最大值: {-heapq.heappop(max_heap)}")

    # ---- 带优先级的任务队列 ----
    # 元素是元组时，按第一个元素排序；第一个相同再比第二个
    tasks = []
    heapq.heappush(tasks, (2, "写代码"))
    heapq.heappush(tasks, (1, "修 bug"))
    heapq.heappush(tasks, (3, "开会"))
    print("\n  按优先级处理任务:")
    while tasks:
        priority, task = heapq.heappop(tasks)
        print(f"    优先级 {priority}: {task}")

    # ⚠️ 注意：如果优先级相同，会比较第二个元素
    # 如果第二个元素不可比较（比如 dict），会报 TypeError
    # 解决：加一个递增序号 (priority, seq, value)


# ============================================================
# 9. 栈的应用
# ============================================================

def demo_stack_apps():
    section("9. 栈的应用")

    # ---- 应用 1：括号匹配 ----
    def is_balanced(text):
        """检查括号是否配对，用栈实现"""
        pairs = {")": "(", "]": "[", "}": "{"}
        stack = []
        for ch in text:
            if ch in "([{":
                stack.append(ch)          # 左括号入栈
            elif ch in ")]}":
                if not stack or stack[-1] != pairs[ch]:
                    return False          # 没有对应的左括号
                stack.pop()               # 配对成功，出栈
        return not stack                  # 栈空才算全部配对

    samples = ["(a + b)", "{[()]}", "(]", "(()", "a(b)c[d]"]
    print("  括号匹配:")
    for s in samples:
        print(f"    {s!r:<14} -> {is_balanced(s)}")

    # ---- 应用 2：逆波兰表达式求值 ----
    # 中缀 (1 + 2) * 3  ->  后缀 1 2 + 3 *
    def eval_rpn(tokens):
        """计算逆波兰表达式，用栈实现"""
        stack = []
        for token in tokens:
            if token in "+-*/":
                right = stack.pop()       # 注意顺序：先弹出的是右操作数
                left = stack.pop()
                if token == "+":
                    stack.append(left + right)
                elif token == "-":
                    stack.append(left - right)
                elif token == "*":
                    stack.append(left * right)
                else:
                    stack.append(left / right)
            else:
                stack.append(int(token))
        return stack[0]

    expression = ["1", "2", "+", "3", "*"]       # (1 + 2) * 3
    print(f"\n  逆波兰表达式 {' '.join(expression)} = {eval_rpn(expression)}")

    expression2 = ["4", "2", "/", "5", "+"]      # 4 / 2 + 5
    print(f"  逆波兰表达式 {' '.join(expression2)} = {eval_rpn(expression2)}")


# ============================================================
# 10. 队列的应用：BFS
# ============================================================

def demo_bfs():
    section("10. 队列的应用：BFS 广度优先搜索")

    # BFS 用队列：先发现的先处理，天然按"层"推进
    # 典型用途：最短路径（无权图）、层序遍历

    graph = {
        "A": ["B", "C"],
        "B": ["A", "D", "E"],
        "C": ["A", "F"],
        "D": ["B"],
        "E": ["B", "F"],
        "F": ["C", "E"],
    }

    def bfs(graph, start):
        """返回从 start 开始的访问顺序"""
        visited = {start}
        queue = deque([start])
        order = []

        while queue:
            node = queue.popleft()        # 从队头取
            order.append(node)
            for neighbor in graph[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)   # 从队尾加

        return order

    print(f"  图: {graph}")
    print(f"  BFS 从 A 出发: {bfs(graph, 'A')}")
    print("  ↑ 按层级推进，先访问完 A 的所有邻居，再访问下一层")

    # ---- 无权图最短路径 ----
    def shortest_path(graph, start, goal):
        """BFS 求无权图最短路径（边数最少）"""
        queue = deque([(start, [start])])
        visited = {start}

        while queue:
            node, path = queue.popleft()
            if node == goal:
                return path
            for neighbor in graph[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        return None

    print(f"\n  A 到 F 的最短路径: {' -> '.join(shortest_path(graph, 'A', 'F'))}")


# ============================================================
# 11. 链表
# ============================================================

def demo_linked_list():
    section("11. 手写单链表")

    # 链表由节点组成，每个节点存"值"和"下一个节点的引用"
    # 优点：头部插入/删除 O(1)
    # 缺点：随机访问 O(n)，每个节点有额外内存开销

    class ListNode:
        __slots__ = ("value", "next")     # 省内存

        def __init__(self, value):
            self.value = value
            self.next = None

    class LinkedList:
        def __init__(self):
            self.head = None
            self.size = 0

        def append(self, value):
            """尾部追加，O(n)（需要先走到尾部）"""
            node = ListNode(value)
            if self.head is None:
                self.head = node
            else:
                current = self.head
                while current.next:
                    current = current.next
                current.next = node
            self.size += 1

        def prepend(self, value):
            """头部插入，O(1)"""
            node = ListNode(value)
            node.next = self.head
            self.head = node
            self.size += 1

        def delete(self, value):
            """删除第一个匹配的节点"""
            current = self.head
            previous = None
            while current:
                if current.value == value:
                    if previous is None:
                        self.head = current.next
                    else:
                        previous.next = current.next
                    self.size -= 1
                    return True
                previous = current
                current = current.next
            return False

        def reverse(self):
            """反转链表，O(n)，面试高频"""
            previous = None
            current = self.head
            while current:
                nxt = current.next
                current.next = previous
                previous = current
                current = nxt
            self.head = previous

        def to_list(self):
            result = []
            current = self.head
            while current:
                result.append(current.value)
                current = current.next
            return result

        def __len__(self):
            return self.size

    ll = LinkedList()
    for x in [1, 2, 3]:
        ll.append(x)
    print(f"  append 1,2,3 -> {ll.to_list()}")

    ll.prepend(0)
    print(f"  prepend(0)    -> {ll.to_list()}")

    ll.delete(2)
    print(f"  delete(2)     -> {ll.to_list()}")

    ll.reverse()
    print(f"  reverse()     -> {ll.to_list()}")

    print(f"  len           -> {len(ll)}")

    print("\n  链表 vs list:")
    print("    list   : 随机访问 O(1)，头部插入 O(n)")
    print("    链表   : 随机访问 O(n)，头部插入 O(1)")
    print("    Python 日常绝大多数场景直接用 list 就好")


# ============================================================
# 12. 二叉树
# ============================================================

def demo_binary_tree():
    section("12. 二叉树与二叉搜索树")

    class TreeNode:
        __slots__ = ("value", "left", "right")

        def __init__(self, value):
            self.value = value
            self.left = None
            self.right = None

    # ---- 三种深度优先遍历 ----
    def preorder(node, result=None):
        """前序：根 -> 左 -> 右"""
        if result is None:
            result = []
        if node:
            result.append(node.value)
            preorder(node.left, result)
            preorder(node.right, result)
        return result

    def inorder(node, result=None):
        """中序：左 -> 根 -> 右（二叉搜索树得到有序序列）"""
        if result is None:
            result = []
        if node:
            inorder(node.left, result)
            result.append(node.value)
            inorder(node.right, result)
        return result

    def postorder(node, result=None):
        """后序：左 -> 右 -> 根"""
        if result is None:
            result = []
        if node:
            postorder(node.left, result)
            postorder(node.right, result)
            result.append(node.value)
        return result

    # 手工构造一棵树
    #         4
    #        / \
    #       2   6
    #      / \ / \
    #     1  3 5  7
    root = TreeNode(4)
    root.left = TreeNode(2)
    root.right = TreeNode(6)
    root.left.left = TreeNode(1)
    root.left.right = TreeNode(3)
    root.right.left = TreeNode(5)
    root.right.right = TreeNode(7)

    print("  树结构:")
    print("          4")
    print("         / \\")
    print("        2   6")
    print("       / \\ / \\")
    print("      1  3 5  7")

    print(f"\n  前序 Preorder : {preorder(root)}")
    print(f"  中序 Inorder  : {inorder(root)}   ← 有序！")
    print(f"  后序 Postorder: {postorder(root)}")

    # ---- 二叉搜索树 BST ----
    class BST:
        """左子树 < 根 < 右子树"""

        def __init__(self):
            self.root = None

        def insert(self, value):
            def _insert(node, value):
                if node is None:
                    return TreeNode(value)
                if value < node.value:
                    node.left = _insert(node.left, value)
                elif value > node.value:
                    node.right = _insert(node.right, value)
                return node          # 相等则忽略（不允许重复）
            self.root = _insert(self.root, value)

        def search(self, value):
            node = self.root
            while node:
                if value == node.value:
                    return True
                node = node.left if value < node.value else node.right
            return False

        def sorted_values(self):
            return inorder(self.root)

    bst = BST()
    for x in [5, 3, 8, 1, 4, 7, 9]:
        bst.insert(x)

    print(f"\n  BST 插入 {[5, 3, 8, 1, 4, 7, 9]}")
    print(f"  中序遍历（有序）: {bst.sorted_values()}")
    print(f"  查找 4: {bst.search(4)}")
    print(f"  查找 6: {bst.search(6)}")
    print(f"  查找复杂度: 平均 O(log n)，最坏 O(n)（退化成链表）")


# ============================================================
# 13. 图
# ============================================================

def demo_graph():
    section("13. 图的表示：邻接表")

    # 图的两种表示：
    #   邻接矩阵: 二维数组，查边 O(1)，但占 O(V^2) 内存
    #   邻接表  : dict + list/set，占 O(V+E) 内存，最常用

    # 无向图
    graph = {
        "A": {"B", "C"},
        "B": {"A", "D"},
        "C": {"A", "D"},
        "D": {"B", "C", "E"},
        "E": {"D"},
    }

    print("  邻接表:")
    for node, neighbors in graph.items():
        print(f"    {node}: {sorted(neighbors)}")

    # ---- DFS 深度优先（用栈或递归）----
    def dfs(graph, start):
        visited = set()
        stack = [start]
        order = []

        while stack:
            node = stack.pop()            # 从栈顶取
            if node in visited:
                continue
            visited.add(node)
            order.append(node)
            # 逆序压栈，保证访问顺序和邻接表顺序一致
            for neighbor in sorted(graph[node], reverse=True):
                if neighbor not in visited:
                    stack.append(neighbor)
        return order

    # ---- BFS 广度优先（用队列）----
    def bfs(graph, start):
        visited = {start}
        queue = deque([start])
        order = []

        while queue:
            node = queue.popleft()
            order.append(node)
            for neighbor in sorted(graph[node]):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        return order

    print(f"\n  DFS（栈）: {dfs(graph, 'A')}")
    print(f"  BFS（队列）: {bfs(graph, 'A')}")

    # ---- 有向图：加权 ----
    weighted = {
        "A": {"B": 1, "C": 4},
        "B": {"C": 2, "D": 5},
        "C": {"D": 1},
        "D": {},
    }
    print(f"\n  加权有向图: {weighted}")
    print("  求最短路径可以用 Dijkstra（基于 heapq 优先队列）")


# ============================================================
# 14. 排序
# ============================================================

def demo_sorting():
    section("14. 排序算法")

    data = [5, 2, 9, 1, 7, 3]
    print(f"  原始: {data}")

    # ---- 冒泡排序 O(n^2) ----
    def bubble_sort(arr):
        a = arr.copy()
        n = len(a)
        for i in range(n):
            swapped = False
            for j in range(n - 1 - i):
                if a[j] > a[j + 1]:
                    a[j], a[j + 1] = a[j + 1], a[j]
                    swapped = True
            if not swapped:               # 提前退出优化
                break
        return a

    print(f"  冒泡排序: {bubble_sort(data)}   O(n^2)，只用于教学")

    # ---- 快速排序 平均 O(n log n) ----
    def quick_sort(arr):
        if len(arr) <= 1:
            return arr
        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]
        return quick_sort(left) + middle + quick_sort(right)

    print(f"  快速排序: {quick_sort(data)}   平均 O(n log n)")

    # ---- 归并排序 O(n log n)，稳定 ----
    def merge_sort(arr):
        if len(arr) <= 1:
            return arr
        mid = len(arr) // 2
        left = merge_sort(arr[:mid])
        right = merge_sort(arr[mid:])

        merged = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:       # <= 保证稳定
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1
        merged.extend(left[i:])
        merged.extend(right[j:])
        return merged

    print(f"  归并排序: {merge_sort(data)}   O(n log n)，稳定")

    # ---- Python 内置 sorted：Timsort，实际最优选择 ----
    print(f"\n  内置 sorted(): {sorted(data)}")
    print("  ↑ 实际开发永远用 sorted()，它是最坏 O(n log n) 的稳定排序")

    # ---- sorted 的三大参数 ----
    words = ["banana", "apple", "cherry", "date"]
    print(f"\n  sorted(key=len)          = {sorted(words, key=len)}")
    print(f"  sorted(reverse=True)     = {sorted(words, reverse=True)}")

    people = [("张三", 25), ("李四", 30), ("王五", 20)]
    print(f"  按年龄排序                = {sorted(people, key=lambda p: p[1])}")

    # 多关键字排序：先按年龄，年龄相同按名字
    people2 = [("张三", 25), ("李四", 25), ("王五", 20)]
    print(f"  多关键字(年龄,名字)       = {sorted(people2, key=lambda p: (p[1], p[0]))}")

    # ---- 稳定性演示 ----
    items = [("a", 2), ("b", 1), ("c", 2), ("d", 1)]
    print(f"\n  稳定性: 按第二列排序 {sorted(items, key=lambda x: x[1])}")
    print("  ↑ 相同 key 的元素保持原有先后顺序，这就是稳定排序")


# ============================================================
# 15. 查找
# ============================================================

def demo_search():
    section("15. 线性查找与二分查找")

    data = [1, 3, 5, 7, 9, 11, 13, 15]
    print(f"  有序数据: {data}")

    # ---- 线性查找 O(n) ----
    def linear_search(arr, target):
        for i, value in enumerate(arr):
            if value == target:
                return i
        return -1

    print(f"  线性查找 7  -> 下标 {linear_search(data, 7)}   O(n)")

    # ---- 二分查找 O(log n)，前提是数据【已排序】 ----
    def binary_search(arr, target):
        low, high = 0, len(arr) - 1
        while low <= high:
            mid = (low + high) // 2
            if arr[mid] == target:
                return mid
            elif arr[mid] < target:
                low = mid + 1
            else:
                high = mid - 1
        return -1

    print(f"  二分查找 7  -> 下标 {binary_search(data, 7)}   O(log n)")
    print(f"  二分查找 8  -> 下标 {binary_search(data, 8)}   （不存在）")

    # ---- 标准库 bisect：更推荐 ----
    print(f"\n  bisect.bisect_left(data, 7)  = {bisect.bisect_left(data, 7)}")
    print(f"  bisect.bisect_right(data, 7) = {bisect.bisect_right(data, 7)}")
    print("  ↑ bisect 返回插入位置，常用来维护有序列表")

    bisect.insort(data, 8)
    print(f"  bisect.insort(data, 8) -> {data}   （保持有序插入）")


# ============================================================
# 16. 选择指南
# ============================================================

def demo_choosing():
    section("16. 选择指南")

    guide = [
        ("有序的一批元素",           "list"),
        ("经常从头部增删",           "deque"),
        ("固定结构的记录",           "tuple / namedtuple"),
        ("按键快速查找",             "dict"),
        ("统计频次",                 "Counter"),
        ("分组 / 缺键自动初始化",     "defaultdict"),
        ("去重 / 快速判断存在",       "set"),
        ("需要不可变的集合作键",      "frozenset"),
        ("始终取最小/最大值",         "heapq"),
        ("先进先出队列",             "deque（不要用 list.pop(0)）"),
        ("后进先出栈",               "list（append / pop）"),
        ("排序",                     "sorted() / list.sort()"),
        ("在有序数据中查找",          "bisect"),
        ("键是连续整数 0..n-1",       "list（比 dict 更快更省）"),
    ]

    print(f"  {'需求':<30}{'首选结构'}")
    print("  " + "-" * 60)
    for need, choice in guide:
        print(f"  {need:<30}{choice}")

    print("\n  三条经验法则:")
    print("    1. 默认用 list；要按键查用 dict；要去重/判断存在用 set")
    print("    2. 头部频繁增删 -> deque；需要优先级 -> heapq")
    print("    3. 先写对，再优化；用错结构导致的慢，往往比算法慢更致命")


# ============================================================
# 主函数
# ============================================================

def main():
    print("Python 数据结构全览")

    demo_overview()
    demo_list_stack()
    demo_queue()
    demo_tuple()
    demo_dict()
    demo_special_dicts()
    demo_set()
    demo_heapq()
    demo_stack_apps()
    demo_bfs()
    demo_linked_list()
    demo_binary_tree()
    demo_graph()
    demo_sorting()
    demo_search()
    demo_choosing()

    section("演示结束")
    print("数据结构演示完毕。")


if __name__ == "__main__":
    main()
