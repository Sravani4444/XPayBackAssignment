from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
from typing import List
from database import get_postgres_connection
from models import UserInDB

app = FastAPI()

# Database connection
postgres_db = get_postgres_connection()

# GET user details endpoint
@app.get("/users/{user_id}", response_model=UserInDB)
async def get_user_details(user_id: int):
    try:
        # Retrieve user details from Users and Profile tables using user_id
        cursor = postgres_db.cursor()
        cursor.execute("""
            SELECT u.id, u.full_name, u.email, u.phone, p.profile_picture
            FROM Users u
            LEFT JOIN Profile p ON u.id = p.user_id
            WHERE u.id = %s
        """, (user_id,))
        user_data = cursor.fetchone()

        if user_data is None:
            raise HTTPException(status_code=404, detail="User not found")

        user_id, full_name, email, phone, profile_picture = user_data
        user_details = UserInDB(id=user_id, full_name=full_name, email=email, phone=phone, profile_picture=profile_picture)
        return user_details
    
    except psycopg2.Error as e:
        postgres_db.rollback()
        raise HTTPException(status_code=500, detail="Database error")

    finally:
        cursor.close()
