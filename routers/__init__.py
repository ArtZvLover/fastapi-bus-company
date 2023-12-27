from fastapi import APIRouter

from routers.drivers import router as drivers_router
from routers.trips import router as trips_router
from routers.routes import router as routes_router
from routers.buses import router as buses_router

router = APIRouter(prefix='/v1')

router.include_router(drivers_router)
router.include_router(buses_router)
router.include_router(routes_router)
router.include_router(trips_router)

