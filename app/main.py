from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI

from app.database import Base, engine
from app.routers import equipment, bookings, documents
from app import storage

app = FastAPI(
    title="Equipment Management API",
    description="Manages field equipment, bookings and supporting documents "
    "for the Department of Environmental Science.",
    version="1.0.0",
)


@app.on_event("startup")
def on_startup():
    # Application container is stateless — tables and the storage bucket
    # are created on startup if they don't already exist.
    Base.metadata.create_all(bind=engine)
    storage.ensure_bucket_exists()


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}


app.include_router(equipment.router)
app.include_router(bookings.router)
app.include_router(documents.router)
