from fastapi import APIRouter, HTTPException

from models import PlanRequest, FoodRecommendationRequest, ExerciseUpdate

from database import users_col
from ml.client import call_ml_model
from datetime import datetime
import json

import httpx

router = APIRouter()


@router.post("/generate/{user_email}")
async def generate_plan(req: PlanRequest, user_email: str):
    user = users_col.find_one({"user_info.email": user_email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    result = await call_ml_model(req.dict())

    update_data = {
        "exercise_plan": {
            "input": req.dict(),
            "output": result,
            "timestamp": datetime.utcnow()
        }

    }

    users_col.update_one({"user_info.email": user_email},
                        {"$set": update_data})

    return {"status": "success", "plan": result}


@router.put("/update-exercise-plan/{email}")
def update_full_plan(email: str, new_plan: ExerciseUpdate):
    user = users_col.find_one({"user_info.email": email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    users_col.update_one(
        {"user_info.email": email},
        {"$set": {"exercise_plan": new_plan.dict()}}
    )

    # return {"status": "success", "message": f"Exercise {exercise_number} on {day} updated"}

    return {"status": "success", "message": "Exercise plan updated successfully"}


NGROK_API_URL = "https://cf50-102-186-253-201.ngrok-free.app/predict"


@router.post("/food-recommendation/{email}")
async def recommend_food(email: str, request: FoodRecommendationRequest):
    user = users_col.find_one({"user_info.email": email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(NGROK_API_URL, json=request.dict())
            response.raise_for_status()
            food_result = response.json()

        users_col.update_one(
            {"user_info.email": email},
            {"$set": {"diet_plan": food_result}}
        )

        return {"status": "success", "recommendation": food_result}

    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"Model error: {str(e)}")
