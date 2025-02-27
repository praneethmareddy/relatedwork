import os
import zipfile
import csv
import collections
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def extract_zip(zip_path, extract_to):
    """Extract ZIP file to a directory."""
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

def clean_text(text):
    """Remove unwanted delimiters and whitespace."""
    return text.strip().replace('"', '').replace("'", "").replace("\t", " ")

def parse_csv(file_path):
    """Parse CSV while handling multi-line sections and removing delimiters."""
    sections = collections.defaultdict(lambda: {"parameters": set(), "values": []})
    current_section = None

    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue  # Skip empty rows
            
            row = [clean_text(cell) for cell in row]
            first_cell = row[0]

            if first_cell.startswith("@"):  # Section name
                current_section = first_cell
                param_row = next(reader, [])
                param_row = [clean_text(param) for param in param_row]
                sections[current_section]["parameters"].update(param_row)
            else:
                if current_section:
                    sections[current_section]["parameters"].update(row)

    return sections

def process_operator(operator_dir):
    """Process all CSVs for a given operator."""
    section_counts = collections.defaultdict(int)
    templates = collections.defaultdict(lambda: collections.defaultdict(set))
    csv_param_sets = []

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
                    section_counts[first_section] += 1
                    
                    csv_params = set()
                    for sec, data in sections.items():
                        templates[sec]["parameters"].update(data["parameters"])
                        csv_params.update(data["parameters"])
                    
                    csv_param_sets.append(csv_params)  # Store params from each CSV

    return section_counts, templates, csv_param_sets

def merge_templates(templates):
    """Merge all section structures into a master template."""
    master_template = {section: sorted(data["parameters"]) for section, data in templates.items()}
    return master_template

def save_master_template(operator, template, output_dir):
    """Save master template as a TXT file."""
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, f"master_template_{operator}.txt")

    with open(file_path, "w", encoding="utf-8") as f:
        for section, params in template.items():
            f.write(f"{section}\n")
            f.write(", ".join(params) + "\n\n")

    print(f"Master template saved: {file_path}")

def process_all_operators(base_directory, output_dir):
    """Process each operator and generate master templates."""
    operator_master_templates = {}
    operator_section_counts = {}
    operator_param_sets = {}

    for operator in os.listdir(base_directory):
        operator_path = os.path.join(base_directory, operator)
        if os.path.isdir(operator_path):
            print(f"Processing Operator: {operator}")

            section_counts, templates, csv_param_sets = process_operator(operator_path)
            operator_master_templates[operator] = merge_templates(templates)
            operator_section_counts[operator] = section_counts
            operator_param_sets[operator] = csv_param_sets  # Store parameter sets per CSV

            # Save operator-specific master template
            save_master_template(operator, operator_master_templates[operator], output_dir)

    return operator_master_templates, operator_section_counts, operator_param_sets

def merge_global_master(operators_templates):
    """Combine all operator templates into a single global master template."""
    global_template = collections.defaultdict(set)

    for templates in operators_templates.values():
        for section, params in templates.items():
            global_template[section].update(params)

    return {sec: sorted(params) for sec, params in global_template.items()}

def save_global_master_template(global_template, output_dir):
    """Save the global master template as a TXT file."""
    file_path = os.path.join(output_dir, "global_master_template.txt")

    with open(file_path, "w", encoding="utf-8") as f:
        for section, params in global_template.items():
            f.write(f"{section}\n")
            f.write(", ".join(params) + "\n\n")

    print(f"Global master template saved: {file_path}")

def analyze_common_parameters(operator_param_sets):
    """Analyze and visualize common parameters within each operator and across operators."""
    operator_common_params = {}
    global_param_sets = []

    for operator, csv_param_sets in operator_param_sets.items():
        if csv_param_sets:
            common_params = set.intersection(*csv_param_sets)
            operator_common_params[operator] = common_params
            global_param_sets.append(set.union(*csv_param_sets))

            print(f"\nOperator: {operator}")
            print(f"Total Parameters in CSVs: {[len(p) for p in csv_param_sets]}")
            print(f"Common Parameters in all CSVs: {len(common_params)}\n")

            # Heatmap for parameter similarity
            plt.figure(figsize=(8, 6))
            param_matrix = [[len(set1 & set2) for set2 in csv_param_sets] for set1 in csv_param_sets]
            sns.heatmap(param_matrix, annot=True, cmap="Blues", xticklabels=False, yticklabels=False)
            plt.title(f"Parameter Similarity Heatmap - {operator}")
            plt.xlabel("CSV Files")
            plt.ylabel("CSV Files")
            plt.show()

    # Global common parameters across all operators
    global_common_params = set.intersection(*global_param_sets) if global_param_sets else set()
    print("\n### Global Common Parameters Across All Operators ###")
    print(f"Total Unique Parameters Per Operator: {[len(p) for p in global_param_sets]}")
    print(f"Common Parameters Across Operators: {len(global_common_params)}")

    # Heatmap for parameter overlap across operators
    plt.figure(figsize=(8, 6))
    operator_list = list(operator_common_params.keys())
    param_matrix = [[len(operator_common_params[o1] & operator_common_params[o2]) for o2 in operator_list] for o1 in operator_list]
    sns.heatmap(param_matrix, annot=True, cmap="Greens", xticklabels=operator_list, yticklabels=operator_list)
    plt.title("Operator-Wise Parameter Overlap Heatmap")
    plt.xlabel("Operators")
    plt.ylabel("Operators")
    plt.show()

def main():
    base_directory = "path/to/your/directory"  # Change this
    output_dir = "path/to/output/directory"  # Change this

    operator_templates, operator_counts, operator_param_sets = process_all_operators(base_directory, output_dir)

    analyze_common_parameters(operator_param_sets)

    global_master_template = merge_global_master(operator_templates)
    save_global_master_template(global_master_template, output_dir)

    print("\n### Global Master Template (Across All Operators) ###")
    for section, params in global_master_template.items():
        print(f"  {section}: {params}")

if __name__ == "__main__":
    main()
