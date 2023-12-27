from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class RouteSchemaBase(BaseModel):
    start_point: str
    end_point: str
    duration: str


class RouteSchemaCreate(RouteSchemaBase):
    pass


class RouteSchemaUpdate(RouteSchemaBase):
    start_point: Optional[str] = None
    end_point: Optional[str] = None
    duration: Optional[str] = None


class RouteSchema(RouteSchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
