import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.session import init_db
from fastapi.middleware.cors import CORSMiddleware
from app.router import waitList
import os
from dotenv import load_dotenv

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    await init_db()
    yield
    print("Shutting down...")


app = FastAPI(
    title='AlphaX waitlist API',
    description='API for managing the AlphaX waitlist',
    version='1.0.0',
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ORIGINS"),
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.include_router(waitList.router, prefix=os.getenv("API_PREFIX"))


@app.get("/")
async def read_root():
    return {
        "message": "Welcome to the AlphaX waitlist API!"
    }


if __name__ == "__main__":
    uvicorn.run(
        app,
        host='0.0.0.0',
        port=5000
    )
