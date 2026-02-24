import os
import sys
import argparse
import time
import argparse
import pandas as pd
import json

from spec_prompt import complete_process

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--project_name", type=str, required=True, help="project name")
    parser.add_argument("--class_name", type=str, required=True, help="class name")
    parser.add_argument("--metadata_method_repo_path", type=str, default="../../tmp/metadata_method_repo/", required=True, help="method-level metadata repo")
    parser.add_argument("--metadata_class_repo_path", type=str, default="../../tmp/metadata_class_repo/", required=True, help="method-level metadata repo")
    parser.add_argument("--spec_repo_path", type=str, default="../../tmp/spec_repo/", required=True, help="spec result repo")

    args = parser.parse_args()

    project_name = args.project_name
    class_name = args.class_name
    metadata_method_repo_path = args.metadata_method_repo_path
    metadata_class_repo_path = args.metadata_class_repo_path
    spec_repo_path = args.spec_repo_path

    metadata_method_path = f"{metadata_method_repo_path}/{project_name}/{class_name}.json"
    metadata_class_path = f"{metadata_class_repo_path}/{project_name}/{class_name}.json"
    spec_path = f"{spec_repo_path}/{project_name}/{class_name}.json"

    complete_process(metadata_method_path, metadata_class_path, spec_path)

    print("GuidedGen - Specification generate finish...")

if __name__ == "__main__":
    main()
