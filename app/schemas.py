import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, ConfigDict


# ---------- Equipment ----------

class EquipmentBase(BaseModel):
    name: str
    category: str
    serial_number: str
    description: Optional[str] = None


class EquipmentCreate(EquipmentBase):
    pass


class EquipmentUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    serial_number: Optional[str] = None
    description: Optional[str] = None


class EquipmentOut(EquipmentBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime.datetime


# ---------- Booking ----------

class BookingBase(BaseModel):
    researcher_name: str
    researcher_email: EmailStr
    start_date: datetime.date
    end_date: datetime.date
    purpose: str


class BookingCreate(BookingBase):
    equipment_id: int


class BookingOut(BookingBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    equipment_id: int
    is_cancelled: bool
    created_at: datetime.datetime


# ---------- Document ----------

class DocumentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    equipment_id: int
    original_filename: str
    content_type: str
    uploaded_at: datetime.datetime
