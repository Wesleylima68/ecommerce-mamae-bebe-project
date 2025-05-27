# users/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from .models import (
    Category, Product, Address, Order, OrderItem, Review, Coupon,
    Wishlist, WishlistProduct
)
from .serializers import (
    UserSerializer, CategorySerializer, ProductSerializer, AddressSerializer,
    OrderSerializer, OrderItemSerializer, ReviewSerializer, CouponSerializer,
    WishlistSerializer, WishlistProductSerializer
)

# ViewSet para o usuário padrão do Django
class UserViewSet(viewsets.ReadOnlyModelViewSet): # ReadOnly porque o gerenciamento de usuários é complexo
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny] # Pode ser ajustado para IsAdminUser se quiser restringir mais

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
    permission_classes = [AllowAny] # Permite qualquer um listar/criar (pode ser ajustado)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('name')
    serializer_class = ProductSerializer
    permission_classes = [AllowAny] # Permite qualquer um listar/criar (pode ser ajustado)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def add_to_wishlist(self, request, pk=None):
        product = self.get_object()
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        wishlist_product, created_item = WishlistProduct.objects.get_or_create(
            wishlist=wishlist, product=product
        )
        if created_item:
            return Response({'status': 'Produto adicionado à lista de desejos'}, status=status.HTTP_201_CREATED)
        return Response({'status': 'Produto já está na lista de desejos'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def remove_from_wishlist(self, request, pk=None):
        product = self.get_object()
        try:
            wishlist = Wishlist.objects.get(user=request.user)
            wishlist_product = WishlistProduct.objects.get(wishlist=wishlist, product=product)
            wishlist_product.delete()
            return Response({'status': 'Produto removido da lista de desejos'}, status=status.HTTP_204_NO_CONTENT)
        except (Wishlist.DoesNotExist, WishlistProduct.DoesNotExist):
            return Response({'status': 'Produto não encontrado na lista de desejos'}, status=status.HTTP_404_NOT_FOUND)

class AddressViewSet(viewsets.ModelViewSet):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated] # Apenas usuários autenticados podem gerenciar seus endereços

    def get_queryset(self):
        # Retorna apenas os endereços do usuário logado
        return Address.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Garante que o usuário logado seja definido como o proprietário do endereço
        serializer.save(user=self.request.user)

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Administradores podem ver todos os pedidos, usuários comuns apenas os seus
        if self.request.user.is_staff: # is_staff é uma propriedade para verificar se é admin
            return Order.objects.all().order_by('-created_at')
        return Order.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        # Associa o pedido ao usuário logado
        order = serializer.save(user=self.request.user)
        # Exemplo de como você criaria OrderItems após criar um Order
        # Em um cenário real, você passaria os itens do carrinho no request.data
        # Por simplicidade aqui, vamos apenas salvar o Order.
        # A lógica para criar OrderItems a partir de um carrinho viria aqui.

        # Simulando criação de OrderItems (você adaptaria isso para usar dados do frontend)
        # Por exemplo, se o frontend enviasse uma lista de products_in_cart no request.data
        # for item_data in self.request.data.get('cart_items', []):
        #     product = Product.objects.get(id=item_data['product_id'])
        #     OrderItem.objects.create(
        #         order=order,
        #         product=product,
        #         quantity=item_data['quantity'],
        #         price_at_purchase=product.price # Ou item_data['price'] se o preço veio do frontend
        #     )
        # Se você fosse realmente finalizar um pedido por aqui, a lógica de esvaziar o carrinho, etc. estaria no frontend após a chamada à API.

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    # Normalmente OrderItems não são criados ou listados diretamente, mas através de Order
    # permission_classes = [IsAdminUser] # Apenas admin pode gerenciar isso diretamente

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Usuários podem ver todas as avaliações, mas só podem editar/deletar as suas
        return Review.objects.all() # Ou filter(user=self.request.user) para ver apenas as suas

    def perform_create(self, serializer):
        serializer.save(user=self.request.user) # Associa a avaliação ao usuário logado

class CouponViewSet(viewsets.ModelViewSet):
    queryset = Coupon.objects.all().order_by('code')
    serializer_class = CouponSerializer
    # Apenas administradores podem criar/gerenciar cupons
    # permission_classes = [IsAdminUser] # Requer uma permissão de admin mais sofisticada
    permission_classes = [AllowAny] # Temporário para teste

class WishlistViewSet(viewsets.ModelViewSet):
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Um usuário só pode ver/gerenciar sua própria lista de desejos
        return Wishlist.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Cria a lista de desejos para o usuário logado
        serializer.save(user=self.request.user)
