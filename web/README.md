# Buy2Express

Buy2Express is a Django e-commerce platform with a full REST API, Elasticsearch-powered search, and separate apps for authentication, products, cart and orders, payments, reviews, wishlist, search and recommendations, shipping and logistics, deals and discounts, and notifications.

## Project Layout

- `authentication/` - login, register, and profile management
- `product_management/` - products, categories, and brands
- `cart_and_orders/` - cart, checkout, and order history
- `payments/` - payment processing
- `reviews/` - product reviews
- `wishlist/` - wishlist and favorite stores
- `search_and_recommendations/` - Elasticsearch-powered search, autocomplete, and recommendations
- `shipping_and_logistics/` - shipping addresses, providers, and tracking
- `deals_and_discounts/` - deals, discounts, and coupons
- `notifications/` - user notifications
- `api/` - REST API (v1) with JWT authentication, pagination, filtering, and sorting
- `templates/` - shared and app templates
- `web/` - Django project settings and URL configuration

## Requirements

- Python 3.10+
- PostgreSQL
- Docker Desktop (for Elasticsearch)

## Setup

### 1. Activate the virtual environment

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
pip install -r requirements.txt
```

### 3. Set up environment variables

Create a `.env` file in the `web/` folder:

```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=buy2express_db
DB_USER=postgres
DB_PASSWORD=your-db-password
DB_HOST=127.0.0.1
DB_PORT=5432
ELASTICSEARCH_HOST=http://localhost:9200
JWT_ACCESS_MINUTES=60
JWT_REFRESH_DAYS=7
```

### 4. Apply migrations

```powershell
cd web
python manage.py migrate
```

### 5. Start Elasticsearch (Docker)

Make sure Docker Desktop is running, then:

```powershell
# First time only
docker run -d --name elasticsearch `
  -p 9200:9200 `
  -e "discovery.type=single-node" `
  -e "xpack.security.enabled=false" `
  elasticsearch:8.11.0

# Auto-restart on Docker startup (run once)
docker update --restart always elasticsearch

# Every time after (just this one command)
docker start elasticsearch
```

### 6. Build the Elasticsearch index

```powershell
python manage.py search_index --rebuild
```

When you add new products, re-populate the index:

```powershell
python manage.py search_index --populate
```

### 7. Start the development server

```powershell
python manage.py runserver 0.0.0.0:8000
```

## Daily Development Workflow

```powershell
# 1. Start Docker Desktop (or it auto-starts if configured)
# 2. Start Elasticsearch
docker start elasticsearch

# 3. Activate venv and run server
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\venv\Scripts\Activate.ps1
cd web
python manage.py runserver
```

## REST API

The API is available at `http://localhost:8000/api/v1/`

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/register/` | Register new user, returns JWT |
| POST | `/api/v1/auth/login/` | Login, returns JWT |
| POST | `/api/v1/auth/logout/` | Blacklist refresh token |
| GET/PUT | `/api/v1/auth/profile/` | View or update profile |
| POST | `/api/v1/auth/token/refresh/` | Refresh access token |

### Products
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/products/` | List products (filterable, sortable) |
| GET | `/api/v1/products/{id}/` | Product detail |
| GET | `/api/v1/products/{id}/reviews/` | Reviews for a product |
| GET | `/api/v1/categories/` | List categories |
| GET | `/api/v1/brands/` | List brands |

### Cart & Orders
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/cart/` | View cart |
| POST | `/api/v1/cart/items/` | Add item to cart |
| PATCH | `/api/v1/cart/items/{id}/` | Update quantity |
| DELETE | `/api/v1/cart/items/{id}/` | Remove item |
| POST | `/api/v1/cart/checkout/` | Place order |
| GET | `/api/v1/orders/` | Order history |
| GET | `/api/v1/orders/{id}/` | Order detail |

### Search
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/search/?q=laptop` | Full-text search with facets |
| GET | `/api/v1/search/autocomplete/?q=lap` | Typeahead suggestions |
| GET | `/api/v1/recommendations/` | Personalised recommendations |

### Other Endpoints
| Endpoint | Description |
|----------|-------------|
| `/api/v1/reviews/` | Product reviews |
| `/api/v1/wishlist/` | Wishlist |
| `/api/v1/deals/` | Active deals |
| `/api/v1/discounts/` | Active discounts |
| `/api/v1/coupons/apply/` | Apply coupon code |
| `/api/v1/notifications/` | User notifications |
| `/api/v1/shipping/addresses/` | Shipping addresses |
| `/api/v1/payments/{order_id}/` | Process payment |

### API Query Parameters (Products & Search)
| Parameter | Example | Description |
|-----------|---------|-------------|
| `q` | `?q=laptop` | Search query |
| `category` | `?category=1` | Filter by category ID |
| `brand` | `?brand=2` | Filter by brand ID |
| `min_price` | `?min_price=100` | Minimum price |
| `max_price` | `?max_price=500` | Maximum price |
| `sort` | `?sort=price_asc` | Sort: `price_asc`, `price_desc`, `name`, `relevance` |
| `page` | `?page=2` | Page number |
| `page_size` | `?page_size=10` | Results per page (max 100) |

### JWT Authentication Usage

Include the access token in every request header: