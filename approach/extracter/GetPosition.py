import requests
import json

def get_definition_position(filepath, line, column):
    data = {
        "filePath": filepath,
        "startLine": line,
        "startCharacter": column
    }

    # send POST request to VS Code extension
    response = requests.post("http://localhost:3000/getCallReturnDefinitionPosition", json=data)

    if response.status_code == 200:
        result = response.json()
    else:
        print("Request fail:", response.text)

    return result['filePath'], result['endLine']
