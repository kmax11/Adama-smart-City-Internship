from django.shortcuts import render, get_object_or_404, redirect

from order.models import Order

#from carts.views import cartIDs
from .models import Product, Review
from mp.models import Category
from carts.views import cart, cartIDs
#from carts.views import cartIDs
from carts.models import CartItem
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q


from .forms import ReviewForm
from django.db.models import  Avg

from django.contrib import messages
#from carts.views import get_cart_ids

# Create your views here.

def shop(request, category_slug=None):
    cat = Category.objects.all()
    if category_slug:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True).order_by('id')
        count = products.count()
        paginator = Paginator(products, 1)  
        page = request.GET.get("page")
        paged_products = paginator.get_page(page)
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(products, 8)
        page = request.GET.get("page")
        paged_products = paginator.get_page(page)
        count = products.count()
    return render(request, "shop.html", {"products": paged_products, "count": count, "cat": cat})

def product_detail(request, category_slug, product_slug):
    detail = get_object_or_404(Product, category__slug=category_slug, slug=product_slug)
    in_cart = CartItem.objects.filter(cart__cart_id=cartIDs(request), product=detail).exists()


    # Fetch reviews and calculate average rating
    reviews = Review.objects.filter(product=detail)
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg'] if reviews.exists() else 0

    # Check if the user is logged in and has purchased the product
    can_review = False
    if request.user.is_authenticated:
        has_purchased = Order.objects.filter(user=request.user, orderproduct__product=detail).exists()
        if has_purchased and not Review.objects.filter(user=request.user, product=detail).exists():
            can_review = True

    if request.method == 'POST' and can_review:
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = detail
            review.user = request.user
            review.save()
            messages.success(request, 'Your review has been submitted successfully.')
            return redirect('product_detail', category_slug=category_slug, product_slug=product_slug)
    else:
        form = ReviewForm()

    return render(request, "product-detail.html", {
        "detail": detail,
        "in_cart": in_cart,
        "reviews": reviews,
        "average_rating": average_rating,
        "form": form if can_review else None,
        "can_review": can_review,
        
    })

    return render(request, "product-detail.html", {"detail": detail, "in_cart": in_cart})

def search(request):
    context = {}
    keyword = request.GET.get('keyword')
    
    if keyword:
        products = Product.objects.order_by('created_date').filter(
            Q(product_name__icontains=keyword) | Q(description__icontains=keyword)
        )
        count = products.count()
        
        # Paginate the search results
        paginator = Paginator(products, 3)  # Display 3 products per page
        page = request.GET.get('page')
        try:
            paged_products = paginator.get_page(page)
        except PageNotAnInteger:
            paged_products = paginator.page(1)
        except EmptyPage:
            paged_products = paginator.page(paginator.num_pages)
        
        context = {
            'products': paged_products,
            'count': count,                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
            'keyword': keyword,
        }
    
    return render(request, "shop.html", context)
