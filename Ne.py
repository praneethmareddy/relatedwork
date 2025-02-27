import os
import zipfile
import csv
import collections

def extract_zip(zip_path, extract_to):
    """Extract ZIP file to a directory."""
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

def parse_csv(file_path):
    """Parse CSV to extract sections and handle multi-line values."""
    sections = collections.defaultdict(lambda: {"parameters": [], "values": []})
    current_section = None

    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue  # Skip empty rows
            
            first_cell = row[0].strip()
            if first_cell.startswith("@"):  # Section name
                current_section = first_cell
                sections[current_section]["parameters"] = next(reader, [])
                sections[current_section]["values"] = next(reader, [])
            else:
                if current_section:  # Handle multi-line values
                    sections[current_section]["values"].extend(row)

    return sections

def process_directory(directory):
    """Process all ZIP and CSV files, count different section types, and group templates."""
    section_counts = collections.defaultdict(int)
    templates = collections.defaultdict(list)

    for root, _, files in os.walk(directory):
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

                    templates[tuple(sections.keys())].append(file_path)  # Cluster by section structure

    return section_counts, templates

def main():
    directory = "path/to/your/directory"  # Change this to your actual directory
    section_counts, templates = process_directory(directory)

    print("Section Type Counts:")
    for section, count in section_counts.items():
        print(f"  {section}: {count}")

    print(f"\nUnique Templates Found: {len(templates)}")
    for i, (template, files) in enumerate(templates.items(), 1):
        print(f"\nMaster Template {i}: {template}")
        print(f"  {len(files)} files match this structure.")

if __name__ == "__main__":
    main()
