from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from cart.forms import CartAddProductForm
from django.db.models import Q


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

   
    available = request.GET.get('available')
    if available == '1':
        products = products.filter(available=True)

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    sort = request.GET.get('sort')
    if sort in ['name', '-name', 'price', '-price']:
        products = products.order_by(sort)

    context = {
        'category': category,
        'categories': categories,
        'products': products,
        'selected_min_price': min_price,
        'selected_max_price': max_price,
        'selected_available': available,
        'current_sort': sort,
    }
    return render(request, 'main/product/list.html', context)

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    related_products = Product.objects.filter(category=product.category,available=True).exclude(id=product.id)[:4]
    cart_product_form = CartAddProductForm()
    return render(request, 'main/product/detail.html', {
        'product': product,
        'related_products': related_products,
        'cart_product_form': cart_product_form
    })