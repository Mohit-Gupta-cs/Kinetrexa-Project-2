"""Context processors: expose cart badge info + nav categories globally."""
from catalog.models import Category

from . import cart as cart_api


def cart(request):
    if request.path.startswith("/admin/"):
        return {}
    return {
        "cart_count": cart_api.cart_count(request),
        "cart_subtotal": cart_api.cart_subtotal(request),
        "nav_categories": Category.objects.filter(products__is_active=True)
        .distinct()
        .order_by("name"),
    }
