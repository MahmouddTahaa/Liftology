from fastapi import APIRouter, HTTPException, Body
from database import users_col
from typing import Optional, Dict, Any
from pydantic import BaseModel, EmailStr

router = APIRouter()


class UserUpdate(BaseModel):
    name: Optional[str] = None
    password: Optional[str] = None
    plan: Optional[Dict[str, Any]] = None  # If needed for manual plan updates


@router.get("/user/{email}")
def get_user(email: str):
    user = users_col.find_one({"user_info.email": email}, {"_id": 0})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/user/{email}")
def update_user(email: str, update_data: dict = Body(...)):
    if not update_data:
        raise HTTPException(
            status_code=400, detail="No data provided for update")

    user = users_col.find_one({"user_info.email": email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Prefix fields with 'user_info.' to update nested structure
    updates = {f"user_info.{k}": v for k, v in update_data.items()}
    result = users_col.update_one(
        {"user_info.email": email}, {"$set": updates})

    if result.modified_count == 0:
        raise HTTPException(status_code=500, detail="Update failed")

    return {"status": "success", "updated_fields": list(update_data.keys())}

# 2. Change Password (Current Password + New Password)


@router.put("/user/{email}/change-password")
def change_password(email: str, change_data: dict = Body(...)):
    current_password = change_data.get("current_password")
    new_password = change_data.get("new_password")

    if not current_password or not new_password:
        raise HTTPException(
            status_code=400, detail="Both current and new passwords are required")

    # Find user by email
    user = users_col.find_one({"user_info.email": email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if the current password matches
    if user["user_info"]["password"] != current_password:
        raise HTTPException(
            status_code=401, detail="Current password is incorrect")

    # Update to the new password
    users_col.update_one(
        {"user_info.email": email},
        {"$set": {"user_info.password": new_password}}
    )

    return {"status": "success", "message": "Password updated successfully"}
