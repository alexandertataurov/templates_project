from app.services.base_service import BaseService

from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import app.models as models
from app.models.specification import Specification
from app.schemas.specification import SpecificationCreate

async def create_specification(db: AsyncSession, contract_id: int, spec_data: SpecificationCreate):
    specification = Specification(**spec_data.model_dump(), contract_id=contract_id)
    db.add(specification)
    await db.commit()
    await db.refresh(specification)
    return specification

async def get_specifications(db: AsyncSession, contract_id: int):
    result = await db.execute(select(Specification).where(Specification.contract_id == contract_id))
    return result.scalars().all()

async def get_specification(db: AsyncSession, spec_id: int):
    return await db.get(Specification, spec_id)

async def delete_specification(db: AsyncSession, spec_id: int):
    spec = await get_specification(db, spec_id)
    if spec:
        await db.delete(spec)
        await db.commit()
        return True
    return False


async def get_contract_by_specification(db: Session, specification_id: int):
    """ Получает контракт, связанный со спецификацией """
    specification = db.query(models.Specification).filter(models.Specification.id == specification_id).first()
    if specification and specification.contract_id:
        return db.query(models.Contract).filter(models.Contract.id == specification.contract_id).first()
    return None
