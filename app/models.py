import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Date,
    DateTime,
    Boolean,
    ForeignKey,
)
from sqlalchemy.orm import relationship

from app.database import Base


class Equipment(Base):
    __tablename__ = "equipment"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)  # e.g. drone, GPS unit, weather station
    serial_number = Column(String, unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    bookings = relationship(
        "Booking", back_populates="equipment", cascade="all, delete-orphan"
    )
    documents = relationship(
        "Document", back_populates="equipment", cascade="all, delete-orphan"
    )


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    equipment_id = Column(Integer, ForeignKey("equipment.id"), nullable=False)
    researcher_name = Column(String, nullable=False)
    researcher_email = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    purpose = Column(Text, nullable=False)
    is_cancelled = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    equipment = relationship("Equipment", back_populates="bookings")


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    equipment_id = Column(Integer, ForeignKey("equipment.id"), nullable=False)
    original_filename = Column(String, nullable=False)
    content_type = Column(String, nullable=False)
    object_key = Column(String, unique=True, nullable=False)  # key in SeaweedFS/S3
    uploaded_at = Column(DateTime, default=datetime.datetime.utcnow)

    equipment = relationship("Equipment", back_populates="documents")
