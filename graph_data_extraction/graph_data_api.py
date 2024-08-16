import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, ValidationError
import re
import json
import logging
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

def process_chunks(chunks: list, prompt: str) -> dict:
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

        try:
            response = chain.invoke({"input": chunk})
            logger.debug("Raw assistant_message content: %s", response)

            if isinstance(response, str):
                try:
                    response_data = json.loads(response)
                    if 'node' in response_data:
                        results.extend(response_data['node'])
                    else:
                        logger.error("Response does not contain 'node': %s", response_data)
                except json.JSONDecodeError as e:
                    logger.error("Failed to decode JSON response: %s", e)
                    continue
            elif isinstance(response, dict):
                if 'node' in response:
                    results.extend(response['node'])
                else:
                    logger.error("Response does not contain 'node': %s", response)
            elif isinstance(response, NodeList):
                results.extend(response.node)
            else:
                logger.error("Unexpected response type: %s", type(response))

        except Exception as e:
            logger.error("Error processing chunk: %s", chunk)
            logger.error("Exception: %s", str(e))

    logger.debug("Results before wrapping: %s", results)
    return {"node": results}

def convert_edge_attributes_to_strings(node):
    if 'edge_attributes' in node:
        node['edge_attributes'] = {key: str(value) if value is not None else None for key, value in node['edge_attributes'].items()}
    return node

def filter_duplicates(nodes):
    seen = {}
    for node in nodes:
        # Ensure edge_attributes['Timestamp'] exists, set to None if not
        timestamp = node['edge_attributes'].get('Timestamp', None)
        node_tuple = (node['node_type'], node['node_name'], timestamp)

        if node_tuple in seen:
            # Compare the number of populated fields
            current_fields = len([v for v in node['edge_attributes'].values() if v])
            seen_fields = len([v for v in seen[node_tuple]['edge_attributes'].values() if v])
            if current_fields > seen_fields:
                seen[node_tuple] = node
        else:
            seen[node_tuple] = node

    return list(seen.values())


GRAPH_PROMPT = """
system

# Objective
Create a structured patient knowledge graph by extracting all entities and relationships related to a patient's illness, medications, lab tests, socio-economic factors, lifestyle, family history, and treatment regime.

# Output Format 
{format_instructions}

# Methodology
1. Information Extraction
   Identify and extract relevant details from the text:
   - User: Name of the Patient  
   - Node Type: One of the following - Illness, Symptoms, Medicine, Lab Test, Clinician/Expert, Hospitalisation, Vitals, Assessment, Food, Nutrients, Family, Lifestyle, Gene, Country, Gender, Sex, Sexual Preference, Relationship Status, Occupation, Income, Political Inclination, Religion, Education, Family Structure, MBTI Personality, Physical Fitness, Medicine, Treatment Route. 
   - Node Name: name of the entity in node type (this field will always have a string value, like paracetamol, Fever, CBC, Therapist etc) 
   - Edge Attributes: this contains the details of the connection between User and Node
      For example, For Node Type "Illness", the edge attributes can be Timestamp, Severity etc.
     
2. Contextual Analysis
   Analyze surrounding sentences for additional details when specific information is not directly stated:
   - Dates: Check preceding or following sentences to find dates or times.
   - Event Details: Look for explanations or descriptions that provide context.

3. Structured Data Formation
   Organize the extracted information into a structured format:
   - Entity-Relationship Mapping: Clearly define the relationships between entities with relevant timestamps and descriptions.
   - Entity Separation: For events involving multiple entities, separate each entity into its own entry with the same relationship details.
   
User Information:
- Name - Ayush Kumar Bar

user 
{input}
assistant
Note: only provide in the format: {format_instructions}. Don't provide notes and additional information."""

class Node(BaseModel):
    user: str = Field(None, description="Patient name, friends/family members, clinician")
    node_type: str = Field(None, description="One of the following: Illness, Symptoms, Medication, Lab Test, Clinician/Expert, Hospitalisation, Vitals, Assessment, Food, Nutrients, Family, Lifestyle, Gene, Country, Gender, Sex, Sexual Preference, Relationship Status, Occupation, Income, Political Inclination, Religion, Education, Family Structure, MBTI Personality, Physical Fitness, Medicine, Treatment Route.")
    node_name: str = Field("", description="Name of the entity in node type (paracetamol, Fever, CBC etc)")
    edge_attributes: Optional[Dict[str, Union[str, int, float, bool, None]]] = Field({}, description="""These define the connection details between User and Node.(The timestamp is essential for all Edge attributes.) 
    For example:
        - **Illness**: Timestamp, Severity
        - **Symptoms**: Timestamp, Severity
        - **Medication**: Timestamp, Allergic to, Dosage, Frequency, Route
        - **Lab Test**: Timestamp, Interpretation, Result Value
        - **Clinician/Expert**: Timestamp, Consultation Type
        - **Hospitalisation**: Timestamp start, Timestamp end
        - **Vitals**: Timestamp, Interpretation, Result Value
        - **Assessment**: Timestamp, Interpretation, Result Value
        - **Food**: Timestamp, Allergic to (Boolean)
        - **Nutrients**: Timestamp, Deficient In, Plentiful In
        - **Family**: Relationship Type
        - **Lifestyle**: Timestamp
        - **Gene**: Timestamp
        - **Country**: Timestamp
        - **Gender**: Timestamp
        - **Sex**: Timestamp
        - **Sexual Preference**: Timestamp
        - **Relationship Status**: Timestamp
        - **Occupation**: Timestamp
        - **Income**: Timestamp
        - **Political Inclination**: Timestamp
        - **Religion**: Timestamp
        - **Education**: Timestamp, Level (Postgrad, Undergrad), Specialisation
        - **Family Structure**: Timestamp
        - **MBTI Personality**: Timestamp
        - **Physical Fitness**: Timestamp
        - **Medicine**: Illness, Symptoms, Timestamp
        - **Treatment Route**: Route administered, Duration, Timestamp
""")

class NodeList(BaseModel):
    node: List[Node] = Field([], description="List of nodes")

class InputData(BaseModel):
    input: str

@app.post("/graph_data")
async def graph_data(data: InputData):
    input_data = data.input
    sanitized_data = input_data

    chunks = chunk_text(sanitized_data, 200, 50)
    results = process_chunks(chunks, GRAPH_PROMPT)

    # Convert edge attributes to strings and filter duplicates
    converted_nodes = [convert_edge_attributes_to_strings(node.dict()) for node in results['node']]
    filtered_nodes = filter_duplicates(converted_nodes)

    # Validate the results
    try:
        validated_results = NodeList(node=[Node(**node) for node in filtered_nodes])
        return validated_results.dict()
    except ValidationError as e:
        logger.error("Validation error: %s", e)
        logger.error("Results causing the error: %s", filtered_nodes)
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8070)
