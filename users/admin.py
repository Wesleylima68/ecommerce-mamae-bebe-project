# users/admin.py
from django.contrib import admin
from .models import Category, Product # Importe os modelos que você criou

# Registre seus modelos aqui para que apareçam no painel de administração
admin.site.register(Category)
admin.site.register(Product)
# users/admin.py (Continuação do arquivo, adicione abaixo dos registros existentes)
from .models import (
    Category, Product, Address, Order, OrderItem, Review, Coupon,
    Wishlist, WishlistProduct
) # Importe todos os seus modelos

# ... (Seu admin.site.register(Category) e admin.site.register(Product) já devem estar aqui) ...

# Registre os novos modelos
admin.site.register(Address)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Review)
admin.site.register(Coupon)
admin.site.register(Wishlist)
admin.site.register(WishlistProduct)