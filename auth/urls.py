from django.contrib import admin
from django.urls import path, include

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('shop/', include("shop.urls")),
    path('carts/', include("carts.urls")),
    path('orders/',include("order.urls")),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include("mp.urls")),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
