<|eot_id|><|start_header_id|>system<|end_header_id|>

# Objective
Create a structured patient knowledge graph by extracting entities and relationships related to a patient's illness and symptoms.

# Output Format
Output line by line in CSV format with only the relevant columns for each sentence.

# Methodology
1. Information Extraction
   Identify and extract relevant details from the text:
   - User: Patient name
   - Node Type: Illness, Symptoms
   - Node Name: name of the entity in node type (e.g., Fever, Generalised Anxiety Disorder)
   - Edge Attributes: this contains the details of the connection between User and Node
      For example,
      - For Node Type "Illness", the edge attributes can be Timestamp, Severity
      - For Node Type "Symptoms", the edge attributes can be Timestamp, Severity

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
   - Node Type: Illness, Symptoms (one of these fields only)
   - Node Name: name of the entity in node type (e.g., Fever, Generalised Anxiety Disorder)
   - Edge Attributes:
     - Expand into relevant columns (e.g., Timestamp, Severity)
     - Ensure that only relevant columns are included for each sentence.
     - For a line having same column headers as the previous one, add the new csv values under the same column headers.

## Example Input
On 2023-06-06, Jane reported anxiety and was diagnosed with Generalised Anxiety Disorder (GAD).

## Example Output

User, Node Type, Node Name, Date
Jane, Illness, Generalised Anxiety Disorder (GAD), 2023-06-06
Jane, Symptoms, anxiety, 2023-06-06

<|eot_id|><|start_header_id|>user<|end_header_id|>
Mary reported experiencing fatigue and was later diagnosed with anemia on 2022-11-03.
<|eot_id|><|start_header_id|>assistant<|end_header_id|>

User, Node Type, Node Name, Date
Mary, Symptoms, fatigue, 2022-11-03
Mary, Illness, anemia, 2022-11-03

<|eot_id|><|start_header_id|>user<|end_header_id|>
Robert had a persistent cough which was identified as bronchitis. This happened on 2021-08-15.
<|eot_id|><|start_header_id|>assistant<|end_header_id|>

User, Node Type, Node Name, Date
Robert, Symptoms, persistent cough, 2021-08-15
Robert, Illness, bronchitis, 2021-08-15

<|eot_id|><|start_header_id|>user<|end_header_id|>
2020-02-29: Alice experienced shortness of breath and was diagnosed with asthma.
<|eot_id|><|start_header_id|>assistant<|end_header_id|>

User, Node Type, Node Name, Date
Alice, Symptoms, shortness of breath, 2020-02-29
Alice, Illness, asthma, 2020-02-29

<|eot_id|><|start_header_id|>user<|end_header_id|>
