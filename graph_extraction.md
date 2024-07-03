# Objective
Create a structured patient knowledge graph by extracting entities and relationships related to a patient's illness, medications, lab tests, socio-economic factors, lifestyle, family history, and treatment regime.

# Output Format
CSV format with columns: Object, Relationship (timestamp, what/when/how), Entity.

# Methodology
1. *Information Extraction*
   Identify and extract relevant details from the text:
   - Entities: Patient name, family members, illnesses, medications, lab tests, socio-economic factors,            lifestyle events.
   - Relationships: The connection between entities (e.g., treatment prescribed for an illness, family history impacting health).
   - Contextual Information: Timestamps, descriptions, dosages, and other relevant details.

2. *Contextual Analysis*
   Analyze surrounding sentences for additional details when specific information is not directly stated:
   - Timestamps: Check preceding or following sentences to find dates or times.
   - Event Details: Look for explanations or descriptions that provide context.

3. *Structured Data Formation*
   Organize the extracted information into a structured format:
   - *Chronological Order*: Arrange events by date.
   - *Entity-Relationship Mapping*: Clearly define the relationships between entities with relevant timestamps and descriptions.
   - *Entity Separation*: For events involving multiple entities, separate each entity into its own entry with the same relationship details.
        - Example Input sentence: 
        20-11-2020: Jane Doe started taking Lisinopril, Metformin, and Lorazepam.
        - Example Output Entry: 
        Jane Doe,"20-11-2020: started taking medication","Lisinopril"
        Jane Doe,"20-11-2020: started taking medication","Metformin"
        Jane Doe,"20-11-2020: started taking medication","Lorazepam"


4. *Formatting for CSV Output*
   Convert the structured data into CSV format with specified columns:
   - Object: The primary subject (e.g., patient, family member).
   - Relationship (timestamp, what/when/how): Detailed description of the relationship, including time and context.
   - Entity: The related entity (e.g., illness, medication).
  
# Implementation Steps
- Text Parsing: Break down the input text into sentences.
- Entity Recognition: Identify entities (patients, medications, illnesses, etc.).
- Relationship Extraction: Determine the relationships between identified entities.
- Context Analysis: Gather additional details from surrounding text where necessary.
- Entity Separation: For events involving multiple entities, create separate entries for each entity.
- Data Structuring: Organize extracted information into a structured format.
- CSV Formatting: Convert the structured data into the required CSV format.

## Input Example

2024-01-21: Jane visited the clinic with a high fever and was prescribed paracetamol 100mg.
2023-06-06: Jane reported anxiety and was diagnosed with Generalised Anxiety Disorder (GAD). She was prescribed clonazepam 250mg.
2022-09-20: Jane was diagnosed with bipolar disorder and started on quetiapine 500mg.
2021-08-25: Jane mentioned during a consultation that her brother had died in a car accident when he was 18, which had a significant impact on her mental health.
20-11-2020: Jane Doe started taking Lisinopril, Metformin, and Lorazepam.

## Example of CSV Output

Object,Relationship (timestamp, what/when/how),Entity
Jane,"2024-01-21: visited the clinic with a high fever and was prescribed","paracetamol 100mg"
Jane,"2023-06-06: reported anxiety and was diagnosed with Generalised Anxiety Disorder (GAD); prescribed","clonazepam 250mg"
Jane,"2022-09-20: was diagnosed with bipolar disorder; started on","quetiapine 500mg"
Jane's brother,"2021-08-25: mentioned during a consultation; died in a car accident when he was 18","car accident"
Jane Doe,"20-11-2020: started taking medication","Lisinopril"
Jane Doe,"20-11-2020: started taking medication","Metformin"
Jane Doe,"20-11-2020: started taking medication","Lorazepam"

