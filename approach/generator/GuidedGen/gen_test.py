import os
import sys
import argparse
import time
import argparse
import pandas as pd
import json

from test_prompt import complete_process

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--project_name", type=str, required=True, help="project name")
    parser.add_argument("--class_name", type=str, required=True, help="class name")
    parser.add_argument("--spec_repo_path", type=str, default="../../tmp/spec_repo/", required=True, help="spec result repo")
    parser.add_argument("--metadata_class_repo_path", type=str, default="../../tmp/metadata_class_repo/", required=True, help="class-level metadata repo")
    parser.add_argument("--test_result_path", type=str, default="../../tmp/test_result/", required=True, help="test result")

    args = parser.parse_args()

    project_name = args.project_name
    class_name = args.class_name
    spec_repo_path = args.spec_repo_path
    metadata_class_repo_path = args.metadata_class_repo_path
    test_result_path = args.test_result_path

    spec_path = f"{spec_repo_path}/{project_name}/{class_name}.json"
    metadata_class_path = f"{metadata_class_repo_path}/{project_name}/{class_name}.json"
    test_path = f"{test_result_path}/{project_name}/{class_name}/GuidedGen"

    complete_process(spec_path, metadata_class_path, test_path)

    print("GuidedGen - Test generate finish...")

if __name__ == "__main__":
    main()
