import requests
import json

def get_definition_position(filepath, line, column):
    # 发送的数据
    data = {
        "filePath": filepath,  # 这里换成你的 Java 文件路径
        "startLine": line,
        "startCharacter": column
    }

    # 发送 POST 请求到 VS Code 扩展
    response = requests.post("http://localhost:3000/getCallReturnDefinitionPosition", json=data)

    # 解析返回的 JSON 数据
    if response.status_code == 200:
        result = response.json()
        # print(f"文件: {result['filePath']}")
        # print(f"开始位置: 行 {result['startLine']}, 列 {result['startCharacter']}")
        # print(f"结束位置: 行 {result['endLine']}, 列 {result['endCharacter']}")
    else:
        print("请求失败:", response.text)

    return result['filePath'], result['endLine']
