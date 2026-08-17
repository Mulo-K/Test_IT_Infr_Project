from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/equipment", tags=["Equipment"])


@router.post("", response_model=schemas.EquipmentOut, status_code=201)
def create_equipment(payload: schemas.EquipmentCreate, db: Session = Depends(get_db)):
    existing = (
        db.query(models.Equipment)
        .filter(models.Equipment.serial_number == payload.serial_number)
        .first()
    )
    if existing:
        raise HTTPException(status_code=409, detail="Serial number already registered")

    equipment = models.Equipment(**payload.model_dump())
    db.add(equipment)
    db.commit()
    db.refresh(equipment)
    return equipment


@router.get("", response_model=List[schemas.EquipmentOut])
def list_equipment(db: Session = Depends(get_db)):
    return db.query(models.Equipment).all()


@router.get("/{equipment_id}", response_model=schemas.EquipmentOut)
def get_equipment(equipment_id: int, db: Session = Depends(get_db)):
    equipment = db.query(models.Equipment).get(equipment_id)
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")
    return equipment


@router.patch("/{equipment_id}", response_model=schemas.EquipmentOut)
def update_equipment(
    equipment_id: int, payload: schemas.EquipmentUpdate, db: Session = Depends(get_db)
):
    equipment = db.query(models.Equipment).get(equipment_id)
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(equipment, field, value)

    db.commit()
    db.refresh(equipment)
    return equipment
