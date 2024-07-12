<|eot_id|><|start_header_id|>system<|end_header_id|>

# Objective
Create a structured patient knowledge graph by extracting entities and relationships related to a patient's lab tests and assessments.

# Output Format
Output line by line in CSV format with only the relevant columns for each sentence.

# Methodology
1. Information Extraction
   Identify and extract relevant details from the text:
   - User: Patient name
   - Node Type: Lab Test, Assessment, Vitals
   - Node Name: name of the entity in node type (e.g., CBC, blood pressure)
   - Edge Attributes: this contains the details of the connection between User and Node
      For example,
      - For Node Type "Lab Test", the edge attributes can be Timestamp, Interpretation, Result Value
      - For Node Type "Assessment", the edge attributes can be Timestamp, Interpretation, Result Value
      - For Node Type "Vitals", the edge attributes can be Timestamp, Interpretation, Result Value

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
   - Node Type: Lab Test, Assessment, Vitals (one of these fields only)
   - Node Name: name of the entity in node type (e.g., CBC, blood pressure)
   - Edge Attributes:
     - Expand into relevant columns (e.g., Timestamp, Interpretation, Result Value)
     - Ensure that only relevant columns are included for each sentence.
     - For a line having same column headers as the previous one, add the new csv values under the same column headers.

<|eot_id|><|start_header_id|>user<|end_header_id|>
On 2024-02-15, Jane had a CBC test with a result value of 13.5 g/dL, which was interpreted as normal.
<|eot_id|><|start_header_id|>assistant<|end_header_id|>

User, Node Type, Node Name, Date, Result Value, Interpretation
Jane, Lab Test, CBC, 2024-02-15, 13.5 g/dL, normal

<|eot_id|><|start_header_id|>user<|end_header_id|>
2023-07-08: Mark underwent a cholesterol test showing 250 mg/dL, interpreted as high.
<|eot_id|><|start_header_id|>assistant<|end_header_id|>

User, Node Type, Node Name, Date, Result Value, Interpretation
Mark, Lab Test, cholesterol, 2023-07-08, 250 mg/dL, high
<|eot_id|><|start_header_id|>user<|end_header_id|>
Amy had a blood glucose test with a result of 110 mg/dL, considered borderline on 2022-11-20.
<|eot_id|><|start_header_id|>assistant<|end_header_id|>

User, Node Type, Node Name, Date, Result Value, Interpretation
Amy, Lab Test, blood glucose, 2022-11-20, 110 mg/dL, borderline
<|eot_id|><|start_header_id|>user<|end_header_id|>
Steve's MRI scan showed normal results. This happended on 2021-03-12.
<|eot_id|><|start_header_id|>assistant<|end_header_id|>

User, Node Type, Node Name, Date, Interpretation
Steve, Lab Test, MRI scan, 2021-03-12, normal

<|eot_id|><|start_header_id|>user<|end_header_id|>
