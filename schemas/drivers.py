from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class DriverSchemaBase(BaseModel):
    first_name: str
    middle_name: str
    last_name: str
    contact_information: str


class DriverSchemaCreate(DriverSchemaBase):
    pass


class DriverSchemaUpdate(DriverSchemaBase):
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    contact_information: Optional[str] = None


class DriverSchema(DriverSchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
