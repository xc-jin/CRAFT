import pandas as pd
import os
import shutil

from ClassMethodParse import parse_focal_class, parse_test_class, write_class_info

def extract_class(project_name, project_repo_path, metadata_repo_path, focal_class_path, test_class_path):
    class_name = os.path.splitext(os.path.basename(focal_class_path))[0]
    folder_path = f"{metadata_repo_path}/{project_name}"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    class_result_path = f"{folder_path}/{class_name}.json"

    if not os.path.exists(class_result_path):
        focal_file_path = project_repo_path + "/" + project_name + focal_class_path
        test_file_path = project_repo_path + "/" + project_name + test_class_path

        focal_imports, class_signatures, constructors, methods, fields = parse_focal_class(focal_file_path)
        test_imports = parse_test_class(test_file_path)
        write_class_info(test_imports, focal_imports, class_signatures, constructors, methods, fields, class_result_path)
