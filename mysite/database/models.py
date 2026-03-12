from .db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Enum, Text, DateTime, ForeignKey
from typing import Optional, List
from enum import Enum as PyEnum
from datetime import datetime


class RoleChoices(str, PyEnum):
    client = 'client'
    owner = 'owner'
    courier = 'courier'


class OrderStatusChoices(str, PyEnum):
    pending = 'pending'
    canceled = 'canceled'
    delivered = 'delivered'


class CourierStatusChoices(str, PyEnum):
    busy = 'busy'
    available = 'available'


class UserProfile(Base):
    __tablename__ = 'user_profile'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(150))
    last_name: Mapped[str] = mapped_column(String(150))
    username: Mapped[str] = mapped_column(String(150), unique=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String)
    phone_number: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    role: Mapped[RoleChoices] = mapped_column(Enum(RoleChoices, create_constraint=False),
                                              default=RoleChoices.client)
    date_registered: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    owned_stores: Mapped[List['Store']] = relationship(back_populates='owner', cascade='all, delete-orphan')
    client_orders: Mapped[List['Order']] = relationship(back_populates='client',
                                                        foreign_keys='Order.client_id',
                                                        cascade='all, delete-orphan')
    courier_orders: Mapped[List['Order']] = relationship(back_populates='courier',
                                                         foreign_keys='Order.courier_id',
                                                         cascade='all, delete-orphan')
    courier_products: Mapped[List['CourierProduct']] = relationship(back_populates='user',
                                                                    cascade='all, delete-orphan')
    client_reviews: Mapped[List['Review']] = relationship(back_populates='client',
                                                          foreign_keys='Review.client_id',
                                                          cascade='all, delete-orphan')
    courier_reviews: Mapped[List['Review']] = relationship(back_populates='courier',
                                                           foreign_keys='Review.courier_id',
                                                           cascade='all, delete-orphan')
    tokens: Mapped[List["RefreshToken"]] = relationship(back_populates="token_user", cascade="all, delete-orphan")


class Category(Base):
    __tablename__ = 'category'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    category_name: Mapped[str] = mapped_column(String(25), unique=True)

    stores: Mapped[List['Store']] = relationship(back_populates='category', cascade='all, delete-orphan')


class Store(Base):
    __tablename__ = 'store'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    category_id: Mapped[int] = mapped_column(ForeignKey('category.id'))
    store_name: Mapped[str] = mapped_column(String(30), unique=True)
    store_image: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    description: Mapped[str] = mapped_column(Text)
    owner_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    category: Mapped['Category'] = relationship(back_populates='stores')
    owner: Mapped['UserProfile'] = relationship(back_populates='owned_stores')
    contacts: Mapped[List['Contact']] = relationship(back_populates='store', cascade='all, delete-orphan')
    addresses: Mapped[List['Address']] = relationship(back_populates='store', cascade='all, delete-orphan')
    store_menus: Mapped[List['StoreMenu']] = relationship(back_populates='store', cascade='all, delete-orphan')
    reviews: Mapped[List['Review']] = relationship(back_populates='store', cascade='all, delete-orphan')


class Contact(Base):
    __tablename__ = 'contact'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    store_id: Mapped[int] = mapped_column(ForeignKey('store.id'))
    contact_name: Mapped[str] = mapped_column(String(20))
    contact_number: Mapped[str] = mapped_column(String)

    store: Mapped['Store'] = relationship(back_populates='contacts')


class Address(Base):
    __tablename__ = 'address'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    store_id: Mapped[int] = mapped_column(ForeignKey('store.id'))
    address_name: Mapped[str] = mapped_column(String(50))

    store: Mapped['Store'] = relationship(back_populates='addresses')


class StoreMenu(Base):
    __tablename__ = 'store_menu'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    store_id: Mapped[int] = mapped_column(ForeignKey('store.id'))
    menu_name: Mapped[str] = mapped_column(String(30), unique=True)

    store: Mapped['Store'] = relationship(back_populates='store_menus')
    products: Mapped[List['Product']] = relationship(back_populates='store_menu', cascade='all, delete-orphan')


class Product(Base):
    __tablename__ = 'product'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    store_menu_id: Mapped[int] = mapped_column(ForeignKey('store_menu.id'))
    product_name: Mapped[str] = mapped_column(String(50))
    product_image: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    product_description: Mapped[str] = mapped_column(Text)
    price: Mapped[int] = mapped_column(Integer)
    quantity: Mapped[int] = mapped_column(Integer, default=1)

    store_menu: Mapped['StoreMenu'] = relationship(back_populates='products')
    orders: Mapped[List['Order']] = relationship(back_populates='product', cascade='all, delete-orphan')


class Order(Base):
    __tablename__ = 'order'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    client_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    product_id: Mapped[int] = mapped_column(ForeignKey('product.id'))
    status: Mapped[OrderStatusChoices] = mapped_column(Enum(OrderStatusChoices, create_constraint=False),
                                                       default=OrderStatusChoices.pending)
    delivery_address: Mapped[str] = mapped_column(Text)
    courier_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    client: Mapped['UserProfile'] = relationship(back_populates='client_orders', foreign_keys=[client_id])
    courier: Mapped['UserProfile'] = relationship(back_populates='courier_orders', foreign_keys=[courier_id])
    product: Mapped['Product'] = relationship(back_populates='orders')
    courier_products: Mapped[List['CourierProduct']] = relationship(back_populates='current_order',
                                                                    cascade='all, delete-orphan')


class CourierProduct(Base):
    __tablename__ = 'courier_product'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    current_order_id: Mapped[int] = mapped_column(ForeignKey('order.id'))
    courier_status: Mapped[CourierStatusChoices] = mapped_column(Enum(CourierStatusChoices, create_constraint=False))

    user: Mapped['UserProfile'] = relationship(back_populates='courier_products')
    current_order: Mapped['Order'] = relationship(back_populates='courier_products')


class Review(Base):
    __tablename__ = 'review'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    client_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    store_id: Mapped[Optional[int]] = mapped_column(ForeignKey('store.id'), nullable=True)
    courier_id: Mapped[Optional[int]] = mapped_column(ForeignKey('user_profile.id'), nullable=True)
    rating: Mapped[int] = mapped_column(Integer)
    text: Mapped[str] = mapped_column(Text)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    client: Mapped['UserProfile'] = relationship(back_populates='client_reviews', foreign_keys=[client_id])
    courier: Mapped['UserProfile'] = relationship(back_populates='courier_reviews', foreign_keys=[courier_id])
    store: Mapped['Store'] = relationship(back_populates='reviews')


class RefreshToken(Base):
    __tablename__ = 'refresh_token'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    token_user: Mapped["UserProfile"] = relationship(back_populates='tokens')
    token: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
