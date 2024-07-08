import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import re
import csv
import io
import json
import logging

app = FastAPI()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

ALLOWLIST_PATTERN = re.compile(r"^[a-zA-Z0-9\s.,;:!?\-]+$")

DEFAULT_MODEL = 'meta-llama/Meta-Llama-3-8B-Instruct'
OPENAI_API_KEY = 'EMPTY'
OPENAI_BASE_URL = 'https://genv2.uwc.world/v1'

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

def clean_edge_attributes(attributes_str):
    """Clean and parse the edge attributes string."""
    attributes_str = attributes_str.replace("'", '"')
    attributes_dict = {}
    
    # Split attributes based on comma outside of any brackets
    parts = re.split(r',\s*(?![^[]*\])', attributes_str.strip('{}'))
    
    for part in parts:
        if ':' in part:
            key, value = part.split(':', 1)
            key = key.strip().strip('"')
            value = value.strip().strip('"')
            if value.startswith('[') and value.endswith(']'):
                value = json.loads(value)
            attributes_dict[key] = value
    
    return attributes_dict

def extract_graph_data(assistant_message):
    """Extract graph data from assistant message and make a second API call for corrections."""
    graph_data = []
    lines = assistant_message.split("\n")
    for line in lines:
        line = line.strip()
        if line.startswith("**") and line.endswith("**"):
            line = line.strip("**")
            parts = line.split(",")
            logger.debug("Parts after split: %s", parts)
            if len(parts) > 1:
                node_type = parts[1].strip()
                if len(parts) >= 3 and node_type != "Node Type":
                    user = parts[0].strip()
                    edge = parts[2].strip()
                    edge_attributes = {part.split(":")[0].strip(): part.split(":")[1].strip() for part in parts[3:] if ":" in part}
                    record = {
                        "user": user,
                        "node_type": node_type,
                        "node_name": edge,
                        "edge_attributes": edge_attributes
                    }
                    graph_data.append(record)

    logger.debug("Graph data before second API call: %s", graph_data)

    # Prepare input for the second API call
    input_data = {"graph_data": graph_data}
    system_url = "https://raw.githubusercontent.com/adityaSR-uwc/fabric/main/graph2.md"
    user_url = "https://raw.githubusercontent.com/danielmiessler/fabric/main/patterns/summarize/user.md"

    system_content = fetch_content_from_url(system_url)
    user_file_content = fetch_content_from_url(user_url)

    system_message = {"role": "system", "content": system_content}
    user_message = {"role": "user", "content": user_file_content + "\n" + json.dumps(input_data, indent=2)}
    messages = [system_message, user_message]

    try:
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
        new_assistant_message = response.json()["choices"][0]["message"]["content"]

        # Log the raw response for debugging
        logger.debug("Raw new_assistant_message: %s", new_assistant_message)

        abc = reformat_graph_data(new_assistant_message)
    except Exception as e:
        logger.error("An error occurred while processing the 2nd request: %s", e)
        raise HTTPException(status_code=500, detail=f"An error occurred while processing the 2nd request: {str(e)}")

    return abc

def reformat_graph_data(data: str) -> dict:
    try:
        # Find the start of the JSON part within the string
        start_index = data.find("{")
        if start_index == -1:
            raise ValueError("Invalid input format. JSON data not found.")

        # Extract the JSON part from the string
        json_data_str = data[start_index:]

        # Remove the initial wrapping text and newlines
        json_data_str = json_data_str.strip()

        # Convert the formatted JSON string back to a dictionary
        formatted_json = json.loads(json_data_str)
        return formatted_json
    except json.JSONDecodeError as e:
        logger.error(f"JSON decoding error: {e}")
        raise HTTPException(status_code=500, detail=f"JSON decoding error: {str(e)}")

def create_messages(system_url, user_url, input_data):
    """Create messages for API request."""
    system_content = fetch_content_from_url(system_url)
    user_file_content = fetch_content_from_url(user_url)

    system_message = {"role": "system", "content": system_content}
    user_message = {"role": "user", "content": user_file_content + "\n" + input_data}
    return [system_message, user_message]

pattern_path_mappings = {
    "medicine": {"system_url": "https://raw.githubusercontent.com/adityaSR-uwc/fabric/main/medicine.md",
                 "user_url": "https://raw.githubusercontent.com/danielmiessler/fabric/main/patterns/summarize/user.md"},
    "history": {"system_url": "https://raw.githubusercontent.com/adityaSR-uwc/fabric/main/history.md",
                "user_url": "https://raw.githubusercontent.com/danielmiessler/fabric/main/patterns/summarize/user.md"},
    "labtest": {"system_url": "https://raw.githubusercontent.com/adityaSR-uwc/fabric/main/labtest.md",
                "user_url": "https://raw.githubusercontent.com/danielmiessler/fabric/main/patterns/summarize/user.md"},
    "illness": {"system_url": "https://raw.githubusercontent.com/adityaSR-uwc/fabric/main/illness.md",
                "user_url": "https://raw.githubusercontent.com/danielmiessler/fabric/main/patterns/summarize/user.md"},
    "graph_extraction": {"system_url": "https://raw.githubusercontent.com/adityaSR-uwc/fabric/main/graph_extraction.md",
                         "user_url": "https://raw.githubusercontent.com/danielmiessler/fabric/main/patterns/summarize/user.md"},
    "keyword": {"system_url": "https://raw.githubusercontent.com/adityaSR-uwc/fabric/main/keyword.md",
                "user_url": "https://raw.githubusercontent.com/danielmiessler/fabric/main/patterns/summarize/user.md"},
    "timeline": {"system_url": "https://raw.githubusercontent.com/adityaSR-uwc/fabric/main/timeline.md",
                 "user_url": "https://raw.githubusercontent.com/danielmiessler/fabric/main/patterns/summarize/user.md"}
}

class InputData(BaseModel):
    input: str

@app.post("/{pattern}")
async def milling(pattern: str, data: InputData):
    """Endpoint to process data based on the specified pattern."""
    if pattern not in pattern_path_mappings:
        raise HTTPException(status_code=404, detail="Pattern not found")

    input_data = data.input
    urls = pattern_path_mappings[pattern]
    system_url, user_url = urls["system_url"], urls["user_url"]

    messages = create_messages(system_url, user_url, input_data)

    try:
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

        if pattern == "medicine":
            medication_history = extract_medication_history(assistant_message)
            return {"medication_history": medication_history}
        elif pattern == "labtest":
            labtest_history = extract_labtest_history(assistant_message)
            return {"labtest_history": labtest_history}
        elif pattern == "illness":
            illness_history = extract_illness_history(assistant_message)
            return {"illness_history": illness_history}
        elif pattern == "history":
            history = extract_history(assistant_message)
            return {"history": history}
        elif pattern == "graph_extraction":
            graph_data = extract_graph_data(assistant_message)
            return {"graph_data": graph_data}
        else:
            return {"response": assistant_message}

    except Exception as e:
        logger.error("An error occurred while processing the request: %s", e)
        raise HTTPException(status_code=500, detail=f"An error occurred while processing the request: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

