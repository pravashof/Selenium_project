from anytree import Node, RenderTree
from parse_csv import parse_csv

def build_tree(mappings, root_name="Root"):
    """
    Builds a tree structure based on mappings.

    Args:
        mappings (list): List of mapping dictionaries containing ID, type, and associations.
        root_name (str): Name of the root node.

    Returns:
        Node: Root of the tree structure.
    """
    # Create the root node
    root = Node(root_name)

    # Dictionary to store created nodes for easy parent-child linkage
    nodes = {}

    for mapping in mappings:
        # Determine parent node
        parent_name = mapping.get("content", root_name)
        parent_node = nodes.get(parent_name, root)

        # Create a new node with additional attributes
        node = Node(
            mapping["id"], 
            parent=parent_node, 
            data=mapping  # Add the full mapping data as a custom attribute
        )
        
        # Store the node for further parent-child relationships
        nodes[mapping["id"]] = node

    return root

def save_tree_to_file(tree, output_path):
    """
    Saves the tree structure to a text file for visualization.

    Args:
        tree (Node): Root of the tree to be saved.
        output_path (str): File path to save the tree structure.
    """
    # Open the file with UTF-8 encoding to handle Unicode characters
    with open(output_path, "w", encoding="utf-8") as file:
        for pre, _, node in RenderTree(tree):
            # Format the node with its name and associated data
            node_data = getattr(node, "data", {})

            # Debugging: Print each node before writing it to the file
            print(f"Writing node: {pre}{node.name}: {node_data}")

            
            file.write(f"{pre}{node.name}: {node_data}\n")

    

if __name__ == "__main__":
    # Input and output file paths
    csv_path = "data/New_document_2.csv"
    output_file = "output/hierarchy_tree.txt"

    # Parse CSV to get mappings
    all_mappings, _ = parse_csv(csv_path)

    # Build the tree structure
    tree = build_tree(all_mappings)

    # Save the tree structure to a file
    save_tree_to_file(tree, output_file)

    print(f"Tree structure saved to {output_file}")
