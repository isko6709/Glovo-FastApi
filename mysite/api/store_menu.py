from fastapi import APIRouter, HTTPException, Depends
from mysite.database.models import StoreMenu
from mysite.database.schema import StoreMenuInputSchema, StoreMenuOutSchema
from mysite.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List

store_menu_router = APIRouter(prefix='/store-menus', tags=['Store Menus'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@store_menu_router.post('/', response_model=StoreMenuOutSchema)
async def create_menu(menu: StoreMenuInputSchema, db: Session = Depends(get_db)):
    menu_db = StoreMenu(**menu.dict())
    db.add(menu_db)
    db.commit()
    db.refresh(menu_db)
    return menu_db

@store_menu_router.get('/', response_model=List[StoreMenuOutSchema])
async def list_menus(db: Session = Depends(get_db)):
    return db.query(StoreMenu).all()

@store_menu_router.delete('/{menu_id}', response_model=dict)
async def delete_menu(menu_id: int, db: Session = Depends(get_db)):
    menu_db = db.query(StoreMenu).filter(StoreMenu.id == menu_id).first()
    if not menu_db:
        raise HTTPException(detail="Menu not found", status_code=404)
    db.delete(menu_db)
    db.commit()
    return {'message': 'Меню было успешно удалено!'}
