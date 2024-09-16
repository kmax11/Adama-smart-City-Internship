from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import Cart, CartItem

@receiver(user_logged_in)
def assign_cart_items_to_user(sender, request, user, **kwargs):
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    try:
        cart = Cart.objects.get(cart_id=session_key)
        cart_items = CartItem.objects.filter(cart=cart, user=None)  # Get items not already assigned to a user
        for item in cart_items:
            item.user = user
            item.save()
    except Cart.DoesNotExist:
        pass
