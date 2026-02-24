import networkx as nx

def has_cycle(G):
    try:
        cycle = nx.find_cycle(G, orientation='original')
        return True, cycle
    except nx.NetworkXNoCycle:
        return False, None

def assign_priority(G):

    # 1. Compute SCCs
    sccs = list(nx.strongly_connected_components(G))

    # 2. Construct SCC Reduced Graph (DAG)
    scc_graph = nx.DiGraph()
    scc_map = {}

    for i, scc in enumerate(sccs):
        scc_graph.add_node(i)
        for node in scc:
            scc_map[node] = i

    # 3. Add an edge in the SCC DAG
    for u, v in G.edges:
        if scc_map[u] != scc_map[v]:
            scc_graph.add_edge(scc_map[u], scc_map[v])

    # 4. Perform a topological sort on the SCC reduced graph to determine the priority order
    topo_order = list(nx.topological_sort(scc_graph))
    
    # 5. Assign priority (from low to high)
    priority_map = {}
    for priority, scc_id in enumerate(topo_order):
        for node in sccs[scc_id]:
            priority_map[node] = priority

    return priority_map

def update_priority(data, priority_map):
    for method in data:
        signature = method["class_signature"]
        if signature in priority_map:
            method["priority"] = priority_map[signature]
        else:
            method["priority"] = -1

    return data

def set_priority(G, method_info):
    cycle_flag, cycle = has_cycle(G)

    priority_map = assign_priority(G)
    update_priority(method_info, priority_map)

    return cycle_flag
