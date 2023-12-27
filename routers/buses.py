from typing import List

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from cruds import managers
from database import get_db
from utils.sockets import notify_clients
from schemas.buses import BusSchema, BusSchemaCreate, BusSchemaUpdate

router = APIRouter(prefix="/buses", tags=["buses"])


@router.post("/", response_model=BusSchema)
async def create_bus(bus_schema: BusSchemaCreate, db: Session = Depends(get_db)):
    bus = managers.BusDBManager(session=db).create(schema=bus_schema)
    await notify_clients(f"Создан Автобус '{bus.model}-{bus.year}/{bus.registration_number} (ID: {bus.id})'")
    return bus


@router.get("/", response_model=List[BusSchema])
async def read_buses(db: Session = Depends(get_db)):
    bus = managers.BusDBManager(session=db).get_all(db=db)
    return bus


@router.get("/", response_model=BusSchema)
async def read_bus(bus_id: int, db: Session = Depends(get_db)):
    try:
        bus = managers.BusDBManager(session=db).get_by_id(obj_id=bus_id)
        return bus
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Bus not found")


@router.patch("/", response_model=BusSchema)
async def update_bus(bus_id: int, bus_schema: BusSchemaUpdate, db: Session = Depends(get_db)):
    try:
        bus = managers.BusDBManager(session=db).update(obj_id=bus_id, schema=bus_schema)
        await notify_clients(f"Обновлён Автобус '{bus.model}-{bus.year}/{bus.registration_number} (ID: {bus.id})'")
        return bus
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Bus not found")


@router.delete("/", status_code=status.HTTP_200_OK)
async def delete_bus(bus_id: int, db: Session = Depends(get_db)):
    try:
        bus = managers.BusDBManager(session=db).delete(obj_id=bus_id)
        await notify_clients(f"Удалён Автобус '{bus.model}-{bus.year}/{bus.registration_number} (ID: {bus.id})'")
        return bus
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Bus not found")
