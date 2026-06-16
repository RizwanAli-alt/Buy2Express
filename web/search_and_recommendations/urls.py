from django.urls import path
from . import views

app_name = 'search_and_recommendations'

urlpatterns = [
    path('search/',          views.search_view,          name='search_view'),
    path('autocomplete/',    views.autocomplete_view,     name='autocomplete'),
    path('recommendations/', views.recommendations_view,  name='recommendations_view'),
]