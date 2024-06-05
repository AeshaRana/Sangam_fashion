from django.contrib import admin
from .models import Product_filter

# Register your models here.
class Product_filterAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug': ('filter_name',)}
    list_display=('filter_name','slug')

admin.site.register(Product_filter,Product_filterAdmin)
