<|eot_id|><|start_header_id|>system<|end_header_id|>

# Objective
Create a structured patient knowledge graph by extracting entities and relationships related to healthcare providers and facilities.

# Output Format
Output line by line in CSV format with only the relevant columns for each sentence.

# Methodology
1. Information Extraction
   Identify and extract relevant details from the text:
   - User: Patient name
   - Node Type: Clinician/Expert, Hospitalisation
   - Node Name: name of the entity in node type (e.g., Dr. Smith, General Hospital)
   - Edge Attributes: this contains the details of the connection between User and Node
      For example,
      - For Node Type "Clinician/Expert", the edge attributes can be Timestamp, Consultation Type
      - For Node Type "Hospitalisation", the edge attributes can be Timestamp start, Timestamp end

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
   - Node Type: Clinician/Expert, Hospitalisation (one of these fields only)
   - Node Name: name of the entity in node type (e.g., Dr. Smith, General Hospital)
   - Edge Attributes:
     - Expand into relevant columns (e.g., Timestamp, Consultation Type, Timestamp start, Timestamp end)
     - Ensure that only relevant columns are included for each sentence.
     - For a line having same column headers as the previous one, add the new csv values under the same column headers.

<|eot_id|><|start_header_id|>user<|end_header_id|>
2023-08-30: Jane consulted Dr. Smith for a follow-up visit.
<|eot_id|><|start_header_id|>assistant<|end_header_id|>

User, Node Type, Node Name, Date, Consultation Type
Jane, Clinician/Expert, Dr. Smith, 2023-08-30, follow-up

<|eot_id|><|start_header_id|>user<|end_header_id|>
On 2022-05-14, Mike was admitted to City Hospital for surgery and was discharged on 2022-05-20.
<|eot_id|><|start_header_id|>assistant<|end_header_id|>

User, Node Type, Node Name, Date Start, Date End
Mike, Hospitalisation, City Hospital, 2022-05-14, 2022-05-20

<|eot_id|><|start_header_id|>user<|end_header_id|>
Sarah had an initial consultation with Dr. Lee at the healthcare clinic on 2021-10-22.
<|eot_id|><|start_header_id|>assistant<|end_header_id|>

User, Node Type, Node Name, Date, Consultation Type
Sarah, Clinician, Dr. Lee, 2021-10-22, initial

<|eot_id|><|start_header_id|>user<|end_header_id|>
2020-12-10: David visited the ER at General Hospital for acute chest pain.
<|eot_id|><|start_header_id|>assistant<|end_header_id|>

User, Node Type, Node Name, Date, Consultation Type
David, Clinician/Expert, ER at General Hospital, 2020-12-10, emergency


<|eot_id|><|start_header_id|>user<|end_header_id|>
