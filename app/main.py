from datetime import datetime
from fastapi import FastAPI
from app.routers import users

app = FastAPI(
    title="Digital Twin - AI ChatBot",
    description="This is a FastAPI application.",
    version="1.0.0",
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT"
    }
)

@app.get("/")
async def root():
    return {
        "message": "Welcome to Digital Twin - AI ChatBot!",
        "api_version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
        "docs": "/docs",
        "redoc": "/redoc",
    }

app.include_router(users.router, prefix="/users")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)