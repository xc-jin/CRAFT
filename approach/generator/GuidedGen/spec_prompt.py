import openai
import json
import os
import re
import pandas as pd
import shutil

client = openai.OpenAI(
    base_url="", # model url
    api_key="" # your api key
)

system_prompt = """
You are an expert in software testing and your task is to generate a concise and structured specification for a given Java method (focal method) to facilitate unit test generation.
Your goal is to:
1.Clearly define the behavior of the focal method.
2.Omit irrelevant information, such as business logic or low-level implementation details.
3.Guide test generation, making it easier for a model to derive effective test cases.

You will receive the following 5 details:
1.The focal method name and signature
2.The class name where the focal method is defined
3.The focal method body
4.A list of methods called by the focal method
5.The specifications of the called methods
6.A list of classes in focal file
7.A list of constructors in focal file
8.A list of methods in focal file

The specification contains 1 **Required** piece and 6 **Optional** pieces. **Optional** pieces should **only be included if relevant** to understanding or testing the method. If a piece does not provide meaningful information, omit it.
Please generate the specification in the following structured format:

[START]
### Method Detailed Purpose (Required)
- Summarize functionality and intention comprehensively.

### Inputs / Preconditions (Optional)
- Include **only if** the method has input constraints (type, range, key conditions).

### Outputs / Return Values (Optional)
- Include **only if** the return type or possible values require explanation.

### Exception Handling (Optional)
- Include **only if** the method throws exceptions or has specific failure conditions.  

### Boundary Value Analysis (Optional)
- Include **only if** boundary cases are crucial for testing.  

### State Changes (Optional)
- Include **only if** the method modifies object or global state.

### Addtional info (Optional)
- Include **only if** there are extra details useful for testing.
[END]
"""

def gpt_35_api(messages: list):
    completion = client.chat.completions.create(
        model="", # model name
        messages=messages,
        temperature=0.1,
        max_tokens=2048
    )
    return completion.choices[0].message.content

def single_prompt_generate(result, class_data):
    imports_string, classes_string, constructors_string, methods_string, fields_string = get_class_info_string(class_data)
    content = f"""
focal method info:
### focal method signature
{result["classSignature"]}

### focal class name
{result["class"]}

### focal method body
{result["body"]}
"""
    content += called_method_list_generate(result)
    content += f"""
### fields in focal file
{fields_string}
"""

    return content

def get_class_info_string(data):
    imports_string = "\n".join(data.get("imports", []))

    classes_string = "\n".join(data.get("classes", []))

    constructors = data.get("constructors", [])
    constructors_string = "\n".join(cst["signature"] for cst in constructors)

    methods = data.get("methods", [])
    methods_string = "\n".join(mtd["signature"] for mtd in methods)

    fields = data.get("fields", [])
    fields_string = "\n".join(fld["code"] for fld in fields)

    return imports_string, classes_string, constructors_string, methods_string, fields_string

def prompt_generate(results, class_data):
    content = ""
    if len(results) == 1:
        content = "Please generate the specification for the following method."
    elif len(results) > 1:
        content = f"\nPlease seperately generate the specifications for {len(results)} following methods."

    for result in results:
        content += single_prompt_generate(result, class_data)

    if len(results) == 1:
        content += "Please generate the specification for this method."
    elif len(results) > 1:
        content += f"Please seperately generate the specifications for these {len(results)} methods."

    return content

def called_method_list_generate(result):
    called = result["calledMethodsSpecs"]

    called_unique = [dict(t) for t in {tuple(sorted(d.items())) for d in called}]

    if not called_unique:
        return ""
    content_lines = ["### called method list"]
    for i, item in enumerate(called_unique):
        line = f"{i+1}. {item['class_signature']}. specification: {item['specification']}"
        content_lines.append(line)
    
    return "\n".join(content_lines)
    

def extract_method_by_priority(json_file, target_priority):
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    results= []

    for method in data:
        if method.get("priority") == target_priority and not method.get("specification"):
            called_methods = method.get("calledMethods", [])
            called_methods_specs = []
            for called_method in method.get("calledMethods", []):
                spec = ""
                for m in data:
                    if m.get("class_signature") == called_method:
                        spec = m.get("specification", "")
                        break
                called_methods_specs.append({"class_signature": called_method, "specification": spec})
            
            result = {
                "signature": method.get("signature"),
                "classSignature": method.get("class_signature"),
                "class": method.get("class"),
                "body": method.get("methodBody"),
                "calledMethods": called_methods,
                "calledMethodsSpecs": called_methods_specs,
                "position": method.get("position").get("line")
            }
            results.append(result)
    return results

def match_result(text, methods_info):
    matches = re.findall(r'\[START\](.*?)\[END\]', text, re.DOTALL)

    for match, method in zip(matches, methods_info):
        method["specification"] = match

def write(json_file, result_file, methods_info):
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    for method_info in methods_info:
        for method in data:
            if method.get("class_signature") == method_info["classSignature"] and method.get("position").get("line") == method_info["position"]:
                method["specification"] = method_info["specification"]
                break
        
    with open(result_file, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def single_priority_process(json_file, result_file, priority, class_data):

    methods_info = extract_method_by_priority(json_file, priority)
    if not methods_info:
        print(f"Priority: {priority}, skip...")
        return
    else:
        print(f"Priority: {priority}, extract spec...")

    user_prompt = prompt_generate(methods_info, class_data)
    messages = [
        {'role': 'system','content': system_prompt},
        {'role': 'user','content': user_prompt},
    ]

    result = gpt_35_api(messages)

    match_result(result, methods_info)
    write(json_file, result_file, methods_info)

def single_bug_process(json_file, result_file, class_data):
    
    with open(json_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    priorities = sorted((method["priority"] for method in data), reverse=True)

    unique_priorities = []
    duplicate_flag = False

    previous = None
    for priority in priorities:
        if priority == previous:
            duplicate_flag = True
        else:
            unique_priorities.append(priority)
        previous = priority

    for i in range(0, len(unique_priorities)):
        if i == 0 and not os.path.exists(result_file):
            single_priority_process(json_file, result_file, unique_priorities[i], class_data)
        else:
            single_priority_process(result_file, result_file, unique_priorities[i], class_data)
        
    return duplicate_flag

def complete_process(json_file, class_file, result_file):
    with open(class_file, "r", encoding="utf-8") as file:
        class_data = json.load(file)
    single_bug_process(json_file, result_file, class_data)