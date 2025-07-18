import json
import os
import warnings
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_groq import ChatGroq
from langchain.chains import ConversationChain
from langchain.memory import ConversationSummaryMemory
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser

warnings.filterwarnings("ignore")
load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise ValueError("API key not found in environment variables")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

chat = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    max_tokens=None,
    timeout=None,
    api_key=groq_api_key
)
memory = ConversationSummaryMemory(llm=chat)
conversation = ConversationChain(llm=chat, memory=memory)

class ChatResponse(BaseModel):
    message: str


style = """polite tone that speaks in English, 
keep the questions direct and concise, asking only for the required details without adding unnecessary conversation."""

system_message = """
You are a specialized medical and fitness assistant.

When you start the conversation, make sure that you introduce yourself and say hello to the user by his name.
Do not repeat the greeting in subsequent messages and do not say his name in subsequent messages.

When you start the conversation, you will be provided with a {object} answer to the user any question related to health, medicine, exercise, nutrition, and wellness. 
ONLY answer questions related to these topics. 
If a question is not related to them, politely decline to answer and explain that you can only provide information about medical and fitness topics.

If user asked to provide another exercise in the exercise_plan, provide it to the user based on his BMI, BMI_case, fitness_goal, and fitness_level.
If user asked to show his exercise_plan, show it to the user in detail.
If user asked about any information about his data, provide it.

Use this flow to build a personalized plan based on the following user input:
user input: {text}
style: {style}
use this instructions to format your response:
{format_instructions}
"""

conversation_prompt_template = ChatPromptTemplate.from_template(system_message)
response_parser = PydanticOutputParser(pydantic_object=ChatResponse)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Chat API"}

class ChatRequest(BaseModel):
    user_input: str
    user_data: dict

@app.post("/chat")
async def chat(chat: ChatRequest):
    user_input = chat.user_input
    user_data = chat.user_data
    format_instructions = response_parser.get_format_instructions()

    try:
        user_messages = conversation_prompt_template.format_messages(
            style=style,
            text=user_input,
            object=user_data,
            format_instructions=format_instructions
        )
        
        raw_response = conversation.run(input=user_messages[0].content)
        parsed_response = response_parser.parse(raw_response)
        
        if user_input.lower() == "quit":
            parsed_response.message = "Thank you for using Helix. Goodbye!"
            conversation.memory.clear()       
        return parsed_response.message

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8002, reload=True)
