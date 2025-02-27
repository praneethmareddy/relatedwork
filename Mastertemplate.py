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
    pending_params = None  # Store parameters if they span multiple lines
    pending_values = None  # Store values if they span multiple lines

    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue  # Skip empty rows
            
            row = [clean_text(cell) for cell in row]  # Clean each cell
            first_cell = row[0]

            if first_cell.startswith("@"):  # Section name
                current_section = first_cell
                pending_params = next(reader, [])
                pending_params = [clean_text(param) for param in pending_params]  # Clean parameters
                pending_values = next(reader, [])
                pending_values = [clean_text(value) for value in pending_values]  # Clean values
                sections[current_section]["parameters"].update(pending_params)
                sections[current_section]["values"].append(pending_values)
            else:
                if current_section:
                    if pending_params:  # Handle multi-line parameters
                        pending_params.extend(row)
                        sections[current_section]["parameters"].update(pending_params)
                        pending_params = None  # Reset after merging
                    else:  # Multi-line values
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

    for operator in os.listdir(base_directory):
        operator_path = os.path.join(base_directory, operator)
        if os.path.isdir(operator_path):
            print(f"Processing Operator: {operator}")

            section_counts, templates = process_operator(operator_path)
            operator_master_templates[operator] = merge_templates(templates)
            operator_section_counts[operator] = section_counts

            # Save operator-specific master template
            save_master_template(operator, operator_master_templates[operator], output_dir)

    return operator_master_templates, operator_section_counts

def merge_global_master(operators_templates):
    """Combine all operator templates into a single global master template."""
    global_template = collections.defaultdict(set)

    for templates in operators_templates.values():
        for section, params in templates.items():
            global_template[section].update(params)

    return {sec: sorted(params) for sec, params in global_template.items()}  # Sorted for consistency

def save_global_master_template(global_template, output_dir):
    """Save the global master template as a TXT file."""
    file_path = os.path.join(output_dir, "global_master_template.txt")

    with open(file_path, "w", encoding="utf-8") as f:
        for section, params in global_template.items():
            f.write(f"{section}\n")
            f.write(", ".join(params) + "\n\n")

    print(f"Global master template saved: {file_path}")

def display_results(operator_templates, operator_counts):
    """Display results in tabular form using pandas."""
    print("\n### Operator-wise Analysis ###")
    all_data = []

    for operator, template in operator_templates.items():
        print(f"\nOperator: {operator}")
        print("Section Type Counts:")
        for section, count in operator_counts[operator].items():
            print(f"  {section}: {count}")
            all_data.append([operator, section, count])

        print("\nMaster Template Before Merging:")
        for section, params in template.items():
            print(f"  {section}: {params}")

    # Convert data to DataFrame for tabular display
    df = pd.DataFrame(all_data, columns=["Operator", "Section Type", "Count"])
    print("\nTabular View:\n", df.to_string(index=False))

    # Plot section counts using Seaborn
    plt.figure(figsize=(10, 6))
    sns.barplot(data=df, x="Operator", y="Count", hue="Section Type")
    plt.title("Section Type Distribution Across Operators")
    plt.xticks(rotation=45)
    plt.xlabel("Operator")
    plt.ylabel("Count")
    plt.legend(title="Section Type")
    plt.show()

def main():
    base_directory = "path/to/your/directory"  # Change this to your actual directory
    output_dir = "path/to/output/directory"  # Change this to where you want TXT files saved

    operator_templates, operator_counts = process_all_operators(base_directory, output_dir)

    display_results(operator_templates, operator_counts)

    global_master_template = merge_global_master(operator_templates)
    save_global_master_template(global_master_template, output_dir)

    print("\n### Global Master Template (Across All Operators) ###")
    for section, params in global_master_template.items():
        print(f"  {section}: {params}")

if __name__ == "__main__":
    main()
