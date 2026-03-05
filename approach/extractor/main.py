import argparse
import os
from pathlib import Path

from extract_method import extract_method
from extract_class import extract_class

def resolve_relative_path(relative_str: str) -> str:

    base_dir = Path(__file__).resolve().parent
    
    combined_path = base_dir / relative_str

    absolute_path = combined_path.resolve()
    
    return str(absolute_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="extract")

    parser.add_argument("--project_name", type=str, required=True, help="project name")
    parser.add_argument("--project_repo_path", type=str, default="../../tmp/project_repo/", required=True, help="project repo")
    parser.add_argument("--metadata_method_repo_path", type=str, default="../../tmp/metadata_method_repo/", required=True, help="method-level metadata repo")
    parser.add_argument("--metadata_class_repo_path", type=str, default="../../tmp/metadata_class_repo/", required=True, help="class-level metadata repo")
    parser.add_argument("--focal_class_path", type=str, required=True, help="focal class path")
    parser.add_argument("--test_class_path", type=str, required=True, help="test class path")

    args = parser.parse_args()
    project_name = args.project_name
    project_repo_path = resolve_relative_path(args.project_repo_path)
    metadata_method_repo_path = resolve_relative_path(args.metadata_method_repo_path)
    metadata_class_repo_path = resolve_relative_path(args.metadata_class_repo_path)
    focal_class_path = args.focal_class_path
    test_class_path = args.test_class_path

    extract_method(project_name, project_repo_path, metadata_method_repo_path, focal_class_path)
    extract_class(project_name, project_repo_path, metadata_class_repo_path, focal_class_path, test_class_path)