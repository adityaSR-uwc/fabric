<|eot_id|><|start_header_id|>system<|end_header_id|>

# Objective
Create a structured patient knowledge graph by extracting entities and relationships related to demographics and family history.

# Output Format
Output line by line in CSV format with only the relevant columns for each sentence.

# Methodology
1. Information Extraction
   Identify and extract relevant details from the text:
   - User: Patient name
   - Node Type: Family, Gene, Country, Gender, Sex, Sexual Preference, Relationship Status
   - Node Name: name of the entity in node type (e.g., brother, XX chromosome, USA)
   - Edge Attributes: this contains the details of the connection between User and Node
      For example,
      - For Node Type "Family", the edge attributes can be Relationship Type, Age at Death, Cause of Death, Impact on Mental Health, Timestamp

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
   - User: Patient name
   - Node Type: Family (one of these fields only)
   - Node Name: name of the entity in node type (e.g., brother, mother, friend etc)
   - Edge Attributes:
     - Expand into relevant columns (e.g., Relationship Type, Age at Death, Cause of Death, Impact on Mental Health, Timestamp)
     - Ensure that only relevant columns are included for each sentence.
     - For a line having same column headers as the previous one, add the new csv values under the same column headers.

<|eot_id|><|start_header_id|>user<|end_header_id|>
2021-08-25: Jane mentioned during a consultation that her brother had died in a car accident when he was 18, which had a significant impact on her mental health.
<|eot_id|><|start_header_id|>assistant<|end_header_id|>

User, Node Type, Node Name, Date, Relationship Type, Age at Death, Cause of Death, Impact on Mental Health
Jane, Family, brother, 2021-08-25, sibling, 18, car accident, significant

<|eot_id|><|start_header_id|>user<|end_header_id|>
John Smith has a complex medical and family history that has significantly impacted his mental health over the years. His father, an alcoholic, passed away on 10-05-1995 at age 45 from liver cirrhosis, while his brother died in a car accident on 15-08-2002 at age 18. His mother suffers from schizophrenia and liver cirrhosis. John's medical history includes several major events. On 05-03-2015, he experienced a major depressive episode triggered by the anniversary of his brother's death.
<|eot_id|><|start_header_id|>assistant<|end_header_id|>

User, Node Type, Node Name, Date, Age at Death, Cause of Death
John Smith, Family, Father, 1995-05-10, 45, liver cirrhosis
John Smith, Family, Brother, 2002-08-15, 18, car accident

User, Node Type, Node Name, Age at Death, Cause of Death
John Smith, Family, Mother, schizophrenia and liver cirrhosis

<|eot_id|><|start_header_id|>user<|end_header_id|>
2023-03-15: Anna's mother, Ella was diagnosed with Alzheimer's disease.
<|eot_id|><|start_header_id|>assistant<|end_header_id|>

User, Node Type, Node Name, Date, Relationship Type, Illness
Anna, Family, Ella, 2023-03-15, mother, Alzheimer's disease

<|eot_id|><|start_header_id|>user<|end_header_id|>
2022-06-12: Bob mentioned that his father passed away at age 70 due to heart failure.
<|eot_id|><|start_header_id|>assistant<|end_header_id|>

User, Node Type, Node Name, Date, Relationship Type, Age at Death, Cause of Death
Bob, Family, father, 2022-06-12, father, 70, heart failure


<|eot_id|><|start_header_id|>user<|end_header_id|>
