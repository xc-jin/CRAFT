import networkx as nx
import matplotlib.pyplot as plt
import os
import json

# from  JavaLangParse import parse_java_file
from TreeSitterParse import parse_java_file
from GetPosition import get_definition_position
from SetPriority import set_priority

def add_node(G, methods_info):
    # 添加节点
    for method in methods_info:
        G.add_node(method["class_signature"], label=method["class_signature"])

def add_edge(file_path, G, methods_info, methods_position):
    # 添加边（调用关系）
    for start_method in methods_info:
        # print("start_method name: " + start_method["signature"])
        for called_method in start_method["calledMethodsinfo"]:
            position = called_method["position"]
            # print("called method name: " + called_method["name"])
            # print("called method line: " + str(called_method["position"]["line"]))
            # 获取最终位置
            end_file_path, end_line = get_definition_position(file_path, position["line"], position["column"])
            # 判断是否还在文件内
            if compare_paths(file_path, end_file_path):
                # 找到被调用的方法
                end_method = find_method_by_line(methods_info, end_line)
                if end_method:
                    # print("called method definition: " + end_method["signature"] + "\n")
                    # 修改信息
                    start_method["calledMethods"].append(end_method["class_signature"])
                    # 加边
                    G.add_edge(start_method["class_signature"], end_method["class_signature"], label="Line "+ str(position["line"]))

def find_method_by_line(methods_info, target_line):
    # 根据line信息找方法
    for method in methods_info:
        if method["position"]["line"] == target_line:
            return method
    return None  # 如果找不到，返回 None

def compare_paths(path1, path2):
    # 统一大小写 & 处理路径分隔符
    norm_path1 = os.path.normcase(path1.replace("/", "\\"))
    norm_path2 = os.path.normcase(path2.replace("/", "\\"))
    
    return norm_path1 == norm_path2


def draw_call_graph(file_path, methods_info, methods_position, graph_path):
    G = nx.DiGraph()

    add_node(G, methods_info)

    add_edge(file_path, G, methods_info, methods_position)

    visualize_graph(G, graph_path) # 可视化
    return G

def visualize_graph(G, graph_path):
    # 图可视化
    plt.figure(figsize=(10, 6))
    pos = nx.spring_layout(G)
    labels = {node: data["label"] for node, data in G.nodes(data=True)}
    
    nx.draw(G, pos, with_labels=True, node_color="lightblue", edge_color="gray", node_size=100, font_size=1)
    nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): "calls" for u, v in G.edges()}, font_size=1)
    
    plt.title("Call Graph")
    plt.savefig(graph_path, format="svg")
    # plt.show()

def write_json(result_path, methods_info):
    with open(result_path, "w", encoding="utf-8") as f:
        json.dump(methods_info, f, indent=4, ensure_ascii=False)
    print(f"methods_info 已保存到 {result_path}")

def call_graph(file_path, result_path, graph_path):
    methods_info, methods_position = parse_java_file(file_path)
    G = draw_call_graph(file_path, methods_info, methods_position, graph_path)
    cycle_flag = set_priority(G, methods_info)
    write_json(result_path, methods_info)
    return cycle_flag

