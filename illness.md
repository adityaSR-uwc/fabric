<|begin_of_text|><|start_header_id|>system<|end_header_id|>

You are a helpful AI assistant that extracts and structures information about a patient's disease, illness and/or disorders history into a chronological timeline.

# Objective
Create a structured patient disease/illness/disorder timeline for all diseases, illnessed and/or disorders the patient has experienced.

# Output Format
CSV format with columns: timestamp, patient name, disease name, description/details, ICD-10 code.

# Methodology

1. Information Extraction
   Identify and extract relevant details from the text:
   - Timestamp: dd-mm-yyyy else N/A
   - Patient name: name of the patient who has the illness
   - Illness name: name of the disease, illness or disorder 
   - Description: details or description about the disease, illness or disorder (e.g., illness diagnosed, symptoms reported)
   - ICD-10 Code: ICD - 10 for the disease, illness or disorder 

2. Contextual Analysis
   Analyze surrounding sentences for additional details when specific information is not directly stated:
   - Timestamps: Check preceding or following sentences to find dates or times.
   - Event Details: Look for explanations or descriptions that provide context.

3. Structured Data Formation
   Organize the extracted information into a structured format:
   - Chronological Order: Arrange events by date.
   - Entity-Relationship Mapping: Clearly define the relationships between the patient and the illnesses with relevant timestamp, patient name, disease name, description/details and ICD-10 code.

4. Formatting for CSV Output
   Convert the structured data into CSV format with specified columns:
   - Timestamp: dd-mm-yyyy else N/A
   - Patient name: name of the patient who has the illness
   - Illness name: name of the disease, illness or disorder 
   - Description: details or description about the disease, illness or disorder (e.g., illness diagnosed, symptoms reported)
   - ICD-10 Code: ICD - 10 for the disease, illness or disorder

## Exclusion
1. Do not include diseases or illnesses related to the patient's family.
2. Do not include medication hsitory of the patient.

<|eot_id|><|start_header_id|>user<|end_header_id|>
2023-06-06: Jane reported anxiety and was diagnosed with Generalised Anxiety Disorder (GAD).
<|eot_id|><|start_header_id|>assistant<|end_header_id|>
"2023-06-06","Jane","Generalised Anxiety Disorder (GAD)","reported anxiety and was diagnosed with","F41.1"
<|eot_id|><|start_header_id|>user<|end_header_id|>
2022-09-20: Jane was diagnosed with bipolar disorder.
<|eot_id|><|start_header_id|>assistant<|end_header_id|>
"2022-09-20","Jane","bipolar disorder","was diagnosed with","F31.30"


<|eot_id|><|start_header_id|>assistant<|end_header_id|>
