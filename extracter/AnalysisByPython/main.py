# 用于RQ: 测试生成能力, 为每个项目获取5个file的call graph, 构建一个json文件

import pandas as pd
import os
import shutil

from CallGraph import call_graph

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
    cycle_excel_path = statistics_repo_path + project_name + "_cycle.xlsx"

    # 读取 Excel 文件
    df = pd.read_excel(excel_path, dtype=str)  # 读取所有数据，并转换为字符串格式
    df.insert(5, "cycle_existence", "")

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
        result_path = folder_path + "/" + class_name + ".json"
        # 创建并存入的调用图svg文件地址
        graph_path = folder_path + "/" + class_name + ".svg"
        
        # 若存在说明已经提取过调用图了, 就不需要再提取了; 若不存在说明需要提取调用图
        if not os.path.exists(result_path):
            # 文件静态地址
            file_path = system_path + project_name + focal_method_path
            print(f"获取调用图: {file_path}")

            # 提取调用图，判断优先级，收集元数据结果存入json，判断是否有环，返回cycle_flag，存入excel文件
            cycle_flag = call_graph(file_path, result_path, graph_path)
            if cycle_flag:
                df.iloc[index, 5] = "T"
                print("Cycle exist: T")
            else:
                df.iloc[index, 5] = "F"
                print("Cycle exist: F")
            # 保存修改后的 Excel 文件
            df.to_excel(cycle_excel_path, index=False)

