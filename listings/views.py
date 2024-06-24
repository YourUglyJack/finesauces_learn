"""
This module contains views for the listings' app.
"""

from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product, Review
from .forms import ReviewForm
from cart.forms import CartAddProductForm


# Create your views here.
def product_list(req, category_slug=None):
    categories = Category.objects.all()  # pylint: disable=no-member
    products = Product.objects.all()  # pylint: disable=no-member
    target_category = None

    if category_slug:
        target_category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=target_category)  # pylint: disable=no-member

    ctx = {
        'categories': categories,
        'products': products,
        'target_category': target_category
    }

    return render(req, 'product/list.html', ctx)


def product_detail(req, category_slug, product_slug):
    category = get_object_or_404(Category, slug=category_slug)
    product = get_object_or_404(
        Product,
        category_id=category.id,  # type: ignore
        slug=product_slug)

    if req.method == 'POST':
        review_form = ReviewForm(req.POST)

        if review_form.is_valid():
            cf = review_form.cleaned_data
            author_name = "Anonymous"
            Review.objects.create(  # pylint: disable=no-member
                product=product,
                author=author_name,
                rating=cf['rating'],
                text=cf['text'])

            return redirect('listings:product_detail',
                            category_slug=category_slug,
                            product_slug=product_slug)
    else:
        review_form = ReviewForm()

    cart_product_form = CartAddProductForm()

    return render(req, 'product/detail.html', {
        'product': product,
        'review_form': review_form,
        'cart_product_form': cart_product_form
    })
