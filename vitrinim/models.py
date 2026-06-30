from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# ----------------------------
# CUSTOM USER MODEL
# ----------------------------
class User(AbstractUser):
    is_seller = models.BooleanField(default=False, verbose_name="Satıcı mı?")
    is_approved = models.BooleanField(default=False, verbose_name="Onaylı kullanıcı mı?")

    def __str__(self):
        return self.username


# ----------------------------
# CATEGORY MODEL
# ----------------------------
class Category(models.Model):
    name = models.CharField("Kategori Adı", max_length=50, unique=True)
    slug = models.SlugField("Slug", max_length=50, unique=True)

    def __str__(self):
        return self.name


# ----------------------------
# PRODUCT MODEL
# ----------------------------
class Product(models.Model):
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Satıcı"
    )
    name = models.CharField("Ürün Adı", max_length=100)
    description = models.TextField("Açıklama")
    price = models.DecimalField("Fiyat", max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField("Stok")
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Kategori"
    )
    image = models.ImageField(
        "Ürün Görseli",
        upload_to='product_images/',
        null=True,
        blank=True
    )
    created_at = models.DateTimeField("Eklenme Tarihi", auto_now_add=True)

    def __str__(self):
        return self.name


# ----------------------------
# CART MODEL
# ----------------------------
class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - Sepet"

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())


# ----------------------------
# CART ITEM MODEL
# ----------------------------
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    @property
    def total_price(self):
        return self.product.price * self.quantity