"""Product catalog models: Category and Product."""
from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "categories"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("catalog:shop_by_category", args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    description = models.TextField(help_text="Full product description shown on the detail page.")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    compare_at_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Optional higher 'was' price to show a discount.",
    )
    image = models.CharField(
        max_length=255,
        blank=True,
        help_text="Path relative to /static/, e.g. img/products/headphones.jpg",
    )
    stock = models.PositiveIntegerField(default=10)
    featured = models.BooleanField(default=False, help_text="Show on the homepage.")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("catalog:product_detail", args=[self.slug])

    @property
    def discount_percent(self):
        """Integer discount % when a compare-at price exists."""
        if self.compare_at_price and self.compare_at_price > self.price:
            return int(round((1 - self.price / self.compare_at_price) * 100))
        return 0

    @property
    def in_stock(self):
        return self.stock > 0
