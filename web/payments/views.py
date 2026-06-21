from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import Payment
from .forms import PaymentForm
from cart_and_orders.models import Order


@login_required
def payment_process(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)  # ← ownership check

    if hasattr(order, 'payment') and order.payment.is_successful():
        messages.info(request, "This order has already been paid for.")
        return redirect('payments:payment_success')

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.order = order
            # COD is settled on delivery, not at checkout time
            payment.payment_status = 'Pending' if payment.payment_method == 'COD' else 'Completed'
            payment.save()

            if payment.is_successful():
                order.status = 'Paid'
                order.save(update_fields=['status'])

            messages.success(request, "Payment recorded.")
            return redirect('payments:payment_success')
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = PaymentForm()

    return render(request, 'payments/payment_form.html', {'form': form, 'order': order})


def payment_success(request):
    return render(request, 'payments/payment_success.html')