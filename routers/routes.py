from typing import List

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from cruds import managers
from database import get_db
from utils.sockets import notify_clients
from schemas.routes import RouteSchema, RouteSchemaCreate, RouteSchemaUpdate

router = APIRouter(prefix="/routes", tags=["routes"])


@router.post("/", response_model=RouteSchema)
async def create_route(route_schema: RouteSchemaCreate, db: Session = Depends(get_db)):
    route = managers.RouteDBManager(session=db).create(schema=route_schema)
    await notify_clients(f"Создан Маршрут 'от {route.start_point} до {route.end_point} (ID: {route.id})'")
    return route


@router.get("/", response_model=List[RouteSchema])
async def read_routes(db: Session = Depends(get_db)):
    route = managers.RouteDBManager(session=db).get_all(db=db)
    return route


@router.get("/", response_model=RouteSchema)
async def read_route(route_id: int, db: Session = Depends(get_db)):
    try:
        route = managers.RouteDBManager(session=db).get_by_id(obj_id=route_id)
        return route
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Route not found")


@router.patch("/", response_model=RouteSchema)
async def update_route(route_id: int, route_schema: RouteSchemaUpdate, db: Session = Depends(get_db)):
    try:
        route = managers.RouteDBManager(session=db).update(obj_id=route_id, schema=route_schema)
        await notify_clients(f"Обновлён Маршрут 'от {route.start_point} до {route.end_point} (ID: {route.id})'")
        return route
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Route not found")


@router.delete("/", status_code=status.HTTP_200_OK)
async def delete_route(route_id: int, db: Session = Depends(get_db)):
    try:
        route = managers.RouteDBManager(session=db).delete(obj_id=route_id)
        await notify_clients(f"Удалён Маршрут 'от {route.start_point} до {route.end_point} (ID: {route.id})'")
        return route
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Route not found")
