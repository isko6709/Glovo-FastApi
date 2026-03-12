from fastapi import APIRouter, HTTPException, Depends
from mysite.database.models import Address
from mysite.database.schema import AddressInputSchema, AddressOutSchema
from mysite.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List

address_router = APIRouter(prefix='/addresses', tags=['Addresses'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@address_router.post('/', response_model=AddressOutSchema)
async def create_address(address: AddressInputSchema, db: Session = Depends(get_db)):
    address_db = Address(**address.dict())
    db.add(address_db)
    db.commit()
    db.refresh(address_db)
    return address_db

@address_router.get('/', response_model=List[AddressOutSchema])
async def list_addresses(db: Session = Depends(get_db)):
    return db.query(Address).all()
