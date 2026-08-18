"""Template filters: Indian-format currency, discount math."""
from django import template

register = template.Library()


def _indian_grouping(number):
    """Format an integer string with Indian digit grouping (e.g. 129999 -> 1,29,999)."""
    s = str(number)
    if len(s) <= 3:
        return s
    head, tail = s[:-3], s[-3:]
    groups = []
    while len(head) > 2:
        groups.insert(0, head[-2:])
        head = head[:-2]
    groups.insert(0, head)
    return ",".join(groups) + "," + tail


@register.filter
def inr(value):
    """Format a Decimal/int as Indian Rupees, e.g. 12999.00 -> ₹12,999."""
    if value is None:
        value = 0
    try:
        num = float(value)
    except (TypeError, ValueError):
        return value
    if num == int(num):
        return "₹" + _indian_grouping(int(num))
    return "₹" + _indian_grouping(int(num)) + f".{int(round((num % 1) * 100)):02d}"


@register.filter
def discount_percent(product):
    return product.discount_percent


@register.filter
def multiply(value, arg):
    try:
        return value * arg
    except (TypeError, ValueError):
        return 0
