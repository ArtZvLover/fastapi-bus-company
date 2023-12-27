from datetime import datetime
from typing import List

from sqlalchemy import Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database import Base


class Driver(Base):
    __tablename__ = 'drivers'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String, index=True)
    middle_name: Mapped[str] = mapped_column(String, index=True, nullable=True)
    last_name: Mapped[str] = mapped_column(String, index=True)
    contact_information: Mapped[str] = mapped_column(String)

    trips: Mapped[List["Trip"]] = relationship(back_populates="driver", lazy="selectin", viewonly=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now, onupdate=func.now())

    def get_full_name(self):
        return f"{self.last_name} {self.first_name} {self.middle_name}".strip()