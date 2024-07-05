# Objective
Refine the existing patient knowledge graph data by correcting node names and types, and structuring edge attributes with keys.

# Input Data
The existing knowledge graph data in JSON format.

## Example Input Data
{
  "graph_data": [
    {
      "user": "John Smith",
      "node_type": "Family",
      "node_name": "Family Member",
      "edge_attributes": [
      "father",
        "deceased",
        "10-05-1995",
        "45",
        "liver cirrhosis"
      ]
    },
    ...
  ]
}

# Output Format
JSON format with the following structure:
- user: The user's name (e.g., "John Smith")
- node_type: Corrected node type (e.g., "Family", "Mental Health", "Medication", "Lifestyle")
- node_name: Corrected node name (e.g., specific family member, illness, medication)
- edge_attributes: A dictionary with keys for each attribute (e.g., timestamp, dose, frequency)

## Example Output Data
{
  "graph_data": [
    {
      "user": "John Smith",
      "node_type": "Family",
      "node_name": "Father",
      "edge_attributes": {
        "relationship": "father",
        "status": "deceased",
        "date": "10-05-1995",
        "age": "45",
        "cause": "liver cirrhosis"
      }
    },
    {
      "user": "John Smith",
      "node_type": "Family",
      "node_name": "Brother",
      "edge_attributes": {
        "relationship": "brother",
        "status": "deceased",
        "date": "15-08-2002",
        "age": "18",
        "cause": "car accident"
      }
    },
    {
      "user": "John Smith",
      "node_type": "Family",
      "node_name": "Mother",
      "edge_attributes": {
        "relationship": "mother",
        "condition": "schizophrenia and liver cirrhosis"
      }
    },
    {
      "user": "John Smith",
      "node_type": "Mental Health",
      "node_name": "Diagnosis",
      "edge_attributes": {
        "condition": "major depressive episode",
        "date": "05-03-2015"
      }
    },
    {
      "user": "John Smith",
      "node_type": "Mental Health",
      "node_name": "Hospitalization",
      "edge_attributes": {
        "date_range": "04-03-2015 to 07-04-2015",
        "treatment": "intensive psychotherapy and ECT"
      }
    },
    {
      "user": "John Smith",
      "node_type": "Mental Health",
      "node_name": "Diagnosis",
      "edge_attributes": {
        "condition": "Bipolar Disorder",
        "date": "20-06-2016"
      }
    },
    {
      "user": "John Smith",
      "node_type": "Mental Health",
      "node_name": "Hospitalization",
      "edge_attributes": {
        "date_range": "25-06-2016 to 15-07-2016",
        "treatment": "Lithium and Valproate"
      }
    },
    {
      "user": "John Smith",
      "node_type": "Mental Health",
      "node_name": "Therapy",
      "edge_attributes": {
        "type": "DBT",
        "date": "10-02-2017"
      }
    },
    {
      "user": "John Smith",
      "node_type": "Mental Health",
      "node_name": "Hospitalization",
      "edge_attributes": {
        "date_range": "15-11-2020 to 21-12-2020",
        "medications": ["Fluoxetine", "Olanzapine"]
      }
    },
    {
      "user": "John Smith",
      "node_type": "Mental Health",
      "node_name": "Therapy",
      "edge_attributes": {
        "type": "CBT",
        "date": "20-03-2017"
      }
    },
    {
      "user": "John Smith",
      "node_type": "Mental Health",
      "node_name": "Therapy",
      "edge_attributes": {
        "type": "Group Therapy",
        "date": "15-12-2020"
      }
    },
    {
      "user": "John Smith",
      "node_type": "Mental Health",
      "node_name": "Therapy",
      "edge_attributes": {
        "type": "CBT",
        "date": "05-04-2024"
      }
    },
    {
      "user": "John Smith",
      "node_type": "Mental Health",
      "node_name": "Therapy",
      "edge_attributes": {
        "type": "MBSR",
        "date": "05-04-2024"
      }
    },
    {
      "user": "John Smith",
      "node_type": "Mental Health",
      "node_name": "Therapy",
      "edge_attributes": {
        "type": "Psychotherapy",
        "date": "05-04-2024"
      }
    },
    {
      "user": "John Smith",
      "node_type": "Mental Health",
      "node_name": "Therapy",
      "edge_attributes": {
        "type": "Occupational Therapy",
        "date": "05-04-2024"
      }
    },
    {
      "user": "John Smith",
      "node_type": "Medication",
      "node_name": "Fluoxetine",
      "edge_attributes": {
        "dose": "20 mg",
        "frequency": "once daily",
        "route": "oral"
      }
    },
    {
      "user": "John Smith",
      "node_type": "Medication",
      "node_name": "Olanzapine",
      "edge_attributes": {
        "dose": "5 mg",
        "frequency": "once daily",
        "route": "oral"
      }
    },
    {
      "user": "John Smith",
      "node_type": "Medication",
      "node_name": "Zolpidem",
      "edge_attributes": {
        "dose": "10 mg",
        "frequency": "as needed",
        "route": "oral"
      }
    },
    {
      "user": "John Smith",
      "node_type": "Medication",
      "node_name": "Aripiprazole",
      "edge_attributes": {
        "dose": "10 mg",
        "frequency": "once daily",
        "route": "oral"
      }
    },
    {
      "user": "John Smith",
      "node_type": "Medication",
      "node_name": "Clonazepam",
      "edge_attributes": {
        "dose": "0.5 mg",
        "frequency": "twice daily",
        "route": "oral"
      }
    },
    {
      "user": "John Smith",
      "node_type": "Lifestyle",
      "node_name": "Hobbies",
      "edge_attributes": {
        "activities": ["reading", "guitar", "hiking"],
        "status": "neglected",
        "date": "01-05-2015"
      }
    },
    {
      "user": "John Smith",
      "node_type": "Lifestyle",
      "node_name": "Relationships",
      "edge_attributes": {
        "status": "strained",
        "with": ["friends", "colleagues"],
        "date": "10-10-2020"
      }
    },
    {
      "user": "John Smith",
      "node_type": "Lifestyle",
      "node_name": "Burnout",
      "edge_attributes": {
        "description": "struggled to open up about struggles and faced unstable work-life balance",
        "date": "20-02-2024"
      }
    }
  ]
}
