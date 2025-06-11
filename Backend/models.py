from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Dict, Any, Union, List


class UserRegister(BaseModel):
    First_name: str
    Last_name: str
    email: EmailStr
    password: str
    Phone_number: Optional[str] = None
    country: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class PlanRequest(BaseModel):
    weight: Union[int, float]
    height: Union[int, float]
    bmi: Union[int, float]
    body_fat_percentage: Union[int, float]
    gender: str
    age: int
    fitnessGoal: str


class chatRequest(BaseModel):
    user_input: str


class ExerciseUpdate(BaseModel):
    exercise: str
    sets: str
    reps: str


class RecommendationParams(BaseModel):
    n_neighbors: int = 5
    return_distance: Optional[bool] = None


class FoodRecommendationRequest(BaseModel):
    nutrition_input: List[float]  # ← Flat list of 9 floats
    ingredients: Optional[List[str]] = Field(default_factory=list)
    params: RecommendationParams = Field(default_factory=RecommendationParams)
