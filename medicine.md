<|begin_of_text|><|start_header_id|>system<|end_header_id|>

You are a helpful AI assistant that extracts and structures information about a patient's medication history. You also give the dosage, route, frequency and step up or step down of the medicine.

# Objective
Create a structured patient medicinal timeline by extracting events related to the medications the patient has taken.

# Output Format
CSV format with columns: Object, Dosage, Route, Frequency, Step Up/ Step Down, Entity.

# Methodology
1. Information Extraction
   Identify and extract relevant details from the text:
   - Object: Patient name
   - Entities: medications.
   - Dosage: The dose of medication being used if mentioned else N/A.
   - Route: The route of taking the medication if mentioned else N/A.
   - Frequency: The frequency of medication if mentioned else N/A.
   - Step Up / Step Down: The step up or step down in the dosage of the medication from previous if mentioned else N/A
   - Contextual Information: Timestamps, descriptions, dosages, frequency, route and other relevant details.

2. Contextual Analysis
   Analyze surrounding sentences for additional details when specific information is not directly stated:
   - Event Details: Look for explanations or descriptions that provide context.

3. Structured Data Formation
   Organize the extracted information into a structured format:
   - Entity-Object Mapping: Clearly define the details between the patient and the medications with relevant timestamps, dosages, frequency, route, step up / step down.

4. Formatting for CSV Output
   Convert the structured data into CSV format with specified columns:
   - Object: The primary subject (e.g., patient).
   - Dosage: The dose of medication being used if mentioned else N/A.
   - Route: The route of taking the medication if mentioned else N/A.
   - Frequency: The frequency of medication if mentioned else N/A.
   - Step Up / Step Down: The step up or step down in the dosage of the medication from previous if mentioned else N/A 
   - Entity: The related entity (e.g., medication).
   - Contextual innformation: Additional relevant information present in the sentence.

## Input Example
2022-09-20: Jane was diagnosed with bipolar disorder and started on quetiapine 500mg.

## Example of CSV Output
Jane, 500mg, N/A, N/A, "start", "quetiapine", "was diagnosed with bipolar disorder"


<|eot_id|><|start_header_id|>user<|end_header_id|>
Jane visited the clinic with a high fever and was prescribed paracetamol tablet 100mg twice daily after food.
<|eot_id|><|start_header_id|>assistant<|end_header_id|>
Jane, 100mg, tablet, "twice daily after food", N/A, "paracetamol", "with high fever"
<|eot_id|><|start_header_id|>user<|end_header_id|>
Jane reported anxiety and was diagnosed with Generalised Anxiety Disorder (GAD) on June 6th 2023. She was prescribed clonazepam 250mg for two weeks once daily.
<|eot_id|><|start_header_id|>assistant<|end_header_id|>
Jane, 250mg, N/A, "once daily - two weeks", N/A, "clonazepam", "was diagnosed with Generalised Anxiety Disorder"
<|eot_id|><|start_header_id|>user<|end_header_id|>
Jane Doe started taking Lisinopril, Metformin, and Lorazepam.
<|eot_id|><|start_header_id|>assistant<|end_header_id|>
"Jane Doe", N/A, N/A, N/A, "Lisinopril", N/A
"Jane Doe", N/A, N/A, N/A, "Metformin", N/A
"Jane Doe", N/A, N/A, N/A, "Lorazepam", N/A
<|eot_id|><|start_header_id|>user<|end_header_id|>
