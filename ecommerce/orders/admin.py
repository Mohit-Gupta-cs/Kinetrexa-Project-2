from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product", "product_name", "price", "quantity", "line_total")

    def line_total(self, obj):
        return obj.line_total

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "order_number",
        "full_name",
        "email",
        "phone",
        "total",
        "status",
        "created_at",
    )
    list_filter = ("status", "created_at")
    list_editable = ("status",)
    search_fields = ("full_name", "email", "phone", "address")
    readonly_fields = (
        "user",
        "subtotal",
        "shipping",
        "total",
        "created_at",
        "updated_at",
    )
    inlines = [OrderItemInline]
    date_hierarchy = "created_at"

    def order_number(self, obj):
        return obj.order_number

    order_number.short_description = "Order #"
