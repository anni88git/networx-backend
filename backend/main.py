from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import users, posts, messages  # Ensure you have messages.py in routes/
import uvicorn

# Initialize the App
app = FastAPI(
    title="Networx Full-Stack API",
    description="FastAPI Backend for Networx Professional Network",
    version="1.2.0"
)

# --- CORS SETUP ---
# This allows your React app (usually port 3000 or 5173) to talk to this Python server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development. Change to your Netlify URL after deployment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- ROUTE MOUNTING ---
# Wiring up all your separate service files
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(posts.router, prefix="/api/posts", tags=["Posts"])
app.include_router(messages.router, prefix="/api/messages", tags=["Messages"])

# Root Route (Health Check)
@app.get("/")
async def root():
    return {
        "status": "online",
        "message": "Networx FastAPI Backend is running 🚀",
        "docs": "/docs"
    }

# Execution logic
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)