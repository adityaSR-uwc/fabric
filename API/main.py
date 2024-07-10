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
    return graph_data

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

def chunk_text(text: str, chunk_size: int, overlap: int) -> list:
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = ' '.join(words[i:i + chunk_size])
        chunks.append(chunk)
        i += chunk_size - overlap
    return chunks

def process_chunks(chunks: list, model: str, prompt: str, api_key: str) -> list:
    results = []
    headers = {"Authorization": f"Bearer {api_key}"}
    
    for chunk in chunks:
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": chunk}
        ]
        
        response = requests.post(
            f"{OPENAI_BASE_URL}/chat/completions",
            json={
                "model": model,
                "messages": messages,
                "temperature": 0.0,
                "top_p": 1,
                "frequency_penalty": 0.1,
                "presence_penalty": 0.1,
            },
            headers=headers
        )
        response.raise_for_status()
        assistant_message = response.json()["choices"][0]["message"]["content"]
        
        # Debug: Log the raw assistant_message content
        logger.debug("Raw assistant_message content: %s", assistant_message)
        
        try:
            # Extract JSON part from the response
            start_index = assistant_message.find("{")
            end_index = assistant_message.rfind("}")
            if start_index != -1 and end_index != -1:
                json_part = assistant_message[start_index:end_index + 1]
                result = clean_and_format_json(json_part)
                results.append(result)
            else:
                logger.error("No JSON found in assistant message")
        except ValueError as e:
            logger.error("Error processing chunk: %s", e)
    
    return results

def process_chunks(chunks: list, model: str, prompt: str, api_key: str) -> list:
    results = []
    headers = {"Authorization": f"Bearer {api_key}"}
    
    for chunk in chunks:
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": chunk}
        ]
        
        response = requests.post(
            f"{OPENAI_BASE_URL}/chat/completions",
            json={
                "model": model,
                "messages": messages,
                "temperature": 0.0,
                "top_p": 1,
                "frequency_penalty": 0.1,
                "presence_penalty": 0.1,
            },
            headers=headers
        )
        response.raise_for_status()
        assistant_message = response.json()["choices"][0]["message"]["content"]

        logger.debug("Raw assistant_message content: %s", assistant_message)

        try:
            json_part = extract_json_from_response(assistant_message)
            result = json.loads(json_part)
            results.append(result)
        except ValueError as e:
            logger.error("Error processing chunk: %s", e)
    
    return results

def extract_json_from_response(response_text: str) -> str:
    start_index = response_text.find("{")
    end_index = response_text.rfind("}")
    if start_index == -1 or end_index == -1:
        raise ValueError("No JSON found in the response")
    json_part = response_text[start_index:end_index + 1]
    return json_part

def merge_results(results: list) -> dict:
    merged_data = {"data": []}
    for result in results:
        merged_data["data"].extend(result["data"])
    return merged_data

def clean_and_format_json(json_data_str: str) -> str:
    try:
        def quote_keys_and_values(match):
            key, value = match.groups()
            return f'"{key}": "{value}"'

        # Ensure keys are quoted
        json_data_str = re.sub(r'(?<!")(\b\w+\b)(?=\s*:)', r'"\1"', json_data_str)
        
        # Ensure values are quoted if they are words or numbers
        json_data_str = re.sub(r'(:\s*)([^,\[\]{}"]+)(?=[,\}\]])', r'\1"\2"', json_data_str)
        
        # Remove extraneous whitespace
        json_data_str = re.sub(r'\s+', ' ', json_data_str)

        # Fix missing commas
        json_data_str = re.sub(r'([^\]},\s])\s*([\{\["])', r'\1,\2', json_data_str)

        # Fix specific known issues manually
        json_data_str = re.sub(r'(\d{2}-\d{2}-\d{4})', r'"\1"', json_data_str)  # Quote dates
        json_data_str = re.sub(r'(\d+mg)', r'"\1"', json_data_str)  # Quote mg units
        json_data_str = re.sub(r'(\d+ times daily)', r'"\1"', json_data_str)  # Quote frequency
        json_data_str = re.sub(r'(\bas needed\b)', r'"\1"', json_data_str)  # Quote "as needed"
        json_data_str = re.sub(r'(\boral\b)', r'"\1"', json_data_str)  # Quote "oral"
        json_data_str = re.sub(r'(\d+)', r'"\1"', json_data_str)  # Quote standalone numbers

        # Ensure all values and keys are properly quoted in key-value pairs
        json_data_str = re.sub(r'([a-zA-Z_]+):\s*"([^"]+)"', quote_keys_and_values, json_data_str)
        
        # Remove trailing commas
        json_data_str = re.sub(r',\s*([\}\]])', r'\1', json_data_str)

        # Convert the cleaned JSON string to a dictionary
        json.loads(json_data_str)  # This ensures it is a valid JSON string
        return json_data_str
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON decoding error: {e.msg} at position {e.pos}")
    except ValueError as e:
        raise ValueError(f"Value error: {str(e)}")
  
def csv_to_json(assistant_message):
    graph_data = []
    try:
        reader = csv.reader(io.StringIO(assistant_message))
        
        # Skip lines until we find the header line
        headers = None
        for line in reader:
            if "User,Node Type,Node Name" in ','.join(line):
                headers = line
                break
        
        if headers is None or len(headers) < 3:
            raise ValueError("The headers do not contain at least 3 fields.")
        
        for row in reader:
            if len(row) >= 3:
                record = {
                    "User": row[0].strip("\""),
                    "Node Type": row[1].strip("\""),
                    "Node Name": row[2].strip("\""),
                    "edge_attributes": {}
                }
                
                # Add remaining columns to edge_attributes if they have non-null values
                for i in range(3, len(headers)):
                    if i < len(row) and row[i].strip("\""):
                        record["edge_attributes"][headers[i].strip("\"")] = row[i].strip("\"")
                
                graph_data.append(record)
            else:
                print(f"Skipping row due to length mismatch: {row}")
    
    except Exception as e:
        print(f"An error occurred while processing the request: {e}")
    
    return graph_data

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

    # if pattern == "graph_extraction":
    #     prompt = fetch_content_from_url(system_url)
    #     chunks = chunk_text(input_data, 200, 50)  # Define chunk size and overlap
    #     results = process_chunks(chunks, DEFAULT_MODEL, prompt, OPENAI_API_KEY)
    #     logger.info("Results: %s", results)
    #     merged_data = merge_results(results)
    #     graph_data = clean_and_format_json(merged_data)
    #     with open("assistant_message.txt", "w") as file:
    #             file.write(results)
    #     return {"assistant_message": merged_data, "json" : graph_data}
    # else:

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
    
        with open("assistant_message.txt", "w") as file:
            file.write(assistant_message)

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
            graph_data = csv_to_json(assistant_message)
            return {"data" : graph_data, "assistant_message": assistant_message}
        else:
            return {"response": assistant_message}

    except Exception as e:
        logger.error("An error occurred while processing the request: %s", e)
        raise HTTPException(status_code=500, detail=f"An error occurred while processing the request: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

