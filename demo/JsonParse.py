import json

def extract_law_content(input_obj: object) -> str:
    """
    从输入对象中提取"法规内容"

    Args:
        input_obj: 可以转换为JSON的对象

    Returns:
        str: 法规内容
    """
    # 如果输入是字符串，则解析为JSON对象
    if isinstance(input_obj, str):
        json_obj = json.loads(input_obj)
    else:
        json_obj = input_obj

    # 获取arg1数组
    arg1_array = json_obj.get("arg1", [])

    # 检查数组长度并获取第二个元素（索引为1）
    if len(arg1_array) > 1:
        law_info = arg1_array[1]
        # 返回法规内容
        return law_info.get("法规内容", "")

    return ""

# 示例用法
if __name__ == "__main__":
    # 测试数据
    test_data = {
        "arg1": [
            [],
            {
                "法规名称": "《桥区水域水上交通安全管理办法（征求意见稿）》",
                "发布文号": "",
                "法规内容": "为加强桥区水域水上交通安全管理，保障桥梁和桥区水域通航安全，我局组织对《桥区水域水上交通安全管理办法》进行了修订，形成了征求意见稿。现面向社会公开征求意见，有关事项通知如下：\n一、公众可以填写意见反馈表，通过以下方式反馈：\n（一）通过电子邮箱反馈。邮箱地址：shixuepeng@msa.gov.cn。\n（二）通过信件反馈。通信地址：北京市建国门内大街11号交通运输部海事局通航管理处，邮编：100736。\n二、本次征求意见时间截止日期为2025年7月12日。"
            }
        ]
    }

    law_content = extract_law_content(test_data)
    print(law_content)
