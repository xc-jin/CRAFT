from tree_sitter import Language, Parser
from typing import List

# 预编译的 Tree-sitter Java 解析器（需要先编译 tree-sitter-java）
JAVA_LANGUAGE = Language('C:/Users/17388/Desktop/class-level/rq_generation_ability/AnalysisByPython/java-grammar.so', 'java')
# file_path = "C:/Users/17388/Desktop/class-level/lang/src/main/java/org/apache/commons/lang3/text/translate/CharSequenceTranslator.java"

def parse_java_file(file_path):
    # print(file_path)
    with open(file_path, "r", errors="ignore") as file:
        source_code = file.read()

    parser = Parser()
    parser.set_language(JAVA_LANGUAGE)
    tree = parser.parse(source_code.encode("utf-8"))
    root_node = tree.root_node

    methods_info = []
    method_positions = {}
    source_lines = source_code.splitlines()

    # 遍历 AST，查找方法声明
    methods = find_methods(root_node, source_code)
    for method_node in methods:
        # 构造方法的提取
        if method_node.type == "constructor_declaration":
            method_name = None
            return_type = "void"
            modifiers = []
            parameters = []
            method_body = ""
            called_methods = []
            method_position = None
            line = 0
            column = 0
            class_name = ""
            class_with_method_signature = ""

            # 解析父节点
            # parent = method_node.parent.parent
            class_name = find_enclosing_class_or_interface(method_node)
            if not class_name:
            #     print(class_name)
            # else:
                print("No class name!")

            # 解析方法名
            for child in method_node.children:
                if child.type == "identifier":
                    method_name = source_code[child.start_byte:child.end_byte]
                    line = child.start_point[0] + 1
                    column = child.start_point[1] + 1
                elif child.type == "modifiers":
                    modifiers = [
                        source_code[mod.start_byte:mod.end_byte]
                        for mod in child.children if mod.type == "modifier"
                    ]
                elif child.type == "type":
                    return_type = source_code[child.start_byte:child.end_byte]
                elif child.type == "formal_parameters":
                    parameters = parse_parameters(child, source_code)
                elif child.type in ["block", "constructor_body"]:  # 方法体
                    method_body = source_code[child.start_byte:child.end_byte]
                method_position = {
                    "line": line,
                    "column": column
                }

            # 解析方法调用
            method_invocations = list()
            # traverse_method_invocation_type(method_node, invocation, '{}_invocation'.format(method_node.type.split('_')[0]))
            # 普通方法调用
            method_invocation = []
            traverse_method_invocation_type(method_node, method_invocation, "method_invocation")
            for inv in method_invocation:
                inv_name = inv.child_by_field_name('name'),
                name = inv_name[0]
                line_start = name.start_point[0]
                line_end = name.end_point[0]
                char_start = name.start_point[1]
                char_end = name.end_point[1]
                lines = source_code.split('\n')
                if line_start != line_end:
                    inv_name = '\n'.join([lines[line_start][char_start:]] + lines[line_start+1:line_end] + [lines[line_end][:char_end]])
                else:
                    inv_name = lines[line_start][char_start:char_end]
                method_invocations.append({
                    "name": inv_name,
                    "position": {
                        "line": line_start + 1,
                        "column": char_start + 1
                    }
                })
            # 还没改完
            # constructor_invocation = []
            # traverse_constructor_invocation_type(method_node, constructor_invocation, "explicit_constructor_invocation")
            # for inv in constructor_invocation:
            #     inv_name = inv.child_by_field_name('name'),
            #     name = inv_name[0]
            #     line_start = name.start_point[0]
            #     line_end = name.end_point[0]
            #     char_start = name.start_point[1]
            #     char_end = name.end_point[1]
            #     lines = source_code.split('\n')
            #     if line_start != line_end:
            #         inv_name = '\n'.join([lines[line_start][char_start:]] + lines[line_start+1:line_end] + [lines[line_end][:char_end]])
            #     else:
            #         inv_name = lines[line_start][char_start:char_end]
            #     method_invocations.append({
            #         "name": inv_name,
            #         "position": {
            #             "line": line_start + 1,
            #             "column": char_start + 1
            #         }
            #     })
            
            # 使用new显式调用的构造方法 
            object_creation = []
            traverse_object_creation_type(method_node, object_creation, "object_creation_expression")
            for inv in object_creation:
                inv_name = inv.child_by_field_name('type'),
                name = inv_name[0]
                line_start = name.start_point[0]
                line_end = name.end_point[0]
                char_start = name.start_point[1]
                char_end = name.end_point[1]
                lines = source_code.split('\n')
                if line_start != line_end:
                    inv_name = '\n'.join([lines[line_start][char_start:]] + lines[line_start+1:line_end] + [lines[line_end][:char_end]])
                else:
                    inv_name = lines[line_start][char_start:char_end]
                method_invocations.append({
                    "name": inv_name,
                    "position": {
                        "line": line_start + 1,
                        "column": char_start + 1
                    }
                })

            method_signature = f"{method_name}({', '.join([ptype + ' ' + pname for ptype, pname in parameters])})"
            if class_name:
                class_with_method_signature = f"{class_name}." + method_signature
            method_info = {
                "name": method_name,
                "category": "constructor_declaration",
                "class": class_name,
                "signature": method_signature,
                "class_signature": class_with_method_signature,
                "returnType": return_type,
                "modifiers": modifiers,
                "parameters": parameters,
                "methodBody": method_body,
                "position": method_position,
                "calledMethodsinfo": method_invocations,
                "calledMethods": []
            }
            # print(method_signature)
            # print(method_position)
            # print(method_invocations)

            methods_info.append(method_info)
            method_positions[class_with_method_signature] = method_position

        # 普通方法的提取
        if method_node.type == "method_declaration":
            method_name = None
            return_type = "void"
            modifiers = []
            parameters = []
            method_body = ""
            called_methods = []
            method_position = None
            line = 0
            column = 0
            class_name = ""
            class_with_method_signature = ""

            # 解析父节点
            # parent = method_node.parent.parent
            class_name = find_enclosing_class_or_interface(method_node)
            if not class_name:
            #     print(class_name)
            # else:
                print("No class name!")

            # 解析方法名
            for child in method_node.children:
                if child.type == "identifier":
                    method_name = source_code[child.start_byte:child.end_byte]
                    line = child.start_point[0] + 1
                    column = child.start_point[1] + 1
                elif child.type == "modifiers":
                    modifiers = [
                        source_code[mod.start_byte:mod.end_byte]
                        for mod in child.children if mod.type == "modifier"
                    ]
                elif child.type == "type":
                    return_type = source_code[child.start_byte:child.end_byte]
                elif child.type == "formal_parameters":
                    parameters = parse_parameters(child, source_code)
                elif child.type in ["block", "constructor_body"]:  # 方法体
                    method_body = source_code[child.start_byte:child.end_byte]
                method_position = {
                    "line": line,
                    "column": column
                }

            # 解析方法调用
            method_invocations = list()
            # traverse_method_invocation_type(method_node, invocation, '{}_invocation'.format(method_node.type.split('_')[0]))
            # 普通方法调用
            method_invocation = []
            traverse_method_invocation_type(method_node, method_invocation, "method_invocation")
            for inv in method_invocation:
                inv_name = inv.child_by_field_name('name'),
                name = inv_name[0]
                line_start = name.start_point[0]
                line_end = name.end_point[0]
                char_start = name.start_point[1]
                char_end = name.end_point[1]
                lines = source_code.split('\n')
                if line_start != line_end:
                    inv_name = '\n'.join([lines[line_start][char_start:]] + lines[line_start+1:line_end] + [lines[line_end][:char_end]])
                else:
                    inv_name = lines[line_start][char_start:char_end]
                method_invocations.append({
                    "name": inv_name,
                    "position": {
                        "line": line_start + 1,
                        "column": char_start + 1
                    }
                })

            # 使用new显式调用的构造方法 
            object_creation = []
            traverse_object_creation_type(method_node, object_creation, "object_creation_expression")
            for inv in object_creation:
                inv_name = inv.child_by_field_name('type'),
                name = inv_name[0]
                line_start = name.start_point[0]
                line_end = name.end_point[0]
                char_start = name.start_point[1]
                char_end = name.end_point[1]
                lines = source_code.split('\n')
                if line_start != line_end:
                    inv_name = '\n'.join([lines[line_start][char_start:]] + lines[line_start+1:line_end] + [lines[line_end][:char_end]])
                else:
                    inv_name = lines[line_start][char_start:char_end]
                method_invocations.append({
                    "name": inv_name,
                    "position": {
                        "line": line_start + 1,
                        "column": char_start + 1
                    }
                })

            method_signature = f"{method_name}({', '.join([ptype + ' ' + pname for ptype, pname in parameters])})"
            if class_name:
                class_with_method_signature = f"{class_name}." + method_signature
            method_info = {
                "name": method_name,
                "category": "method_declaration",
                "class": class_name,
                "signature": method_signature,
                "class_signature": class_with_method_signature,
                "returnType": return_type,
                "modifiers": modifiers,
                "parameters": parameters,
                "methodBody": method_body,
                "position": method_position,
                "calledMethodsinfo": method_invocations,
                "calledMethods": []
            }
            # print(method_signature)
            # print(method_position)
            # print(method_invocations)

            methods_info.append(method_info)
            method_positions[class_with_method_signature] = method_position

    return methods_info, method_positions

def find_methods(node, source_code):
    methods = []
    if node.type in ["method_declaration", "constructor_declaration"]:
        methods.append(node)
    
    for child in node.children:
        methods.extend(find_methods(child, source_code))  # 递归遍历子节点
    
    return methods

def parse_parameters(param_node, source_code):
    """
    解析方法的参数列表
    """
    parameters = []
    
    for child in param_node.children:
        if child.type == "formal_parameter":
            parsed_param = parse_formal_parameter(child, source_code)
            if parsed_param:  # 只有解析成功才添加
                parameters.append(parsed_param)
        elif child.type == "spread_parameter":
            parsed_param = parse_spread_parameter(child, source_code)
            if parsed_param:  # 只有解析成功才添加
                parameters.append(parsed_param)

    
    return parameters


def parse_formal_parameter(param, source_code):
    """
    解析formal参数，返回 (参数类型, 参数名)
    """
    param_type = None
    param_name = "this"
    
    for child in param.children:
        # print(child.type)
        if child.type in ["void_type", "integral_type", "floating_point_type", "boolean_type", "scoped_type_identifier", "generic_type", "type_identifier"]:
            param_type = extract_type(child, source_code)
        elif child.type == "identifier":  
            param_name = extract_variable_name(child, source_code)
    
    if param_type and param_name:
        return param_type, param_name
    else:
        # print(f"Warning: 未能解析参数 -> {source_code[param.start_byte:param.end_byte]}")
        tmp_code = source_code[param.start_byte:param.end_byte]
        parts = tmp_code.rsplit(" ", 1)  # 以最后一个空格为分界点拆分
        return parts[0], parts[1] 

def parse_spread_parameter(param, source_code):
    """
    解析spread参数，返回 (参数类型, 参数名)
    """
    param_type = None
    param_name = None
    
    for child in param.children:
        if child.type in ["void_type", "integral_type", "floating_point_type", "boolean_type", "scoped_type_identifier", "generic_type", "type_identifier"]:
            param_type = source_code[child.start_byte:child.end_byte]
        elif child.type == "variable_declarator":  
            param_name = source_code[child.start_byte:child.end_byte]
    
    if param_type and param_name:
        return param_type+"...", param_name
    else:
        # print(f"Warning: 未能解析参数 -> {source_code[param.start_byte:param.end_byte]}")
        tmp_code = source_code[param.start_byte:param.end_byte]
        parts = tmp_code.rsplit(" ", 1)  # 以最后一个空格为分界点拆分
        return parts[0], parts[1] 
    
def extract_type(type_node, source_code):
    """递归解析类型"""
    if not type_node:
        return None
    return source_code[type_node.start_byte:type_node.end_byte]


def extract_variable_name(var_node, source_code):
    """提取变量名"""
    for child in var_node.children:
        if child.type == "identifier":
            return source_code[child.start_byte:child.end_byte]
    return source_code[var_node.start_byte:var_node.end_byte]

def traverse_method_invocation_type(node, results: List, kind: str) -> None:
        """
        Traverses nodes of given type and save in results
        """
        # print(1)
        if node.type == kind:
            results.append(node)
        if not node.children:
            return
        for n in node.children:
            traverse_method_invocation_type(n, results, kind)

# def traverse_constructor_invocation_type(node, results: List, kind: str) -> None:
#         """
#         Traverses nodes of given type and save in results
#         """
#         # print(1)
#         if node.type == kind:
#             results.append(node)
#         if not node.children:
#             return
#         for n in node.children:
#             traverse_constructor_invocation_type(n, results, kind)

def traverse_object_creation_type(node, results: List, kind: str) -> None:
        """
        Traverses nodes of given type and save in results
        """
        # print(1)
        if node.type == kind:
            results.append(node)
        if not node.children:
            return
        for n in node.children:
            traverse_object_creation_type(n, results, kind)
               
def match_from_span(node, blob: str) -> str:
	"""
	Extract the source code associated with a node of the tree
	"""
	line_start = node.start_point[0]
	line_end = node.end_point[0]
	char_start = node.start_point[1]
	char_end = node.end_point[1]
	lines = blob.split('\n')
	if line_start != line_end:
		return '\n'.join([lines[line_start][char_start:]] + lines[line_start+1:line_end] + [lines[line_end][:char_end]])
	else:
		return lines[line_start][char_start:char_end]

def find_enclosing_class_or_interface(method_node):
    """
    递归向上查找 method_declaration 所属的类 (class_declaration) 或接口 (interface_declaration)
    """
    node = method_node.parent  # 获取方法的父节点

    while node:
        if node.type in ("class_declaration", "interface_declaration"):
            # 找到 class_declaration 或 interface_declaration，返回其名称
            for child in node.children:
                if child.type == "identifier":  # 类名或接口名
                    return child.text.decode("utf-8")  # 返回类名（转换成字符串）

        node = node.parent  # 继续向上遍历

    return None  # 没找到所属的类或接口

def extract_method_calls(method_node, source_code):
    """
    解析方法调用
    """
    called_methods = []
    for descendant in method_node.children:
        if descendant.type == "method_invocation":
            method_name = None
            method_position = None
            for child in descendant.children:
                if child.type == "identifier":
                    method_name = source_code[child.start_byte:child.end_byte]
                    method_position = {
                        "line": descendant.start_point[0] + 1,
                        "column": descendant.start_point[1] + 1
                    }
            if method_name:
                called_methods.append({
                    "name": method_name,
                    "position": method_position
                })
    return called_methods

# parse_java_file(file_path)