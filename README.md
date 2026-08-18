🛒 UrbanKart — Django E-Commerce Store

UrbanKart is a simple full-stack e-commerce website built with Python and Django. It provides product browsing, product details, a session-based shopping cart, user authentication, checkout, and order management.

This project is suitable for a beginner/intermediate Django e-commerce assignment or portfolio project.

✨ Features

🏠 E-commerce homepage with featured products

🛍️ Product listing and category browsing

🔎 Product detail pages

🛒 Shopping cart with quantity updates and item removal

👤 User registration, login, and logout

📦 Checkout and order processing

🧾 My Orders page

🔐 Django authentication

⚙️ Django admin panel

🗄️ SQLite database

📱 Responsive frontend

🎨 Custom HTML/CSS/JavaScript UI

🌱 Database seed command for sample products

🛠️ Tech Stack

Frontend

HTML5

CSS3

JavaScript

Backend

Python 3

Django 5+

Database

SQLite

Other

Django Templates

Django ORM

Django Sessions

Git/GitHub

📁 Project Structure

ecommerce/
├── manage.py
├── requirements.txt
├── db.sqlite3
│
├── store/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── accounts/
│   ├── forms.py
│   ├── views.py
│   ├── urls.py
│   └── ...
│
├── catalog/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── management/
│       └── commands/
│           └── seed.py
│
├── cart/
│   ├── cart.py
│   ├── views.py
│   ├── urls.py
│   └── context_processors.py
│
├── orders/
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
│
├── templates/
│   ├── base.html
│   ├── catalog/
│   ├── cart/
│   ├── accounts/
│   ├── orders/
│   └── includes/
│
└── static/
    ├── css/
    ├── js/
    └── img/

⚙️ Installation

1. Clone the repository

git clone <YOUR-GITHUB-REPOSITORY-URL>
cd ecommerce

2. Create a virtual environment

Windows:

python -m venv .venv

3. Activate the virtual environment

PowerShell:

.venv\Scripts\Activate.ps1

Command Prompt:

.venv\Scripts\activate

4. Install dependencies

pip install -r requirements.txt

The project currently requires Django 5.x/6.x-compatible versions through:

Django>=5.0,<7.0

🗄️ Database Setup

Run migrations:

python manage.py makemigrations
python manage.py migrate

The project uses SQLite, so no separate database server is required.

🌱 Add Sample Products

The project includes a custom seed command:

python manage.py seed

This can be used to populate the store with sample categories and products.

👨‍💻 Create an Admin User

Create a Django superuser:

python manage.py createsuperuser

Enter the requested username, email, and password.

▶️ Run the Project

Start the Django development server:

python manage.py runserver

Open:

http://127.0.0.1:8000/

Django admin:

http://127.0.0.1:8000/admin/

🛍️ Main User Flow

Open the store homepage.

Browse products or categories.

Open a product detail page.

Add products to the shopping cart.

Change quantities or remove items.

Register or log in.

Continue to checkout.

Enter delivery details.

Place the order.

View the order from My Orders.

📦 Order Management

Orders contain:

Customer information

Delivery address

Subtotal

Shipping cost

Total amount

Order status

Ordered products

Product price snapshot

Quantity

Order creation/update timestamps

Available order statuses:

Pending
Processing
Shipped
Delivered
Cancelled

🗃️ Main Database Models

Product

Stores:

Product name

Category

Description

Price

Compare-at price

Image

Stock

Featured status

Active status

Creation/update dates

Category

Stores:

Category name

Slug

Description

Order

Stores:

Customer

Contact details

Delivery address

Subtotal

Shipping

Total

Status

Creation/update dates

OrderItem

Stores:

Product

Product name at purchase time

Price at purchase time

Quantity

Line total

🔐 Authentication

The project uses Django's built-in authentication system for:

Registration

Login

Logout

Authenticated user sessions

🧰 Useful Django Commands

Check the project:

python manage.py check

Create migrations:

python manage.py makemigrations

Apply migrations:

python manage.py migrate

Create admin account:

python manage.py createsuperuser

Run development server:

python manage.py runserver

Run tests:

python manage.py test

📋 Assignment Requirements

This project covers the requested Simple E-Commerce Store requirements:

Requirement

Status

HTML

✅

CSS

✅

JavaScript

✅

Django/Python Backend

✅

Product Listings

✅

Product Details Page

✅

Shopping Cart

✅

User Registration/Login

✅

Order Processing

✅

Database

✅

Product Management

✅

Order Management

✅

🔮 Future Improvements

Possible improvements include:

💳 Online payment integration

❤️ Wishlist

⭐ Product reviews and ratings

🔍 Advanced product search

🏷️ Coupons and discount codes

📧 Order confirmation emails

📊 Sales dashboard

🔔 Order status notifications

🖼️ Django media/image uploads

🌐 REST API

🐘 PostgreSQL for production

🚀 Deployment to AWS, Render, Railway, or another hosting platform

🔒 Production Notes

This repository is configured for development. Before deploying to production:

Change the Django SECRET_KEY

Set DEBUG = False

Configure ALLOWED_HOSTS

Use environment variables for secrets

Configure a production database

Configure static/media file serving

Enable HTTPS

Review Django security settings

👨‍💻 Author

Mohit Gupta

B.Tech Computer Science Engineering Student
