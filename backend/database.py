import os
from motor.motor_asyncio import AsyncIOMotorClient

# Make sure there are 'quotes' around the entire link!
MONGO_URI = 'mongodb+srv://anni:networx@cluster0.qlglzgl.mongodb.net/NetworxDB?retryWrites=true&w=majority&appName=Cluster0'

print("🚀 Attempting to connect directly to MongoDB Atlas...")

try:
    client = AsyncIOMotorClient(MONGO_URI)
    db = client.NetworxDB
    print("✅ Direct connection initialized!")
except Exception as e:
    print(f"❌ Connection failed: {e}")