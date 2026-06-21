from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Review
from product_management.models import Product  # Import the Product model
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count
from django.contrib import messages

@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if Review.objects.filter(product=product, user=request.user).exists():
        messages.info(request, "You've already reviewed this product.")
        return redirect('product_management:product_detail', slug=product.slug)

    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.save()
            messages.success(request, "Thanks for your review!")
            return redirect('product_management:product_detail', slug=product.slug)
    else:
        form = ReviewForm()
    return render(request, 'reviews/review_form.html', {'form': form, 'product': product})


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, pk=review_id, user=request.user)
    if request.method == 'POST':
        product_slug = review.product.slug
        review.delete()
        messages.success(request, "Review deleted.")
        return redirect('product_management:product_detail', slug=product_slug)
    return render(request, 'reviews/review_confirm_delete.html', {'review': review})


def rating_breakdown_api(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = Review.objects.filter(product=product)
    rating_breakdown = reviews.values('rating').annotate(count=Count('rating')).order_by('-rating')
    breakdown = {str(r['rating']): r['count'] for r in rating_breakdown}
    for i in range(1, 6):
        breakdown.setdefault(str(i), 0)
    return JsonResponse({'breakdown': breakdown})
