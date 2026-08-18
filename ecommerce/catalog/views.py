"""Catalog views: homepage, shop listing with filters, product detail."""
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import Category, Product


def home(request):
    featured = Product.objects.filter(is_active=True, featured=True)[:8]
    return render(request, "catalog/home.html", {"featured_products": featured})


def shop(request, category_slug=None):
    """Product listing. Filters: ?category=slug, ?q=search, ?sort=..."""
    products = Product.objects.filter(is_active=True).select_related("category")

    category = None
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    elif request.GET.get("category"):
        category_slug = request.GET.get("category")
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    query = request.GET.get("q", "").strip()
    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    sort = request.GET.get("sort")
    sort_map = {
        "price_asc": "price",
        "price_desc": "-price",
        "newest": "-created_at",
        "name": "name",
    }
    if sort in sort_map:
        products = products.order_by(sort_map[sort])

    paginator = Paginator(products, 12)
    page_obj = paginator.get_page(request.GET.get("page"))

    context = {
        "page_obj": page_obj,
        "categories": Category.objects.all(),
        "active_category": category,
        "query": query,
        "active_sort": sort,
    }
    return render(request, "catalog/product_list.html", context)


def product_detail(request, slug):
    product = get_object_or_404(
        Product.objects.select_related("category"), slug=slug, is_active=True
    )
    related = (
        Product.objects.filter(category=product.category, is_active=True)
        .exclude(id=product.id)[:4]
    )
    return render(
        request,
        "catalog/product_detail.html",
        {"product": product, "related_products": related},
    )
