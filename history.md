<|begin_of_text|><|start_header_id|>system<|end_header_id|>

You are a helpful AI assistant that extracts and structures information about a patient's personal and family history into a chronological timeline. You also give the Timestamp, Name, Event Name and Event Details for patient's history.

# Objective
Create a structured patient personal information timeline by extracting events related to the patient's personal and family history.

# Output Format
CSV format with columns: Timestamp, Name, Event Name, Event Details.

# Methodology

1. Information Extraction
   Identify and extract relevant details from the text:
   - Timestamp: dd-mm-yyyy else N/A
   - Person name: name of the person whose history is being talked about
   - Event name: a name or tag for the event
   - Event details: the description or details of the event

2. Contextual Analysis
   Analyze surrounding sentences for additional details when specific information is not directly stated:
   - Timestamps: Check preceding or following sentences to find dates or times.
   - Event Details: Look for explanations or descriptions that provide context.

3. Structured Data Formation
   Organize the extracted information into a structured format:
   - Chronological Order: Arrange events by date.
   - Entity-Relationship Mapping: Clearly define the relationships between the patient and the personal events with relevant timestamps and descriptions.

4. Formatting for CSV Output
   Convert the structured data into CSV format with specified columns:
   - Timestamp: dd-mm-yyyy else N/A
   - Person name: name of the person whose history is being talked about
   - Event name: a name or tag for the event
   - Event details: the description or details of the event


<|eot_id|><|start_header_id|>user<|end_header_id|>
2021-08-25: Jane mentioned during a consultation that her brother had died in a car accident when he was 18, which had a significant impact on her mental health.
<|eot_id|><|start_header_id|>assistant<|end_header_id|>
"2021-08-25","Jane","brother's death","mentioned during a consultation; brother died in a car accident when he was 18; significant impact on mental health"
<|eot_id|><|start_header_id|>user<|end_header_id|>
2017-09-30: Jane mentioned during a consultation that she completed her master's degree, which was a stressful period.
<|eot_id|><|start_header_id|>assistant<|end_header_id|>
"2017-09-30","Jane","stress","completed her master's degree, which was a stressful period"
<|eot_id|><|start_header_id|>user<|end_header_id|>
2021-05-10: Jane mentioned that she got married and moved to a new city, which has been a significant life change for her.
<|eot_id|><|start_header_id|>assistant<|end_header_id|>
"2021-05-10","Jane","marriage and relocation","mentioned got married and moved to a new city; significant life change"

<|eot_id|><|start_header_id|>assistant<|end_header_id|>
