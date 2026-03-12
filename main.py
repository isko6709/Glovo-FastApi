from fastapi import FastAPI
import uvicorn
from mysite.api import (
    user, category, store, contact, address,
    store_menu, product, order, courier_product, review, auth
)
from mysite.admin.setup import setup_admin

glovo_app = FastAPI(title="glovo")

glovo_app.include_router(user.user_router)
glovo_app.include_router(category.category_router)
glovo_app.include_router(store.store_router)
glovo_app.include_router(contact.contact_router)
glovo_app.include_router(address.address_router)
glovo_app.include_router(store_menu.store_menu_router)
glovo_app.include_router(product.product_router)
glovo_app.include_router(order.order_router)
glovo_app.include_router(courier_product.courier_router)
glovo_app.include_router(review.review_router)
glovo_app.include_router(auth.auth_router)

setup_admin(glovo_app)

if __name__ == '__main__':
    uvicorn.run(glovo_app, host="127.0.0.1", port=8000)

