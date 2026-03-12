from mysite.database.models import (
    UserProfile, Category, Store, Contact, Address,
    StoreMenu, Product, Order, CourierProduct, Review
)
from sqladmin import ModelView

class UserProfileAdmin(ModelView, model=UserProfile):
    column_list = [UserProfile.id, UserProfile.username, UserProfile.role]

class CategoryAdmin(ModelView, model=Category):
    column_list = [Category.id, Category.category_name]

class StoreAdmin(ModelView, model=Store):
    column_list = [Store.id, Store.store_name, Store.owner_id]

class ContactAdmin(ModelView, model=Contact):
    column_list = [Contact.id, Contact.contact_name, Contact.contact_number]

class AddressAdmin(ModelView, model=Address):
    column_list = [Address.id, Address.address_name]

class StoreMenuAdmin(ModelView, model=StoreMenu):
    column_list = [StoreMenu.id, StoreMenu.menu_name]

class ProductAdmin(ModelView, model=Product):
    column_list = [Product.id, Product.product_name, Product.price]

class OrderAdmin(ModelView, model=Order):
    column_list = [Order.id, Order.status, Order.client_id]

class CourierProductAdmin(ModelView, model=CourierProduct):
    column_list = [CourierProduct.id, CourierProduct.courier_status]

class ReviewAdmin(ModelView, model=Review):
    column_list = [Review.id, Review.rating] # В твоей модели Review поле rating обычно присутствует
