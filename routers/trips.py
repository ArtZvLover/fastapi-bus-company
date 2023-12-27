from typing import List

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from cruds import managers
from database import get_db
from utils.sockets import notify_clients
from schemas.trips import TripSchema, TripSchemaCreate, TripSchemaUpdate

router = APIRouter(prefix="/trips", tags=["trips"])


@router.post("/", response_model=TripSchema)
async def create_trip(trip_schema: TripSchemaCreate, db: Session = Depends(get_db)):
    trip = managers.TripDBManager(session=db).create(schema=trip_schema)
    await notify_clients(
        f"Создан Рейс '(ID: {trip.id})' "
        f"Водителю '{trip.driver.get_full_name()} (ID: {trip.driver.id})' "
        f"Автобуса '{trip.bus.model}-{trip.bus.year}/{trip.bus.registration_number} (ID: {trip.bus.id})' "
        f"Маршрута '{trip.route.start_point} -> {trip.route.end_point} (ID: {trip.route.id})'"
    )
    return trip


@router.get("/", response_model=List[TripSchema])
async def read_trips(db: Session = Depends(get_db)):
    trip = managers.TripDBManager(session=db).get_all(db=db)
    return trip


@router.get("/", response_model=TripSchema)
async def read_trip(trip_id: int, db: Session = Depends(get_db)):
    try:
        trip = managers.TripDBManager(session=db).get_by_id(obj_id=trip_id)
        return trip
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Trip not found")


@router.patch("/", response_model=TripSchema)
async def update_trip(trip_id: int, trip_schema: TripSchemaUpdate, db: Session = Depends(get_db)):
    try:
        trip = managers.TripDBManager(session=db).update(obj_id=trip_id, schema=trip_schema)
        await notify_clients(
            f"Обновлён Рейс '(ID: {trip.id})' "
            f"Водителю '{trip.driver.get_full_name()} (ID: {trip.driver.id})' "
            f"Автобуса '{trip.bus.model}-{trip.bus.year}/{trip.bus.registration_number} (ID: {trip.bus.id})' "
            f"Маршрута '{trip.route.start_point} -> {trip.route.end_point} (ID: {trip.route.id})'"
        )
        return trip
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Trip not found")


@router.delete("/", status_code=status.HTTP_200_OK)
async def delete_trip(trip_id: int, db: Session = Depends(get_db)):
    try:
        trip = managers.TripDBManager(session=db).delete(obj_id=trip_id)
        await notify_clients(
            f"Удалён Рейс '(ID: {trip.id})' "
            f"Водителю '{trip.driver.get_full_name()} (ID: {trip.driver.id})' "
            f"Автобуса '{trip.bus.model}-{trip.bus.year}/{trip.bus.registration_number} (ID: {trip.bus.id})' "
            f"Маршрута '{trip.route.start_point} -> {trip.route.end_point} (ID: {trip.route.id})'"
        )
        return trip
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Trip not found")
