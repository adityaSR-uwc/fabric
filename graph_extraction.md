<|eot_id|><|start_header_id|>system<|end_header_id|>

# Objective
Create a structured patient knowledge graph by extracting entities and relationships related to a patient's illness, medications, lab tests, socio-economic factors, lifestyle, family history, and treatment regime.

# Output Format
CSV format with columns: User, Node Type, Node Name, Timestamp, Dose, Frequency, Route, Relationship Type, Age at Death, Cause of Death, Impact on Mental Health etc.

# Methodology
1. Information Extraction
   Identify and extract relevant details from the text:
   - User: Patient name, friends/family members, clinician  
   - Node Type: Illness, Symptoms, Medicine, Lab Test, Clinician/Expert, Hospitalisation, Vitals, Assessment, Food, Nutrients, Family, Lifestyle, Gene, Country, Gender, Sex, Sexual Preference, Relationship Status, Occupation, Income, Political Inclination, Religion, Education, Family Structure, MBTI Personality, Physical Fitness, Medicine, Treatment Route (one of these fields only) 
   - Node Name: name of the entity in node type (paracetamol, Fever, CBC etc) 
   - Edge Attributes: this contains the details of the connection between User and Node (e.g., dose, frequency, Allergic to, Dosage, Frequency, Route, Severity, Allergic to, Dosage, Frequency, Route, Interpretation, Result Value, Consultation Type, Timestamp start, Timestamp end, Interpretation, Result Value, Interpretation, Result Value, Allergic to (Boolean), Deficient In, Plentiful In, Timestamp, Level (Postgrad, Undergrad), Specialisation, Illness, Symptoms, route administered, duration).

2. Contextual Analysis
   Analyze surrounding sentences for additional details when specific information is not directly stated:
   - Timestamps: Check preceding or following sentences to find dates or times.
   - Event Details: Look for explanations or descriptions that provide context.

3. Structured Data Formation
   Organize the extracted information into a structured format:
   - Entity-Relationship Mapping: Clearly define the relationships between entities with relevant timestamps and descriptions.
   - Entity Separation: For events involving multiple entities, separate each entity into its own entry with the same relationship details.

4. Formatting for CSV Output
   Convert the structured data into CSV format with specified columns:
   - User: Patient name, friends/family members, clinician (single value)
   - Node Type: Illness, Symptoms, Medicine, Lab Test, Clinician/Expert, Hospitalisation, Vitals, Assessment, Food, Nutrients, Family, Lifestyle, Gene, Country, Gender, Sex, Sexual Preference, Relationship Status, Occupation, Income, Political Inclination, Religion, Education, Family Structure, MBTI Personality, Physical Fitness, Medicine, Treatment Route (one of these fields only) (single value)
   - Node Name: name of the entity in node type (paracetamol, Fever, CBC etc) (single value)
   - Edge Attributes: Expand into columns like Timestamp, Dose, Frequency, Route, Relationship Type, Age at Death, Cause of Death, Impact on Mental Health etc.

# Implementation Steps
1. Text Parsing: Break down the input text into sentences.
2. Entity Recognition: Identify entities (patients, medications, illnesses, etc.).
3. Relationship Extraction: Determine the relationships between identified entities.
4. Context Analysis: Gather additional details from surrounding text where necessary.
5. Entity Separation: For events involving multiple entities, create separate entries for each entity.
6. Data Structuring: Organize extracted information into a structured format.
7. CSV Formatting: Convert the structured data into the required CSV format with columns format: User, Nose Name, Node Type, Edge attributes (expanded into columns like Timestamp, dose, frequency, Allergic to, Dosage, Frequency, Route, Severity, Allergic to, Dosage, Frequency, Route, Interpretation, Result Value, Consultation Type, Timestamp start, Timestamp end, Interpretation, Result Value, Interpretation, Result Value, Allergic to (Boolean), Deficient In, Plentiful In, Timestamp, Level (Postgrad, Undergrad), Specialisation, Illness, Symptoms, route administered, duration)

<|eot_id|><|start_header_id|>user<|end_header_id|>
20-11-2020: Jane Doe started taking Lisinopril, Metformin, and Lorazepam.
<|eot_id|><|start_header_id|>assistant<|end_header_id|>
User, Node Type, Node Name, Timestamp, Dose, Frequency, Route, Relationship Type, Age at Death, Cause of Death, Impact on Mental Health
Jane Doe,Medicine,Lisinopril,20-11-2020,,,,,,,
Jane Doe,Medicine,Metformin,20-11-2020,,,,,,,
Jane Doe,Medicine,Lorazepam,20-11-2020,,,,,,,
<|eot_id|><|start_header_id|>user<|end_header_id|>
2024-01-21: Jane visited the clinic with a high fever and was prescribed paracetamol 100mg twice daily after food.
<|eot_id|><|start_header_id|>assistant<|end_header_id|>
User, Node Type, Node Name, Timestamp, Dose, Frequency, Route, Relationship Type, Age at Death, Cause of Death, Impact on Mental Health
Jane,Symptoms,high fever,2024-01-21,,,,,,,
Jane,Medicine,paracetamol,2024-01-21,100mg,twice daily,oral,,,,
<|eot_id|><|start_header_id|>user<|end_header_id|>
2023-06-06: Jane reported anxiety and was diagnosed with Generalised Anxiety Disorder (GAD). She was prescribed clonazepam 250mg for two weeks once daily.
<|eot_id|><|start_header_id|>assistant<|end_header_id|>
User, Node Type, Node Name, Timestamp, Dose, Frequency, Route, Relationship Type, Age at Death, Cause of Death, Impact on Mental Health
Jane,Illness,Generalised Anxiety Disorder (GAD),2023-06-06,,,,,,,
Jane,Medicine,clonazepam,2023-06-06,250mg,once daily for two weeks,oral,,,,
<|eot_id|><|start_header_id|>user<|end_header_id|>
2022-09-20: Jane was diagnosed with bipolar disorder and started on quetiapine 500mg.
<|eot_id|><|start_header_id|>assistant<|end_header_id|>
User, Node Type, Node Name, Timestamp, Dose, Frequency, Route, Relationship Type, Age at Death, Cause of Death, Impact on Mental Health
Jane,Illness,bipolar disorder,2022-09-20,,,,,,,
Jane,Medicine,quetiapine,2022-09-20,500mg,,,,,
<|eot_id|><|start_header_id|>user<|end_header_id|>
2021-08-25: Jane mentioned during a consultation that her brother had died in a car accident when he was 18, which had a significant impact on her mental health.
<|eot_id|><|start_header_id|>assistant<|end_header_id|>
User, Node Type, Node Name, Timestamp, Dose, Frequency, Route, Relationship Type, Age at Death, Cause of Death, Impact on Mental Health
Jane,Family,brother,,,,,,sibling,18,car accident,significant

<|eot_id|><|start_header_id|>user<|end_header_id|>
