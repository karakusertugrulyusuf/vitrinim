from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import KullaniciKayitFormu, ProductForm
from .models import Product, Cart, CartItem


# ----------------------------
# AUTH
# ----------------------------
def kayit(request):
    if request.method == 'POST':
        form = KullaniciKayitFormu(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_seller = form.cleaned_data['is_seller']
            user.save()
            login(request, user)
            return redirect('vitrinim:home')
    else:
        form = KullaniciKayitFormu()

    return render(request, 'kayit.html', {'form': form})


def giris(request):
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST.get('username'),
            password=request.POST.get('password')
        )

        if user:
            login(request, user)
            return redirect('vitrinim:home')

        messages.error(request, "Kullanıcı adı veya şifre hatalı")

    return render(request, 'giris.html')


def logout_view(request):
    logout(request)
    return redirect('vitrinim:home')


# ----------------------------
# HOME (🔥 CRASH FIXED)
# ----------------------------
def home(request):
    try:
        products = Product.objects.all().order_by('-created_at')
    except Exception:
        products = []

    return render(request, 'home.html', {'products': products})


# ----------------------------
# PROFILE
# ----------------------------
@login_required(login_url='vitrinim:giris')
def profile(request):
    return render(request, 'profile.html')


@login_required(login_url='vitrinim:giris')
def seller_profile(request):
    products = Product.objects.filter(seller=request.user)
    return render(request, 'seller_profile.html', {'products': products})


# ----------------------------
# PRODUCT
# ----------------------------
@login_required(login_url='vitrinim:giris')
def add_product(request):
    if not request.user.is_seller:
        return redirect('vitrinim:home')

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            messages.success(request, "Ürün eklendi")
            return redirect('vitrinim:seller_profile')
    else:
        form = ProductForm()

    return render(request, 'add_product.html', {'form': form})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_detail.html', {'product': product})


def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})


# ----------------------------
# EDIT PRODUCT
# ----------------------------
@login_required(login_url='vitrinim:giris')
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, seller=request.user)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Ürün güncellendi")
            return redirect('vitrinim:seller_profile')
    else:
        form = ProductForm(instance=product)

    return render(request, 'edit_product.html', {
        'form': form,
        'product': product
    })


# ----------------------------
# DELETE PRODUCT
# ----------------------------
@login_required(login_url='vitrinim:giris')
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, seller=request.user)

    if request.method == 'POST':
        product.delete()
        messages.success(request, "Ürün silindi")
        return redirect('vitrinim:seller_profile')

    return render(request, 'delete_product.html', {'product': product})


# ----------------------------
# CART
# ----------------------------
@login_required(login_url='vitrinim:giris')
def cart_detail(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    return render(request, 'cart_detail.html', {'cart': cart})


@login_required(login_url='vitrinim:giris')
def add_to_cart(request, product_id):
    if request.method != "POST":
        return redirect('vitrinim:product_list')

    product = get_object_or_404(Product, id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if created:
        cart_item.quantity = 1
    else:
        cart_item.quantity += 1

    cart_item.save()
    return redirect('vitrinim:cart_detail')


@login_required(login_url='vitrinim:giris')
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    return redirect('vitrinim:cart_detail')


@login_required(login_url='vitrinim:giris')
def increase_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

    if item.quantity < item.product.stock:
        item.quantity += 1
        item.save()

    return redirect('vitrinim:cart_detail')


@login_required(login_url='vitrinim:giris')
def decrease_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()

    return redirect('vitrinim:cart_detail')