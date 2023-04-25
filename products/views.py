from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from products.models import ProductCategory, Product, Basket

# Create your views here.
# контроллеры = views = функции


def index(request):
    context = {
        'title': 'Store'
    }
    return render(request, "products/index.html", context)


def products(request, category_id=None, page=1):
    context = {'title': 'Store - Каталог', 'categories': ProductCategory.objects.all()}
    if category_id:
        products = Product.objects.filter(category_id=category_id)
    else:
        products = Product.objects.all()
    paginator = Paginator(products, 3)
    products_paginator = paginator.page(page)
    context.update({'products': products_paginator})
    return render(request, "products/products.html", context)


@login_required()
def basket_add(request, product_id):
    current_page = request.META.get('HTTP_REFERER')
    product = Product.objects.get(id=product_id)
    basket = Basket.objects.filter(user=request.user, product=product)

    if not basket.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
        return HttpResponseRedirect(current_page)
    else:
        bas = basket.first()
        bas.quantity += 1
        bas.save()
        return HttpResponseRedirect(current_page)


def basket_delete(request, id):
    basket = Basket.objects.get(id=id)
    basket.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def test_context(request):
    context = {
        'title': 'store',
        'header': 'Добро пожаловать!',
        'username': "Иван Иванов",
        'products': [
            {"name": 'Худи черного цвета с монограммами adidas Originals', 'price': 6090},
            {"name": 'Синяя куртка The North Face', 'price': 23725},
            {"name": 'Коричневый спортивный oversized-топ ASOS DESIGN', 'price': 3390},
        ],
        'promotion': True,
        'products_of_promotions': [
            {'name': 'Чёрный рюкзак Nike Heritage', 'price': 2340}
        ]
    }
    return render(request, 'products/test-context.html', context)
