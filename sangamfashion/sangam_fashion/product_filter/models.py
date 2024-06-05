from django.db import models

# Create your models here.
class Product_filter(models.Model):
    filter_name=models.CharField(max_length=50,unique=True)
    slug=models.SlugField(max_length=100,unique=True)


    class Meta:
        verbose_name='product_filter'
        verbose_name_plural='product_filters'

    def __str__(self):
        return self.filter_name
    

