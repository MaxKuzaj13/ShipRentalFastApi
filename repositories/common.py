from sqlalchemy.orm import Session
from sqlalchemy import update
from typing import Type, TypeVar, Generic, List

# Add CRUD for all
ModelType = TypeVar("ModelType")


class Repository(Generic[ModelType]):
    """
        Base repository class providing common CRUD operations.
    """
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def create(self, db: Session, **kwargs) -> ModelType:
        """
        Create a new object in the database based on the provided data.

        Args:
            db (Session): Database session.
            **kwargs: Keyword arguments used to create the new object.

        Returns:
            ModelType: Newly created object.
        """
        db_obj = self.model(**kwargs)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def fetch_one(self, db: Session, item_id: int) -> ModelType:
        """
        Fetch one object from the database based on the provided item_id.

        Args:
            db (Session): Database session.
            item_id (int): Identifier of the item to fetch.

        Returns:
            ModelType: Fetched object or None if not found.
        """
        item = db.get(self.model, item_id)
        return item

    def delete_one(self, db: Session, item_id: int) -> ModelType:
        """
        Delete one object from the database based on the provided item_id.

        Args:
            db (Session): Database session.
            item_id (int): Identifier of the item to delete.

        Returns:
            ModelType: Deleted object or None if not found.
        """
        item = db.get(self.model, item_id)
        if item:
            db.delete(item)
            db.commit()
            return item
        else:
            return None

    def fetch_all(self, db: Session) -> List[ModelType]:
        """
        Fetch all objects of the associated model from the database.

        Args:
            db (Session): Database session.

        Returns:
            List[ModelType]: List of fetched objects.
        """
        return db.query(self.model).all()

    def update_one(self, db: Session, item_id: int, **kwargs) -> ModelType:
        """
        Update one object in the database based on the provided item_id and kwargs.

        Args:
            db (Session): Database session.
            item_id (int): Identifier of the item to update.
            **kwargs: Keyword arguments containing the updated data.

        Returns:
            ModelType: Updated object or None if not found.
        """
        db_obj = db.execute(update(self.model).where(self.model.id == item_id).values(**kwargs))
        if db_obj.rowcount > 0:
            db.commit()
            updated_data = kwargs.copy()
            updated_data['id'] = item_id
            return updated_data
        else:
            return None
