from django.shortcuts import render, redirect, get_object_or_404
from .models import Coupon, Deal, Discount
from .forms import CouponForm, DealForm, DiscountForm
from django.utils import timezone

def deal_list(request):
    deals = Deal.objects.filter(is_active=True, end_date__gte=timezone.now()).order_by('start_date')
    return render(request, 'deals_and_discounts/deal_list.html', {'deals': deals})

def deal_create(request):
    if request.method == 'POST':
        form = DealForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('deals_and_discounts:deal_list')
    else:
        form = DealForm()
    return render(request, 'deals_and_discounts/deal_form.html', {'form': form})

def discount_list(request):
    discounts = Discount.objects.filter(is_active=True, end_date__gte=timezone.now()).order_by('start_date')
    return render(request, 'deals_and_discounts/discount_list.html', {'discounts': discounts})

def discount_create(request):
    if request.method == 'POST':
        form = DiscountForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('deals_and_discounts:discount_list')
    else:
        form = DiscountForm()
    return render(request, 'deals_and_discounts/discount_form.html', {'form': form})

def apply_coupon(request):
    if request.method == 'POST':
        coupon_code = request.POST.get('coupon_code')
        try:
            coupon = Coupon.objects.get(code=coupon_code, active=True, valid_until__gte=timezone.now())
            return render(request, 'deals_and_discounts/apply_coupon_success.html', {'coupon': coupon})
        except Coupon.DoesNotExist:
            return render(request, 'deals_and_discounts/apply_coupon_fail.html', {'error': 'Invalid or expired coupon'})
    return render(request, 'deals_and_discounts/apply_coupon.html')
