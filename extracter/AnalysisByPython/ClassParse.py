from tree_sitter import Language, Parser
import json

# 预编译的 Tree-sitter Java 解析器（需要先编译 tree-sitter-java）
JAVA_LANGUAGE = Language('C:/Users/17388/Desktop/class-level/AnalysisByPython/java-grammar.so', 'java')

def parse_focal_class(focal_file_path):
    # print(file_path)
    with open(focal_file_path, "r") as file:
        source_code = file.read()
    
    parser = Parser()
    parser.set_language(JAVA_LANGUAGE)
    tree = parser.parse(bytes(source_code, "utf8"))
    root_node = tree.root_node

    constructors = []
    class_signatures = []

    def traverse(node):
        if node.type in ["class_declaration", "interface_declaration", "enum_declaration"]:
            # 提取类、接口或枚举的完整签名
            class_signature = source_code[node.start_byte:node.end_byte].split("{")[0].strip()
            class_signatures.append(class_signature)

        elif node.type == "constructor_declaration":
            # 提取完整的构造方法签名（包括参数）
            constructor_signature = source_code[node.start_byte:node.end_byte].split("{")[0].strip()

            constructors.append({
                "signature": constructor_signature,
                "line": node.start_point[0] + 1  # 代码行号（Tree-sitter 是 0-based）
            })

        # 递归遍历所有子节点
        for child in node.children:
            traverse(child)

    traverse(root_node)

    return constructors, class_signatures

def parse_test_class(test_file_path):
    # print(file_path)
    with open(test_file_path, "r") as file:
        source_code = file.read()
    
    parser = Parser()
    parser.set_language(JAVA_LANGUAGE)
    tree = parser.parse(bytes(source_code, "utf8"))
    root_node = tree.root_node

    imports = []

    def traverse(node):
        if node.type == "import_declaration":
            # 获取 import 语句内容
            imports.append(source_code[node.start_byte:node.end_byte].strip())

        # 递归遍历所有子节点
        for child in node.children:
            traverse(child)

    traverse(root_node)

    return imports

def write_class_info(imports, class_signatures, constructors, output_json_path):
    # 组织 JSON 数据
    result = {
        "imports": imports,
        "classes": class_signatures,
        "constructors": constructors
    }

    # 写入 JSON 文件
    with open(output_json_path, 'w', encoding='utf-8') as json_file:
        json.dump(result, json_file, indent=4, ensure_ascii=False)