# Objective
Correct and format the structured patient knowledge graph data to ensure node names and node types match the allowed list and edge attributes have appropriate keys.

# Allowed Node Types and Relationships
The allowed list of node types and relationships is as follows:

Node Type 1 Node Type 2 Edge Edge Attribute

User Illness user → Illness Timestamp, Severity
User Symptoms user → symptom Timestamp, Severity
User Medicine user → medicine Timestamp, Allergic to, Dosage, Frequency, Route
User Lab Test user → labtest Timestamp, Interpretation, Result Value
User Clinican/Expert user → clinican Timestamp, Consultation Type
User Hospitalisation user → hospital Timestamp start, Timestamp end
User Vitals user → vital Timestamp, Interpretation, Result Value
User Assessment user → assessment Timestamp, Interpretation, Result Value
User Food user → food Timestamp, Allergic to (Boolean)
User Nutrients user → nutrients Timestamp, Defecient In, Plentiful In
User Family user → family Relationship Type
User Lifestyle user → lifestyle Timestamp
User Gene user → gene Timestamp
User Country user → country Timestamp
User Gender user → gender Timestamp
User Sex user → sex Timestamp
User Sexual Preference user → perference Timestamp
User Relationship Status user → status Timestamp
User Occupation user → occupation Timestamp
User Income user → income level Timestamp
User Political Inclination user → political inclination Timestamp
User Religion user → religion Timestamp
User Education user → education Timestamp, Level (Postgrad, Undergrad), Specialisation
User Family Structure user → family structure Timestamp
User M B T I Personality user → MBTI personality Timestamp
User Physical Fitness user → physical fitness Timestamp
Clinician Medicine expert → medicine Illness, Symptoms, Timestamp
Clinician Treatment Route expert → treatment route route adminstered, duration, timestamp

# Methodology
1. Input Parsing
  Read the previously formatted data.
  - Identify and correct the node types and node names according to the allowed list.
  - Edge Attribute Formatting
  Ensure edge attributes are formatted with keys (e.g., "timestamp", "dosage", "frequency").
  Convert edge attributes into a dictionary format.

2. Data Structuring
  Reformat the data into the specified structured format.
  Verify that all entries comply with the allowed node types and relationships.

3. Output Formatting
  Convert the corrected and structured data into the required JSON format.

## Example Input

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
    {
      "user": "John Smith",
      "node_type": "Medication",
      "node_name": "Meds",
      "edge_attributes": [
        "Fluoxetine",
        "20 mg",
        "once daily",
        "oral"
      ]
    }
  ]
}

## Example Output

{
  "graph_data": [
    {
      "user": "John Smith",
      "node_type": "Family",
      "node_name": "father",
      "edge_attributes": {
        "relationship_type": "deceased",
        "timestamp": "10-05-1995",
        "age": "45",
        "cause_of_death": "liver cirrhosis"
      }
    },
    {
      "user": "John Smith",
      "node_type": "Medicine",
      "node_name": "Fluoxetine",
      "edge_attributes": {
        "dosage": "20 mg",
        "frequency": "once daily",
        "route": "oral"
      }
    }
  ]
}

# Implementation Steps
1. Parse Input Data: Read the JSON input data.
2. Validate and Correct Node Types and Names:
3. Ensure each node type and node name matches the allowed list.
4. Update any incorrect node types or names.
5. Format Edge Attributes:
6. Convert edge attributes to key-value pairs.
7. Ensure all required keys are present and correctly labeled.
8. Generate Structured Output: Format the corrected data into the specified JSON output format.
9. Export JSON: Output the final structured data as JSON
