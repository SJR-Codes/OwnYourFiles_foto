#from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from . import oyf_models, schemas

async def get_category(db: AsyncSession, category_id: int):
    result = await db.execute(select(oyf_models.OYF_Category).where(oyf_models.OYF_Category.id == category_id))
    return result.scalars().first()

async def get_categories(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(oyf_models.OYF_Category).offset(skip).limit(limit))
    return result.scalars().all()

async def create_category(db: AsyncSession, category: schemas.CategoryCreate):
    db_category = oyf_models.OYF_Category(title=category.title)    
    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)

    return db_category