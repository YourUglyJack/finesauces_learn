from decimal import Decimal
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from listings.models import Product
from .forms import CartAddProductForm


# Create your views here.
def get_cart(request):
    cart = request.session.get(settings.CART_ID)
    if not cart:
        cart = request.session[settings.CART_ID] = {}
    return cart


def cart_add(request, product_id):
    cart = get_cart(request)
    product = get_object_or_404(Product, id=product_id)
    product_id = str(product_id)
    form = CartAddProductForm(request.POST)
    print(cart)
    if form.is_valid():
        cd = form.cleaned_data
        print('enter', cd)
        
        if product_id not in cart:
            cart[product_id] = {'quantity': 0, 'price': str(product.price)}

        if request.POST.get('overwrite_qty'):  # 在购物车界面提交cart_add就会带有该字段，直接覆盖数量
            cart[product_id]['quantity'] = cd['quantity']
        else:
            cart[product_id]['quantity'] += cd['quantity']  # 再商品界面提交cart_add

        request.session.modified = True

    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = get_cart(request)
    product_ids = cart.keys()
    products = Product.objects.filter(id__in=product_ids)  # pylint: disable=no-member
    cart_for_cal = cart.copy()

    cart_total_price = 0
    for product in products:
        cart_item = cart_for_cal[str(product.id)]  # type: ignore
        cart_item['product'] = product
        cart_item['update_quantity_form'] = CartAddProductForm(initial={'quantity': cart_item['quantity']})
        cart_item['total_price'] = (Decimal(cart_item['price'])) * cart_item['quantity']
        cart_total_price += cart_item['total_price']

    return render(request, 'detail.html', {
        'cart': cart_for_cal.values(),
        'cart_total_price': cart_total_price
    })


def cart_remove(request, product_id):
    cart = get_cart(request)
    product_id = str(product_id)
    if product_id in cart:
        del cart[product_id]

        request.session.modified = True

        return redirect('cart:cart_detail')


def cart_clear(request):
    del request.session[settings.CART_ID]
