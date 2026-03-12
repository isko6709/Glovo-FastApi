from pydantic import BaseModel, EmailStr
from typing import Optional
from .models import RoleChoices, OrderStatusChoices, CourierStatusChoices
from datetime import datetime

class UserProfileInputSchema(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    password: str
    phone_number: Optional[str]
    role: RoleChoices

class UserProfileOutSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    phone_number: Optional[str]
    role: RoleChoices
    date_registered: datetime

class UserLoginSchema(BaseModel):
    username: str
    password: str

class CategoryInputSchema(BaseModel):
    category_name: str

class CategoryOutSchema(BaseModel):
    id: int
    category_name: str

class StoreInputSchema(BaseModel):
    category_id: int
    store_name: str
    store_image: Optional[str]
    description: str
    owner_id: int

class StoreOutSchema(BaseModel):
    id: int
    category_id: int
    store_name: str
    store_image: Optional[str]
    description: str
    owner_id: int
    created_date: datetime


class ContactInputSchema(BaseModel):
    store_id: int
    contact_name: str
    contact_number: str

class ContactOutSchema(BaseModel):
    id: int
    store_id: int
    contact_name: str
    contact_number: str


class AddressInputSchema(BaseModel):
    store_id: int
    address_name: str

class AddressOutSchema(BaseModel):
    id: int
    store_id: int
    address_name: str



class StoreMenuInputSchema(BaseModel):
    store_id: int
    menu_name: str

class StoreMenuOutSchema(BaseModel):
    id: int
    store_id: int
    menu_name: str


class ProductInputSchema(BaseModel):
    store_menu_id: int
    product_name: str
    product_image: Optional[str]
    product_description: str
    price: int
    quantity: int

class ProductOutSchema(BaseModel):
    id: int
    store_menu_id: int
    product_name: str
    product_image: Optional[str]
    product_description: str
    price: int
    quantity: int


class OrderInputSchema(BaseModel):
    client_id: int
    product_id: int
    status: OrderStatusChoices
    delivery_address: str
    courier_id: int

class OrderOutSchema(BaseModel):
    id: int
    client_id: int
    product_id: int
    status: OrderStatusChoices
    delivery_address: str
    courier_id: int
    created_at: datetime


class CourierProductInputSchema(BaseModel):
    user_id: int
    current_order_id: int
    courier_status: CourierStatusChoices

class CourierProductOutSchema(BaseModel):
    id: int
    user_id: int
    current_order_id: int
    courier_status: CourierStatusChoices

class ReviewInputSchema(BaseModel):
    client_id: int
    store_id: Optional[int]
    courier_id: Optional[int]
    rating: int
    text: str

class ReviewOutSchema(BaseModel):
    id: int
    client_id: int
    store_id: Optional[int]
    courier_id: Optional[int]
    rating: int
    text: str
    created_date: datetime