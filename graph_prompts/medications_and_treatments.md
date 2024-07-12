<|eot_id|><|start_header_id|>system<|end_header_id|>

# Objective
Create a structured patient knowledge graph by extracting entities and relationships related to a patient's medications and treatment routes.

# Output Format
Output line by line in CSV format with only the relevant columns for each sentence.

# Methodology
1. Information Extraction
   Identify and extract relevant details from the text:
   - User: Patient name
   - Node Type: Medicine, Treatment Route
   - Node Name: name of the entity in node type (e.g., paracetamol, oral)
   - Edge Attributes: this contains the details of the connection between User and Node
      For example,
      - For Node Type "Medicine", the edge attributes can be Timestamp, Allergic to, Dosage, Frequency, Route
      - For Node Type "Treatment Route", the edge attributes can be Duration, Timestamp

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
   - Node Type: Medicine, Treatment Route (one of these fields only)
   - Node Name: name of the entity in node type (e.g., paracetamol, oral)
   - Edge Attributes:
     - Expand into relevant columns (e.g., Timestamp, Allergic to, Dosage, Frequency, Route, Duration)
     - Ensure that only relevant columns are included for each sentence.
     - For a line having same column headers as the previous one, add the new csv values under the same column headers.

<|eot_id|><|start_header_id|>user<|end_header_id|>
20-11-2020: Jane Doe started taking Lisinopril, Metformin, and Lorazepam.
<|eot_id|><|start_header_id|>assistant<|end_header_id|>

User, Node Type, Node Name, Date
Jane Doe, Medicine, Lisinopril, 2020-11-20
Jane Doe, Medicine, Metformin, 2020-11-20
Jane Doe, Medicine, Lorazepam, 2020-11-20

<|eot_id|><|start_header_id|>user<|end_header_id|>
2024-01-21: Jane visited the clinic with a high fever and was prescribed paracetamol 100mg twice daily after food.
<|eot_id|><|start_header_id|>assistant<|end_header_id|>

User, Node Type, Node Name, Date
Jane, Symptoms, high fever, 2024-01-21

User, Node Type, Node Name, Date, Dose, Frequency, Route
Jane, Medicine, paracetamol, 2024-01-21, 100mg, twice daily, oral

<|eot_id|><|start_header_id|>user<|end_header_id|>
2021-12-01: Tom was given aspirin 75mg once daily for heart protection.
<|eot_id|><|start_header_id|>assistant<|end_header_id|>
User, Node Type, Node Name, Date, Dose, Frequency, Route
Tom, Medicine, aspirin, 2021-12-01, 75mg, once daily, oral

<|eot_id|><|start_header_id|>user<|end_header_id|>
2020-07-22: Emma's doctor prescribed her metformin 1000mg twice a day for diabetes management.
<|eot_id|><|start_header_id|>assistant<|end_header_id|>

User, Node Type, Node Name, Date, Dose, Frequency, Route
Emma, Medicine, metformin, 2020-07-22, 1000mg, twice a day, oral

User, Node Type, Node Name
Emma, Illness, Diabetes

<|eot_id|><|start_header_id|>user<|end_header_id|>
