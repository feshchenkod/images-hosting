from dotenv import load_dotenv
import os
import psycopg

load_dotenv()

DB_CONFIG = {
    "dbname": os.getenv('POSTGRES_DB'),
    "user": os.getenv('POSTGRES_USER'),
    "password": os.getenv('POSTGRES_PASSWORD'),
    "host": os.getenv('DB_HOST')
}

def get_conn():
    return psycopg.connect(**DB_CONFIG)