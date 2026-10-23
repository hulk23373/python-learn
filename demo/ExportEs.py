from elasticsearch import Elasticsearch
import pandas as pd
import os


def export():
    # 设置兼容性模式环境变量
    os.environ['ELASTIC_CLIENT_APIVERSIONING'] = '1'

    # 连接Elasticsearch
    es = Elasticsearch(
        ["http://192.168.1.42:9700"],
        basic_auth=('elastic', 'xtinno@9876#JKL'),
        request_timeout=30
    )

    # 查询数据
    query = {
        "_source": [
            "caseInfo.documentNumber",
            "civilCauseInfo.caseCause",
            "civilCauseInfo.caseCause_standard_name",
            "causeFeatureTag.tags.tagId",
            "causeFeatureTag.tags.tagName",
            "causeFeatureTag.tags.originalText",
            "causeFeatureTag.tags.sameCaseTag",
            "dt_create_time"
        ],
        "query": {
            "range": {
                "dt_create_time": {
                    "gte": "2025-09-18T18:00:00",
                    "lte": "2025-09-19T21:00:00",
                    "format": "yyyy-MM-dd'T'HH:mm:ss"
                }
            }
        },
        "size": 1000
    }

    try:
        # 执行查询
        response = es.search(index="arbitration_cases", body=query)

        # 提取数据并转换为DataFrame
        if response["hits"]["hits"]:
            data = [hit["_source"] for hit in response["hits"]["hits"]]
            df = pd.DataFrame(data)

            # 处理嵌套的tags数组
            df_expanded = expand_tags_column(df)

            # 保存为Excel文件
            df_expanded.to_excel("output_expanded.xlsx", index=False)
            print(f"成功导出 {len(df_expanded)} 条数据到 output_expanded.xlsx")
        else:
            print("未查询到符合条件的数据")

    except Exception as e:
        print(f"查询失败: {e}")


def expand_tags_column(df):
    """
    展开包含tags数组的列，每个tag对象成为一行
    """
    # 确保causeFeatureTag列存在
    if 'causeFeatureTag' not in df.columns:
        print("警告: 数据中未找到causeFeatureTag列")
        return df

    # 创建一个新的DataFrame来存储展开后的数据
    expanded_rows = []

    # 遍历原始DataFrame的每一行
    for idx, row in df.iterrows():
        # 获取tags数据
        cause_feature_tag = row.get('causeFeatureTag', {})
        tags = cause_feature_tag.get('tags', []) if isinstance(cause_feature_tag, dict) else []

        # 如果没有tags，保留原始行
        if not tags:
            new_row = row.to_dict()
            # 添加空的tag列
            new_row['tagId'] = None
            new_row['tagName'] = None
            new_row['originalText'] = None
            new_row['sameCaseTag'] = None
            expanded_rows.append(new_row)
            continue

        # 为每个tag创建新行
        for tag in tags:
            new_row = row.to_dict()
            # 添加tag信息
            new_row['tagId'] = tag.get('tagId')
            new_row['tagName'] = tag.get('tagName')
            new_row['originalText'] = tag.get('originalText')
            new_row['sameCaseTag'] = tag.get('sameCaseTag')
            expanded_rows.append(new_row)

    # 创建新的DataFrame
    df_expanded = pd.DataFrame(expanded_rows)

    # 移除原始的causeFeatureTag列
    if 'causeFeatureTag' in df_expanded.columns:
        df_expanded = df_expanded.drop('causeFeatureTag', axis=1)

    return df_expanded


if __name__ == '__main__':
    export()