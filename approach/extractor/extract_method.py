import pandas as pd
import os
import shutil

from CallGraph import call_graph

def extract_method(project_name, project_repo_path, metadata_repo_path, focal_class_path):
    class_name = os.path.splitext(os.path.basename(focal_class_path))[0]
    folder_path = f"{metadata_repo_path}/{project_name}"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    result_path = f"{folder_path}/{class_name}.json"

    if not os.path.exists(result_path):
        file_path = f"{project_repo_path}/{project_name}{focal_class_path}"
        print(f"Extract call graph: {file_path}. extract.")

        call_graph(file_path, result_path)
    else:
        print(f"Call graph exist: {result_path}. skip...")

