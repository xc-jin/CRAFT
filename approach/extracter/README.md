**extracter**
extract class-level and method-level metadata, and construct call graph for class.

# Quick Start
Follow these 3 steps to run the analysis:

1. Save the Target Project
Save the project you want to analyze at `./tmp/project_repo/`.

2. Install the VS Code Extension
Search for and install the following extension in the VS Code Marketplace: `get-call-return-definition-position`.
Activate the extension: Open any `.java` file, click on any method, and run the command `>Get Call Return Definition Position` from the Command Palette (`Ctrl+Shift+P` on Windows/Linux, or `Cmd+Shift+P` on macOS).

3. Run the Analysis Script
Run the Python script.

```bash
cd ./approach/extracter/

python main.py --project_name example-project1 --project_repo_path ../../tmp/project_repo/ --metadata_method_repo_path ../../tmp/metadata_method_repo/ --metadata_class_repo_path ../../tmp/metadata_class_repo/ --focal_class_path /src/main/java/Foo.java --test_class_path /src/test/java/FooTest.java
```