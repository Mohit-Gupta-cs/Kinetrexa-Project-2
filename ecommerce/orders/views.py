"""Order views: checkout, order confirmation, order history."""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from cart import cart as cart_api

from .forms import CheckoutForm
from .models import Order

SUCCESS_ORDER_SESSION_KEY = "last_order_id"


def checkout(request):
    lines = cart_api.cart_lines(request)
    if not lines:
        messages.info(request, "Your cart is empty — add something before checking out.")
        return redirect("cart:detail")

    subtotal = cart_api.cart_subtotal(request)
    shipping = cart_api.shipping_cost(subtotal)

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.subtotal = subtotal
            order.shipping = shipping
            order.total = subtotal + shipping
            order.save()

            # Snapshot items + decrement stock.
            for product, qty in lines:
                if qty > product.stock:
                    messages.error(
                        request,
                        f"Sorry, only {product.stock} of “{product.name}” is in stock. "
                        "Please adjust quantities and try again.",
                    )
                    order.delete()
                    return redirect("cart:detail")
                order.items.create(
                    product=product,
                    product_name=product.name,
                    price=product.price,
                    quantity=qty,
                )
                product.stock -= qty
                product.save(update_fields=["stock"])

            cart_api.cart_clear(request)
            request.session[SUCCESS_ORDER_SESSION_KEY] = order.pk
            return redirect("orders:success")

        messages.error(request, "Please fix the errors below and try again.")
    else:
        initial = {}
        if request.user.is_authenticated:
            initial = {
                "full_name": request.user.get_full_name() or request.user.username,
                "email": request.user.email,
            }
        form = CheckoutForm(initial=initial)

    context = {
        "form": form,
        "lines": lines,
        "subtotal": subtotal,
        "shipping": shipping,
        "total": subtotal + shipping,
        "free_shipping_threshold": cart_api.FREE_SHIPPING_THRESHOLD,
        "shipping_flat_rate": cart_api.SHIPPING_FLAT_RATE,
    }
    return render(request, "orders/checkout.html", context)


def order_success(request):
    order_id = request.session.get(SUCCESS_ORDER_SESSION_KEY)
    if not order_id:
        return redirect("catalog:home")
    order = get_object_or_404(Order, id=order_id)
    # Only the buyer (or staff) may view it; guests get it once via session.
    if (
        order.user
        and request.user.is_authenticated
        and order.user_id != request.user.id
        and not request.user.is_staff
    ):
        return redirect("catalog:home")
    request.session.pop(SUCCESS_ORDER_SESSION_KEY, None)
    return render(request, "orders/order_success.html", {"order": order})


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).prefetch_related("items")
    return render(request, "orders/my_orders.html", {"orders": orders})
