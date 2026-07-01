from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class KullaniciKayitFormu(UserCreationForm):
    email = forms.EmailField(required=True)
    is_seller = forms.BooleanField(required=False, label="Ben satıcıyım")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'is_seller']
from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock', 'image']