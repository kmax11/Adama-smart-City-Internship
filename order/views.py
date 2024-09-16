
import logging

import random
import uuid
from venv import logger

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from auth import settings
from .forms import OrderForm
from .models import Order, OrderProduct
from carts.models import Cart, CartItem
from carts.views import cartIDs
from shop.models import Product
from django.urls import reverse
from django.db import transaction
import requests





@login_required(login_url="login")
def place_order(request, total=0, quantity=0, cart_item=None, carts=0):
    current_user = request.user
    final = 0
    tax = 0
    try:
        cart = Cart.objects.get(cart_id=cartIDs(request))
        cart_item = CartItem.objects.filter(cart=cart, is_active=True)
        
        if request.user.is_authenticated:
            cart_item = cart_item.filter(user=request.user)
            
        for item in cart_item:
            carts += item.quantity
            total += (item.product.price * item.quantity)
        tax = 2 * total / 100
        final = total + tax
    except Cart.DoesNotExist:
        pass

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line1 = form.cleaned_data['address_line1']
            data.address_line2 = form.cleaned_data['address_line2']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.country = form.cleaned_data['country']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = final
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            
            order_number = random.randint(100000, 999999)
            data.order_number = order_number
            data.save()

            return redirect('payment', order_number=order_number)
    else:
        form = OrderForm()

    context = {
        "total": total,
        "quantity": quantity,
        "cart_item": cart_item,
        "final": final,
        "tax": tax,
        "carts": carts,
        'form': form,
    }
    return render(request, "place-order.html", context)

@login_required(login_url="login")
@transaction.atomic
def payment(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    total = 0
    cart_items = CartItem.objects.filter(user=request.user, is_active=True)

    for item in cart_items:
        order_product = OrderProduct()
        order_product.order = order
        order_product.user = request.user
        order_product.product = item.product
        order_product.quantity = item.quantity
        order_product.price = item.product.price
        order_product.is_ordered = True
        order_product.save()
        
        for variation in item.variations.all():
            order_product.variation.add(variation)
        
        total += (item.product.price * item.quantity)

    tax = 2 * total / 100
    final = total + tax
    context = {
        'order': order,
        'total': total,
        'final': final,
        'cart_items': cart_items
    }
    
    return render(request, 'payment.html', context)

@login_required(login_url="login")
def chapa_payment(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    callback_url = request.build_absolute_uri(reverse('chapa_payment_verify'))

    try:
        response = requests.post(
            'https://api.chapa.co/v1/transaction/initialize',headers={'Authorization': f'Bearer {settings.CHAPA_SECRET_KEY}'},
            json={
                'amount': str(order.order_total),
                'currency': 'ETB',
                'email': order.email,
                'first_name': order.first_name,
                'last_name': order.last_name,
                'tx_ref': str(order_number),
                'callback_url': callback_url,
                'return_url': callback_url,
            },
        )

        response_data = response.json()
        logger.debug(f"Chapa response: {response_data}")

        if response_data.get('status') == 'success':
            return redirect(response_data['data']['checkout_url'])
        else:
            return render(request, 'payment_error.html', {'error': response_data['message']})
    except requests.RequestException as e:
        logger.error(f"Chapa payment initialization error: {e}")
        return render(request, 'payment_error.html', {'error': 'Payment initialization failed'})
def chapa_payment_verify(request):
     
    tx_ref = request.GET.get('trx_ref')
    print(tx_ref)
    if tx_ref:
        order = get_object_or_404(Order, order_number=tx_ref)
        order.amount_paid = order.order_total
        order.status = 'completed'
        order.is_ordered = True
        order.save()
        CartItem.objects.filter(user=order.user).delete()
    return render(request, "order_complete.html", {"tx_ref": tx_ref})


