# reviews/urls.py
from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('product/<int:product_id>/reviews/add/', views.add_review, name='add_review'),
    path('review/<int:review_id>/delete/', views.delete_review, name='delete_review'),
    path('product/<int:product_id>/rating-breakdown/', views.rating_breakdown_api, name='rating_breakdown_api'),
]
