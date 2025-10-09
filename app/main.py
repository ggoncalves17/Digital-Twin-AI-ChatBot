from datetime import datetime
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal, get_db
from app.routers import users
from app.crud import user_crud 

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

@app.post("/create")
def create_user(user: users.UserRegistration, db: Session = Depends(get_db)):
    """
    Cria um utilizador novo via JSON.
    """
    try :
        new_user = user_crud.create_user_from_data(db, user)
        return {
            "id": new_user.id,
            "first_name": new_user.first_name,
            "last_name": new_user.last_name,
            "email": new_user.email,
            "password": new_user.password,
            "date_of_birth": new_user.date_of_birth.isoformat() if new_user.date_of_birth else None
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        return {"error": str(e)}
    

@app.get("/health")
async def health_check():
    return {"status": "ok", "timestamp": datetime.now().isoformat()}

@app.get("/users")
def read_users(db: Session = Depends(get_db)):
    users = db.query(user_crud.DBUser).all()
    return users

@app.get("/users/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(user_crud.DBUser).filter(user_crud.DBUser.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

app.include_router(users.router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
    