import javalang

def parse_java_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        source_code = file.read()
    
    tree = javalang.parse.parse(source_code)
    methods_info = []
    method_positions = {}
    source_lines = source_code.splitlines()

    
    for path, node in tree.filter(javalang.tree.MethodDeclaration):
        method_name = node.name
        return_type = node.return_type.name if node.return_type else "void"
        modifiers = node.modifiers
        parameters = [(param.type.name, param.name) for param in node.parameters]
        
        method_signature = f"{method_name}({', '.join([ptype + ' ' + pname for ptype, pname in parameters])})"
        
        method_body = source_code[node.position.line-1:node.body[-1].position.line] if node.body else ""
        
        called_methods = []
        for _, call_node in node.filter(javalang.tree.MethodInvocation):
            corrected_col = get_correct_column(source_lines, call_node.position.line, call_node.member, call_node.position.column)
            called_methods.append({
                "name": call_node.member,
                "position": {
                    "line": call_node.position.line,
                    "column": corrected_col
                }
            })
        
        method_info = {
            "name": method_name,
            "signature": method_signature,
            "returnType": return_type,
            "modifiers": list(modifiers),
            "parameters": parameters,
            "methodBody": method_body,
            "position": {
                "line": node.position.line,
                "column": node.position.column
            },
            "calledMethodsinfo": called_methods,
            "calledMethods":[]
        }
        
        methods_info.append(method_info)
        method_positions[method_name] = node.position
    
    return methods_info, method_positions

def get_correct_column(source_lines, line_number, method_name, approx_column):
    """
    通过源码找到方法名的实际起始列号
    """
    if 0 <= line_number - 1 < len(source_lines):
        line_text = source_lines[line_number - 1]  # 获取方法调用所在的行
        actual_col = line_text.find(method_name, approx_column)  # 在附近搜索
        if actual_col != -1:
            return actual_col + 1  # 转换为1-based index
    return approx_column  # 找不到时返回原始列号