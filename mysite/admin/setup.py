from fastapi import FastAPI
from sqladmin import Admin
from mysite.database.db import engine
from .views import (
    UserProfileAdmin, CategoryAdmin, StoreAdmin, ContactAdmin,
    AddressAdmin, StoreMenuAdmin, ProductAdmin, OrderAdmin,
    CourierProductAdmin, ReviewAdmin
)
def setup_admin(booking_app: FastAPI):
    admin = Admin(booking_app, engine)
    admin.add_view(UserProfileAdmin)
    admin.add_view(CategoryAdmin)
    admin.add_view(StoreAdmin)
    admin.add_view(ContactAdmin)
    admin.add_view(AddressAdmin)
    admin.add_view(StoreMenuAdmin)
    admin.add_view(ProductAdmin)
    admin.add_view(OrderAdmin)
    admin.add_view(CourierProductAdmin)
    admin.add_view(ReviewAdmin)
