"""Cart views: view cart, add / update / remove items (AJAX + form fallback)."""
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from catalog.models import Product

from . import cart as cart_api


def cart_detail(request):
    lines = cart_api.cart_lines(request)
    subtotal = cart_api.cart_subtotal(request)
    shipping = cart_api.shipping_cost(subtotal)
    context = {
        "lines": lines,
        "subtotal": subtotal,
        "shipping": shipping,
        "total": subtotal + shipping,
        "free_shipping_threshold": cart_api.FREE_SHIPPING_THRESHOLD,
        "free_shipping_remaining": max(0, cart_api.FREE_SHIPPING_THRESHOLD - subtotal),
        "shipping_flat_rate": cart_api.SHIPPING_FLAT_RATE,
    }
    return render(request, "cart/cart_detail.html", context)


@require_POST
def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)
    try:
        quantity = max(1, int(request.POST.get("quantity", 1)))
    except (TypeError, ValueError):
        quantity = 1

    new_qty = cart_api.cart_add(request, product, quantity)

    # AJAX request? Return JSON so the page can toast + update the badge.
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse(
            {
                "ok": True,
                "count": cart_api.cart_count(request),
                "quantity": new_qty,
                "subtotal": str(cart_api.cart_subtotal(request)),
            }
        )

    messages.success(request, f"Added {product.name} to your cart.")
    # Return to the product page unless the user asked for the cart.
    next_url = request.POST.get("next")
    if next_url and next_url.startswith("/"):
        return redirect(next_url)
    return redirect("cart:detail")


@require_POST
def cart_update(request, product_id):
    """AJAX endpoint used by the quantity steppers on the cart page."""
    product = get_object_or_404(Product, id=product_id, is_active=True)
    try:
        quantity = int(request.POST.get("quantity", 1))
    except (TypeError, ValueError):
        quantity = 0

    cart_api.cart_set_quantity(request, product, quantity)

    lines = cart_api.cart_lines(request)
    subtotal = cart_api.cart_subtotal(request)
    shipping = cart_api.shipping_cost(subtotal)
    line_total = None
    if quantity > 0:
        line_total = product.price * quantity

    return JsonResponse(
        {
            "ok": True,
            "count": cart_api.cart_count(request),
            "line_total": str(line_total) if line_total else None,
            "subtotal": str(subtotal),
            "shipping": str(shipping),
            "total": str(subtotal + shipping),
            "empty": not lines,
        }
    )


@require_POST
def cart_remove(request, product_id):
    get_object_or_404(Product, id=product_id)
    cart_api.cart_remove(request, product_id)
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse({"ok": True})
    messages.info(request, "Item removed from cart.")
    return redirect("cart:detail")


@require_POST
def cart_clear(request):
    cart_api.cart_clear(request)
    messages.info(request, "Your cart has been emptied.")
    return redirect("cart:detail")
