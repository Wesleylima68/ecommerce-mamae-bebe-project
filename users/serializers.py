# users/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User # Django's built-in User model
from .models import (
    Category, Product, Address, Order, OrderItem, Review, Coupon,
    Wishlist, WishlistProduct
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email'] # Campos que queremos expor do User padrão

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__' # Inclui todos os campos do modelo

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True) # Exibe a categoria aninhada
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source='category', write_only=True)

    class Meta:
        model = Product
        fields = '__all__' # Inclui todos os campos do modelo, incluindo a URL da imagem principal e variações

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True) # Nome do produto
    product_price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True) # Preço atual do produto

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'product_price', 'quantity', 'price_at_purchase', 'order']
        read_only_fields = ['order'] # O order será definido na viewset do Order

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True) # Inclui os itens do pedido
    shipping_address = AddressSerializer(read_only=True) # Inclui os dados do endereço de entrega

    class Meta:
        model = Order
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True) # Exibe o usuário que fez a avaliação
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = Review
        fields = '__all__'

class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'

class WishlistProductSerializer(serializers.ModelSerializer):
    product_details = ProductSerializer(source='product', read_only=True)

    class Meta:
        model = WishlistProduct
        fields = ['product', 'added_at', 'product_details'] # O 'product' aqui é o ID do produto

class WishlistSerializer(serializers.ModelSerializer):
    products = WishlistProductSerializer(source='wishlistproduct_set', many=True, read_only=True) # Acessa a tabela de junção

    class Meta:
        model = Wishlist
        fields = '__all__'