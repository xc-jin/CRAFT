from tree_sitter import Language, Parser
import json

JAVA_LANGUAGE = Language('./java-grammar.so', 'java')

def parse_focal_class(focal_file_path):
    with open(focal_file_path, "r", errors="ignore") as file:
        source_code = file.read()
    
    parser = Parser()
    parser.set_language(JAVA_LANGUAGE)
    tree = parser.parse(bytes(source_code, "utf8"))
    root_node = tree.root_node

    class_signatures = []
    constructors = []
    methods = []
    fields = []
    imports = []

    def traverse(node):
        if node.type in ["class_declaration", "interface_declaration", "enum_declaration"]:
            class_signature = source_code[node.start_byte:node.end_byte].split("{")[0].strip()
            class_signatures.append(class_signature)

        elif node.type == "constructor_declaration":
            constructor_signature = source_code[node.start_byte:node.end_byte].split("{")[0].strip()
            constructors.append({
                "signature": constructor_signature,
                "line": node.start_point[0] + 1
            })
        
        elif node.type == "method_declaration":
            method_signature = source_code[node.start_byte:node.end_byte].split("{")[0].strip()
            methods.append({
                "signature": method_signature,
                "line": node.start_point[0] + 1
            })

        elif node.type == "field_declaration":
            field_code = source_code[node.start_byte:node.end_byte].strip()
            fields.append({
                "code": field_code,
                "line": node.start_point[0] + 1
            })

        elif node.type == "import_declaration":
            imports.append(source_code[node.start_byte:node.end_byte].strip())

        for child in node.children:
            traverse(child)

    traverse(root_node)

    return imports, class_signatures, constructors, methods, fields

def parse_test_class(test_file_path):
    with open(test_file_path, "r", encoding='utf-8') as file:
        source_code = file.read()
    
    parser = Parser()
    parser.set_language(JAVA_LANGUAGE)
    tree = parser.parse(bytes(source_code, "utf8"))
    root_node = tree.root_node

    imports = []

    def traverse(node):
        if node.type == "import_declaration":
            imports.append(source_code[node.start_byte:node.end_byte].strip())

        for child in node.children:
            traverse(child)

    traverse(root_node)

    return imports

def write_class_info(test_imports, focal_imports, class_signatures, constructors, methods, fields, output_json_path):
    result = {
        "imports": test_imports,
        "focal_imports": focal_imports,
        "classes": class_signatures,
        "constructors": constructors,
        "methods": methods,
        "fields": fields
    }

    with open(output_json_path, 'w', encoding='utf-8') as json_file:
        json.dump(result, json_file, indent=4, ensure_ascii=False)