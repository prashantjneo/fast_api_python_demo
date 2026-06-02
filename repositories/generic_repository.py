from typing import List, Optional, Any, TypeVar, Generic, Type
from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType")

class GenericRepository(Generic[ModelType]):
    """
    A generic repository for basic CRUD operations using SQLAlchemy.
    """
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get_all(self, db: Session) -> List[ModelType]:
        """Retrieve all records from the table."""
        return db.query(self.model).all()

    def get_by_id(self, db: Session, item_id: int) -> Optional[ModelType]:
        """Retrieve a specific record by its ID."""
        return db.query(self.model).filter(self.model.id == item_id).first()

    def create(self, db: Session, data: dict) -> ModelType:
        """Create a new record in the table."""
        db_obj = self.model(**data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, item_id: int, data: dict) -> Optional[ModelType]:
        """Update an existing record in the table by its ID."""
        db_obj = self.get_by_id(db, item_id)
        if not db_obj:
            return None
            
        for key, value in data.items():
            setattr(db_obj, key, value)
            
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, item_id: int) -> bool:
        """Delete a record from the table by its ID."""
        db_obj = self.get_by_id(db, item_id)
        if not db_obj:
            return False
            
        db.delete(db_obj)
        db.commit()
        return True
