from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Product, Category, Cart, CartItem


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "id",
        "username",
        "email",
        "is_seller",
        "is_approved",
        "is_active",
        "is_staff",
        "is_superuser",
        "date_joined",
    )

    list_filter = (
        "is_seller",
        "is_approved",
        "is_active",
        "is_staff",
        "is_superuser",
    )

    search_fields = (
        "username",
        "email",
    )

    ordering = ("-date_joined",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "seller",
        "price",
        "stock",
        "created_at",
    )

    list_filter = (
        "seller",
        "created_at",
    )

    search_fields = (
        "name",
        "description",
        "seller__username",
    )

    ordering = ("-created_at",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "slug",
    )

    search_fields = (
        "name",
    )


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "created_at",
    )

    search_fields = (
        "user__username",
    )


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "cart",
        "product",
        "quantity",
    )

    search_fields = (
        "product__name",
        "cart__user__username",
    )