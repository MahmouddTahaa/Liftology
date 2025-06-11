from fastapi import APIRouter, HTTPException
from database import users_col
from models import chatRequest
import httpx

router = APIRouter()


@router.post("/chat/{email}")
async def chat_with_assistant(email: str, input: chatRequest):
    user = users_col.find_one({"user_info.email": email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user_data = user  # Extract only user_info for the chatbot
    user_data.get("exercise_plan", {}).pop("timestamp", None)
    user_data.pop("_id", None)
    chatbot_url = "https://chatbot-production-8a57.up.railway.app/chat"

    payload = {
        "user_input": input.user_input,
        "user_data": user_data
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(chatbot_url, json=payload)
            response.raise_for_status()
            return {"bot_response": response.json()}
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=500, detail=f"Chatbot error: {e.response.text}")
