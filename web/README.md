# Buy2Express

Buy2Express is a Django e-commerce project with separate apps for authentication, products, cart and orders, payments, reviews, wishlist, search and recommendations, shipping and logistics, deals and discounts, and notifications.

## Project Layout

- `authentication/` - login, register, and profile management
- `product_management/` - products, categories, and brands
- `cart_and_orders/` - cart, checkout, and order history
- `payments/` - payment processing
- `reviews/` - product reviews
- `wishlist/` - wishlist and favorite stores
- `search_and_recommendations/` - search and recommendations
- `shipping_and_logistics/` - shipping addresses, providers, and tracking
- `deals_and_discounts/` - deals, discounts, and coupons
- `notifications/` - user notifications
- `templates/` - shared and app templates
- `web/` - Django project settings and URL configuration

## Setup

1. Activate the virtual environment from the repository parent folder:

```powershell
.\venv\Scripts\Activate.ps1
```

2. Run commands from this folder:

```powershell
cd c:\Users\HP\Desktop\Buy2Express\web
```

3. Apply migrations:

```powershell
python manage.py migrate
```

4. Start the development server:

```powershell
python manage.py runserver 0.0.0.0:8000
```

## Git Push

From `c:\Users\HP\Desktop\Buy2Express\web`, use:

```powershell
git add README.md .gitignore .gitattributes
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/RizwanAli-alt/Buy2Express.git
git push -u origin main
```

## Notes

- The custom user model is `authentication.CustomUser`.
- Shared templates live in `templates/`.
- If you add new models, run `python manage.py makemigrations` and `python manage.py migrate`.
