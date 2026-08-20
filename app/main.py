from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
# Replace with, at the top of the file (near the FastAPI import):
from contextlib import asynccontextmanager

from app.database import Base, engine
from app.routers import equipment, bookings, documents
from app import storage

app = FastAPI(
    title="Equipment Management API",
    description="Manages field equipment, bookings and supporting documents "
    "for the Department of Environmental Science.",
    version="1.0.0",
    lifespan=lifespan,
)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    storage.ensure_bucket_exists()


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}


app.include_router(equipment.router)
app.include_router(bookings.router)
app.include_router(documents.router)
