from sqlalchemy.orm import Session
from sqlalchemy import update
from typing import Type, TypeVar, Generic

# Add CRUD for all
ModelType = TypeVar("ModelType")


class Repository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def create(self, db: Session, **kwargs) -> ModelType:
        db_obj = self.model(**kwargs)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def fetch_one(self, db: Session, item_id: int) -> ModelType:
        item = db.get(self.model, item_id)
        return item

    def delete_one(self, db: Session, item_id: int) -> ModelType:
        item = db.get(self.model, item_id)
        if item:
            db.delete(item)
            db.commit()
            return item
        else:
            return None

    def fetch_all(self, db: Session) -> list[ModelType]:
        return db.query(self.model).all()

    def update_one(self, db: Session, item_id: int, **kwargs) -> ModelType:
        db_obj = db.execute(update(self.model).where(self.model.id == item_id).values(**kwargs))
        if db_obj.rowcount > 0:
            db.commit()
            updated_data = kwargs.copy()
            updated_data['id'] = item_id
            return updated_data
        else:
            return None
