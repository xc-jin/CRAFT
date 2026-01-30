# 用于用于RQ: 测试生成能力, 在获取调用图结束后，根据获取到的json，refine excel文件中的focal_method内容，以便后续对应上处理
import os
import json
import pandas as pd

# 修改
# project_name = "apollo"
# project_name = "dubbo"
# project_name = "java-design-patterns"
# project_name = "nacos"
# project_name = "seata"
project_name = "Sentinel"
# 修改

# === 配置文件路径 ===
statistics_repo_path = "C:/Users/17388/Desktop/class-level/rq_generation_ability/target_file_pair_get/sort_result/"
result_repo_path = "C:/Users/17388/Desktop/class-level/rq_generation_ability/call_graph_result/"
excel_path = statistics_repo_path + project_name + ".xlsx"        # Excel 文件路径
json_repo_path = result_repo_path + project_name

# === 读取 Excel ===
df = pd.read_excel(excel_path)

fail_id = []

for index, row in df.iterrows():
    focal_method_path = row['focal_method_path']
    focal_method = row['focal_method']
    id_ = row['id']

    # 提取类名，比如 BadRequestException.java -> BadRequestException.json
    class_name = os.path.splitext(os.path.basename(focal_method_path))[0]
    json_path = os.path.join(json_repo_path, f"{class_name}.json")

    if not os.path.exists(json_path):
        print(f"[Warning] JSON 文件不存在: {json_path}")
        fail_id.append(id_)
        continue

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
    except Exception as e:
        print(f"[Error] 读取 JSON 失败: {json_path} - {e}")
        fail_id.append(id_)
        continue

    # 找到所有包含 focal_method 的 class_signature
    matched = [item.get("class_signature", "") for item in json_data if focal_method in item.get("class_signature", "")]

    if len(matched) == 1:
        df.at[index, 'focal_method'] = matched[0]
    else:
        fail_id.append(id_)

# === 保存修改后的 Excel ===
df.to_excel(excel_path, index=False)
print(f"✅ Excel 文件已保存到: {excel_path}")
print(f"❌ 未匹配到的方法 ID 有: {fail_id}")