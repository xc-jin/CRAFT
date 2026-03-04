# GuidedGen
Generate test by extracted specification.

## Quick Start
Follow these 3 steps to generate test:

1. Configure Required Information

    `base_url`, `api_key` and `model` in spec_prompt and test_prompt.

    `java_version` in test_prompt.

2. Extract Specification.
    ```bash
    cd ./approach/generator/GuidedGen/

    python gen_spec.py --project_name example-project --class_name BonusCalculator --metadata_method_repo_path ../../../tmp/metadata_method_repo/ --metadata_class_repo_path ../../../tmp/metadata_class_repo/ --spec_repo_path ../../../tmp/spec_repo/
    ```

3. Generate test.
    ```bash
    cd ./approach/generator/GuidedGen/

    python gen_test.py --project_name example-project --class_name BonusCalculator --spec_repo_path ../../../tmp/spec_repo/ --metadata_class_repo_path ../../../tmp/metadata_class_repo/ --test_result_path ../../../tmp/test_result/
    ```