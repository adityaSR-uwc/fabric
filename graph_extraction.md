# Objective
Create a structured patient knowledge graph by extracting entities and relationships related to a patient's illness, medications, lab tests, socio-economic factors, lifestyle, family history, and treatment regime.

# Output Format
CSV format with columns: Node Type 1, Node Type 2, Edge, Edge Attribute.

# Methodology
1. Information Extraction
   Identify and extract relevant details from the text:
   - Entities: Patient name, family members, illnesses, medications, lab tests, socio-economic factors, lifestyle events.
   - Relationships: The connection between entities (e.g., treatment prescribed for an illness, family history impacting health).
   - Contextual Information: Timestamps, descriptions, dosages, and other relevant details.

2. Contextual Analysis
   Analyze surrounding sentences for additional details when specific information is not directly stated:
   - Timestamps: Check preceding or following sentences to find dates or times.
   - Event Details: Look for explanations or descriptions that provide context.

3. Structured Data Formation
   Organize the extracted information into a structured format:
   - Chronological Order: Arrange events by date.
   - Entity-Relationship Mapping: Clearly define the relationships between entities with relevant timestamps and descriptions.
   - Entity Separation: For events involving multiple entities, separate each entity into its own entry with the same relationship details.

4. Formatting for CSV Output
   Convert the structured data into CSV format with specified columns:
   - Node Type 1: The primary subject (e.g., User, Clinician).
   - Node Type 2: The related entity (e.g., illness, medication).
   - Edge: Relationship type between Node Type 1 and Node Type 2.
   - Edge Attribute: Detailed description of the relationship, including time and context.

# Implementation Steps
1. Text Parsing: Break down the input text into sentences.
2. Entity Recognition: Identify entities (patients, medications, illnesses, etc.).
3. Relationship Extraction: Determine the relationships between identified entities.
4. Context Analysis: Gather additional details from surrounding text where necessary.
5. Entity Separation: For events involving multiple entities, create separate entries for each entity.
6. Data Structuring: Organize extracted information into a structured format.
7. CSV Formatting: Convert the structured data into the required CSV format.

## Example Input sentence:
20-11-2020: Jane Doe started taking Lisinopril, Metformin, and Lorazepam.

## Example Output Entry:
User, Medicine, user → medicine, 20-11-2020, Allergic to, Dosage, Frequency, Route
Jane Doe, Lisinopril, user → medicine, 20-11-2020, , Dosage, ,
Jane Doe, Metformin, user → medicine, 20-11-2020, , , ,
Jane Doe, Lorazepam, user → medicine, 20-11-2020, , , ,


<|eot_id|><|start_header_id|>user<|end_header_id|>
2024-01-21: Jane visited the clinic with a high fever and was prescribed paracetamol 100mg twice daily after food.
<|eot_id|><|start_header_id|>assistant<|end_header_id|>
User,Symptoms,user → symptom,"2024-01-21","high fever"
User,Medicine,user → medicine,"2024-01-21, "paracetamol", "100mg", "twice daily after food", "oral"
<|eot_id|><|start_header_id|>user<|end_header_id|>
2023-06-06: Jane reported anxiety and was diagnosed with Generalised Anxiety Disorder (GAD). She was prescribed clonazepam 250mg for two weeks once daily.
<|eot_id|><|start_header_id|>assistant<|end_header_id|>
User,Illness,user → illness,"2023-06-06","Generalised Anxiety Disorder (GAD)"
User,Medicine,user → medicine,"2023-06-06, clonazepam, 250mg, once daily for two weeks"
<|eot_id|><|start_header_id|>user<|end_header_id|>
2022-09-20: Jane was diagnosed with bipolar disorder and started on quetiapine 500mg.
<|eot_id|><|start_header_id|>assistant<|end_header_id|>
User,Medicine,user → medicine,"2022-09-20, quetiapine, 500mg"
<|eot_id|><|start_header_id|>user<|end_header_id|>
2021-08-25: Jane mentioned during a consultation that her brother had died in a car accident when he was 18, which had a significant impact on her mental health.
<|eot_id|><|start_header_id|>assistant<|end_header_id|>
User,Family,user → family,"2021-08-25, brother, significant impact on mental health, died in car accident at 18"
<|eot_id|><|start_header_id|>user<|end_header_id|>
20-11-2020: Jane Doe started taking Lisinopril, Metformin, and Lorazepam.
<|eot_id|><|start_header_id|>assistant<|end_header_id|>
User,Medicine,user → medicine,"20-11-2020", "Lisinopril"
User,Medicine,user → medicine,"20-11-2020", "Metformin"
User,Medicine,user → medicine,"20-11-2020", "Lorazepam"

<|eot_id|><|start_header_id|>user<|end_header_id|>
