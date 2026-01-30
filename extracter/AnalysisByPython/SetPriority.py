import networkx as nx

def has_cycle(G):
    """
    检测有向图 G 是否存在环
    """
    try:
        cycle = nx.find_cycle(G, orientation='original')
        # visualize_graph(cycle)
        return True, cycle  # 如果找到环，返回 True 和环的边
    except nx.NetworkXNoCycle:
        return False, None  # 没有找到环

def assign_priority(G):
    """
    为有向图 G 中的节点分配优先级：
    - 起点优先级低，终点优先级高
    - 互相可达的节点（强连通分量）拥有相同的优先级
    """

    # 1. 计算强连通分量（SCCs），每个 SCC 形成一个组
    sccs = list(nx.strongly_connected_components(G))

    # 2. 构建 SCC 缩约图（DAG）
    scc_graph = nx.DiGraph()
    scc_map = {}  # 记录每个节点属于哪个 SCC

    for i, scc in enumerate(sccs):
        scc_graph.add_node(i)  # SCC 作为 DAG 中的超级节点
        for node in scc:
            scc_map[node] = i  # 标记每个节点属于哪个 SCC

    # 3. 在 SCC DAG 中添加边（缩约原图的边）
    for u, v in G.edges:
        if scc_map[u] != scc_map[v]:  # 只保留不同 SCC 之间的边
            scc_graph.add_edge(scc_map[u], scc_map[v])

    # 4. 对 SCC 缩约图执行拓扑排序，确定优先级顺序
    topo_order = list(nx.topological_sort(scc_graph))
    
    # 5. 赋予优先级（拓扑排序顺序即为优先级，从低到高）
    priority_map = {}
    for priority, scc_id in enumerate(topo_order):
        for node in sccs[scc_id]:
            priority_map[node] = priority  # 该 SCC 内所有节点共享相同优先级

    return priority_map

def update_priority(data, priority_map):
    """
    根据方法签名更新 JSON 数据的 priority 字段
    """
    for method in data:
        signature = method["class_signature"]
        if signature in priority_map:
            method["priority"] = priority_map[signature]  # 添加 priority
        else:
            method["priority"] = -1  # 若找不到，赋值为 -1 代表未定义

    return data

def set_priority(G, method_info):
    # 判断环的存在性，后面存入excel，作为empirical study之一
    cycle_flag, cycle = has_cycle(G)

    priority_map = assign_priority(G)
    # for node, priority in sorted(priority_map.items()):
    #     print(f"节点 {node} 的优先级: {priority}")
    update_priority(method_info, priority_map)

    return cycle_flag
