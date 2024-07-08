def reformat_graph_data(data: str) -> str:
    # Finding the start of the JSON part within the string
    start_index = data.find("{")
    if start_index == -1:
        raise ValueError("Invalid input format. JSON data not found.")

    # Extracting the JSON part from the string
    json_data_str = data[start_index:]
    
    # Remove the initial wrapping text and newlines
    json_data_str = json_data_str.strip()

    # Split the string into lines for processing
    lines = json_data_str.splitlines()

    # Initialize the formatted JSON string
    formatted_json_lines = []

    # Track the level of indentation
    indent_level = 0

    # Function to add formatted line with appropriate indentation
    def add_formatted_line(line):
        nonlocal indent_level
        stripped_line = line.strip()
        if stripped_line.startswith("}") or stripped_line.startswith("],"):
            indent_level -= 1
        formatted_json_lines.append("  " * indent_level + stripped_line)
        if stripped_line.endswith("{") or stripped_line.endswith("["):
            indent_level += 1

    # Process each line
    for line in lines:
        add_formatted_line(line)

    # Join the formatted lines into a single string
    formatted_json_str = "\n".join(formatted_json_lines)

    return formatted_json_str

# Example usage
input_data = """Here is the refined output data in the desired format:\n\n{\n  "graph_data": [\n    {\n      "user": "John Smith",\n      "node_type": "Family",\n      "node_name": "Father",\n      "edge_attributes": {\n        "relationship": "father",\n        "status": "deceased",\n        "date": "10-05-1995",\n        "age": "45",\n        "cause": "liver cirrhosis"\n      }\n    },\n    {\n      "user": "John Smith",\n      "node_type": "Family",\n      "node_name": "Brother",\n      "edge_attributes": {\n        "relationship": "brother",\n        "status": "deceased",\n        "date": "15-08-2002",\n        "age": "18",\n        "cause": "car accident"\n      }\n    },\n    {\n      "user": "John Smith",\n      "node_type": "Family",\n      "node_name": "Mother",\n      "edge_attributes": {\n        "relationship": "mother",\n        "condition": "schizophrenia and liver cirrhosis"\n      }\n    },\n    {\n      "user": "John Smith",\n      "node_type": "Mental Health",\n      "node_name": "Diagnosis",\n      "edge_attributes": {\n        "condition": "major depressive episode",\n        "date": "05-03-2015"\n      }\n    },\n    {\n      "user": "John Smith",\n      "node_type": "Mental Health",\n      "node_name": "Hospitalization",\n      "edge_attributes": {\n        "date_range": "04-03-2015 to 07-04-2015",\n        "treatment": "intensive psychotherapy and ECT"\n      }\n    },\n    {\n      "user": "John Smith",\n      "node_type": "Mental Health",\n      "node_name": "Diagnosis",\n      "edge_attributes": {\n        "condition": "Bipolar Disorder",\n        "date": "20-06-2016"\n      }\n    },\n    {\n      "user": "John Smith",\n      "node_type": "Mental Health",\n      "node_name": "Hospitalization",\n      "edge_attributes": {\n        "date_range": "25-06-2016 to 15-07-2016",\n        "treatment": "Lithium and Valproate"\n      }\n    },\n    {\n      "user": "John Smith",\n      "node_type": "Mental Health",\n      "node_name": "Therapy",\n      "edge_attributes": {\n        "type": "DBT",\n        "date": "10-02-2017"\n      }\n    },\n    {\n      "user": "John Smith",\n      "node_type": "Mental Health",\n      "node_name": "Hospitalization",\n      "edge_attributes": {\n        "date_range": "15-11-2020 to 21-12-2020",\n        "medications": ["Fluoxetine", "Olanzapine"]\n      }\n    },\n    {\n      "user": "John Smith",\n      "node_type": "Mental Health",\n      "node_name": "Therapy",\n      "edge_attributes": {\n        "type": ["CBT"]\n        }\n    }\n  ]\n}"""

formatted_data = reformat_graph_data(input_data)
print(formatted_data)