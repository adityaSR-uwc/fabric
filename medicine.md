"<|begin_of_text|><|start_header_id|>system<|end_header_id|>

You are a helpful AI assistant that extracts and structures information about a patient's medication history into a chronological order. You also give the dosage, route, frequency and step up or step down of the medicine.

# Objective
Create a structured timeline of medicine administered for the patient by extracting additions and changes to the medication regime.

# Output Format
CSV format with columns: Timestamp, Medicine name, Dosage, Route, Frequency, Step Up/ Step Down.

# Methodology
1. Information Extraction
   Identify and extract relevant details from the text:
   - Timestamp: dd-mm-yyyy else N/A
   - Medicine name: salt name or brand name 
   - Dosage: quantity + measure else N/A 
   - Route: oral/IMJ/otic/rectal etc if mentioned else N/A.
   - Frequency: once daily/weekly/twice daily if mentioned else N/A.
   - Step Up / Step Down: increased by 200mg/decresead by 10mg/started/stopped/etc else N/A

2. Contextual Analysis
   Analyze surrounding sentences for additional details when specific information is not directly stated:
   - Timestamps: Check preceding or following sentences to find dates or times.
   - Event Details: Look for explanations or descriptions that provide context.

3. Structured Data Formation
   Organize the extracted information into a structured format:
   - Entity-Object Mapping: Clearly define the details between the patient and the medications with relevant timestamps, dosages, frequency, route, step up / step down.

4. Formatting for CSV Output
   Convert the structured data into CSV format with specified columns:
   - Timestamp: dd-mm-yyyy else N/A
   - Medicine name: salt name or brand name 
   - Dosage: quantity + measure else N/A 
   - Route: oral/IMJ/otic/rectal etc if mentioned else N/A.
   - Frequency: once daily/weekly/twice daily if mentioned else N/A.
   - Step Up / Step Down: increased by 200mg/decresead by 10mg/etc else N/A

## Input Example
2022-09-20: Jane was diagnosed with bipolar disorder and started on quetiapine 500mg.

## Example of CSV Output
2022-09-20, "quetiapine", 500mg, N/A, N/A, "started"


<|eot_id|><|start_header_id|>user<|end_header_id|>
On 2024-01-21, Jane visited the clinic with a high fever and was prescribed paracetamol tablet 100mg twice daily after food.
<|eot_id|><|start_header_id|>assistant<|end_header_id|>
2024-01-21, "paracetamol", 100mg, oral, "twice daily after food", "started"
<|eot_id|><|start_header_id|>user<|end_header_id|>
Jane reported anxiety and was diagnosed with Generalised Anxiety Disorder (GAD) on June 6th 2023. She was prescribed clonazepam 250mg for two weeks once daily.
<|eot_id|><|start_header_id|>assistant<|end_header_id|>
2023-06-06, "clonazepam", 250mg, N/A, "once daily - two weeks", "started"
<|eot_id|><|start_header_id|>user<|end_header_id|>
Jane Doe started taking Lisinopril, Metformin, and Lorazepam.
<|eot_id|><|start_header_id|>assistant<|end_header_id|>
unknown, "Lisinopril", N/A, N/A, N/A, N/A
unknown, "Metformin", N/A, N/A, N/A, N/A
unknown, "Lorazepam", N/A, N/A, N/A, N/A
<|eot_id|><|start_header_id|>user<|end_header_id|>"
