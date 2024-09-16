from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from shop.models import Product,Variation
from .models import Cart,CartItem
from django.contrib.auth.decorators import login_required
#from shop.views import *
# Create your views here.
def cartIDs(request):
	cart=request.session.session_key
	if not cart:
		cart=request.session.create()
	return cart
def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    product_variation = []

    if request.method == 'POST':
        for item in request.POST:
            key = item
            value = request.POST[key]
            try:
                variation = Variation.objects.get(
                    product=product,
                    variation_category__iexact=key,
                    variation_value__iexact=value
                )
                product_variation.append(variation)
            except Variation.DoesNotExist:
                pass

    # Get or create a cart
    cart, created = Cart.objects.get_or_create(cart_id=cartIDs(request))
    
    is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()

    if is_cart_item_exists:
        cart_item = CartItem.objects.filter(product=product, cart=cart)
        ex_var_list = []
        item_ids = []

        for item in cart_item:
            existing_variation = item.variations.all()
            ex_var_list.append(list(existing_variation))
            item_ids.append(item.id)

        if product_variation in ex_var_list:
            index = ex_var_list.index(product_variation)
            item_id = item_ids[index]
            item = CartItem.objects.get(product=product, id=item_id)
            item.quantity += 1
            item.save()
        else:
            item = CartItem.objects.create(
                product=product,
                cart=cart,
                quantity=1
            )
            if product_variation:
                item.variations.clear()
                item.variations.add(*product_variation)
            item.save()
    else:
        item = CartItem.objects.create(
            product=product,
            cart=cart,
            quantity=1
        )
        if product_variation:
            item.variations.clear()
            item.variations.add(*product_variation)
        item.save()
    cart= Cart.objects.get(cart_id=cartIDs(request))
    #print(cart)
    cart_item=CartItem.objects.filter(cart=cart)
    if request.user.is_authenticated:
         for item in cart_item:
            item.user=request.user
            item.save()
        
        #CartItem.objects.update(user=request.user)
        

    return redirect("cart")
def remove_cart(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id=cartIDs(request))
    product = get_object_or_404(Product, id=product_id)
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        if request.user.is_authenticated and cart_item.user != request.user:
            # Prevent modification of another user's cart item
            return redirect("cart")

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except CartItem.DoesNotExist:
        pass
    return redirect("cart")
def remove_cart_item(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id=cartIDs(request))
    product = get_object_or_404(Product, id=product_id)
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        if request.user.is_authenticated and cart_item.user != request.user:
            return HttpResponse("You do not have permission to modify others item")

            # Prevent modification of another user's cart item
        return redirect("cart")

        cart_item.delete()
    except CartItem.DoesNotExist:
        pass
    return redirect("cart")
def cart(request, total=0, quantity=0, cart_item=None, carts=0):
    final = 0
    tax = 0
    try:
        cart = Cart.objects.get(cart_id=cartIDs(request))
        cart_item = CartItem.objects.filter(cart=cart, is_active=True)
     
            
        for item in cart_item:
            carts += item.quantity
            total += (item.product.price * item.quantity)
        tax = 2 * total / 100
        final = total + tax
    except Cart.DoesNotExist:
        pass

    context = {
        "total": total,
        "quantity": quantity,
        "cart_item": cart_item,
        "final": final,
        "tax": tax,
        "carts": carts,
    }
    return render(request, "cart.html", context)


def checkout(request):
    if request.method == 'POST':
        pass
    else:
        cart_items = CartItem.objects.all()
        return render(request, 'checkout.html', {'cart_items': cart_items})
    return render(request, 'checkout.html')

