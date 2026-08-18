"""Seed the database with demo categories, products, a demo user and sample orders.

Usage:  python manage.py seed
"""
from decimal import Decimal

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone

from catalog.models import Category, Product
from orders.models import Order, OrderItem

PRODUCTS = [
    # (category, name, slug, price, compare_at, stock, featured, image, description)
    (
        "Electronics",
        "Aura Pro Wireless Headphones",
        "aura-pro-wireless-headphones",
        "4999.00",
        "6999.00",
        15,
        True,
        "img/products/headphones.jpg",
        "Drown out the world with active noise cancellation, 40-hour battery life and "
        "plush memory-foam ear cushions. Bluetooth 5.3, low-latency gaming mode and a "
        "built-in mic for crystal-clear calls. Includes a hard travel case and USB-C "
        "fast charging — 10 minutes of charge gives you 5 hours of playback.",
    ),
    (
        "Electronics",
        "Pulse Smart Fitness Watch",
        "pulse-smart-fitness-watch",
        "2499.00",
        "3499.00",
        25,
        True,
        "img/products/smartwatch.jpg",
        "Track heart rate, SpO2, sleep and 100+ sport modes on a bright AMOLED display. "
        "5ATM water resistance, 7-day battery and smart notifications for calls and apps. "
        "Works with Android and iOS via the companion app.",
    ),
    (
        "Electronics",
        "KeyForge Mechanical Keyboard",
        "keyforge-mechanical-keyboard",
        "3499.00",
        "4499.00",
        12,
        True,
        "img/products/keyboard.jpg",
        "Hot-swappable mechanical switches, per-key RGB backlighting and a solid "
        "aluminium frame. Full anti-ghosting with 104 keys, USB-C and detachable cable. "
        "Perfect for typing marathons and gaming sessions alike.",
    ),
    (
        "Fashion",
        "StrideFlex Running Sneakers",
        "strideflex-running-sneakers",
        "2999.00",
        "3999.00",
        20,
        True,
        "img/products/sneakers.jpg",
        "Featherlight knit upper with responsive cushioning for everyday runs. "
        "Breathable, flexible and grippy on wet roads. Available in a range of sizes; "
        "true to size fit.",
    ),
    (
        "Fashion",
        "Essential Cotton Crew T-Shirt",
        "essential-cotton-crew-tshirt",
        "699.00",
        "999.00",
        40,
        True,
        "img/products/tshirt.jpg",
        "A wardrobe staple in 100% combed cotton. Soft hand-feel, pre-shrunk and "
        "tag-free neck label. Regular fit with a ribbed crew neck.",
    ),
    (
        "Accessories",
        "Metro 25L Urban Backpack",
        "metro-25l-urban-backpack",
        "1799.00",
        "2499.00",
        18,
        True,
        "img/products/backpack.jpg",
        "Water-repellent 25L pack with a padded 15.6\" laptop sleeve, USB pass-through "
        "port and anti-theft back pocket. Ergonomic shoulder straps make commutes and "
        "weekend trips comfortable.",
    ),
    (
        "Accessories",
        "Solace Polarized Sunglasses",
        "solace-polarized-sunglasses",
        "1299.00",
        "1799.00",
        30,
        True,
        "img/products/sunglasses.jpg",
        "Polarized UV400 lenses cut glare while driving or at the beach. Lightweight "
        "acetate frame with spring hinges, plus a hard case and microfibre cloth.",
    ),
    (
        "Accessories",
        "HydroSteel Insulated Bottle",
        "hydrosteel-insulated-bottle",
        "899.00",
        "1299.00",
        35,
        True,
        "img/products/bottle.jpg",
        "Double-wall vacuum insulation keeps drinks cold for 24 hours or hot for 12. "
        "Leak-proof stainless steel body in a 750 ml size — BPA-free, dishwasher-safe lid.",
    ),
    (
        "Home & Living",
        "Lumen LED Desk Lamp",
        "lumen-led-desk-lamp",
        "1499.00",
        "1999.00",
        22,
        True,
        "img/products/lamp.jpg",
        "Eye-friendly stepless dimming with 3 colour temperatures (warm/neutral/cool). "
        "Adjustable neck and a USB charging port built into the base. Great for study "
        "desks and late-night work.",
    ),
    (
        "Home & Living",
        "Ceramic Mug Set (Set of 2)",
        "ceramic-mug-set",
        "599.00",
        "899.00",
        28,
        True,
        "img/products/mug.jpg",
        "Minimalist matte ceramic mugs, 350 ml each, with a smooth handle and "
        "dishwasher-safe glaze. Sold as a set of two — a lovely gift for tea and "
        "coffee lovers.",
    ),
]


class Command(BaseCommand):
    help = "Create demo categories, products, a demo user and sample orders."

    def handle(self, *args, **options):
        # --- Categories -------------------------------------------------
        category_objs = {}
        for name, slug, desc in [
            ("Electronics", "electronics", "Gadgets, audio and smart devices."),
            ("Fashion", "fashion", "Clothing and footwear for everyday life."),
            ("Accessories", "accessories", "Bags, eyewear and everyday carry."),
            ("Home & Living", "home-living", "Things that make your space better."),
        ]:
            cat, _ = Category.objects.get_or_create(
                slug=slug, defaults={"name": name, "description": desc}
            )
            category_objs[name] = cat
        self.stdout.write(self.style.SUCCESS(f"✓ Categories ({Category.objects.count()})"))

        # --- Products ---------------------------------------------------
        for category_name, name, slug, price, compare, stock, featured, image, desc in PRODUCTS:
            Product.objects.update_or_create(
                slug=slug,
                defaults={
                    "category": category_objs[category_name],
                    "name": name,
                    "price": Decimal(price),
                    "compare_at_price": Decimal(compare),
                    "stock": stock,
                    "featured": featured,
                    "image": image,
                    "description": desc,
                    "is_active": True,
                },
            )
        self.stdout.write(self.style.SUCCESS(f"✓ Products ({Product.objects.count()})"))

        # --- Demo user --------------------------------------------------
        demo, created = User.objects.get_or_create(
            username="demo",
            defaults={
                "email": "demo@urbankart.in",
                "first_name": "Demo",
                "last_name": "Shopper",
            },
        )
        if created:
            demo.set_password("demo12345")
            demo.save()
        self.stdout.write(self.style.SUCCESS("✓ Demo user: demo / demo12345"))

        # --- Sample orders for the demo user -----------------------------
        if not Order.objects.filter(user=demo).exists():
            now = timezone.now()
            sample = [
                {
                    "product_slug": "essential-cotton-crew-tshirt",
                    "qty": 2,
                    "days_ago": 12,
                    "status": "delivered",
                },
                {
                    "product_slug": "pulse-smart-fitness-watch",
                    "qty": 1,
                    "days_ago": 4,
                    "status": "shipped",
                },
            ]
            for item in sample:
                product = Product.objects.get(slug=item["product_slug"])
                qty = item["qty"]
                subtotal = product.price * qty
                shipping = 0 if subtotal >= 999 else 79
                order = Order.objects.create(
                    user=demo,
                    full_name="Demo Shopper",
                    email=demo.email,
                    phone="9876543210",
                    address="221B MG Road, Shastri Nagar",
                    city="Meerut",
                    state="Uttar Pradesh",
                    postal_code="250004",
                    subtotal=subtotal,
                    shipping=shipping,
                    total=subtotal + shipping,
                    status=item["status"],
                    created_at=now - timezone.timedelta(days=item["days_ago"]),
                )
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    product_name=product.name,
                    price=product.price,
                    quantity=qty,
                )
            self.stdout.write(self.style.SUCCESS("✓ 2 sample orders for demo user"))

        self.stdout.write(self.style.SUCCESS("\nSeed complete. Happy shopping! 🛍️"))
