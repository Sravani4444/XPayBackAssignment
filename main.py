from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import List
import os
from database import get_postgres_connection, get_mongodb_connection
from models import UserCreate, UserInDB

app = FastAPI()

# Database connections
postgres_db = get_postgres_connection()
mongodb_db = get_mongodb_connection()

# User registration endpoint
@app.post("/register/")
async def register_user(user_data: UserCreate, profile_picture: UploadFile = File(None)):
    # Check if email already exists in PostgreSQL
    cursor = postgres_db.cursor()
    cursor.execute("SELECT id FROM users WHERE email = %s", (user_data.email,))
    existing_user = cursor.fetchone()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Insert user data into PostgreSQL
    insert_query = """
        INSERT INTO users (full_name, email, password, phone)
        VALUES (%s, %s, %s, %s)
        RETURNING id
    """
    cursor.execute(insert_query, (user_data.full_name, user_data.email, user_data.password, user_data.phone))
    user_id = cursor.fetchone()[0]
    postgres_db.commit()

    # Save profile picture to MongoDB
    if profile_picture:
        file_name = profile_picture.filename
        # Example: Save file to MongoDB GridFS
        # Adapt this part based on your MongoDB setup
        with open(file_name, 'wb') as f:
            f.write(profile_picture.file.read())
        profile_picture_path = f"/profile_pictures/{file_name}"
        mongodb_db['profile_pictures'].insert_one({"user_id": user_id, "profile_picture_path": profile_picture_path})
    else:
        profile_picture_path = None

    # Return user data
    user_in_db = UserInDB(id=user_id, full_name=user_data.full_name, email=user_data.email, phone=user_data.phone)
    return user_in_db
