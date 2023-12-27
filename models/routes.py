from datetime import datetime
from typing import List

from sqlalchemy import Integer, DateTime, func, ForeignKey, Date, String, Float
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database import Base


class Route(Base):
    __tablename__ = 'routes'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    start_point: Mapped[str] = mapped_column(String)
    end_point: Mapped[str] = mapped_column(String)
    duration: Mapped[str] = mapped_column(String)
    
    bus_id: Mapped[int] = mapped_column(Integer, ForeignKey('buses.id'), nullable=True)
    bus: Mapped["Bus"] = relationship(back_populates="routes", lazy="selectin", viewonly=True)

    trips: Mapped[List["Trip"]] = relationship(back_populates="route", lazy="selectin", viewonly=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now, onupdate=func.now())
