from tree_sitter import Language, Parser
from typing import List
import re

JAVA_LANGUAGE = Language('./java-grammar.so', 'java')

def remove_special_char(file_path, output_path=None):
    # delete unASCII char
    chinese_pattern = re.compile(r'[^\x00-\x7F]')

    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()

    total_removed = 0
    new_lines = []
    for line in lines:
        cleaned_line, num_subs = chinese_pattern.subn('', line)
        total_removed += num_subs
        new_lines.append(cleaned_line)

    if not output_path:
        output_path = file_path

    with open(output_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

    print(f"Delete done: delete {total_removed} chars in total.")
    return total_removed

def parse_java_file(file_path):
    remove_special_char(file_path)
    with open(file_path, "r", errors="ignore") as file:
        source_code = file.read()

    parser = Parser()
    parser.set_language(JAVA_LANGUAGE)
    tree = parser.parse(source_code.encode("utf-8"))
    root_node = tree.root_node

    methods_info = []
    method_positions = {}
    source_lines = source_code.splitlines()

    methods = find_methods(root_node, source_code)
    for method_node in methods:
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

            class_name = find_enclosing_class_or_interface(method_node)
            if not class_name:
                print("No class name!")

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
                elif child.type in ["block", "constructor_body"]:
                    method_body = source_code[child.start_byte:child.end_byte]
                method_position = {
                    "line": line,
                    "column": column
                }

            method_invocations = list()
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

            methods_info.append(method_info)
            method_positions[class_with_method_signature] = method_position

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

            class_name = find_enclosing_class_or_interface(method_node)
            if not class_name:
                print("No class name!")

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
                elif child.type in ["block", "constructor_body"]:
                    method_body = source_code[child.start_byte:child.end_byte]
                method_position = {
                    "line": line,
                    "column": column
                }

            method_invocations = list()
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

            methods_info.append(method_info)
            method_positions[class_with_method_signature] = method_position

    return methods_info, method_positions

def find_methods(node, source_code):
    methods = []
    if node.type in ["method_declaration", "constructor_declaration"]:
        methods.append(node)
    
    for child in node.children:
        methods.extend(find_methods(child, source_code))
    
    return methods

def parse_parameters(param_node, source_code):
    parameters = []
    
    for child in param_node.children:
        if child.type == "formal_parameter":
            parsed_param = parse_formal_parameter(child, source_code)
            if parsed_param:
                parameters.append(parsed_param)
        elif child.type == "spread_parameter":
            parsed_param = parse_spread_parameter(child, source_code)
            if parsed_param:
                parameters.append(parsed_param)

    
    return parameters


def parse_formal_parameter(param, source_code):
    param_type = None
    param_name = "this"
    
    for child in param.children:
        if child.type in ["void_type", "integral_type", "floating_point_type", "boolean_type", "scoped_type_identifier", "generic_type", "type_identifier"]:
            param_type = extract_type(child, source_code)
        elif child.type == "identifier":  
            param_name = extract_variable_name(child, source_code)
    
    if param_type and param_name:
        return param_type, param_name
    else:
        tmp_code = source_code[param.start_byte:param.end_byte]
        parts = tmp_code.rsplit(" ", 1)
        return parts[0], parts[1] 

def parse_spread_parameter(param, source_code):
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
        tmp_code = source_code[param.start_byte:param.end_byte]
        parts = tmp_code.rsplit(" ", 1)
        return parts[0], parts[1] 
    
def extract_type(type_node, source_code):
    if not type_node:
        return None
    return source_code[type_node.start_byte:type_node.end_byte]


def extract_variable_name(var_node, source_code):
    for child in var_node.children:
        if child.type == "identifier":
            return source_code[child.start_byte:child.end_byte]
    return source_code[var_node.start_byte:var_node.end_byte]

def traverse_method_invocation_type(node, results: List, kind: str) -> None:
    if node.type == kind:
        results.append(node)
    if not node.children:
        return
    for n in node.children:
        traverse_method_invocation_type(n, results, kind)

def traverse_object_creation_type(node, results: List, kind: str) -> None:
    if node.type == kind:
        results.append(node)
    if not node.children:
        return
    for n in node.children:
        traverse_object_creation_type(n, results, kind)
               
def match_from_span(node, blob: str) -> str:
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
    node = method_node.parent
    while node:
        if node.type in ("class_declaration", "interface_declaration"):
            for child in node.children:
                if child.type == "identifier":
                    return child.text.decode("utf-8")
        node = node.parent
    return None

def extract_method_calls(method_node, source_code):
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