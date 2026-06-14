# Buy2Express

Buy2Express is a Django e-commerce project with separate apps for authentication, products, cart and orders, payments, reviews, wishlist, search and recommendations, shipping and logistics, deals and discounts, and notifications.

## Project Structure

- `web/` - Django project root
- `web/authentication/` - user registration, login, profile
- `web/product_management/` - products, categories, and brands
- `web/cart_and_orders/` - cart, checkout, and order history
- `web/payments/` - payment processing
- `web/reviews/` - product reviews
- `web/wishlist/` - wishlist and favorite stores
- `web/search_and_recommendations/` - search and recommendations
- `web/shipping_and_logistics/` - shipping addresses, providers, and tracking
- `web/deals_and_discounts/` - deals, discounts, and coupons
- `web/notifications/` - user notifications
- `web/templates/` - shared templates and app templates

## Requirements

- Python 3.10+
- Django

## Local Setup

1. Open a terminal in the repository root.
2. Activate the virtual environment:

```powershell
.\venv\Scripts\Activate.ps1
```

3. Move into the Django project folder:

```powershell
cd web
```

4. Run migrations:

```powershell
python manage.py migrate
```

5. Start the development server:

```powershell
python manage.py runserver 0.0.0.0:8000
```

## Notes

- The custom user model is configured as `authentication.CustomUser`.
- Shared templates live in `web/templates`.
- Most app pages inherit the shared storefront theme from `templates/base.html`.
- If you add new apps or models, run `python manage.py makemigrations` and `python manage.py migrate` from the `web/` directory.
