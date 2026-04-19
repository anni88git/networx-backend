import os
from dotenv import load_dotenv

# This loads local variables if you are on your laptop, but ignores it on Render
load_dotenv() 

# This is the MAGIC line. It pulls the string securely from Render's environment
MONGO_URI = os.getenv("MONGO_URI") 

# Then you pass it to your client
client = MongoClient(MONGO_URI)