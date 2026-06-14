from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Review
from product_management.models import Product  # Import the Product model
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count

# View for Product Detail Page
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = Review.objects.filter(product=product).select_related('user')
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    review_count = reviews.count()
    rating_breakdown = reviews.values('rating').annotate(count=Count('rating')).order_by('-rating')
    breakdown = {str(rating['rating']): rating['count'] for rating in rating_breakdown}
    for i in range(1, 6):
        breakdown.setdefault(str(i), 0)

    context = {
        'product': product,
        'reviews': reviews,
        'average_rating': round(average_rating, 1),
        'review_count': review_count,
        'rating_breakdown': breakdown,
    }
    return render(request, 'reviews/product_detail.html', context)

@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user  
            review.product = product
            review.save()
            return redirect('reviews:product_detail', product_id=product_id)
    else:
        form = ReviewForm()
    return render(request, 'reviews/review_form.html', {'form': form, 'product': product})

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, pk=review_id, user=request.user)
    if request.method == 'POST':
        review.delete()
        return redirect('reviews:product_detail', product_id=review.product_id)
    return render(request, 'reviews/review_confirm_delete.html', {'review': review})

# API endpoint to fetch rating breakdown (optional for AJAX or dynamic updates)
def rating_breakdown_api(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = Review.objects.filter(product=product)
    rating_breakdown = reviews.values('rating').annotate(count=Count('rating')).order_by('-rating')
    breakdown = {str(rating['rating']): rating['count'] for rating in rating_breakdown}
    for i in range(1, 6):
        breakdown.setdefault(str(i), 0)

    return JsonResponse({'breakdown': breakdown})
