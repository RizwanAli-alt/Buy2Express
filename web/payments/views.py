from django.shortcuts import render, redirect, get_object_or_404
from .models import Payment
from .forms import PaymentForm
from cart_and_orders.models import Order  


def payment_process(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.order = order
            payment.payment_status = 'Completed' if payment.payment_method in ['Card', 'Wallet', 'COD'] else 'Pending'
            payment.save()

        
            if payment.is_successful():
                order.status = 'Paid'
                order.save()

            return redirect('payments:payment_success')
    else:
        form = PaymentForm()

    return render(request, 'payments/payment_form.html', {'form': form, 'order': order})


def payment_success(request):
    return render(request, 'payments/payment_success.html')
