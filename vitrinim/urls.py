from django.urls import path
from . import views

app_name = "vitrinim"

urlpatterns = [
    # ---------------- HOME ----------------
    path('', views.home, name='home'),

    # ---------------- AUTH ----------------
    path('kayit/', views.kayit, name='kayit'),
    path('giris/', views.giris, name='giris'),
    path('cikis/', views.logout_view, name='logout'),

    # ---------------- PROFIL ----------------
    path('profil/', views.profile, name='profile'),
    path('satici-panel/', views.seller_profile, name='seller_profile'),

    # ---------------- PRODUCT ----------------
    path('urunler/', views.product_list, name='product_list'),
    path('urun/<int:pk>/', views.product_detail, name='product_detail'),

    path('urun-ekle/', views.add_product, name='add_product'),
    path('urun-duzenle/<int:product_id>/', views.edit_product, name='edit_product'),
    path('urun-sil/<int:product_id>/', views.delete_product, name='delete_product'),

    # ---------------- CART ----------------
    path('sepete-ekle/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('sepet/', views.cart_detail, name='cart_detail'),
    path('sepet-sil/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),

    # ⚠️ BU İKİSİ views.py’de OLMALI
    path('sepet-arttir/<int:item_id>/', views.increase_quantity, name='increase_quantity'),
    path('sepet-azalt/<int:item_id>/', views.decrease_quantity, name='decrease_quantity'),
]