<|eot_id|><|start_header_id|>system<|end_header_id|>


# Objective
Create a structured patient knowledge graph by extracting entities and relationships related to personal and socio-economic factors.

# Output Format
Output line by line in CSV format with only the relevant columns for each sentence.

# Methodology
1. Information Extraction
   Identify and extract relevant details from the text:
   - User: Patient name
   - Node Type: Lifestyle, Occupation, Income, Political Inclination, Religion, Education, Family Structure, MBTI Personality, Physical Fitness
   - Node Name: name of the entity in node type (e.g., running, engineer, atheist)
   - Edge Attributes: this contains the details of the connection between User and Node
      For example,
      - For Node Type "Lifestyle", the edge attributes can be Timestamp
      - For Node Type "Occupation", the edge attributes can be Timestamp
      - For Node Type "Income", the edge attributes can be Timestamp
      - For Node Type "Political Inclination", the edge attributes can be Timestamp
      - For Node Type "Religion", the edge attributes can be Timestamp
      - For Node Type "Education", the edge attributes can be Timestamp, Level (Postgrad, Undergrad), Specialisation
      - For Node Type "Family Structure", the edge attributes can be Timestamp
      - For Node Type "MBTI Personality", the edge attributes can be Timestamp
      - For Node Type "Physical Fitness", the edge attributes can be Timestamp

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
   - Node Type: Lifestyle, Occupation, Income, Political Inclination, Religion, Education, Family Structure, MBTI Personality, Physical Fitness (one of these fields only)
   - Node Name: name of the entity in node type (e.g., running, engineer, atheist)
   - Edge Attributes:
     - Expand into relevant columns (e.g., Timestamp, Level (Postgrad, Undergrad), Specialisation)
     - Ensure that only relevant columns are included for each sentence.
     - For a line having same column headers as the previous one, add the new csv values under the same column headers.

<|eot_id|><|start_header_id|>user<|end_header_id|>
2023-01-25: Emma completed her undergraduate degree in biology.
<|eot_id|><|start_header_id|>assistant<|end_header_id|>

User, Node Type, Node Name, Date, Level, Specialisation
Emma, Education, degree, 2023-01-25, undergraduate, biology

<|eot_id|><|start_header_id|>user<|end_header_id|>
On 2022-09-10, Mark started working as a software engineer.
<|eot_id|><|start_header_id|>assistant<|end_header_id|>

User, Node Type, Node Name, Date
Mark, Occupation, software engineer, 2022-09-10

<|eot_id|><|start_header_id|>user<|end_header_id|>
Sara reported an income of $75,000 per year on 2021-05-15.
<|eot_id|><|start_header_id|>assistant<|end_header_id|>

User, Node Type, Node Name, Date, Income
Sara, Income, annual, 2021-05-15, $75,000

<|eot_id|><|start_header_id|>user<|end_header_id|>
John identified as politically inclined towards the left. This happened on 2020-08-20.
<|eot_id|><|start_header_id|>assistant<|end_header_id|>

User, Node Type, Node Name, Date
John, Political Inclination, left, 2020-08-20


<|eot_id|><|start_header_id|>user<|end_header_id|>
