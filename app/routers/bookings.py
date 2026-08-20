from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.post("", response_model=schemas.BookingOut, status_code=201)
def create_booking(payload: schemas.BookingCreate, db: Session = Depends(get_db)):
    equipment = db.get(models.Equipment, payload.equipment_id)
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")

    if payload.end_date < payload.start_date:
        raise HTTPException(status_code=422, detail="end_date must be on or after start_date")

    # Prevent overlapping ACTIVE bookings for the same equipment.
    # Two date ranges overlap when: existing.start <= new.end AND existing.end >= new.start
    overlap = (
        db.query(models.Booking)
        .filter(
            models.Booking.equipment_id == payload.equipment_id,
            models.Booking.is_cancelled.is_(False),
            models.Booking.start_date <= payload.end_date,
            models.Booking.end_date >= payload.start_date,
        )
        .first()
    )
    if overlap:
        raise HTTPException(
            status_code=409,
            detail="This equipment already has an active booking that overlaps these dates",
        )

    booking = models.Booking(**payload.model_dump())
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking


@router.get("", response_model=List[schemas.BookingOut])
def list_bookings(
    equipment_id: Optional[int] = None,
    include_cancelled: bool = False,
    db: Session = Depends(get_db),
):
    query = db.query(models.Booking)
    if equipment_id is not None:
        query = query.filter(models.Booking.equipment_id == equipment_id)
    if not include_cancelled:
        query = query.filter(models.Booking.is_cancelled.is_(False))
    return query.all()


@router.delete("/{booking_id}", response_model=schemas.BookingOut)
def cancel_booking(booking_id: int, db: Session = Depends(get_db)):
    booking = db.get(models.Booking, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    booking.is_cancelled = True
    db.commit()
    db.refresh(booking)
    return booking
