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
            "causeFeatureLabels.claimLabels.labels.labelId",
            "causeFeatureLabels.claimLabels.labels.labelName",
            "causeFeatureLabels.claimLabels.labels.originalText",
            "causeFeatureLabels.factualElementLabels.labels.labelId",
            "causeFeatureLabels.factualElementLabels.labels.labelName",
            "causeFeatureLabels.factualElementLabels.labels.originalText",
            "causeFeatureLabels.defenseArgumentLabels.labels.labelId",
            "causeFeatureLabels.defenseArgumentLabels.labels.labelName",
            "causeFeatureLabels.defenseArgumentLabels.labels.originalText",
            "causeFeatureLabels.procedureLabels.labels.labelId",
            "causeFeatureLabels.procedureLabels.labels.labelName",
            "causeFeatureLabels.procedureLabels.labels.originalText",
            "dt_create_time"
        ],
        "query": {
            "range": {
                "dt_create_time": {
                    "gte": "2025-10-31T19:50:00",
                    "lte": "2025-11-01T10:40:00",
                    "format": "yyyy-MM-dd'T'HH:mm:ss"
                }
            }
        },
        "size": 1200
    }

    try:
        # 执行查询
        response = es.search(index="arbitration_cases", body=query)

        # 提取数据并转换为DataFrame
        if response["hits"]["hits"]:
            data = [hit["_source"] for hit in response["hits"]["hits"]]
            df = pd.DataFrame(data)

            # 将查询结果导出到Excel文件，并将查询条件中的_source中的信息转为Excel列名
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
    展开嵌套的causeFeatureLabels对象，处理数组结构的数据
    """
    # 创建一个新的DataFrame来存储展开后的数据
    expanded_rows = []

    # 遍历原始DataFrame的每一行
    for idx, row in df.iterrows():
        # 获取causeFeatureLabels数据
        cause_feature_labels = row.get('causeFeatureLabels', {}) if isinstance(row.get('causeFeatureLabels'), dict) else {}
        
        # 创建基础行
        base_row = row.to_dict()
        
        # 处理causeFeatureLabels字段中的各类标签数组
        label_types = ['claimLabels', 'factualElementLabels', 'defenseArgumentLabels', 'procedureLabels']
        
        for label_type in label_types:
            if label_type in cause_feature_labels:
                labels_data = cause_feature_labels[label_type]
                if isinstance(labels_data, dict) and 'labels' in labels_data:
                    labels = labels_data['labels']
                    if isinstance(labels, list) and len(labels) > 0:
                        # 处理标签数组中的所有数据
                        label_ids = []
                        label_names = []
                        original_texts = []
                        
                        for label in labels:
                            if isinstance(label, dict):
                                label_id = label.get('labelId', '')
                                label_name = label.get('labelName', '')
                                original_text = label.get('originalText', '')
                                
                                # 处理可能为空的情况
                                label_ids.append(str(label_id) if label_id is not None else '')
                                label_names.append(str(label_name) if label_name is not None else '')
                                original_texts.append(str(original_text) if original_text is not None else '')
                        
                        # 将数组中的所有值用分号连接，过滤掉空值
                        non_empty_label_ids = [id for id in label_ids if id]
                        non_empty_label_names = [name for name in label_names if name]
                        non_empty_original_texts = [text for text in original_texts if text]
                        
                        base_row[f'causeFeatureLabels.{label_type}.labels.labelId'] = '; '.join(non_empty_label_ids)
                        base_row[f'causeFeatureLabels.{label_type}.labels.labelName'] = '; '.join(non_empty_label_names)
                        base_row[f'causeFeatureLabels.{label_type}.labels.originalText'] = '; '.join(non_empty_original_texts)
        
        # 展开其他简单字段
        civil_cause_info = row.get('civilCauseInfo', {}) if isinstance(row.get('civilCauseInfo'), dict) else {}
        case_info = row.get('caseInfo', {}) if isinstance(row.get('caseInfo'), dict) else {}
        
        # 展开civilCauseInfo字段
        for key, value in civil_cause_info.items():
            base_row[f'civilCauseInfo.{key}'] = value
            
        # 展开caseInfo字段
        for key, value in case_info.items():
            base_row[f'caseInfo.{key}'] = value
        
        # 移除原始的嵌套字段
        for field in ['causeFeatureLabels', 'civilCauseInfo', 'caseInfo']:
            if field in base_row:
                del base_row[field]
        
        expanded_rows.append(base_row)

    # 创建新的DataFrame
    df_expanded = pd.DataFrame(expanded_rows)
    return df_expanded


if __name__ == '__main__':
    export()