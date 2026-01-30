import pandas as pd
import os
import shutil
from ClassParse import parse_focal_class, parse_test_class, write_class_info

if __name__ == "__main__":
    # file_path = "C:/Users/17388/Desktop/class-level/lang/src/main/java/org/apache/commons/lang3/text/translate/CharSequenceTranslator.java"  # 替换为你的 Java 文件路径
    # result_path = "C:/Users/17388/Desktop/class-level/AnalysisByPython/result/6_3.json"
    project_name = "lang"
    system_path = "C:/Users/17388/Desktop/class-level/"

    statistics_repo_path = "C:/Users/17388/Desktop/class-level/defects4j_statistics/"

    # excel文件路径
    excel_path = statistics_repo_path + project_name + "/" + project_name + "_spec.xlsx"

    # 读取 Excel 文件
    df = pd.read_excel(excel_path, dtype=str)  # 读取所有数据，并转换为字符串格式

    # 遍历数据（从第二行开始）
    for index, row in df.iloc[0:].iterrows():  # 直接在 df 上遍历
        bug_id = row["bug_id"]
        print("bug_id: " + bug_id)
        Usable = row["Usable"]
        print("Usable: " + Usable)
        # 处理数据
        if Usable == "T":
            # 获取excel中存的focal file的地址
            focal_file = row["focal file"]
            focal_name = os.path.basename(focal_file)

            # 获取excel中存的test file的地址
            test_file = row["test file"]
            test_name = os.path.basename(test_file)

            # # # 要删除的文件地址
            # file_path = system_path + project_name + focal_file
            # print(file_path)
            # 要复制的文件地址
            focal_file_path = statistics_repo_path + "/" + project_name + "/" + project_name + "/" + bug_id + "/" + focal_name
            test_file_path = statistics_repo_path + "/" + project_name + "/test_file/" + bug_id + "/" + test_name

            # # 先删除原文件
            # if os.path.exists(file_path):
            #     os.remove(file_path)
            # 
            # # 移动 copy_file_path 到 file_path
            # if os.path.exists(copy_file_path):
            #     shutil.copy2(copy_file_path, file_path)

            # 创建并存入的json文件地址
            result_path = statistics_repo_path + project_name + "/" + project_name + "/" + bug_id + "/" + bug_id + ".json"
            # 存储类信息的json文件地址
            class_result_path = statistics_repo_path + project_name + "/" + project_name + "/" + bug_id + "/" + bug_id + "_class.json"
            # 创建并存入的调用图svg文件地址
            graph_path = statistics_repo_path + project_name + "/" + project_name + "/" + bug_id + "/" + bug_id + ".svg"

            # # 提取调用图，判断优先级，收集元数据结果存入json，判断是否有环，返回cycle_flag，存入excel文件
            # cycle_flag = call_graph(file_path, result_path, graph_path)
            # if cycle_flag:
            #     df.iloc[index, 9] = "T"
            #     print("Cycle exist: T")
            # else:
            #     df.iloc[index, 9] = "F"
            #     print("Cycle exist: F")
            # # 保存修改后的 Excel 文件
            # df.to_excel(excel_path, index=False)

            class_signatures, constructors = parse_focal_class(focal_file_path)
            imports = parse_test_class(test_file_path)
            write_class_info(imports, class_signatures, constructors, class_result_path)


