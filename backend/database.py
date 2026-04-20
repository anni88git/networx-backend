import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

# Back to basics - no certifi needed for local testing
client = MongoClient(MONGO_URI)
db = client["NetworxDB"]