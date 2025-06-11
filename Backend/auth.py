from fastapi import APIRouter, HTTPException
from database import users_col
from models import UserRegister, UserLogin
from utils.security import validate_password
router = APIRouter()


@router.post("/signup")
def signup(user: UserRegister):
    if users_col.find_one({"user_info.email": user.email}):
        raise HTTPException(status_code=400, detail="Email already exists")
    validate_password(user.password)
    users_col.insert_one({
        "user_info": {
            "first name": user.First_name,
            "last name": user.Last_name,
            "email": user.email,
            "password": user.password,
            "phone number": user.Phone_number,
            "country": user.country,
        },
        "exercise_plan": None,
        "diet_plan": None,
    })
    return {"message": "User registered successfully"}


@router.post("/login")
def login(data: UserLogin):
    user = users_col.find_one({"user_info.email": data.email})
    if not user or user["user_info"]["password"] != data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    user.pop('_id', None)
    user.pop('password', None)
    return {
        "message": "Login successful",
        "user": user
    }
