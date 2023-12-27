from sqlalchemy.orm import Session

from cruds.crud import DBManager
from models import Bus, Driver, Route, Trip


class DriverDBManager(DBManager):
    def __init__(self, session: Session = None):
        super().__init__(session=session, model=Driver)


class BusDBManager(DBManager):
    def __init__(self, session: Session = None):
        super().__init__(session=session, model=Bus)


class RouteDBManager(DBManager):
    def __init__(self, session: Session = None):
        super().__init__(session=session, model=Route)


class TripDBManager(DBManager):
    def __init__(self, session: Session = None):
        super().__init__(session=session, model=Trip)
