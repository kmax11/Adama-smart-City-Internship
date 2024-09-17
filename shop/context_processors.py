#
from .models import Product

def menu_link(request):
    links = Category.objects.all()
    return dict(links=links)
