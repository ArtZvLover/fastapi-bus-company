from datetime import datetime

from sqlalchemy import Integer, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database import Base


class Trip(Base):
    __tablename__ = 'trips'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    start_time = mapped_column(DateTime(timezone=True), server_default=func.now())
    bus_id: Mapped[int] = mapped_column(Integer, ForeignKey('buses.id'), nullable=True)
    driver_id: Mapped[int] = mapped_column(Integer, ForeignKey('drivers.id'), nullable=True)
    route_id = mapped_column(Integer, ForeignKey('routes.id'))

    bus: Mapped["Bus"] = relationship(back_populates="trips", lazy="selectin", viewonly=True)
    driver: Mapped["Driver"] = relationship(back_populates="trips", lazy="selectin", viewonly=True)
    route: Mapped["Route"] = relationship(back_populates="trips", lazy="selectin", viewonly=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now,
                                                 server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now, onupdate=func.now())
