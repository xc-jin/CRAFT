# BaseGen
Generate test by metadata.

# Quick Start
Follow these 2 steps to generate test:

1. Configure Required Information
`base_url`, `api_key`, `java_version` and `model` in and test_prompt.

2. Generate test.
```bash
cd ./approach/genertor/BaseGen/

python gen_test_llama.py --project_name example-project1 --class_name Foo --metadata_method_repo_path ../../../tmp/metadata_method_repo/ --metadata_class_repo_path ../../../tmp/metadata_class_repo/ --test_result_path ../../../tmp/test_result/
```