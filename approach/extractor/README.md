# extractor
extract class-level and method-level metadata, and construct call graph for class.

# Usage
Follow these 3 steps to extract:

1. Save the Target Project

    Save the project you want to analyze at `./tmp/project_repo/`.

2. Install the VS Code Extension

    Search for and install the following extension in the VS Code Marketplace: `get-call-return-definition-position`.

    Activate the extension: Open any `.java` file, click on any method, and run the command `>Get Call Return Definition Position` from the Command Palette (`Ctrl+Shift+P` on Windows/Linux, or `Cmd+Shift+P` on macOS).

3. Run the Analysis Script

    ```bash
    cd ./approach/extractor/

    python main.py --project_name example-project --project_repo_path ../../tmp/project_repo/ --metadata_method_repo_path ../../tmp/metadata_method_repo/ --metadata_class_repo_path ../../tmp/metadata_class_repo/ --focal_class_path /src/main/java/com/example/BonusCalculator.java --test_class_path /src/test/java/com/example/BonusCalculatorTest.java
    ```