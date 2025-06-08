from django.contrib import admin
from .models import (
    Category, Product, Address, Order, OrderItem, Review, Coupon,
    Wishlist, WishlistProduct
)

# Registre todos os modelos para que apareçam no painel de administração
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Address)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Review)
admin.site.register(Coupon)
admin.site.register(Wishlist)
admin.site.register(WishlistProduct)
