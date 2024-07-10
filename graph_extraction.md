<|eot_id|><|start_header_id|>system<|end_header_id|>

system

# Objective
Create a structured patient knowledge graph by extracting entities and relationships related to a patient's illness, medications, lab tests, socio-economic factors, lifestyle, family history, and treatment regime.

# Output Format
Output line by line in CSV format with only the relevant columns for each sentence.

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
   Convert the structured data into CSV format with relevant columns for each sentence:
   - User: Patient name, friends/family members, clinician (single value)
   - Node Type: Illness, Symptoms, Medicine, Lab Test, Clinician/Expert, Hospitalisation, Vitals, Assessment, Food, Nutrients, Family, Lifestyle, Gene, Country, Gender, Sex, Sexual Preference, Relationship Status, Occupation, Income, Political Inclination, Religion, Education, Family Structure, MBTI Personality, Physical Fitness, Medicine, Treatment Route (one of these fields only) (single value)
   - Node Name: name of the entity in node type (paracetamol, Fever, CBC etc) (single value)
   - Edge Attributes:
     - Expand into relevant columns (e.g., Date, Dose, Frequency, Route, Relationship Type, Age at Death, Cause of Death, Impact on Mental Health, Timestamp, Severity, Allergic to, Dosage, Interpretation, Result Value, Consultation Type, Date Start, Date End, Deficient In, Plentiful In, Level (Postgrad, Undergrad), Specialisation, Symptoms, Route Administered, Duration)
     - Convert the structured data into CSV format with relevant columns for each sentence.
   - Ensure that only relevant columns are included for each sentence.

<|eot_id|><|start_header_id|>user<|end_header_id|>
20-11-2020: Jane Doe started taking Lisinopril, Metformin, and Lorazepam.

<|eot_id|><|start_header_id|>assistant<|end_header_id|>
User, Node Type, Node Name, Date
Jane Doe,Medicine,Lisinopril,2020-11-20

User, Node Type, Node Name, Date
Jane Doe,Medicine,Metformin,2020-11-20

User, Node Type, Node Name, Date
Jane Doe,Medicine,Lorazepam,2020-11-20
<|eot_id|><|start_header_id|>user<|end_header_id|>
2024-01-21: Jane visited the clinic with a high fever and was prescribed paracetamol 100mg twice daily after food.
<|eot_id|><|start_header_id|>assistant<|end_header_id|>
User, Node Type, Node Name, Date
Jane,Symptoms,high fever,2024-01-21

User, Node Type, Node Name, Date, Dose, Frequency, Route
Jane,Medicine,paracetamol,2024-01-21,100mg,twice daily,oral
<|eot_id|><|start_header_id|>user<|end_header_id|>
2023-06-06: Jane reported anxiety and was diagnosed with Generalised Anxiety Disorder (GAD). She was prescribed clonazepam 250mg for two weeks once daily.
<|eot_id|><|start_header_id|>assistant<|end_header_id|>
User, Node Type, Node Name, Date
Jane,Illness,Generalised Anxiety Disorder (GAD),2023-06-06

User, Node Type, Node Name, Date, Dose, Frequency, Route
Jane,Medicine,clonazepam,2023-06-06,250mg,once daily for two weeks,oral
<|eot_id|><|start_header_id|>user<|end_header_id|>
2022-09-20: Jane was diagnosed with bipolar disorder and started on quetiapine 500mg.
<|eot_id|><|start_header_id|>assistant<|end_header_id|>
User, Node Type, Node Name, Date
Jane,Illness,bipolar disorder,2022-09-20

User, Node Type, Node Name, Date, Dose
Jane,Medicine,quetiapine,2022-09-20,500mg
<|eot_id|><|start_header_id|>user<|end_header_id|>
2021-08-25: Jane mentioned during a consultation that her brother had died in a car accident when he was 18, which had a significant impact on her mental health.
<|eot_id|><|start_header_id|>assistant<|end_header_id|>
User, Node Type, Node Name, Date, Relationship Type, Age at Death, Cause of Death, Impact on Mental Health
Jane,Family,brother,2021-08-25,,,,,sibling,18,car accident,significant
<|eot_id|><|start_header_id|>user<|end_header_id|>
John Smith has a complex medical and family history that has significantly impacted his mental health over the years. His father, an alcoholic, passed away on 10-05-1995 at age 45 from liver cirrhosis, while his brother died in a car accident on 15-08-2002 at age 18. His mother suffers from schizophrenia and liver cirrhosis. John's medical history includes several major events. On 05-03-2015, he experienced a major depressive episode triggered by the anniversary of his brother's death.
<|eot_id|><|start_header_id|>assistant<|end_header_id|>
User, Node Type, Node Name, Date, Age at Death, Cause of Death
John Smith,Family,Father,1995-05-10,45,liver cirrhosis

User, Node Type, Node Name, Date, Age at Death, Cause of Death
John Smith,Family,Brother,2002-08-15,18,car accident

User, Node Type, Node Name, Age at Death, Cause of Death
John Smith,Family,Mother,schizophrenia and liver cirrhosis

User, Node Type, Node Name, Date
John Smith,Illness,major depressive episode,2015-03-05

<|eot_id|><|start_header_id|>user<|end_header_id|>

