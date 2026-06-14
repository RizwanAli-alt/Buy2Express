from django.shortcuts import render, redirect, get_object_or_404
from .models import Wishlist, FavoriteStore
from django.contrib.auth.decorators import login_required
from product_management.models import Product

@login_required
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
    return render(request, 'wishlist/wishlist.html', {'wishlist_items': wishlist_items})


@login_required
def add_to_wishlist(request, product_id):
    get_object_or_404(Product, id=product_id)
    Wishlist.objects.get_or_create(user=request.user, product_id=product_id)
    return redirect('wishlist:wishlist_view')


@login_required
def remove_from_wishlist(request, wishlist_id):
    wishlist_item = get_object_or_404(Wishlist, id=wishlist_id, user=request.user)
    if request.method == 'POST':
        wishlist_item.delete()
    return redirect('wishlist:wishlist_view')


@login_required
def favorite_stores_view(request):
    favorite_stores = FavoriteStore.objects.filter(user=request.user).select_related('seller')
    return render(request, 'wishlist/favorite_stores.html', {'favorite_stores': favorite_stores})


@login_required
def add_favorite_store(request, seller_id):
    FavoriteStore.objects.get_or_create(user=request.user, seller_id=seller_id)
    return redirect('wishlist:favorite_stores_view')


@login_required
def remove_favorite_store(request, favorite_store_id):
    favorite_store = get_object_or_404(FavoriteStore, id=favorite_store_id, user=request.user)
    if request.method == 'POST':
        favorite_store.delete()
    return redirect('wishlist:favorite_stores_view')
