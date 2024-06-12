from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
import uvicorn
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from routes import app as api_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)

# Include router from routes.py
app.include_router(api_router, prefix="/api")

# Run with py
if '__main__' == __name__:
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)



