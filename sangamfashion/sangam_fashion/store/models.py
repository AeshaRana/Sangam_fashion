from django.db import models
from category.models import Category
from product_filter.models import Product_filter
from django.urls import reverse
from accounts.models import Account
from django.core.validators import MinValueValidator
from django.db.models import Avg,Count

# Create your models here.

# GENDER_CHOICES = [
#         ('M', 'Men'),
#         ('W', 'Women'),
#         ('K', 'Kids')
#     ]

    
class Product(models.Model):
    product_name=models.CharField(max_length=200,unique=True)
    slug=models.SlugField(max_length=200,unique=True)
    description=models.TextField(max_length=500,blank=True)
    advance_search=models.TextField(max_length=500,blank=True)
    price=models.IntegerField(validators=[MinValueValidator(1)])
    images=models.ImageField(upload_to='photos/product')
    stock=models.IntegerField(validators=[MinValueValidator(0)])
    is_avaliable=models.BooleanField(default=False)
    created_date=models.DateTimeField(auto_now_add=True)
    modified_date=models.DateTimeField(auto_now=True)
    brand=models.CharField(max_length=200,blank=True)
    men=models.BooleanField(default=False)
    women=models.BooleanField(default=False)
    kids=models.BooleanField(default=False)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    product_filter=models.ForeignKey(Product_filter,on_delete=models.CASCADE)

    # class Meta:
    #     constraints = [
    #         models.CheckConstraint(check=models.Q(price__gte=0), name="score_gte_0"),
    #     ]

    def get_url(self):
        return reverse('product_detail',args=[self.category.slug,self.slug])
       

    def __str__(self):
        return self.product_name
    
    def averageReview(self):
        reviews = ReviewRating.objects.filter(product=self,status=True).aggregate(average=Avg('rating'))
        avg=0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg
    
    def countReview(self):
        reviews = ReviewRating.objects.filter(product=self,status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:    
            count = int(reviews['count'])            
        return count

# allow us to modify queryset
class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager,self).filter(variation_category='color',is_active=True)
    
    def sizes(self):
        return super(VariationManager,self).filter(variation_category='size',is_active=True)

    

variation_category_choice=(
    ('color','color'),
    ('size','size'),
)
    
class Variation(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    variation_category=models.CharField(max_length=100,choices=variation_category_choice)
    variation_value=models.CharField(max_length=100)
    is_active=models.BooleanField(default=True)
    created_date=models.DateTimeField(auto_now=True)

    objects=VariationManager()


    def __str__(self):
        return self.variation_value

    
   

class ReviewRating(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    subject = models.CharField(max_length=100,blank=True)
    review = models.TextField(max_length=500,blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20,blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject




