from datetime import datetime
from typing import List

from sqlalchemy import Integer, String, DateTime, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database import Base


class Bus(Base):
    __tablename__ = 'buses'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    model: Mapped[str] = mapped_column(String)
    year: Mapped[int] = mapped_column(Integer)
    registration_number: Mapped[str] = mapped_column(String, index=True)
    capacity: Mapped[int] = mapped_column(Integer)

    routes: Mapped[List["Route"]] = relationship(back_populates="bus", lazy="selectin", viewonly=True)
    trips: Mapped[List["Trip"]] = relationship(back_populates="bus", lazy="selectin", viewonly=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now, onupdate=func.now())
