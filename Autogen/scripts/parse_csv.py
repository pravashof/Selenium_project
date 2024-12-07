# Parses CSV to extract mappings for graphical objects
import csv

# Function to parse the CSV file and extract mappings
def parse_csv(file_path):
    """
    Reads the CSV file containing graphical objects and extracts their properties.
    
    Args:
        file_path (str): Path to the CSV file.

    Returns:
        list: A list of dictionaries with each element's ID, bounding box, type, and associated text.
    """
    mappings = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            mappings.append({
                "id": row["ID"],               # Unique ID for the graphical object
                "bbox": row["bbox"],           # Bounding box coordinates of the object
                "type": row["type"],           # Type of the object (e.g., edit box, combo box, etc.)
                "associated_text": row.get("associated_text", "")  # Associated text, if any
            })
    return mappings

if __name__ == "__main__":
    # File path for the CSV file
    csv_path = "data/New_document_2.csv"
    # Parse the CSV file
    mappings = parse_csv(csv_path)
    
    # Print the mappings for verification
    for mapping in mappings:
        print(mapping)
