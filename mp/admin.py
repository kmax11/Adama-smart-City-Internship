from django.contrib import admin
from .models import *


# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ('category_name',)}
    list_display = ('category_name', 'slug')

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'birth_date')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Profile, ProfileAdmin)
