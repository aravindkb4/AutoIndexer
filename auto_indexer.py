#!/usr/bin/env python3

import os
import re
from typing import Dict, List, Tuple

# Define the order of columns
COLUMN_ORDER = ['title', 'description', 'authors']

def extract_header_content(file_path: str) -> Tuple[str, str]:
    """
    Extract header content from README.md files (Jekyll-style front matter).
    Returns tuple of (header_content, file_path)
    """
    header_content = ""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Look for content between --- markers at start of file
            header_match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
            if header_match:
                header_content = header_match.group(1)
    except Exception as e:
        print(f"Error reading {file_path}: {str(e)}")
    
    return (header_content, file_path)

def parse_header(header_content: str) -> Dict[str, str]:
    """Parse YAML-like header content into a dictionary"""
    header_dict = {}
    if header_content:
        for line in header_content.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                header_dict[key.strip()] = value.strip()
    return header_dict

def find_readme_files(root_dir: str) -> List[str]:
    """Find all README.md files in the project directory and subdirectories"""
    readme_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        if '.git' in dirpath:  # Skip .git directory
            continue
        for filename in filenames:
            if filename.lower() == 'readme.md':
                readme_files.append(os.path.join(dirpath, filename))
    return readme_files

def generate_index_table(headers: List[Tuple[Dict[str, str], str]]) -> str:
    """Generate markdown table from headers with specified column order"""
    if not headers:
        return "No README files with headers found."

    # Create table header
    table = "| Title | Description | Authors | Path |\n"
    table += "|--------|-------------|---------|------|\n"

    # Add rows
    for header, file_path in sorted(headers, key=lambda x: x[0].get('title', '').lower()):
        relative_path = os.path.relpath(file_path, '.')
        path_cell = f"[{os.path.dirname(relative_path)}]({relative_path})"
        
        # Get values for each column, using empty string if not found
        title = header.get('title', '')
        description = header.get('description', '')
        authors = header.get('authors', '')

        table += f"| {title} | {description} | {authors} | {path_cell} |\n"

    return table

def update_main_readme(index_content: str):
    """Update main README.md with the index table"""
    readme_path = 'README.md'
    index_marker_start = "<!-- AUTO-GENERATED-INDEX-START -->"
    index_marker_end = "<!-- AUTO-GENERATED-INDEX-END -->"

    try:
        # Read existing content
        if os.path.exists(readme_path):
            with open(readme_path, 'r', encoding='utf-8') as f:
                content = f.read()
        else:
            content = ""

        # Find or create section for index
        if index_marker_start not in content:
            content += f"\n\n{index_marker_start}\n{index_marker_end}"

        # Replace content between markers
        pattern = f"{index_marker_start}.*?{index_marker_end}"
        new_content = re.sub(
            pattern,
            f"{index_marker_start}\n{index_content}\n{index_marker_end}",
            content,
            flags=re.DOTALL
        )

        # Write updated content
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

    except Exception as e:
        print(f"Error updating main README.md: {str(e)}")
        exit(1)

def main():
    # Find all README.md files
    readme_files = find_readme_files('.')

    # Extract and parse headers
    headers = []
    for file_path in readme_files:
        header_content, path = extract_header_content(file_path)
        if header_content:
            header_dict = parse_header(header_content)
            headers.append((header_dict, path))

    # Generate index table
    index_table = generate_index_table(headers)

    # Update main README.md
    update_main_readme(index_table)

if __name__ == '__main__':
    main()
