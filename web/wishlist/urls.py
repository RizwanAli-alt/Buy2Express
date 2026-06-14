from django.urls import path
from . import views

app_name = 'wishlist'

urlpatterns = [
    path('', views.wishlist_view, name='wishlist_view'),  # This corresponds to the wishlist page
    path('add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove/<int:wishlist_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('favorite-stores/', views.favorite_stores_view, name='favorite_stores_view'),
    path('add-favorite-store/<int:seller_id>/', views.add_favorite_store, name='add_favorite_store'),
    path('remove-favorite-store/<int:favorite_store_id>/', views.remove_favorite_store, name='remove_favorite_store'),
]
