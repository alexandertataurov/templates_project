from sqlalchemy.orm import Session

class BaseService:
    model = None  # Этот параметр должен быть переопределен в дочерних классах

    @classmethod
    def create(cls, db: Session, obj_in):
        """Создает новый объект"""
        db_obj = cls.model(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @classmethod
    def get_all(cls, db: Session):
        """Возвращает все объекты"""
        return db.query(cls.model).all()

    @classmethod
    def get(cls, db: Session, obj_id: int):
        """Возвращает один объект по ID"""
        return db.query(cls.model).filter(cls.model.id == obj_id).first()

    @classmethod
    def delete(cls, db: Session, obj_id: int):
        """Удаляет объект по ID"""
        obj = db.query(cls.model).filter(cls.model.id == obj_id).first()
        if obj:
            db.delete(obj)
            db.commit()
        return obj
