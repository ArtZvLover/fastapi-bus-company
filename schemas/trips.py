from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class TripSchemaBase(BaseModel):
    start_time: datetime
    bus_id: int
    driver_id: int
    route_id: int


class TripSchemaCreate(TripSchemaBase):
    pass


class TripSchemaUpdate(TripSchemaBase):
    start_time: Optional[datetime] = None
    bus_id: Optional[int] = None
    driver_id: Optional[int] = None
    route_id: Optional[int] = None


class TripSchema(TripSchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
