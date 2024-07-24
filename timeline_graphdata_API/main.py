import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import re
import csv
import io
from io import StringIO
import json
import logging
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from pydantic import *
from typing import Optional, List, Dict, Union
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from datetime import datetime

app = FastAPI()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

ALLOWLIST_PATTERN = re.compile(r"^[a-zA-Z0-9\s.,;:!?\-]+$")

DEFAULT_MODEL = 'meta-llama/Meta-Llama-3-8B-Instruct'
OPENAI_API_KEY = 'EMPTY'
OPENAI_BASE_URL = 'https://genv2.uwc.world/v1'

now_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def sanitize_content(content):
    return "".join(char for char in content if ALLOWLIST_PATTERN.match(char))

def fetch_content_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        logger.error(f"Error fetching content from URL: {url} - {e}")
        return str(e)
 
def extract_medication_history(assistant_message):
    medication_history = []
    lines = assistant_message.split("\n")
    current_date = None
    for line in lines:
        line = line.strip()
        if line.startswith("**") and line.endswith("**"):
            current_date = line.strip("**")
        elif line.startswith("* Medicine:") and current_date:
            parts = line.split(", ")
            if len(parts) >= 5:
                medication = parts[0].replace("* Medicine:", "").strip()
                dosage = parts[1].strip()
                route = parts[2].strip()
                frequency = parts[3].strip()
                status = parts[4].strip("\"") if parts[4] != "N/A" else None
                record = {
                    "date": current_date,
                    "medication": medication,
                    "dosage": dosage,
                    "route": route,
                    "frequency": frequency,
                    "status": status
                }
                medication_history.append(record)
    return medication_history

def extract_labtest_history(assistant_message):
    labtest_history = []
    reader = csv.reader(io.StringIO(assistant_message))
    for row in reader:
        if len(row) == 4:
            labtest_name = row[1].strip("\"") if row[1] != "N/A" else None
            if labtest_name:
                record = {
                    "date": row[0].strip("\""),
                    "labtest_name": labtest_name,
                    "description": row[2].strip("\""),
                    "patient": row[3].strip("\"")
                }
                labtest_history.append(record)
    return labtest_history

def extract_illness_history(assistant_message):
    illness_history = []
    reader = csv.reader(io.StringIO(assistant_message))
    for row in reader:
        if len(row) == 5:
            illness_name = row[2].strip("\"") if row[2] != "N/A" else None
            icd = row[4].strip("\"") if row[4] != "N/A" else None
            if illness_name and icd and illness_name != "Disease/Illness/Disorder":
                record = {
                    "timestamp": row[0].strip("\""),
                    "patient_name": row[1].strip("\""),
                    "disease": illness_name,
                    "description_details": row[3].strip("\""),
                    "icd_10_code": icd
                }
                illness_history.append(record)
    return illness_history

def extract_history(assistant_message):
    history = []
    reader = csv.reader(io.StringIO(assistant_message))
    for row in reader:
        if len(row) == 4:
            record = {
                "date": row[0].strip("\""),
                "patient_name": row[1].strip("\""),
                "event": row[2].strip("\""),
                "details": row[3].strip("\"")
            }
            history.append(record)
    return history

def create_messages(system_url, user_url, input_data):
    """Create messages for API request."""
    system_content = system_url
    user_file_content = user_url

    system_message = {"role": "system", "content": system_content}
    user_message = {"role": "user", "content": user_file_content + "\n" + input_data}
    return [system_message, user_message]

def chunk_text(text: str, chunk_size: int, overlap: int) -> list:
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = ' '.join(words[i:i + chunk_size])
        chunks.append(chunk)
        i += chunk_size - overlap
    return chunks

def process_chunks(chunks: list, prompt: str) -> list:
    results = []
    graph_keyword_parser = PydanticOutputParser(pydantic_object=NodeList)

    for chunk in chunks:
        graph_prompt = PromptTemplate(
            template=prompt, input_variables=["input"], partial_variables={"format_instructions": graph_keyword_parser.get_format_instructions()}
        )

        llm = ChatOpenAI(
            model=DEFAULT_MODEL,
            temperature=0,
            max_tokens=5000,
            max_retries=2,
            api_key=OPENAI_API_KEY,  
            base_url=OPENAI_BASE_URL
        )

        chain = graph_prompt | llm | graph_keyword_parser

        response = chain.invoke({"input": chunk})
        if response:
            results.extend(response.node)
        else:
            logger.error("Received empty response for chunk: %s", chunk)

        logger.debug("Raw assistant_message content: %s", response)

    return results

def convert_edge_attributes_to_strings(node):
    if 'edge_attributes' in node:
        node['edge_attributes'] = {key: str(value) if value is not None else None for key, value in node['edge_attributes'].items()}
    return node

def parse_timeline(response):
    try:
        print("Raw response:", response)  # Debugging line to print raw response
        
        lines = response.split('\n')
        timeline_data = [line for line in lines if line.strip() and "Here is the structured and chronological patient timeline" not in line]
        
        output = []
        for line in timeline_data:
            try:
                date, event_name, description, tags = line.split(' - ', 3)
                output.append({
                    "datetime": date.strip(),
                    "event_name": event_name.strip(),
                    "event_description": description.strip(),
                    "event_tags": tags.strip()
                })
            except ValueError:
                print(f"Skipping line due to unexpected format: {line}")
                continue
        
        return output
    
    except Exception as e:
        print(f"Error processing response: {e}")
        return []    

def merge_timeline_chunks(chunks):
    merged_timeline = []
    seen_events = set()
    for chunk in chunks:
        for event in chunk:
            event_tuple = (event["datetime"], event["event_name"], event["event_description"], event["event_tags"])
            if event_tuple not in seen_events:
                seen_events.add(event_tuple)
                merged_timeline.append(event)
    return merged_timeline

timeline_prompt = f"""system

# Objective:
Create a structured and chronological patient timeline of all the clinical and important life events. Focusing on the patients illness, medication, lab-tests, socio-economic factors, lifestyle, family history, treatment regime.

# Output Format:
  Datetime - Event Name - Event Description - Event Clinical tag - ICD-10 code
 
# Steps to extract clinical and important life events

1.*Extract Relevant Information:*
   - Identify sections related to family history, diseases, and medications.
   - Organize the extracted information chronologically.
   - If dates are not provided, leave the datetime as unknown.

2.*Structure the Information:*
   - Create entries for each relevant event along with Date-time and Event Name.
   - Add a short event description to the relevant event.
   - Use the event description to extract the clinical tags.
   - Give the ICD 10 Code of the diseases.
   - Current date is {now_datetime} 

3.*Format the Information*
    - Example of the output :-
       - 2024-01-21 12:45:00 - Paracetamol - Took paracetamol 100mg for fever - Medicine,Fever
       - 2023-06-06 13:45:00 - Clonazepam - Took clonazepam 250mg for Generalised Anxiety Disorders - Medicine, Anxiety, Generalised Anxiety Disorder - F41.1
       - 2022-09-20 16:50:00 - Olanzapine - Took olanzapine 500mg for bipolar disorder - Medicine, Bipolar Disorder - F31. 9
       - 2021-08-25 15:30:00 - Brother's Death - John's brother died in a car accident at age 18 - Family History, Death, Brother, Trauma
       - unknown - Fever -  John had a fever of 104 degrees - Fever

assistant
"""

pattern_path_mappings = {
    "medicine": {"system_url": """<|begin_of_text|><|start_header_id|>system<|end_header_id|>

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
<|eot_id|><|start_header_id|>user<|end_header_id|>
    """,
                 "user_url": "https://raw.githubusercontent.com/danielmiessler/fabric/main/patterns/summarize/user.md"},
    "history": {"system_url": """<|begin_of_text|><|start_header_id|>system<|end_header_id|>

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

<|eot_id|><|start_header_id|>assistant<|end_header_id|> """,
                "user_url": "https://raw.githubusercontent.com/danielmiessler/fabric/main/patterns/summarize/user.md"},
    "labtest": {"system_url": """<|begin_of_text|><|start_header_id|>system<|end_header_id|>

You are a helpful AI assistant that extracts and structures information about a patient's labtest history into a chronological timeline. You extract the date, test name, description/details and patient name.   

# Objective
Create a structured timeline of clinical labtests and psycometric assessments administered or recommended to the patient along with the vitals of each test.

# Output Format
CSV format with columns: Timestamps, Lab test name, description/details and patient name   

# Methodology

1. Information Extraction
   Identify and extract relevant details from the text:
   - Timestamp: dd-mm-yyyy else N/A
   - Labtest name: name of the labtest, therapies etc
      - vital name
      - vital score
      - recommended threshold
      - notes/feedback/recommendations
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


<|eot_id|><|start_header_id|>assistant<|end_header_id|> """,
                "user_url": "https://raw.githubusercontent.com/danielmiessler/fabric/main/patterns/summarize/user.md"},
    "illness": {"system_url": """<|begin_of_text|><|start_header_id|>system<|end_header_id|>

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
1. Do not include any diseases or illnesses or disorders related to the patient's family.
2. Do not include medication history of the patient. (eg. Past hopitalisations, medication regime change etc)

<|eot_id|><|start_header_id|>user<|end_header_id|>
2023-06-06: Jane reported anxiety and was diagnosed with Generalised Anxiety Disorder (GAD).
<|eot_id|><|start_header_id|>assistant<|end_header_id|>
"2023-06-06","Jane","Generalised Anxiety Disorder (GAD)","reported anxiety and was diagnosed with","F41.1"
<|eot_id|><|start_header_id|>user<|end_header_id|>
2022-09-20: Jane was diagnosed with bipolar disorder.
<|eot_id|><|start_header_id|>assistant<|end_header_id|>
"2022-09-20","Jane","bipolar disorder","was diagnosed with","F31.30"


<|eot_id|><|start_header_id|>assistant<|end_header_id|> """,
                "user_url": "https://raw.githubusercontent.com/danielmiessler/fabric/main/patterns/summarize/user.md"},
    "graph_extraction": {"system_url": """<|eot_id|><|start_header_id|>system<|end_header_id|>

system

# Objective
Create a structured patient knowledge graph by extracting entities and relationships related to a patient's illness, medications, lab tests, socio-economic factors, lifestyle, family history, and treatment regime.

# Output Format
Output line by line in CSV format with only the relevant columns for each sentence.

# Methodology
1. Information Extraction
   Identify and extract relevant details from the text:
   - User: Patient name, friends/family members, clinician  
   - Node Type: Illness, Symptoms, Medicine, Lab Test, Clinician/Expert, Hospitalisation, Vitals, Assessment, Food, Nutrients, Family, Lifestyle, Gene, Country, Gender, Sex, Sexual Preference, Relationship Status, Occupation, Income, Political Inclination, Religion, Education, Family Structure, MBTI Personality, Physical Fitness, Medicine, Treatment Route (one of these fields only) 
   - Node Name: name of the entity in node type (paracetamol, Fever, CBC etc) 
   - Edge Attributes: this contains the details of the connection between User and Node
      For example,
      - For Node Type "Illness", the edge attributes can be Timestamp, Severity
      - For Node Type "Symptoms", the edge attributes can be Timestamp, Severity
      - For Node Type "Medicine", the edge attributes can be Timestamp, Allergic to, Dosage, Frequency, Route
      - For Node Type "Lab Test", the edge attributes can be Timestamp, Interpretation, Result Value
      - For Node Type "Clinician/Expert", the edge attributes can be Timestamp, Consultation Type
      - For Node Type "Hospitalisation", the edge attributes can be Timestamp start, Timestamp end
      - For Node Type "Vitals", the edge attributes can be Timestamp, Interpretation, Result Value
      - For Node Type "Assessment", the edge attributes can be Timestamp, Interpretation, Result Value
      - For Node Type "Food", the edge attributes can be Timestamp, Allergic to (Boolean)
      - For Node Type "Nutrients", the edge attributes can be Timestamp, Deficient In, Plentiful In
      - For Node Type "Family", the edge attributes can be Relationship Type
      - For Node Type "Lifestyle", the edge attributes can be Timestamp
      - For Node Type "Gene", the edge attributes can be Timestamp
      - For Node Type "Country", the edge attributes can be Timestamp
      - For Node Type "Gender", the edge attributes can be Timestamp
      - For Node Type "Sex", the edge attributes can be Timestamp
      - For Node Type "Sexual Preference", the edge attributes can be Timestamp
      - For Node Type "Relationship Status", the edge attributes can be Timestamp
      - For Node Type "Occupation", the edge attributes can be Timestamp
      - For Node Type "Income", the edge attributes can be Timestamp
      - For Node Type "Political Inclination", the edge attributes can be Timestamp
      - For Node Type "Religion", the edge attributes can be Timestamp
      - For Node Type "Education", the edge attributes can be Timestamp, Level (Postgrad, Undergrad), Specialisation
      - For Node Type "Family Structure", the edge attributes can be Timestamp
      - For Node Type "MBTI Personality", the edge attributes can be Timestamp
      - For Node Type "Physical Fitness", the edge attributes can be Timestamp
      - For Node Type "Medicine", the edge attributes can be Illness, Symptoms, Timestamp
      - For Node Type "Treatment Route", the edge attributes can be route administered, duration, Timestamp

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
   - User: Patient name, friends/family members, clinician (single value)
   - Node Type: Illness, Symptoms, Medicine, Lab Test, Clinician/Expert, Hospitalisation, Vitals, Assessment, Food, Nutrients, Family, Lifestyle, Gene, Country, Gender, Sex, Sexual Preference, Relationship Status, Occupation, Income, Political Inclination, Religion, Education, Family Structure, MBTI Personality, Physical Fitness, Medicine, Treatment Route (one of these fields only) (single value)
   - Node Name: name of the entity in node type (paracetamol, Fever, CBC etc) (single value)
   - Edge Attributes:
     - Expand into relevant columns (e.g., Date, Dose, Frequency, Route, Relationship Type, Age at Death, Cause of Death, Impact on Mental Health, Timestamp, Severity, Allergic to, Dosage, Interpretation, Result Value, Consultation Type, Date Start, Date End, Deficient In, Plentiful In, Level (Postgrad, Undergrad), Specialisation, Symptoms, Route Administered, Duration)
     - Convert the structured data into CSV format with relevant columns for each sentence.
   - Ensure that only relevant columns are included for each sentence.
   - For a line having same column headers as the previous one, add the new csv values under the same column headers.

<|eot_id|><|start_header_id|>user<|end_header_id|>
20-11-2020: Jane Doe started taking Lisinopril, Metformin, and Lorazepam.

<|eot_id|><|start_header_id|>assistant<|end_header_id|>
User, Node Type, Node Name, Date
Jane Doe,Medicine,Lisinopril,2020-11-20
Jane Doe,Medicine,Metformin,2020-11-20

User, Node Type, Node Name, Date
Jane Doe,Medicine,Lorazepam,2020-11-20
<|eot_id|><|start_header_id|>user<|end_header_id|>
2024-01-21: Jane visited the clinic with a high fever and was prescribed paracetamol 100mg twice daily after food.
<|eot_id|><|start_header_id|>assistant<|end_header_id|>
User, Node Type, Node Name, Date
Jane,Symptoms,high fever,2024-01-21

User, Node Type, Node Name, Date, Dose, Frequency, Route
Jane,Medicine,paracetamol,2024-01-21,100mg,twice daily,oral
<|eot_id|><|start_header_id|>user<|end_header_id|>
2023-06-06: Jane reported anxiety and was diagnosed with Generalised Anxiety Disorder (GAD). She was prescribed clonazepam 250mg for two weeks once daily.
<|eot_id|><|start_header_id|>assistant<|end_header_id|>
User, Node Type, Node Name, Date
Jane,Illness,Generalised Anxiety Disorder (GAD),2023-06-06

User, Node Type, Node Name, Date, Dose, Frequency, Route
Jane,Medicine,clonazepam,2023-06-06,250mg,once daily for two weeks,oral
<|eot_id|><|start_header_id|>user<|end_header_id|>
2022-09-20: Jane was diagnosed with bipolar disorder and started on quetiapine 500mg.
<|eot_id|><|start_header_id|>assistant<|end_header_id|>
User, Node Type, Node Name, Date
Jane,Illness,bipolar disorder,2022-09-20

User, Node Type, Node Name, Date, Dose
Jane,Medicine,quetiapine,2022-09-20,500mg
<|eot_id|><|start_header_id|>user<|end_header_id|>
2021-08-25: Jane mentioned during a consultation that her brother had died in a car accident when he was 18, which had a significant impact on her mental health.
<|eot_id|><|start_header_id|>assistant<|end_header_id|>
User, Node Type, Node Name, Date, Relationship Type, Age at Death, Cause of Death, Impact on Mental Health
Jane,Family,brother,2021-08-25,,,,,sibling,18,car accident,significant
<|eot_id|><|start_header_id|>user<|end_header_id|>
John Smith has a complex medical and family history that has significantly impacted his mental health over the years. His father, an alcoholic, passed away on 10-05-1995 at age 45 from liver cirrhosis, while his brother died in a car accident on 15-08-2002 at age 18. His mother suffers from schizophrenia and liver cirrhosis. John's medical history includes several major events. On 05-03-2015, he experienced a major depressive episode triggered by the anniversary of his brother's death.
<|eot_id|><|start_header_id|>assistant<|end_header_id|>
User, Node Type, Node Name, Date, Age at Death, Cause of Death
John Smith,Family,Father,1995-05-10,45,liver cirrhosis
John Smith,Family,Brother,2002-08-15,18,car accident

User, Node Type, Node Name, Cause of Death
John Smith,Family,Mother,schizophrenia and liver cirrhosis

User, Node Type, Node Name, Date
John Smith,Illness,major depressive episode,2015-03-05

<|eot_id|><|start_header_id|>user<|end_header_id|>
On 05-03-2015, Jane experienced a major depressive episode triggered by the anniversary of her brother's death. She was hospitalized for four weeks, receiving intensive psychotherapy.
<|eot_id|><|start_header_id|>assistant<|end_header_id|>
User, Node Type, Node Name, Start Date, End Date
Jane, Hospitalisation, major depressive episode,2015-03-05,2015-04-03

User, Node Type, Node Name, Date
Jane,Therapy,Psychotherapy,2015-03-05

<|eot_id|><|start_header_id|>user<|end_header_id|>
At the age of 15, Jane had a severe bout of Pneumonia.
<|eot_id|><|start_header_id|>assistant<|end_header_id|>
User, Node Type, Node Name, Age at Illness
Jane,Illness,Pneumonia,15

<|eot_id|><|start_header_id|>user<|end_header_id|> """,
                         "user_url": "https://raw.githubusercontent.com/danielmiessler/fabric/main/patterns/summarize/user.md"},
    "keyword": {"system_url": """<|begin_of_text|><|start_header_id|>system<|end_header_id|>
# IDENTITY and PURPOSE
You extract all relevant single word keywords from the input text.
Take a step back and think step-by-step about how to extract the best possible keywords by following the steps below.
# STEPS
- Identify all relevant single keywords from the text.
- Extract 5 to 15 of the most relevant, insightful, and/or interesting keywords and phrases from the input text.
- If intents such "kill, suicide, harmful behavior, aggression violence", are found in the text, then return "sos".
# OUTPUT INSTRUCTIONS
- Output only the single keywords section.
- Do not give warnings or notes; only output the requested sections.
- Use a comma-separated list for the output.
- Ensure you follow ALL these instructions when creating your output.
- Format the results as presented in the examples below:

<|eot_id|><|start_header_id|>user<|end_header_id|>
In machine learning, the term stochastic parrot is a metaphor to describe the theory that large language models, though able to generate plausible language
<|eot_id|><|start_header_id|>assistant<|end_header_id|>
stochastic parrot, machine learning, large language models, generate plausible language
<|eot_id|><|start_header_id|>user<|end_header_id|>
Suicide is a profound and complex public health issue that affects individuals, families, and communities worldwide. It often stems from untreated mental health conditions.
<|eot_id|><|start_header_id|>assistant<|end_header_id|>
sos,Suicide,Depression,Anxiety,Trauma<|eot_id|> """,
                "user_url": "https://raw.githubusercontent.com/danielmiessler/fabric/main/patterns/summarize/user.md"},
    "timeline": {"system_url": timeline_prompt,
                 "user_url": "https://raw.githubusercontent.com/danielmiessler/fabric/main/patterns/summarize/user.md"}
}

graph_prompts = {
    "health_conditions_and_symptoms": "https://raw.githubusercontent.com/adityaSR-uwc/fabric/main/graph_prompts/health_conditions_and_symptoms.md",
    "medications_and_treatments": "https://raw.githubusercontent.com/adityaSR-uwc/fabric/main/graph_prompts/medications_and_treatments.md",
    "lab_tests_and_assessments": "https://raw.githubusercontent.com/adityaSR-uwc/fabric/main/graph_prompts/labtests.md",
    "healthcare_providers_and_facilities": "https://raw.githubusercontent.com/adityaSR-uwc/fabric/main/graph_prompts/healthcare_providers_and_facilities.md",
    "diet_and_nutrition": "https://raw.githubusercontent.com/adityaSR-uwc/fabric/main/graph_prompts/diet_and_nutrition.md",
    "personal_and_socioeconomic_factors": "https://raw.githubusercontent.com/adityaSR-uwc/fabric/main/graph_prompts/personal_and_socioeconomic_factors.md",
    "family_history": "https://raw.githubusercontent.com/adityaSR-uwc/fabric/main/graph_prompts/family_history.md",
}

GRAPH_PROMPT = """
system

# Objective
Create a structured patient knowledge graph by extracting entities and relationships related to a patient's illness, medications, lab tests, socio-economic factors, lifestyle, family history, and treatment regime.

# Output Format 
{format_instructions}

# Methodology
1. Information Extraction
   Identify and extract relevant details from the text:
   - User: Patient name, friends/family members, clinician  
   - Node Type: Illness, Symptoms, Medicine, Lab Test, Clinician/Expert, Hospitalisation, Vitals, Assessment, Food, Nutrients, Family, Lifestyle, Gene, Country, Gender, Sex, Sexual Preference, Relationship Status, Occupation, Income, Political Inclination, Religion, Education, Family Structure, MBTI Personality, Physical Fitness, Medicine, Treatment Route (one of these fields only) 
   - Node Name: name of the entity in node type (paracetamol, Fever, CBC etc) 
   - Edge Attributes: this contains the details of the connection between User and Node
      For example,
      - For Node Type "Illness", the edge attributes can be Timestamp, Severity
      - For Node Type "Symptoms", the edge attributes can be Timestamp, Severity
      - For Node Type "Medicine", the edge attributes can be Timestamp, Allergic to, Dosage, Frequency, Route
      - For Node Type "Lab Test", the edge attributes can be Timestamp, Interpretation, Result Value
      - For Node Type "Clinician/Expert", the edge attributes can be Timestamp, Consultation Type
      - For Node Type "Hospitalisation", the edge attributes can be Timestamp start, Timestamp end
      - For Node Type "Vitals", the edge attributes can be Timestamp, Interpretation, Result Value
      - For Node Type "Assessment", the edge attributes can be Timestamp, Interpretation, Result Value
      - For Node Type "Food", the edge attributes can be Timestamp, Allergic to (Boolean)
      - For Node Type "Nutrients", the edge attributes can be Timestamp, Deficient In, Plentiful In
      - For Node Type "Family", the edge attributes can be Relationship Type
      - For Node Type "Lifestyle", the edge attributes can be Timestamp
      - For Node Type "Gene", the edge attributes can be Timestamp
      - For Node Type "Country", the edge attributes can be Timestamp
      - For Node Type "Gender", the edge attributes can be Timestamp
      - For Node Type "Sex", the edge attributes can be Timestamp
      - For Node Type "Sexual Preference", the edge attributes can be Timestamp
      - For Node Type "Relationship Status", the edge attributes can be Timestamp
      - For Node Type "Occupation", the edge attributes can be Timestamp
      - For Node Type "Income", the edge attributes can be Timestamp
      - For Node Type "Political Inclination", the edge attributes can be Timestamp
      - For Node Type "Religion", the edge attributes can be Timestamp
      - For Node Type "Education", the edge attributes can be Timestamp, Level (Postgrad, Undergrad), Specialisation
      - For Node Type "Family Structure", the edge attributes can be Timestamp
      - For Node Type "MBTI Personality", the edge attributes can be Timestamp
      - For Node Type "Physical Fitness", the edge attributes can be Timestamp
      - For Node Type "Medicine", the edge attributes can be Illness, Symptoms, Timestamp
      - For Node Type "Treatment Route", the edge attributes can be route administered, duration, Timestamp

2. Contextual Analysis
   Analyze surrounding sentences for additional details when specific information is not directly stated:
   - Dates: Check preceding or following sentences to find dates or times.
   - Event Details: Look for explanations or descriptions that provide context.
   - Have a 

3. Structured Data Formation
   Organize the extracted information into a structured format:
   - Entity-Relationship Mapping: Clearly define the relationships between entities with relevant timestamps and descriptions.
   - Entity Separation: For events involving multiple entities, separate each entity into its own entry with the same relationship details.

User Information:
- Name - Ayush
- Gender - Male
- Age - 24
- Date of Birth - 25-09-2000

user {input}
assistant
Note: only provide in the format: {format_instructions}. Don't provide notes and additional information."""

class Node(BaseModel):
    user: str = Field(None, description="Patient name, friends/family members, clinician")
    node_type: str = Field(None, description="One of the following: Illness, Symptoms, Medicine, Lab Test, Clinician/Expert, Hospitalisation, Vitals, Assessment, Food, Nutrients, Family, Lifestyle, Gene, Country, Gender, Sex, Sexual Preference, Relationship Status, Occupation, Income, Political Inclination, Religion, Education, Family Structure, MBTI Personality, Physical Fitness, Medicine, Treatment Route.")
    node_name: str = Field("", description="Name of the entity in node type (paracetamol, Fever, CBC etc)")
    edge_attributes: Dict[str, Union[str, int, None]] = Field(default_factory=dict, description="Details of the connection between User and Node.")

class NodeList(BaseModel):
    node: List[Node] = []

class InputData(BaseModel):
    input: str

@app.post("/timeline_data")
async def timeline(data: InputData):
    """Endpoint to process data based on the specified pattern."""
    # if pattern not in pattern_path_mappings:
    #     raise HTTPException(status_code=404, detail="Pattern not found")

    input_data = data.input
    urls = pattern_path_mappings["timeline"]
    system_url, user_url = urls["system_url"], urls["user_url"]

    chunks = chunk_text(input_data, chunk_size=1000, overlap=100)
    all_responses = []
    try:
        for chunk in chunks:
            messages = create_messages(system_url, user_url, chunk)
            response = requests.post(
                f"{OPENAI_BASE_URL}/chat/completions",
                json={
                    "model": DEFAULT_MODEL,
                    "messages": messages,
                    "temperature": 0.0,
                    "top_p": 1,
                    "frequency_penalty": 0.1,
                    "presence_penalty": 0.1,
                },
                headers={"Authorization": f"Bearer {OPENAI_API_KEY}"}
            )
            response.raise_for_status()
            assistant_message = response.json()["choices"][0]["message"]["content"]
            all_responses.append(parse_timeline(assistant_message))

        with open("assistant_message.txt", "w") as file:
            file.write(assistant_message)

        timeline_data = merge_timeline_chunks(all_responses)
        return {"timeline_data": timeline_data}

              
    except Exception as e:
        logger.error("An error occurred while processing the request: %s", e)
        raise HTTPException(status_code=500, detail=f"An error occurred while processing the request: {str(e)}")

    #     if pattern == "medicine":
    #         medication_history = extract_medication_history(assistant_message)
    #         return {"medication_history": medication_history}
    #     elif pattern == "labtest":
    #         labtest_history = extract_labtest_history(assistant_message)
    #         return {"labtest_history": labtest_history}
    #     elif pattern == "illness":
    #         illness_history = extract_illness_history(assistant_message)
    #         return {"illness_history": illness_history}
    #     elif pattern == "history":
    #         history = extract_history(assistant_message)
    #         return {"history": history}
    #     elif pattern == "timeline":
    #         timeline_data = parse_timeline(assistant_message)
    #         return {"timeline_data": timeline_data}
    #     else:
    #         return {"assistant_message": assistant_message}

    # except Exception as e:
    #     logger.error("An error occurred while processing the request: %s", e)
    #     raise HTTPException(status_code=500, detail=f"An error occurred while processing the request: {str(e)}")


@app.post("/graph_data")
async def graph_data(data: InputData):
    input_data = data.input
    chunk_size = 200  # Define chunk size
    overlap = 50  # Define overlap
    chunks = chunk_text(input_data, chunk_size, overlap)
    results = process_chunks(chunks, GRAPH_PROMPT)

    if not results:
        raise HTTPException(status_code=500, detail="Failed to process chunks into graph data.")

    # Convert all edge attributes to strings
    results = [convert_edge_attributes_to_strings(node.dict()) for node in results]
    
    return {"graph_data": results}
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

