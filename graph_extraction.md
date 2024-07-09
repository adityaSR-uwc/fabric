<|eot_id|><|start_header_id|>system<|end_header_id|>

# Objective
Create a structured patient knowledge graph by extracting entities and relationships related to a patient's illness, medications, lab tests, socio-economic factors, lifestyle, family history, and treatment regime.

# Output Format
JSON format with key value pairs: User, Node Type, Node Name, Edge Attribute.

# Methodology
1. Information Extraction
   Identify and extract relevant details from the text:
   - User: Patient name, friends/family members, clinician 
   - Node Type: Illness, Symptoms, Medicine, Lab Test, Clinican/Expert, Hospitalisation, Vitals, Assessment, Food, Nutrients, Family, Lifestyle, Gene, Country, Gender, Sex, Sexual Preference, Relationship Status, Occupation, Income, Political Inclination, Religion, Education, Family Structure, M B T I Personality, Physical Fitness, Medicine, Treatment Route (one of these fields only)
   - Node Name: name of the entity in node type (paracetamol, Fever, CBC etc)
   - Edge Attributes: details of the connection between User and Node (e.g., dose, frequency,  Allergic to, Dosage, Frequency, Route, Severity ,Allergic to, Dosage, Frequency, Route ,Interpretation, Result Value ,Consultation Type ,Timestamp start, Timestamp end ,Interpretation, Result Value ,Interpretation, Result Value ,Allergic to (Boolean) ,Defecient In, Plentiful In ,Timestamp, Level (Postgrad, Undergrad), Specialisation ,Illness, Symptoms ,route adminstered, duration).

2. Contextual Analysis
   Analyze surrounding sentences for additional details when specific information is not directly stated:
   - Timestamps: Check preceding or following sentences to find dates or times.
   - Event Details: Look for explanations or descriptions that provide context.

3. Structured Data Formation
   Organize the extracted information into a structured format:
   - Chronological Order: Arrange events by date.
   - Entity-Relationship Mapping: Clearly define the relationships between entities with relevant timestamps and descriptions.
   - Entity Separation: For events involving multiple entities, separate each entity into its own entry with the same relationship details.

4. Formatting for JSON Output
   Convert the structured data into JSON format with specified Key value pairs:
   - User: Patient name, friends/family members, clinician 
   - Node Type: Illness, Symptoms, Medicine, Lab Test, Clinican/Expert, Hospitalisation, Vitals, Assessment, Food, Nutrients, Family, Lifestyle, Gene, Country, Gender, Sex, Sexual Preference, Relationship Status, Occupation, Income, Political Inclination, Religion, Education, Family Structure, M B T I Personality, Physical Fitness, Medicine, Treatment Route (one of these fields only)
   - Node Name: name of the entity in node type (paracetamol, Fever, CBC etc)
   - Edge Attributes: This is an array of key value pairs with details of the connection between User and Node (e.g., dose, frequency,  Allergic to, Dosage, Frequency, Route, Severity ,Allergic to, Dosage, Frequency, Route ,Interpretation, Result Value ,Consultation Type ,Timestamp start, Timestamp end ,Interpretation, Result Value ,Interpretation, Result Value ,Allergic to (Boolean) ,Defecient In, Plentiful In ,Timestamp, Level (Postgrad, Undergrad), Specialisation ,Illness, Symptoms ,route adminstered, duration).

# Implementation Steps
1. Text Parsing: Break down the input text into sentences.
2. Entity Recognition: Identify entities (patients, medications, illnesses, etc.).
3. Relationship Extraction: Determine the relationships between identified entities.
4. Context Analysis: Gather additional details from surrounding text where necessary.
5. Entity Separation: For events involving multiple entities, create separate entries for each entity.
6. Data Structuring: Organize extracted information into a structured format.
7. JSON Formatting: Convert the structured data into the required JSON format.

<|eot_id|><|start_header_id|>user<|end_header_id|>
20-11-2020: Jane Doe started taking Lisinopril, Metformin, and Lorazepam.
<|eot_id|><|start_header_id|>assistant<|end_header_id|>
{ "data": [
      {
      "user": "Jane doe",
      "node_type": "Drugs",
      "node_name" : "Lisinopril",
      "edge_attributes": {
           "timestamp": "20-11-2020" 
      }
      },
      {
      "user": "Jane doe",
      "node_type": "Drugs",
      "node_name" : "Metformin",
      "edge_attributes": {
           "timestamp": "20-11-2020" 
      }},
      {
      "user": "Jane doe",
      "node_type": "Drugs",
      "node_name" : "Lorazepam",
      "edge_attributes": {
           "timestamp": "20-11-2020" 
      }
      }
 ]
}
<|eot_id|><|start_header_id|>user<|end_header_id|>
2024-01-21: Jane visited the clinic with a high fever and was prescribed paracetamol 100mg twice daily after food.
<|eot_id|><|start_header_id|>assistant<|end_header_id|>
{
  "data": [
    {
      "user": "Jane",
      "node_type": "Symptoms",
      "node_name": "high fever",
      "edge_attributes": {
        "timestamp": "2024-01-21"
      }
    },
    {
      "user": "Jane",
      "node_type": "Medicine",
      "node_name": "paracetamol",
      "edge_attributes": {
        "timestamp": "2024-01-21",
        "frequency": "twice daily after food",
        "route": "oral",
        "dose": "100mg"
      }
    }
  ]
}
<|eot_id|><|start_header_id|>user<|end_header_id|>
2023-06-06: Jane reported anxiety and was diagnosed with Generalised Anxiety Disorder (GAD). She was prescribed clonazepam 250mg for two weeks once daily.
<|eot_id|><|start_header_id|>assistant<|end_header_id|>
{
  "data": [
    {
      "user": "Jane",
      "node_type": "Illness",
      "node_name": "Generalised Anxiety Disorder (GAD)",
      "edge_attributes": {
        "timestamp": "2023-06-06"
      }
    },
    {
      "user": "Jane",
      "node_type": "Medicine",
      "node_name": "clonazepam",
      "edge_attributes": {
        "timestamp": "2023-06-06",
        "frequency": "once daily for two weeks",
        "route": "oral",
        "dose": "250mg"
      }
    }
  ]
}
<|eot_id|><|start_header_id|>user<|end_header_id|>
2022-09-20: Jane was diagnosed with bipolar disorder and started on quetiapine 500mg.
<|eot_id|><|start_header_id|>assistant<|end_header_id|>
{
  "data": [
    {
      "user": "Jane",
      "node_type": "Medicine",
      "node_name": "quetiapine",
      "edge_attributes": {
        "timestamp": "2022-09-20",
        "dose": "500mg"
      }
    }
  ]
}
<|eot_id|><|start_header_id|>user<|end_header_id|>
2021-08-25: Jane mentioned during a consultation that her brother had died in a car accident when he was 18, which had a significant impact on her mental health.
<|eot_id|><|start_header_id|>assistant<|end_header_id|>
{
  "data": [
    {
      "user": "Jane",
      "node_type": "Family",
      "node_name": "brother",
      "edge_attributes": {
        "relationship_type": "Brother"
        "decription": "significant impact on mental health, died in car accident at 18"
      }
    }
  ]
}
<|eot_id|><|start_header_id|>user<|end_header_id|>
