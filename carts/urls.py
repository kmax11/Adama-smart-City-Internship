from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.cart, name='cart'),
    path('add_cart/<int:product_id>/',views.add_cart,name="add_cart"),
    path('remove_cart/<int:product_id>/<int:cart_item_id>/',views.remove_cart,name="remove_cart"),
    path('remove_cart_item/<int:product_id>/<int:cart_item_id>/',views.remove_cart_item,name="remove_cart_item"),
    path('checkout',views.checkout,name="checkout"),
 
] +  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

