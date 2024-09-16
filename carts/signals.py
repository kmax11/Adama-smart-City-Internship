from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import Cart, CartItem

@receiver(user_logged_in)
def assign_cart_items_to_user(sender, request, user, **kwargs):
    cart_id = request.session.session_key
    if not cart_id:
        return

    try:
        cart = Cart.objects.get(cart_id=cart_id)
        cart_items = CartItem.objects.filter(cart=cart)
        for item in cart_items:
            item.user = user
            item.save()
    except Cart.DoesNotExist:
        pass
