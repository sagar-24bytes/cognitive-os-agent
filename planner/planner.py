from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel
from typing import List
import time

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    temperature=0
)

# ---- Structured schema ----

class Step(BaseModel):
    tool: str
    args: dict

class Plan(BaseModel):
    goal: str
    steps: List[Step]

parser = PydanticOutputParser(pydantic_object=Plan)

# ---- LangGraph node ----

def planner_node(state):
    user_text = state["user_text"]

    prompt = f"""
You are an AI planning module for a personal operating system.

You must ONLY output a JSON plan.
You are NOT allowed to answer the user.
You are NOT allowed to explain.
You are NOT allowed to create intermediate variables.
You are NOT allowed to reference outputs of other tools.
Each step must be directly executable.

Only use these tools:
scan_folder(path)
create_folder(path, categories?)
move_file(source_directory, destination_directory, file_pattern)

{parser.get_format_instructions()}

User goal:
"{user_text}"
"""



    for attempt in range(3):
        try:
            resp = llm.invoke(prompt)
            plan = parser.parse(resp.content)
            return {"plan": plan.dict()}
        
        except Exception as e:
            print(f"Gemini error, retrying... ({attempt+1}/3)")
            time.sleep(2)

    # Fallback if all retries fail
    return {
        "plan": {
            "error": "Gemini API failed after retries"
        }
    }
