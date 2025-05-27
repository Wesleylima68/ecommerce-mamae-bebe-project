# users/models.py
from django.db import models
from decimal import Decimal # Importar para o tipo Decimal

# Modelo para Categorias de Produtos
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Nome da Categoria")

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ['name'] # Ordenar categorias por nome

    def __str__(self):
        return self.name

# Modelo para Produtos
class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nome do Produto")
    description = models.TextField(blank=True, null=True, verbose_name="Descrição")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preço")
    stock = models.IntegerField(default=0, verbose_name="Estoque")
    # Campo para armazenar URLs de imagens. Para múltiplos, usaremos um CharField
    # e trataremos como lista de URLs na aplicação ou um modelo Image separado.
    # Por simplicidade, vamos usar um CharField para uma URL principal por enquanto.
    # Mais tarde, podemos criar um modelo 'ProductImage' separado para múltiplas imagens.
    main_image_url = models.URLField(blank=True, null=True, verbose_name="URL da Imagem Principal")

    # Relacionamento One-to-Many com Category (Uma categoria pode ter muitos produtos)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='products', verbose_name="Categoria")

    # Variações como uma string JSON ou Text. Para simplicidade inicial, Text.
    # Você pode armazenar algo como "Pequeno,Médio,Grande" ou "Azul,Rosa".
    # Em projetos maiores, um modelo 'Variation' seria mais robusto.
    variations = models.TextField(blank=True, null=True, help_text="Ex: 'Tamanho: P, M, G | Cor: Azul, Rosa'")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última Atualização")

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
        ordering = ['name'] # Ordenar produtos por nome

    def __str__(self):
        return self.name

# Os outros modelos (Order, OrderItem, Review, Coupon, Wishlist) virão depois.
# users/models.py (Continuação do arquivo, cole abaixo dos modelos existentes)
from django.conf import settings # Importar para acessar o modelo User padrão do Django

# Modelo para Endereços
class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='addresses', verbose_name="Usuário")
    street = models.CharField(max_length=255, verbose_name="Rua")
    number = models.CharField(max_length=10, verbose_name="Número")
    complement = models.CharField(max_length=100, blank=True, null=True, verbose_name="Complemento")
    neighborhood = models.CharField(max_length=100, verbose_name="Bairro")
    city = models.CharField(max_length=100, verbose_name="Cidade")
    state = models.CharField(max_length=100, verbose_name="Estado")
    zip_code = models.CharField(max_length=10, verbose_name="CEP")
    is_default = models.BooleanField(default=False, verbose_name="Endereço Padrão")

    class Meta:
        verbose_name = "Endereço"
        verbose_name_plural = "Endereços"

    def __str__(self):
        return f"{self.street}, {self.number} - {self.city}/{self.state}"

# Modelo para Pedidos
class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pendente'),
        ('PROCESSING', 'Processando'),
        ('SHIPPED', 'Enviado'),
        ('DELIVERED', 'Entregue'),
        ('CANCELED', 'Cancelado'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders', verbose_name="Usuário")
    order_number = models.CharField(max_length=50, unique=True, verbose_name="Número do Pedido") # Gerado automaticamente ou por API
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor Total")
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Custo de Frete")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING', verbose_name="Status")
    payment_method = models.CharField(max_length=50, verbose_name="Método de Pagamento")
    shipping_address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Endereço de Entrega")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data do Pedido")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última Atualização")

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ['-created_at'] # Ordenar pedidos do mais novo para o mais antigo

    def __str__(self):
        return f"Pedido {self.order_number} - {self.user.username}"

# Modelo para Itens do Pedido
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name="Pedido")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Produto")
    quantity = models.IntegerField(verbose_name="Quantidade")
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preço na Compra") # Preço do produto no momento da compra

    class Meta:
        verbose_name = "Item do Pedido"
        verbose_name_plural = "Itens do Pedido"
        unique_together = ('order', 'product') # Um produto único por pedido

    def __str__(self):
        return f"{self.quantity} x {self.product.name} (Pedido {self.order.order_number})"

# Modelo para Avaliações de Produto
class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews', verbose_name="Usuário")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', verbose_name="Produto")
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], verbose_name="Avaliação (1-5)") # Avaliação de 1 a 5 estrelas
    comment = models.TextField(blank=True, null=True, verbose_name="Comentário")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data da Avaliação")

    class Meta:
        verbose_name = "Avaliação"
        verbose_name_plural = "Avaliações"
        unique_together = ('user', 'product') # Um usuário pode avaliar um produto apenas uma vez

    def __str__(self):
        return f"Avaliação de {self.user.username} para {self.product.name}"

# Modelo para Cupons de Desconto
class Coupon(models.Model):
    DISCOUNT_TYPE_CHOICES = [
        ('PERCENTAGE', 'Porcentagem'),
        ('FIXED', 'Valor Fixo'),
    ]

    code = models.CharField(max_length=50, unique=True, verbose_name="Código do Cupom")
    discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPE_CHOICES, verbose_name="Tipo de Desconto")
    discount_value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor do Desconto")
    expiration_date = models.DateTimeField(blank=True, null=True, verbose_name="Data de Expiração")
    is_active = models.BooleanField(default=True, verbose_name="Ativo")
    usage_limit = models.IntegerField(blank=True, null=True, verbose_name="Limite de Usos")
    times_used = models.IntegerField(default=0, verbose_name="Vezes Usado")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Criado Por")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última Atualização")

    class Meta:
        verbose_name = "Cupom"
        verbose_name_plural = "Cupons"

    def __str__(self):
        return self.code

# Modelo para Lista de Desejos
class Wishlist(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wishlist', verbose_name="Usuário")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última Atualização")

    products = models.ManyToManyField(Product, through='WishlistProduct', related_name='wishlisted_by', verbose_name="Produtos Desejados")

    class Meta:
        verbose_name = "Lista de Desejos"
        verbose_name_plural = "Listas de Desejos"

    def __str__(self):
        return f"Lista de Desejos de {self.user.username}"

# Modelo de Junção para M:N entre Wishlist e Product (Necessário para adicionar metadados como 'added_at')
class WishlistProduct(models.Model):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True, verbose_name="Adicionado Em")

    class Meta:
        verbose_name = "Produto na Lista de Desejos"
        verbose_name_plural = "Produtos na Lista de Desejos"
        unique_together = ('wishlist', 'product') # Garante que um produto não seja adicionado duas vezes na mesma lista

    def __str__(self):
        return f"{self.product.name} em {self.wishlist.user.username}'s Wishlist"
    