from fastapi import APIRouter, HTTPException, Depends
from mysite.database.models import CourierProduct
from mysite.database.schema import CourierProductInputSchema, CourierProductOutSchema
from mysite.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List

courier_router = APIRouter(prefix='/courier-products', tags=['Courier Products'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@courier_router.post('/', response_model=CourierProductOutSchema)
async def create_courier_status(data: CourierProductInputSchema, db: Session = Depends(get_db)):
    courier_db = CourierProduct(**data.dict())
    db.add(courier_db)
    db.commit()
    db.refresh(courier_db)
    return courier_db

@courier_router.get('/', response_model=List[CourierProductOutSchema])
async def list_courier_statuses(db: Session = Depends(get_db)):
    return db.query(CourierProduct).all()

@courier_router.put('/{status_id}', response_model=dict)
async def update_courier_status(status_id: int, data: CourierProductInputSchema, db: Session = Depends(get_db)):
    courier_db = db.query(CourierProduct).filter(CourierProduct.id == status_id).first()
    if not courier_db:
        raise HTTPException(detail="Status not found", status_code=404)

    for key, value in data.dict().items():
        setattr(courier_db, key, value)

    db.commit()
    db.refresh(courier_db)
    return {'message': 'Статус курьера обновлен!'}

@courier_router.delete('/{status_id}', response_model=dict)
async def delete_courier_status(status_id: int, db: Session = Depends(get_db)):
    courier_db = db.query(CourierProduct).filter(CourierProduct.id == status_id).first()
    if not courier_db:
        raise HTTPException(detail="Status not found", status_code=404)
    db.delete(courier_db)
    db.commit()
    return {'message': 'Запись удалена!'}
