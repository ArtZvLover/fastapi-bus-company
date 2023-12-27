from typing import List

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from cruds import managers
from database import get_db
from utils.sockets import notify_clients
from schemas.drivers import DriverSchema, DriverSchemaCreate, DriverSchemaUpdate

router = APIRouter(prefix="/drivers", tags=["drivers"])


@router.post("/", response_model=DriverSchema)
async def create_driver(driver_schema: DriverSchemaCreate, db: Session = Depends(get_db)):
    driver = managers.DriverDBManager(session=db).create(schema=driver_schema)
    await notify_clients(f"Создан Водитель '{driver.get_full_name()} (ID: {driver.id})'")
    return driver


@router.get("/", response_model=List[DriverSchema])
async def read_drivers(db: Session = Depends(get_db)):
    driver = managers.DriverDBManager(session=db).get_all(db=db)
    return driver


@router.get("/", response_model=DriverSchema)
async def read_driver(driver_id: int, db: Session = Depends(get_db)):
    try:
        driver = managers.DriverDBManager(session=db).get_by_id(obj_id=driver_id)
        return driver
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Driver not found")


@router.patch("/", response_model=DriverSchema)
async def update_driver(driver_id: int, driver_schema: DriverSchemaUpdate, db: Session = Depends(get_db)):
    try:
        driver = managers.DriverDBManager(session=db).update(obj_id=driver_id, schema=driver_schema)
        await notify_clients(f"Обновлён Водитель '{driver.get_full_name()} (ID: {driver.id})'")
        return driver
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Driver not found")


@router.delete("/", status_code=status.HTTP_200_OK)
async def delete_driver(driver_id: int, db: Session = Depends(get_db)):
    try:
        driver = managers.DriverDBManager(session=db).delete(obj_id=driver_id)
        await notify_clients(f"Удалён Водитель '{driver.get_full_name()} (ID: {driver_id})'")
        return driver
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Driver not found")
