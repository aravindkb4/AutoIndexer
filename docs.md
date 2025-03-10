
## Steps to add the AutoIndexer to Pre-commit

Here's how to set up the script as a pre-commit hook using pre-commit framework, which is the recommended way to manage Git hooks:

First, install pre-commit if you haven't already:

```pip install pre-commit```

Create a file named `generate_index.py` in your project root or in a `.hooks` directory with the Python script we created.

Create a `.pre-commit-config.yaml` file in your project root (or add to existing one):

```
repos:
-   repo: local 
    hooks:
    -   id: generate-readme-index
        name: Generate README Index
        entry: python .hooks/generate_index.py  # adjust path if needed
        language: python
        files: README\.md$
        pass_filenames: false
        additional_dependencies: []
```

Initialize pre-commit in your repository (if not already done):
```
pre-commit install
```

Now, whenever you commit your changes in the git, this script will extract headers in README.md of sub-folders and updates the main folder README.md table.