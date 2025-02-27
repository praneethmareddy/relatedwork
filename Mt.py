import os
import zipfile
import csv
import collections
from itertools import chain

def extract_zip(zip_path, extract_to):
    """Extract ZIP file to a directory."""
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

def parse_csv(file_path):
    """Parse CSV to extract sections and handle multi-line values."""
    sections = collections.defaultdict(lambda: {"parameters": set(), "values": []})
    current_section = None

    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue  # Skip empty rows
            
            first_cell = row[0].strip()
            if first_cell.startswith("@"):  # Section name
                current_section = first_cell
                sections[current_section]["parameters"].update(next(reader, []))
                sections[current_section]["values"].append(next(reader, []))
            else:
                if current_section:  # Handle multi-line values
                    sections[current_section]["values"].append(row)

    return sections

def process_operator(operator_dir):
    """Process all CSVs for a given operator."""
    section_counts = collections.defaultdict(int)
    templates = collections.defaultdict(lambda: collections.defaultdict(set))

    for root, _, files in os.walk(operator_dir):
        for file in files:
            file_path = os.path.join(root, file)

            if file.endswith(".zip"):
                extract_to = os.path.join(root, file.replace(".zip", ""))
                extract_zip(file_path, extract_to)
            
            elif file.endswith(".csv"):
                sections = parse_csv(file_path)

                if sections:
                    first_section = next(iter(sections))
                    section_counts[first_section] += 1  # Count occurrences of section types
                    
                    for sec, data in sections.items():
                        templates[sec]["parameters"].update(data["parameters"])

    return section_counts, templates

def merge_templates(templates):
    """Merge all section structures into a master template."""
    master_template = {}
    for section, data in templates.items():
        master_template[section] = sorted(data["parameters"])  # Sorted for consistency
    return master_template

def process_all_operators(base_directory):
    """Process each operator and generate master templates."""
    operator_master_templates = {}
    operator_section_counts = {}

    for operator in os.listdir(base_directory):
        operator_path = os.path.join(base_directory, operator)
        if os.path.isdir(operator_path):
            print(f"Processing Operator: {operator}")

            section_counts, templates = process_operator(operator_path)
            operator_master_templates[operator] = merge_templates(templates)
            operator_section_counts[operator] = section_counts

    return operator_master_templates, operator_section_counts

def merge_global_master(operators_templates):
    """Combine all operator templates into a single global master template."""
    global_template = collections.defaultdict(set)

    for templates in operators_templates.values():
        for section, params in templates.items():
            global_template[section].update(params)

    return {sec: sorted(params) for sec, params in global_template.items()}  # Sorted for consistency

def main():
    base_directory = "path/to/your/directory"  # Change this to your actual directory
    operator_templates, operator_counts = process_all_operators(base_directory)

    print("\n### Operator-wise Analysis ###")
    for operator, template in operator_templates.items():
        print(f"\nOperator: {operator}")
        print("Section Type Counts:")
        for section, count in operator_counts[operator].items():
            print(f"  {section}: {count}")

        print("\nMaster Template Before Merging:")
        for section, params in template.items():
            print(f"  {section}: {params}")

    global_master_template = merge_global_master(operator_templates)

    print("\n### Global Master Template (Across All Operators) ###")
    for section, params in global_master_template.items():
        print(f"  {section}: {params}")

if __name__ == "__main__":
    main()
