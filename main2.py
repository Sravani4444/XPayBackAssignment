from fastapi import FastAPI, HTTPException
from database import get_postgres_connection, get_mongodb_connection
from models import UserInDB

app = FastAPI()

# Database connections
postgres_db = get_postgres_connection()
mongodb_db = get_mongodb_connection()

# GET user details endpoint
@app.get("/users/{user_id}", response_model=UserInDB)
async def get_user_details(user_id: int):
    # Retrieve user details from PostgreSQL
    postgres_cursor = postgres_db.cursor()
    postgres_cursor.execute("SELECT full_name, email, phone FROM users WHERE id = %s", (user_id,))
    user_postgres = postgres_cursor.fetchone()
    postgres_db.commit()

    if user_postgres is None:
        raise HTTPException(status_code=404, detail="User not found in PostgreSQL")

    full_name, email, phone = user_postgres

    # Retrieve profile picture path from MongoDB (assuming it's stored as a path)
    # Modify this part according to how you store profile pictures in MongoDB
    mongodb_collection = mongodb_db['profile_pictures']
    mongo_user = mongodb_collection.find_one({"user_id": user_id})
    if mongo_user:
        profile_picture_path = mongo_user.get("profile_picture_path", "")
    else:
        profile_picture_path = ""

    user_details = UserInDB(id=user_id, full_name=full_name, email=email, phone=phone, profile_picture_path=profile_picture_path)
    return user_details
