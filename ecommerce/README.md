# 🛍️ UrbanKart — Simple E-commerce Store

A complete, working e-commerce web application built with **Django** (backend) and
**HTML / CSS / vanilla JavaScript** (frontend). It includes a product catalog,
session-based shopping cart, checkout & order processing, user registration/login,
an admin dashboard, and a SQLite database.

![stack](https://img.shields.io/badge/backend-Django%206-green) ![stack](https://img.shields.io/badge/frontend-HTML%20%2B%20CSS%20%2B%20JS-blue) ![db](https://img.shields.io/badge/database-SQLite-orange)

---

## ✨ Features

| Feature | Details |
|---|---|
| 🏷️ **Product catalog** | 10 seeded products across 4 categories, product detail pages, related products, search, sort, category filter, pagination |
| 🛒 **Shopping cart** | Session-based cart (works for guests *and* logged-in users), quantity steppers, AJAX add/update/remove, free-shipping progress bar, live totals |
| 📦 **Order processing** | Checkout with delivery form + validation, order + order-item creation, automatic stock decrement, order confirmation page, status tracking (Pending → Processing → Shipped → Delivered) |
| 👤 **Auth** | Register (with auto-login), login, logout, order history per user |
| 🔐 **Admin dashboard** | Django admin: manage products, categories, orders (change status), order items |
| 🇮🇳 **Localized** | Indian Rupee formatting with Indian digit grouping (₹1,29,999), Asia/Kolkata timezone |
| 📱 **Responsive UI** | Modern design, works on desktop and mobile |

## 🚀 Quick start

```bash
# 1. Create & activate a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Prepare the database
python manage.py migrate
python manage.py seed            # demo data: 10 products, 4 categories, demo user, 2 sample orders

# 4. (Optional) create an admin account
python manage.py createsuperuser

# 5. Run the dev server
python manage.py runserver
```

Then open **http://127.0.0.1:8000** 🎉

## 👤 Demo accounts

| Role | Username | Password | Notes |
|---|---|---|---|
| Shopper | `demo` | `demo12345` | Has 2 sample orders to view under *My Orders* |
| Admin | `admin` | `admin123` | Django admin at `/admin/` |

> You can also **register a new account** from the Sign up button, or check out as a **guest**.

## 🗂️ Project structure

```
ecommerce/
├── manage.py
├── requirements.txt
├── store/                # Django project config (settings, root urls)
├── catalog/              # Products & categories (models, views, admin, seed command)
│   └── management/commands/seed.py
├── cart/                 # Session cart logic, views, context processor
├── orders/               # Order & OrderItem models, checkout, order history
├── accounts/             # Registration / login / logout
├── templates/            # base.html + page templates (catalog, cart, orders, accounts)
└── static/
    ├── css/style.css     # All styling
    ├── js/main.js        # Toasts, AJAX cart, quantity steppers
    └── img/products/     # Product photos
```

## 🧠 How it works

- **Cart** — stored in the user's session as `{product_id: quantity}`, so it survives
  without a database table and works for anonymous visitors. Quantities are capped at
  available stock.
- **Checkout** — a `CheckoutForm` validates delivery details (phone, 6-digit PIN).
  Submitting creates an `Order` + `OrderItem` snapshots (name/price copied at purchase
  time), decrements stock, clears the cart, and redirects to a confirmation page keyed
  by the order id in the session.
- **Orders** — linked to the user when logged in (`user` FK); guests keep their order
  number on the confirmation page. Admins update statuses in `/admin/`.
- **AJAX** — add-to-cart and cart updates post via `fetch()` with the CSRF token,
  returning JSON so the cart badge and totals update without a page reload.
- **Security** — CSRF protection on all forms, Django auth for passwords/sessions,
  `@login_required` on order history, template auto-escaping.

## 🔧 Customizing

- **Add products** — use the admin (`/admin/`) or edit `catalog/management/commands/seed.py` and re-run `python manage.py seed`.
- **Prices / shipping** — constants live in `cart/cart.py` (`FREE_SHIPPING_THRESHOLD = 999`, `SHIPPING_FLAT_RATE = 79`).
- **Product images** — drop files into `static/img/products/` and set the `image` field to `img/products/<file>.jpg`.

## ⚠️ Notes

- Demo store — **no real payments are processed**; checkout is simulated.
- `SECRET_KEY` and `DEBUG=True` are dev defaults — set a real secret key and `DEBUG=False`
  with proper `ALLOWED_HOSTS` before deploying.
