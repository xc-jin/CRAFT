# 用于RQ: 测试生成能力, 为每个项目获取5个focal file和test file的info, 构建一个json文件

import pandas as pd
import os
import shutil
from ClassMethodParse import parse_focal_class, parse_test_class, write_class_info

if __name__ == "__main__":
    # 修改
    # project_name = "apollo"
    # project_name = "dubbo"
    # project_name = "java-design-patterns"
    # project_name = "nacos"
    # project_name = "seata"
    project_name = "Sentinel"
    # 修改

    system_path = "C:/Users/17388/Desktop/class-level/rq_generation_ability/repo/"

    statistics_repo_path = "C:/Users/17388/Desktop/class-level/rq_generation_ability/target_file_pair_get/sort_result/"

    result_repo_path = "C:/Users/17388/Desktop/class-level/rq_generation_ability/call_graph_result/"

    # excel文件路径
    excel_path = statistics_repo_path + project_name + ".xlsx"

    # 读取 Excel 文件
    df = pd.read_excel(excel_path, dtype=str)  # 读取所有数据，并转换为字符串格式

    # 遍历数据（从第二行开始）
    for index, row in df.iloc[0:].iterrows():  # 直接在 df 上遍历
        # 获取2个path
        focal_method_path = row["focal_method_path"]
        test_method_path = row["test_method_path"]

        # 获取类名，也就是文件名，用于存储json文件
        class_name = os.path.splitext(os.path.basename(focal_method_path))[0]
        print("class_name: " + class_name)
        folder_path = result_repo_path + project_name
        # 创建存入的文件夹
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        # 创建并存入的json文件地址
        class_result_path = folder_path + "/" + class_name + "_class_method.json"

        # 若存在说明已经提取过了类信息了, 就不需要再提取了; 若不存在说明需要提取
        if not os.path.exists(class_result_path):
            # 文件静态地址
            focal_file_path = system_path + project_name + focal_method_path
            test_file_path = system_path + project_name + test_method_path

            class_signatures, constructors, methods = parse_focal_class(focal_file_path)
            imports = parse_test_class(test_file_path)
            write_class_info(imports, class_signatures, constructors, methods, class_result_path)
