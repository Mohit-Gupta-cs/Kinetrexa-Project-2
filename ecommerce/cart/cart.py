"""Session-based shopping cart.

The cart lives in the request session as {product_id: quantity} and works for
both anonymous (guest) visitors and logged-in users. No extra database table
needed for the cart itself — it becomes an Order when the user checks out.
"""
from django.conf import settings

CART_SESSION_KEY = "cart"
FREE_SHIPPING_THRESHOLD = getattr(settings, "FREE_SHIPPING_THRESHOLD", 999)
SHIPPING_FLAT_RATE = getattr(settings, "SHIPPING_FLAT_RATE", 79)


def get_cart(request):
    """Return the raw cart dict, creating it lazily if needed."""
    return request.session.setdefault(CART_SESSION_KEY, {})


def save_cart(request, cart):
    request.session[CART_SESSION_KEY] = cart
    request.session.modified = True


def cart_add(request, product, quantity=1):
    """Add `quantity` of `product` to the cart (capped at available stock)."""
    cart = get_cart(request)
    pid = str(product.id)
    current = int(cart.get(pid, 0))
    new_qty = min(current + quantity, product.stock)
    cart[pid] = new_qty
    save_cart(request, cart)
    return new_qty


def cart_set_quantity(request, product, quantity):
    """Set an exact quantity (<= 0 removes the line). Returns the new qty."""
    cart = get_cart(request)
    pid = str(product.id)
    if quantity <= 0:
        cart.pop(pid, None)
    else:
        cart[pid] = min(quantity, product.stock)
    save_cart(request, cart)
    return max(quantity, 0) if quantity > 0 else 0


def cart_remove(request, product_id):
    cart = get_cart(request)
    cart.pop(str(product_id), None)
    save_cart(request, cart)


def cart_clear(request):
    request.session.pop(CART_SESSION_KEY, None)
    request.session.modified = True


def cart_lines(request):
    """Return [(product, quantity)] for every product currently in the cart."""
    from catalog.models import Product

    cart = get_cart(request)
    product_ids = [int(pid) for pid in cart.keys()]
    products = Product.objects.filter(id__in=product_ids, is_active=True)
    product_map = {p.id: p for p in products}
    lines = []
    for pid in cart.keys():
        product = product_map.get(int(pid))
        if product is None:
            continue  # product deleted or deactivated — skip it
        lines.append((product, int(cart[pid])))
    return lines


def cart_count(request):
    return sum(int(q) for q in get_cart(request).values())


def cart_subtotal(request):
    from decimal import Decimal

    total = Decimal("0.00")
    for product, qty in cart_lines(request):
        total += product.price * qty
    return total


def shipping_cost(subtotal):
    if subtotal >= FREE_SHIPPING_THRESHOLD or subtotal == 0:
        return 0
    return SHIPPING_FLAT_RATE
