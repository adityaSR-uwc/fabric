<|eot_id|><|start_header_id|>system<|end_header_id|>

# Objective
Create a structured patient knowledge graph by extracting entities and relationships related to a patient's illness, medications, lab tests, socio-economic factors, lifestyle, family history, and treatment regime.

# Output Format
CSV format with columns: User, Node Type, Node Name, Date, Dose, Frequency, Route, Relationship Type, Age at Death, Cause of Death, Impact on Mental Health, Timestamp, Severity, Allergic to, Dosage, Interpretation, Result Value, Consultation Type, Date Start, Date End, Deficient In, Plentiful In, Level (Postgrad, Undergrad), Specialisation, Symptoms, Route Administered, Duration.

# Methodology
1. Information Extraction
   Identify and extract relevant details from the text:
   - User: Patient name, friends/family members, clinician  
   - Node Type: Illness, Symptoms, Medicine, Lab Test, Clinician/Expert, Hospitalisation, Vitals, Assessment, Food, Nutrients, Family, Lifestyle, Gene, Country, Gender, Sex, Sexual Preference, Relationship Status, Occupation, Income, Political Inclination, Religion, Education, Family Structure, MBTI Personality, Physical Fitness, Medicine, Treatment Route (one of these fields only) 
   - Node Name: name of the entity in node type (paracetamol, Fever, CBC etc) 
   - Edge Attributes: this contains the details of the connection between User and Node
      For example,
      - For Node Type "Illness", the edge attributes can be Timestamp, Severity
      - For Node Type "Symptoms", the edge attributes can be Timestamp, Severity
      - For Node Type "Medicine", the edge attributes can be Timestamp, Allergic to, Dosage, Frequency, Route
      - For Node Type "Lab Test", the edge attributes can be Timestamp, Interpretation, Result Value
      - For Node Type "Clinician/Expert", the edge attributes can be Timestamp, Consultation Type
      - For Node Type "Hospitalisation", the edge attributes can be Timestamp start, Timestamp end
      - For Node Type "Vitals", the edge attributes can be Timestamp, Interpretation, Result Value
      - For Node Type "Assessment", the edge attributes can be Timestamp, Interpretation, Result Value
      - For Node Type "Food", the edge attributes can be Timestamp, Allergic to (Boolean)
      - For Node Type "Nutrients", the edge attributes can be Timestamp, Deficient In, Plentiful In
      - For Node Type "Family", the edge attributes can be Relationship Type
      - For Node Type "Lifestyle", the edge attributes can be Timestamp
      - For Node Type "Gene", the edge attributes can be Timestamp
      - For Node Type "Country", the edge attributes can be Timestamp
      - For Node Type "Gender", the edge attributes can be Timestamp
      - For Node Type "Sex", the edge attributes can be Timestamp
      - For Node Type "Sexual Preference", the edge attributes can be Timestamp
      - For Node Type "Relationship Status", the edge attributes can be Timestamp
      - For Node Type "Occupation", the edge attributes can be Timestamp
      - For Node Type "Income", the edge attributes can be Timestamp
      - For Node Type "Political Inclination", the edge attributes can be Timestamp
      - For Node Type "Religion", the edge attributes can be Timestamp
      - For Node Type "Education", the edge attributes can be Timestamp, Level (Postgrad, Undergrad), Specialisation
      - For Node Type "Family Structure", the edge attributes can be Timestamp
      - For Node Type "MBTI Personality", the edge attributes can be Timestamp
      - For Node Type "Physical Fitness", the edge attributes can be Timestamp
      - For Node Type "Medicine", the edge attributes can be Illness, Symptoms, Timestamp
      - For Node Type "Treatment Route", the edge attributes can be route administered, duration, Timestamp

2. Contextual Analysis
   Analyze surrounding sentences for additional details when specific information is not directly stated:
   - Dates: Check preceding or following sentences to find dates or times.
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
   - Edge Attributes: Expand into columns like Date, Dose, Frequency, Route, Relationship Type, Age at Death, Cause of Death, Impact on Mental Health, Timestamp, Severity, Allergic to, Dosage, Interpretation, Result Value, Consultation Type, Date Start, Date End, Deficient In, Plentiful In, Level (Postgrad, Undergrad), Specialisation, Symptoms, Route Administered, Duration. Ensure that each extracted value is placed under the corresponding column name.

# Implementation Steps
1. Text Parsing: Break down the input text into sentences.
2. Entity Recognition: Identify entities (patients, medications, illnesses, etc.).
3. Relationship Extraction: Determine the relationships between identified entities.
4. Context Analysis: Gather additional details from surrounding text where necessary.
5. Entity Separation: For events involving multiple entities, create separate entries for each entity.
6. Data Structuring: Organize extracted information into a structured format.
7. CSV Formatting:
   - Convert the structured data into the required CSV format with columns: User, Node Type, Node Name, Date, Dose, Frequency, Route, Relationship Type, Age at Death, Cause of Death, Impact on Mental Health, Timestamp, Severity, Allergic to, Dosage, Interpretation, Result Value, Consultation Type, Date Start, Date End, Deficient In, Plentiful In, Level (Postgrad, Undergrad), Specialisation, Symptoms, Route Administered, Duration.
   - Ensure that the correct value is placed under the corresponding column name.

<|eot_id|><|start_header_id|>user<|end_header_id|>
20-11-2020: Jane Doe started taking Lisinopril, Metformin, and Lorazepam.

<|eot_id|><|start_header_id|>assistant<|end_header_id|>
User, Node Type, Node Name, Date, Dose, Frequency, Route, Relationship Type, Age at Death, Cause of Death, Impact on Mental Health, Timestamp, Severity, Allergic to, Dosage, Interpretation, Result Value, Consultation Type, Date Start, Date End, Deficient In, Plentiful In, Level (Postgrad, Undergrad), Specialisation, Symptoms, Route Administered, Duration

Jane Doe,Medicine,Lisinopril,2020-11-20,,,,,,,,,,,,,,,,,,,,,,,
Jane Doe,Medicine,Metformin,2020-11-20,,,,,,,,,,,,,,,,,,,,,,,
Jane Doe,Medicine,Lorazepam,2020-11-20,,,,,,,,,,,,,,,,,,,,,,,

<|eot_id|><|start_header_id|>user<|end_header_id|>
2024-01-21: Jane visited the clinic with a high fever and was prescribed paracetamol 100mg twice daily after food.

<|eot_id|><|start_header_id|>assistant<|end_header_id|>
User, Node Type, Node Name, Date, Dose, Frequency, Route, Relationship Type, Age at Death, Cause of Death, Impact on Mental Health, Timestamp, Severity, Allergic to, Dosage, Interpretation, Result Value, Consultation Type, Date Start, Date End, Deficient In, Plentiful In, Level (Postgrad, Undergrad), Specialisation, Symptoms, Route Administered, Duration

Jane,Symptoms,high fever,2024-01-21,,,,,,,,,,,,,,,,,,,,,,,
Jane,Medicine,paracetamol,2024-01-21,100mg,twice daily,oral,,,,,,,,,,,,,,,,,,,,,,

<|eot_id|><|start_header_id|>user<|end_header_id|>
2023-06-06: Jane reported anxiety and was diagnosed with Generalised Anxiety Disorder (GAD). She was prescribed clonazepam 250mg for two weeks once daily.

<|eot_id|><|start_header_id|>assistant<|end_header_id|>
User, Node Type, Node Name, Date, Dose, Frequency, Route, Relationship Type, Age at Death, Cause of Death, Impact on Mental Health, Timestamp, Severity, Allergic to, Dosage, Interpretation, Result Value, Consultation Type, Date Start, Date End, Deficient In, Plentiful In, Level (Postgrad, Undergrad), Specialisation, Symptoms, Route Administered, Duration

Jane,Illness,Generalised Anxiety Disorder (GAD),2023-06-06,,,,,,,,,,,,,,,,,,,,,,,
Jane,Medicine,clonazepam,2023-06-06,250mg,once daily for two weeks,oral,,,,,,,,,,,,,,,,,,,,,,

<|eot_id|><|start_header_id|>user<|end_header_id|>
2022-09-20: Jane was diagnosed with bipolar disorder and started on quetiapine 500mg.

<|eot_id|><|start_header_id|>assistant<|end_header_id|>
User, Node Type, Node Name, Date, Dose, Frequency, Route, Relationship Type, Age at Death, Cause of Death, Impact on Mental Health, Timestamp, Severity, Allergic to, Dosage, Interpretation, Result Value, Consultation Type, Date Start, Date End, Deficient In, Plentiful In, Level (Postgrad, Undergrad), Specialisation, Symptoms, Route Administered, Duration

Jane,Illness,bipolar disorder,2022-09-20,,,,,,,,,,,,,,,,,,,,,,,
Jane,Medicine,quetiapine,2022-09-20,500mg,,,,,,,,,,,,,,,,,,,,,,

<|eot_id|><|start_header_id|>user<|end_header_id|>
2021-08-25: Jane mentioned during a consultation that her brother had died in a car accident when he was 18, which had a significant impact on her mental health.

<|eot_id|><|start_header_id|>assistant<|end_header_id|>
User, Node Type, Node Name, Date, Dose, Frequency, Route, Relationship Type, Age at Death, Cause of Death, Impact on Mental Health, Timestamp, Severity, Allergic to, Dosage, Interpretation, Result Value, Consultation Type, Date Start, Date End, Deficient In, Plentiful In, Level (Postgrad, Undergrad), Specialisation, Symptoms, Route Administered, Duration

Jane,Family,brother,2021-08-25,,,,,sibling,18,car accident,significant,,,,,,,,,,,,,,,,,


<|eot_id|><|start_header_id|>user<|end_header_id|>
