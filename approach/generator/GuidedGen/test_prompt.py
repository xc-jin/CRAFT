import openai
import json
import os
import re
import pandas as pd
import concurrent.futures
from tqdm import tqdm

client = openai.OpenAI(
    base_url="", # model url
    api_key="" # your api key
)

java_version = "8" # test java version

system_prompt = f"""
You are an expert in software testing and your task is to generate a high-quality JUnit test case for a given Java method (focal method). 

You will receive the following 9 details:
1.The focal method name and signature
2.The focal class name
3.The focal method body
4.The focal method test specification
5.A list of methods called by the focal method
6.The test specifications of the called methods
7.A list of imports in test file
8.A list of classes in focal file
9.A list of constructors in focal file
10.A list of methods in focal file

Your goal is to:
1.Use #Java {java_version}# and JUnit.
2.Ensure that the test case adhere to the given test specification.
3.If the focal method calls other methods, utilize the provided test specifications of those methods if you need.
4.Output only the test methods, not the test class.
5.Use a testing framework that is compatible with the imports in test file provided. List all the necessary imports to ensure successful compilation.
6.Include multiple test cases if necessary to achieve full coverage. 
7.Use Java reflection to access private classes and invoke private methods to ensure the code compiles successfully.

Please generate the test cases with the necessary import in the following structured format:
[IMPORT-START]
// unique imports.
[IMPORT-END]

[TEST-CASE-START]
// generated test cases.
@Test
public void testExample1() {{
    // test example1 code
}}

@Test
public void testExample2() {{
    // test example2 code
}}
[TEST-CASE-END]
"""

def gpt_35_api(messages: list):
    completion = client.chat.completions.create(
        model="", # model name
        messages=messages,
        temperature=0.1,
        max_tokens=2048
    )
    return completion.choices[0].message.content

def prompt_generate(focal_method_signature, data, class_data):

    focal_method_single_signature = ""
    focal_method_class = ""
    focal_method_body = ""
    focal_method_specification = ""
    focal_method_call_methods = []
    
    for method in data:
        if method["class_signature"] == focal_method_signature:
            focal_method_single_signature = method["signature"]
            focal_method_class = method["class"]
            focal_method_body = method["methodBody"]
            focal_method_specification = method["specification"]
            focal_method_call_methods = method["calledMethods"]
            break

    if focal_method_single_signature == "":
        return ""
    
    content = f"""Please generate the test case for the focal method {focal_method_single_signature}.

focal method info:
### focal method signature
{focal_method_signature}

### focal class name
{focal_method_class}

### focal method body
{focal_method_body}

### focal method test specification
{focal_method_specification}
"""
    method_spec_map = {method["class_signature"]: method.get("specification", "N/A") for method in data}
    results = []
    for method in focal_method_call_methods:
        spec = method_spec_map.get(method, "Not Found")
        results.append({"method": method, "specification": spec})

    content += called_method_list_generate(results)

    imports_string, focal_imports_string, classes_string, constructors_string, methods_string, fields_string = get_class_info_string(class_data)
    content += f"""
### imports in test file
{imports_string}

### imports in focal file
{focal_imports_string}

### classes in focal file
{classes_string}

### constructors in focal file
{constructors_string}

### methods in focal file
{methods_string}

### fields in focal file
{fields_string}
"""
    return content

def called_method_list_generate(results):
    called_unique = [dict(t) for t in {tuple(sorted(d.items())) for d in results}]
    if len(results) == 0:
        return ""
    content_lines = ["### called method list"]
    for i, item in enumerate(called_unique):
        line = f"{i+1}. {item['method']}. specification: {item['specification']}"
        content_lines.append(line)
    return "\n".join(content_lines)

def get_class_info_string(data):
    imports_string = "\n".join(data.get("imports", []))
    focal_imports_string = "\n".join(data.get("focal_imports", []))
    classes_string = "\n".join(data.get("classes", []))
    constructors = data.get("constructors", [])
    constructors_string = "\n".join(cst["signature"] for cst in constructors)
    methods = data.get("methods", [])
    methods_string = "\n".join(mtd["signature"] for mtd in methods)
    fields = data.get("fields", [])
    fields_string = "\n".join(fld["code"] for fld in fields)

    return imports_string, focal_imports_string, classes_string, constructors_string, methods_string, fields_string

def match_result(text):
    import_matches = re.findall(r'\[IMPORT-START\](.*?)\[IMPORT-END\]', text, re.DOTALL)
    import_result = import_matches[0]

    test_matches = re.findall(r'\[TEST-CASE-START\](.*?)\[TEST-CASE-END\]', text, re.DOTALL)
    test_result = test_matches[0]

    return import_result, test_result

def write(result_file, text):
    with open(result_file, 'w', encoding='utf-8') as file:
        file.write(text)

def single_bug_process(focal_method_signature, data, class_data, result_import_file, result_test_file):
    try:
        user_prompt = prompt_generate(focal_method_signature, data, class_data)
        messages = [
            {'role': 'system','content': system_prompt},
            {'role': 'user','content': user_prompt},
        ]
        
        print(f"Generate test for {focal_method_signature}.")
        
        result = gpt_35_api(messages)

        result_import, result_test = match_result(result)
        write(result_import_file, result_import)
        write(result_test_file, result_test)
        
        return True
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def complete_process(spec_gen_path, class_info_path, test_gen_dir):

    with open(spec_gen_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    with open(class_info_path, "r", encoding="utf-8") as file:
        class_data = json.load(file)

    os.makedirs(test_gen_dir, exist_ok=True)

    for index, item in enumerate(data):
        focal_method_signature = item["class_signature"]
        result_dir = f"{test_gen_dir}/{index}"
        os.makedirs(result_dir, exist_ok=True)
        result_import_file = f"{result_dir}/{index}_import.txt"
        result_test_file = f"{result_dir}/{index}_test.txt"
        if os.path.exists(result_test_file):
            continue
        single_bug_process(focal_method_signature, data, class_data, result_import_file, result_test_file)