from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem, Order
from .forms import CartItemForm, OrderForm
from product_management.models import Product

@login_required
def cart_view(request):
    """View the current user's cart."""
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    return render(request, 'cart_and_orders/cart.html', {'cart': cart, 'cart_items': cart_items})

@login_required
def add_to_cart(request, product_id):
    """Add a product to the user's cart."""
    cart, created = Cart.objects.get_or_create(user=request.user)
    product = get_object_or_404(Product, pk=product_id)
    
    if request.method == 'POST':
        form = CartItemForm(request.POST)
        if form.is_valid():
            cart_item = form.save(commit=False)
            cart_item.cart = cart
            cart_item.product = product
            cart_item.save()
            messages.success(request, f"{product.name} added to cart.")
            return redirect('cart_and_orders:cart_view')
        else:
            messages.error(request, "Error adding product to cart.")
    else:
        form = CartItemForm()
    
    return render(request, 'cart_and_orders/add_to_cart.html', {'form': form, 'product': product})

@login_required
def checkout(request):
    """Checkout the current user's cart."""
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total_price = sum(item.product.price * item.quantity for item in cart_items)
            order.save()
            
            # Save order items
            for item in cart_items:
                order.items.create(
                    product=item.product,
                    variant=item.variant,
                    quantity=item.quantity,
                    price=item.product.price
                )
            # Clear the cart
            cart.clear()
            messages.success(request, "Order placed successfully.")
            return redirect('cart_and_orders:order_success')
        else:
            messages.error(request, "Error processing your order.")
    else:
        form = OrderForm()
    
    return render(request, 'cart_and_orders/checkout.html', {'form': form, 'cart': cart, 'cart_items': cart_items})

@login_required
def order_success(request):
    """Display the order success page."""
    return render(request, 'cart_and_orders/order_success.html')

@login_required
def orders_view(request):
    """View the current user's past orders."""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')  # Adjust field names as per your model
    return render(request, 'cart_and_orders/orders.html', {'orders': orders})
