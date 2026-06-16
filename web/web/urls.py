from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", TemplateView.as_view(template_name="base.html"), name="home"),
    path("api/v1/", include("api.urls")),        # ← REST API
    path("auth/", include("authentication.urls")),
    path("products/", include("product_management.urls")),
    path("shop/", include("cart_and_orders.urls")),
    path("payments/", include("payments.urls")),
    path("reviews/", include("reviews.urls")),
    path("wishlist/", include("wishlist.urls")),
    path("search/", include("search_and_recommendations.urls")),
    path("shipping/", include("shipping_and_logistics.urls")),
    path("deals/", include("deals_and_discounts.urls")),
    path("notifications/", include("notifications.urls")),
    path("admin/", admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)