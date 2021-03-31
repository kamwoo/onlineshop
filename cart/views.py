from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
# Create your views here.

from shop.models import Product
from .forms import AddProductForm
from .cart import Cart
from coupon.forms import AddCouponForm

@require_POST
def add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    form = AddProductForm(request.POST)
    # 클라이언트에서 서버로 데이터를 전달할 때
    # 유효성 검사. injection 전처리를 대신해준다.
    # 클라이언트로부터 받은 데이터를 꼭 form을 사용하여 받아서 클린 데이터로 처리한다.

    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'],is_update=cd['is_update'])

    return redirect('cart:detail')

def remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:detail')

def detail(request):
    cart = Cart(request)
    add_coupon = AddCouponForm()
    for product in cart:
        product['quantity_form'] = AddProductForm(initial={'quantity': product['quantity'], 'is_update':True})

    return render(request, 'cart/detail.html',{'cart':cart, 'add_coupon': add_coupon})