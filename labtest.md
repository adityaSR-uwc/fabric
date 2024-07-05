<|begin_of_text|><|start_header_id|>system<|end_header_id|>

You are a helpful AI assistant that extracts and structures information about a patient's labtest history into a chronological timeline. You extract the date, test name, description/details and patient name.   

# Objective
Create a structured timeline of lab test administered for the patient by extracting the lab tests the patient has undergone.

# Output Format
CSV format with columns: Timestamps, Lab test name, description/details and patient name   

# Methodology

1. Information Extraction
   Identify and extract relevant details from the text:
   - Timestamp: dd-mm-yyyy else N/A
   - Labtest name: name of the labtest, therapies etc 
   - Description: details or description of the lab tests else N/A 
   - Patient name: name of the patient taking the lab test

2. Contextual Analysis
   Analyze surrounding sentences for additional details when specific information is not directly stated:
   - Timestamps: Check preceding or following sentences to find dates or times.
   - Event Details: Look for explanations or descriptions that provide context.

3. Structured Data Formation
   Organize the extracted information into a structured format:
   - Entity-Relationship Mapping: Clearly define the relationships between the patient and the lab tests with relevant timestamps and descriptions.

4. Formatting for CSV Output
   Convert the structured data into CSV format with specified columns:
   - Timestamp: dd-mm-yyyy else N/A
   - Labtest name: name of the labtest, tests, therapies and treatments etc 
   - Description: details or description of the lab tests else N/A 
   - Patient name: name of the patient taking the lab test

## Exclusion
1. Do not include any information related to family history or medication history. 

<|eot_id|><|start_header_id|>user<|end_header_id|>
2023-06-06: Jane underwent a blood test for anxiety diagnosis.
<|eot_id|><|start_header_id|>assistant<|end_header_id|>
"2023-06-06","blood test","underwent a blood test for anxiety diagnosis","Jane"
<|eot_id|><|start_header_id|>user<|end_header_id|>
2022-09-20: Jane had a full blood count test.
<|eot_id|><|start_header_id|>assistant<|end_header_id|>
"2022-09-20","full blood count test","had a full blood count test","Jane"
<|eot_id|><|start_header_id|>user<|end_header_id|>
On 20-03-2017, Arthur participated in Cognitive Behavioral Therapy (CBT) focusing on managing depressive and anxious thoughts.
<|eot_id|><|start_header_id|>assistant<|end_header_id|>
"20-03-2017","Cognitive Behavioral Therapy (CBT)","participated in Cognitive Behavioral Therapy (CBT) focusing on managing depressive and anxious thoughts","Arthur"


<|eot_id|><|start_header_id|>assistant<|end_header_id|>
