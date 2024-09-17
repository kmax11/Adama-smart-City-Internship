from django.db import models
from django.urls import reverse
from django.utils import timezone
from mp.models import *
from django.contrib.auth.models import User

# Create your models here.


class stores(models.Model):
    store_id = models.AutoField(primary_key=True)
    product = models.CharField(max_length=100)
    quantity = models.BigIntegerField()
    price = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f'{self.product}'

class Product(models.Model):
    product_name = models.CharField(max_length=50)
    slug = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    price = models.IntegerField()
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add= True)
    modified_date = models.DateTimeField(auto_now= True)
    image = models.ImageField(upload_to='products/')

   

    def __str__(self) -> str:
        return f'{self.product_name}'
    def get_url(self):
        return reverse('product_detail', args=[self.slug])
    
class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager,self).filter(variation_category = "color", is_active = True)
    def sizes(self):
        return super(VariationManager,self).filter(variation_category = "size", is_active = True)
variation_category_choice=(
    ('color','color'),
    ('size','size')
)

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100, choices=variation_category_choice)
    variation_value = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    created_date = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return self.variation_value
    objects = VariationManager()




class Dashboard(models.Model):
    total_sales = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_products = models.IntegerField(default=0)
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_customers = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f'Total sales :  {self.total_sales}'
    
    top_selling_products = models.CharField(max_length=255, blank=True)
    date = models.DateField(default=timezone.now)

    def __str__(self) -> str:
        return f'Dashboard for {self.date}'
    

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=1)  # Rating field
    review_text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def str(self):
        return f'{self.user.username} - {self.product.product_name}'

    class Meta:
        unique_together = ('user', 'product')   
