from typing import TypeVar, Type

from pydantic import BaseModel as SchemaBase
from sqlalchemy.orm import Session

from database import Base as ModelBase

DBModelType = TypeVar("DBModelType", bound=ModelBase)


class DBManager:
    def __init__(self, session: Session, model: Type[DBModelType]):
        self.model = model
        self.session = session

    def create(self, schema: SchemaBase, **kwargs):
        obj_data = schema.model_dump()
        obj_data.update(kwargs)
        obj = self.model(**obj_data)

        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)

        return obj

    def get(self, **kwargs):
        return self.filter(**kwargs).first()

    def get_by_id(self, obj_id: int):
        return self.filter(id=obj_id).first()

    def get_all(self, offset: int = 0, limit: int = None, **kwargs):
        if kwargs:
            query = self.filter(**kwargs).offset(offset)
        else:
            query = self.session.query(self.model).offset(offset)

        if limit is not None:
            query = query.limit(limit)
        return query.all()

    def filter(self, **kwargs):
        valid_attributes = [attr for attr in kwargs.keys() if hasattr(self.model, attr)]
        filters = [getattr(self.model, attr) == value for attr, value in kwargs.items() if attr in valid_attributes]
        return self.session.query(self.model).filter(*filters)

    def update(self, obj_id: int, schema: SchemaBase):
        session_obj = self.get_by_id(obj_id)

        for var, value in vars(schema).items():
            setattr(session_obj, var, value) if value or str(value) == 'False' else None

        self.session.commit()
        self.session.refresh(session_obj)
        return session_obj

    def delete(self, obj_id: int):
        session_obj = self.get_by_id(obj_id)
        self.session.delete(session_obj)
        self.session.commit()
        return session_obj

    def delete_all(self):
        self.session.query(self.model).delete()
        self.session.commit()
        return True
