from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import psycopg2
from typing import Optional
from database import get_postgres_connection
from models import UserCreate

app = FastAPI()

# Database connection
postgres_db = get_postgres_connection()

# User registration endpoint
@app.post("/register/")
async def register_user(user_data: UserCreate):
    try:
        # Check if email already exists
        cursor = postgres_db.cursor()
        cursor.execute("SELECT id FROM Users WHERE email = %s", (user_data.email,))
        existing_email = cursor.fetchone()
        if existing_email:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Check if phone number already exists
        cursor.execute("SELECT id FROM Users WHERE phone = %s", (user_data.phone,))
        existing_phone = cursor.fetchone()
        if existing_phone:
            raise HTTPException(status_code=400, detail="Phone number already registered")
        
        # Insert user data into Users table
        insert_query = """
            INSERT INTO Users (full_name, email, password, phone)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """
        cursor.execute(insert_query, (user_data.full_name, user_data.email, user_data.password, user_data.phone))
        user_id = cursor.fetchone()[0]
        
        # Insert profile picture path into Profile table
        insert_profile_query = """
            INSERT INTO Profile (user_id, profile_picture)
            VALUES (%s, %s)
        """
        cursor.execute(insert_profile_query, (user_id, user_data.profile_picture))
        
        postgres_db.commit()
        return {"message": "User registered successfully", "user_id": user_id}
    
    except psycopg2.Error as e:
        postgres_db.rollback()
        raise HTTPException(status_code=500, detail="Database error")

    finally:
        cursor.close()

# Dependency to get database connection
def get_postgres():
    try:
        yield postgres_db
    finally:
        postgres_db.close()
