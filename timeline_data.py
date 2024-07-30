import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import re
import json
import logging
from datetime import datetime
from dotenv import load_dotenv

app = FastAPI()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

load_dotenv()

ALLOWLIST_PATTERN = re.compile(r"^[a-zA-Z0-9\s.,;:!?\-]+$")

DEFAULT_MODEL = os.getenv('DEFAULT_MODEL')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_BASE_URL = os.getenv('OPENAI_BASE_URL')

now_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

EVENT_TYPES = [
    "Illness", "Symptoms", "Medicine", "Lab Test", "Clinician/Expert", "Hospitalisation", "Vitals", 
    "Assessment", "Food", "Nutrients", "Family", "Lifestyle", "Gene", "Country", "Gender", "Sex", 
    "Sexual Preference", "Relationship Status", "Occupation", "Income", "Political Inclination", 
    "Religion", "Education", "Family Structure", "M B T I Personality", "Physical Fitness", 
    "Medicine", "Treatment Route"
]

def sanitize_content(content):
    return "".join(char for char in content if ALLOWLIST_PATTERN.match(char))

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
        # Create a chunk with a size of chunk_size words
        chunk_end = i + chunk_size + overlap
        chunk = ' '.join(words[i:chunk_end])
        chunks.append(chunk)
        # Move the starting index forward by chunk_size to start the next chunk
        i += chunk_size
    return chunks

def parse_timeline(response):
    try:
        lines = response.split('\n')
        timeline_data = [line for line in lines if line.strip() and "Here is the structured and chronological patient timeline" not in line]
        return timeline_data
    except Exception as e:
        print(f"Error processing response: {e}")
        return []    

def merge_timeline_chunks(chunks):
    merged_timeline = []
    seen_events = set()
    for chunk in chunks:
        for event in chunk:
            if event not in seen_events:
                seen_events.add(event)
                merged_timeline.append(event)
    return merged_timeline

timeline_prompt = f"""system

# Objective:
Create a structured and chronological patient timeline of all the clinical and important life events. Focus on the patient's illness, medication, lab tests, socio-economic factors, lifestyle, family history, and treatment regime.

# Output Format:
  Datetime - Event Type - Event Name - Event Description - Event Tags

# Steps to extract clinical and important life events

1.*Extract Relevant Information:*
  Identify and extract relevant details from the text:
   - Datetime: date-time when the event is taking place
   - Event Type: It can only be one of the following: "Illness", "Symptoms", "Medicine", "Lab Test", "Clinician/Expert", "Hospitalisation", "Vitals", "Assessment", "Food", "Nutrients", "Family", "Lifestyle", "Gene", "Country", "Gender", "Sex", "Sexual Preference", "Relationship Status", "Occupation", "Income", "Political Inclination", "Religion", "Education", "Family Structure", "M B T I Personality", "Physical Fitness", "Treatment Route".
   - Event Name: name of the event
   - Event Description: concise information regarding the event.
   - Event Tags: a list of tags relevant to the event

2.*Structure the Information:*
   - Create entries for each relevant event along with Datetime and Event Name.
   - Classify the event name into one of the Event Types mentioned above.
   - Add a short event description to the relevant event.
   - Use the event description to extract the event tags.
   - Current date is {now_datetime}

3.*Format the Information:*
    - Example format of the output:
       - 2024-01-21 12:45:00 - Medicine - Paracetamol - Took paracetamol 100mg for fever - Medicine, Fever
       - 2023-06-06 13:45:00 - Medicine - Clonazepam - Took clonazepam 250mg for Generalised Anxiety Disorders - Medicine, Anxiety, Generalised Anxiety Disorder 
       - 2022-09-20 16:50:00 - Medicine - Olanzapine - Took olanzapine 500mg for bipolar disorder - Medicine, Bipolar Disorder 
       - 2021-08-25 15:30:00 - Family - Brother's Death - John's brother died in a car accident at age 18 - Family History, Death, Brother, Trauma
       - unknown - Symptoms - Fever - John had a fever of 104 degrees - Fever
       - unknown - Family - Father's death - John's father died due to old age - Family History, Death, Father
       - unknown - Family - Family Therapy Sessions - John considers family therapy sessions to address unresolved issues related to his father and brother's deaths - Family Therapy, Family History
       - unknown - Lifestyle - Occasional Social Drinking - John occasionally consumes alcohol socially, but avoids excessive drinking due to his father's history of alcoholism - Lifestyle, Substance Use, Family History
       - unknown - Lifestyle - Social Support - John has a close-knit group of friends and colleagues, but struggles to open up about his mental health issues - Social Support, Mental Health
       - 2024-05-29 00:00:00 - Assessment - Mental Status Exam - John took a Psychiatric Assessment on 5-09-2024 - Mental Health, Assessment
       - 2016-2017 - Lab Test - Dialectical Behavior Therapy (DBT) - Dialectical Behavior Therapy (DBT) for emotion regulation and distress tolerance - Therapy, DBT

# NOTE
    - Do not assume Event Type. Select one from the following: "Illness", "Symptoms", "Medicine", "Lab Test", "Clinician/Expert", "Hospitalisation", "Vitals", "Assessment", "Food", "Nutrients", "Family", "Lifestyle", "Gene", "Country", "Gender", "Sex", "Sexual Preference", "Relationship Status", "Occupation", "Income", "Political Inclination", "Religion", "Education", "Family Structure", "M B T I Personality", "Physical Fitness", "Treatment Route".
    - Do not include any additional information or notes other than the Output format.

## Examples for Each Event Type:

1. Illness:
   - 2022-09-20 16:50:00 - Illness - Bipolar Disorder - Diagnosed with bipolar disorder - Bipolar Disorder

2. Symptoms:
   - unknown - Symptoms - Fever - John had a fever of 104 degrees - Fever

3. Medicine:
   - 2024-01-21 12:45:00 - Medicine - Paracetamol - Took paracetamol 100mg for fever - Medicine, Fever

4. Lab Test:
   - 2023-06-06 13:45:00 - Lab Test - Blood Test - Underwent a blood test for anxiety diagnosis - Blood Test, Anxiety

5. Clinician/Expert:
   - 2024-03-15 14:00:00 - Clinician/Expert - Dr. Smith - Consulted with Dr. Smith for a follow-up - Clinician, Follow-up

6. Hospitalisation:
   - 2021-11-05 09:00:00 - Hospitalisation - Knee Surgery - Hospitalized for knee surgery - Surgery, Hospitalisation

7. Vitals:
   - 2024-02-20 08:30:00 - Vitals - Blood Pressure - Recorded blood pressure at 130/85 mmHg - Vitals, Blood Pressure

8. Assessment:
   - 2024-05-29 00:00:00 - Assessment - Mental Status Exam - John took a Psychiatric Assessment on 5-09-2024 - Mental Health, Assessment

9. Food:
   - 2023-07-10 18:30:00 - Food - Vegetarian Diet - Started a vegetarian diet - Diet, Food

10. Nutrients:
    - 2023-08-01 08:00:00 - Nutrients - Vitamin D Supplement - Began taking Vitamin D supplements - Nutrients, Vitamin D

11. Family:
    - 2021-08-25 15:30:00 - Family - Brother's Death - John's brother died in a car accident at age 18 - Family History, Death, Brother, Trauma

12. Lifestyle:
    - unknown - Lifestyle - Occasional Social Drinking - John occasionally consumes alcohol socially, but avoids excessive drinking due to his father's history of alcoholism - Lifestyle, Substance Use, Family History

13. Gene:
    - unknown - Gene - BRCA1 Mutation - Tested positive for BRCA1 mutation - Genetic, BRCA1

14. Country:
    - 2022-11-10 10:00:00 - Country - Moved to Canada - Relocated to Canada for work - Relocation, Country

15. Gender:
    - unknown - Gender - Male - Identified as male - Gender

16. Sex:
    - unknown - Sex - Male - Biological sex is male - Sex

17. Sexual Preference:
    - unknown - Sexual Preference - Heterosexual - Identifies as heterosexual - Sexual Preference

18. Relationship Status:
    - 2021-05-10 15:00:00 - Relationship Status - Married - Got married to Jane - Marriage, Relationship

19. Occupation:
    - 2023-04-01 09:00:00 - Occupation - Software Engineer - Started a new job as a Software Engineer - Job, Occupation

20. Income:
    - 2022-12-01 00:00:00 - Income - Salary Increase - Received a salary increase - Income, Salary

21. Political Inclination:
    - unknown - Political Inclination - Liberal - Identifies as politically liberal - Politics, Inclination

22. Religion:
    - unknown - Religion - Christianity - Practices Christianity - Religion

23. Education:
    - 2017-09-30 14:00:00 - Education - Master's Degree - Completed a master's degree in computer science - Education, Degree

24. Family Structure:
    - unknown - Family Structure - Nuclear Family - Lives in a nuclear family - Family Structure

25. M B T I Personality:
    - unknown - M B T I Personality - INTJ - Identifies as INTJ personality type - Personality

26. Physical Fitness:
    - 2024-04-15 06:00:00 - Physical Fitness - Marathon Training - Started training for a marathon - Fitness, Training

27. Treatment Route:
    - 2023-09-10 14:30:00 - Treatment Route - Oral Medication - Prescribed oral medication for hypertension - Medicine, Treatment

assistant
"""

pattern_path_mappings = {
    "timeline": {"system_url": timeline_prompt,
                 "user_url": "https://raw.githubusercontent.com/danielmiessler/fabric/main/patterns/summarize/user.md"}
}

class InputData(BaseModel):
    input: str

@app.post("/timeline_data")
async def timeline(data: InputData):
    """Endpoint to process data based on the specified pattern."""
    input_data = data.input
    urls = pattern_path_mappings["timeline"]
    system_url, user_url = urls["system_url"], urls["user_url"]

    chunks = chunk_text(input_data, chunk_size=200, overlap=50)
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8050)
