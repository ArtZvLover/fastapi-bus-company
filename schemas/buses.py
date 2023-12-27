from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class BusSchemaBase(BaseModel):
    model: str
    year: int = Field(
        ...,
        ge=1900,
        le=datetime.today().year,
        description="Год Автобуса не может быть ниже 1900 и выше текущего года.",
    )
    registration_number: str
    capacity: int


class BusSchemaCreate(BusSchemaBase):
    pass


class BusSchemaUpdate(BusSchemaBase):
    model: Optional[str] = None
    year: Optional[int] = Field(
        None,
        ge=1900,
        le=datetime.today().year,
        description="Год Автобуса не может быть ниже 1900 и выше текущего года.",
    )
    registration_number: Optional[str] = None
    capacity: Optional[int] = None


class BusSchema(BusSchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
