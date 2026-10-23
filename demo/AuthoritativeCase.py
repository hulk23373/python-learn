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
            "paragraph.keywords.content",
            "paragraph.basicFacts.content",
            "paragraph.judicialPoints.content",
            "paragraph.judicialResult.content",
            "paragraph.judicialReason.content",
            "paragraph.judicialSummary.content",
            "paragraph.associativeIndexing.content",
            "paragraph.relatedLaws.content",
            "basicInfo.caseCause",
            "basicInfo.caseCause_source_text",
            "basicInfo.caseCause_standard_name",
            "basicInfo.caseNumber",
            "basicInfo.caseType",
            "basicInfo.caseType_source_text",
            "basicInfo.caseType_standard_name",
            "basicInfo.catgegory",
            "basicInfo.court",
            "basicInfo.court_source_text",
            "basicInfo.court_standard_name",
            "basicInfo.indate",
            "basicInfo.judgeDate",
            "basicInfo.judicialLevel",
            "basicInfo.modifyDate",
            "basicInfo.storageCode",
            "basicInfo.subtitle",
            "basicInfo.title",
            "caseTheme.caseCauseId",
            "judicialRules.content",
            "focus.content",
            "dt_create_time"
        ],
        "query": {
          "query_string": {
            "query": "*"
          }
        },
        "size": 3000
    }

    try:
        # 执行查询
        response = es.search(index="authoritative_cases", body=query)

        # 提取数据并转换为DataFrame
        if response["hits"]["hits"]:
            data = [hit["_source"] for hit in response["hits"]["hits"]]
            df = pd.DataFrame(data)

            # 处理嵌套的paragraph数组、basicInfo对象、caseTheme对象、judicialRules对象、focus数组
            df_expanded = expand_column(df)

            # 保存为Excel文件
            df_expanded.to_excel("output_expanded.xlsx", index=False)
            print(f"成功导出 {len(df_expanded)} 条数据到 output_expanded.xlsx")
        else:
            print("未查询到符合条件的数据")

    except Exception as e:
        print(f"查询失败: {e}")

def expand_column(df):
    """
    展开嵌套的paragraph数组、basicInfo对象、caseTheme对象、judicialRules对象、focus数组
    """
    # 创建一个新的DataFrame来存储展开后的数据
    expanded_rows = []

    # 遍历原始DataFrame的每一行
    for idx, row in df.iterrows():
        # 获取paragraph数据
        paragraph = row.get('paragraph', {}) if isinstance(row.get('paragraph'), dict) else {}
        
        # 获取basicInfo数据
        basic_info = row.get('basicInfo', {}) if isinstance(row.get('basicInfo'), dict) else {}
        
        # 获取caseTheme数据
        case_theme = row.get('caseTheme', {}) if isinstance(row.get('caseTheme'), dict) else {}
        
        # 获取judicialRules数据
        judicial_rules = row.get('judicialRules', {}) if isinstance(row.get('judicialRules'), dict) else {}
        
        # 获取focus数据
        focus_list = row.get('focus', []) if isinstance(row.get('focus'), list) else []
        
        # 创建基础行，包含所有非paragraph的展开数据
        base_row = row.to_dict()
        
        # 展开basicInfo字段
        for key, value in basic_info.items():
            base_row[f'basicInfo.{key}'] = value
        
        # 展开caseTheme字段
        for key, value in case_theme.items():
            base_row[f'caseTheme.{key}'] = value
        
        # 处理judicialRules字段
        if isinstance(judicial_rules, dict) and 'content' in judicial_rules:
            base_row['judicialRules.content'] = judicial_rules['content']
        
        # 处理focus字段，将所有content取出并以换行符分割
        if focus_list and isinstance(focus_list, list):
            focus_contents = []
            for focus_item in focus_list:
                if isinstance(focus_item, dict) and 'content' in focus_item:
                    focus_contents.append(focus_item['content'])
            base_row['focus.content'] = '\n'.join(focus_contents) if focus_contents else None
        else:
            base_row['focus.content'] = None
        
        # 处理paragraph字段
        if paragraph:
            # 处理paragraph中的各个字段
            for field_name, field_value in paragraph.items():
                # 每个字段值是一个包含content对象的数组
                if isinstance(field_value, list) and len(field_value) > 0:
                    content_obj = field_value[0]  # 取第一个元素
                    if isinstance(content_obj, dict) and 'content' in content_obj:
                        base_row[f'paragraph.{field_name}.content'] = content_obj['content']
                else:
                    base_row[f'paragraph.{field_name}'] = str(field_value) if field_value is not None else None
        
        # 移除原始的嵌套字段
        for field in ['paragraph', 'basicInfo', 'caseTheme', 'judicialRules', 'focus']:
            if field in base_row:
                del base_row[field]
        
        expanded_rows.append(base_row)

    # 创建新的DataFrame
    df_expanded = pd.DataFrame(expanded_rows)
    return df_expanded

if __name__ == '__main__':
    export()