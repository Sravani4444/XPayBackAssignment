import psycopg2
from pymongo import MongoClient

# PostgreSQL Connection
def get_postgres_connection():
    conn = psycopg2.connect(
        dbname="your_dbname",
        user="your_username",
        password="your_password",
        host="localhost"
    )
    return conn

# MongoDB Connection
def get_mongodb_connection():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['your_mongodb_database']
    return db
