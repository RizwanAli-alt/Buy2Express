from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ShippingAddress, OrderTracking, ShippingProvider
from .forms import ShippingAddressForm, OrderTrackingForm, ShippingProviderForm

@login_required
def shipping_address_list(request):
    addresses = ShippingAddress.objects.filter(user=request.user)
    return render(request, 'shipping_and_logistics/address_list.html', {'addresses': addresses})

@login_required
def shipping_address_create(request):
    if request.method == 'POST':
        form = ShippingAddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            return redirect('shipping_and_logistics:shipping_address_list')
    else:
        form = ShippingAddressForm()
    return render(request, 'shipping_and_logistics/address_form.html', {'form': form})

@login_required
def order_tracking_view(request, order_id):
    tracking_details = get_object_or_404(OrderTracking, order__id=order_id)
    return render(request, 'shipping_and_logistics/tracking_details.html', {'details': tracking_details})

@login_required
def add_shipping_provider(request):
    if request.method == 'POST':
        form = ShippingProviderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('shipping_and_logistics:shipping_provider_list')
    else:
        form = ShippingProviderForm()
    return render(request, 'shipping_and_logistics/shipping_provider_form.html', {'form': form})

@login_required
def shipping_provider_list(request):
    providers = ShippingProvider.objects.all()
    return render(request, 'shipping_and_logistics/provider_list.html', {'providers': providers})
