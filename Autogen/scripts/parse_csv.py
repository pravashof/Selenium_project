import csv

def parse_csv(file_path):
    """
    Parses the CSV file to extract element mappings.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        tuple: A list of all mappings and a list of mappings with interactivity set to True.
    """
    all_mappings = []
    interactive_mappings = []

    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            mapping = {
                "id": row["ID"],
                "bbox": row["bbox"],
                "type": row["type"],
                "content": row["content"],
                "interactivity": row.get("interactivity", "").strip().lower() == "true",
            }
            all_mappings.append(mapping)
            if mapping["interactivity"]:
                interactive_mappings.append(mapping)
    return all_mappings, interactive_mappings
