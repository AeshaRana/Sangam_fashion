from django.shortcuts import render,get_object_or_404, redirect
from .models import Product,ReviewRating
from category.models import Category
from django.db.models import Q
from carts.models import CartItem
from carts.views import _cart_id
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from django.http import HttpResponse
from django.db.models import Q
from django.urls import reverse
from .forms import ReviewForm
from django.contrib import messages
from orders.models import OrderProduct
# Create your views here.



# def store(request, category_slug=None):
#     categories = None
#     products = None

#     men_checked = request.GET.get('men') == '1'
#     women_checked = request.GET.get('women') == '1'
#     kids_checked = request.GET.get('kids') == '1'

    

#     if category_slug:
#         categories = get_object_or_404(Category, slug=category_slug)
#         filter_conditions = {'category': categories}
#         if men_checked:
#             filter_conditions['men'] = True
#         if women_checked:
#             filter_conditions['women'] = True
#         if kids_checked:
#             filter_conditions['kids'] = True
#         products = Product.objects.filter(**filter_conditions).order_by('-id')
#         paginator=Paginator(products,6)
#         page=request.GET.get('page')
#         paged_products=paginator.get_page(page)

#     else:
#         filter_conditions = {}
#         if men_checked:
#             filter_conditions['men'] = True
#         if women_checked:
#             filter_conditions['women'] = True
#         if kids_checked:
#             filter_conditions['kids'] = True
#         products = Product.objects.filter(**filter_conditions).order_by('-id')
#         paginator=Paginator(products,6)
#         page=request.GET.get('page')
#         paged_products=paginator.get_page(page)

#     product_count = products.count()

#     context = {
#         'products': paged_products,
#         'product_count': product_count,
         
#     }

#     return render(request, 'store/store.html', context)

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Category, Product

def store(request, category_slug=None):
    categories = None
    products = None

    men_checked = request.GET.get('men') == '1'
    women_checked = request.GET.get('women') == '1'
    kids_checked = request.GET.get('kids') == '1'

    filter_conditions = {}

    if men_checked:
        filter_conditions['men'] = True
    if women_checked:
        filter_conditions['women'] = True
    if kids_checked:
        filter_conditions['kids'] = True

    if category_slug:
        categories = get_object_or_404(Category, slug=category_slug)
        filter_conditions['category'] = categories

    products = Product.objects.filter(**filter_conditions).order_by('-id')

    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    paged_products = paginator.get_page(page_number)

    product_count = products.count()

    context = {
        'products': paged_products,
        'product_count': product_count,
        'category_slug': category_slug,  # Pass the category_slug to the template
        'men_checked': men_checked,      # Pass the men_checked value to the template
        'women_checked': women_checked,  # Pass the women_checked value to the template
        'kids_checked': kids_checked     # Pass the kids_checked value to the template
    }

    return render(request, 'store/store.html', context)


    return render(request, 'store/store.html', context)


def product_detail(request,category_slug,product_slug):
    try:
        single_product=Product.objects.get(category__slug=category_slug,slug=product_slug)
        in_cart=CartItem.objects.filter(cart__cart_id=_cart_id(request),product=single_product).exists()
    except Exception as e:
        raise e
    
    if request.user.is_authenticated:
        try:
            orderproduct = OrderProduct.objects.filter(user=request.user,product_id=single_product.id).exists()
        except OrderProduct.DoesNotExist:
            orderproduct=None
    else:
        orderproduct=None
        
    #get the reviews : 
    reviews = ReviewRating.objects.filter(product_id=single_product.id,status=True)


    context={
        'single_product':single_product,
        'in_cart':in_cart,
        'orderproduct':orderproduct,
        'reviews' : reviews,
    }
    return render(request,'store/product_details.html',context)


def search(request):
    if 'keyword' in request.GET:
        keyword=request.GET['keyword']
        if keyword:
            products=Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword) | Q(advance_search__icontains=keyword))
            product_count = products.count()

    # products_in_rows = [products[i:i + 3] for i in range(0, len(products), 3)]
        
    context={
        'products': products,
        # 'products_in_rows':products_in_rows,
        'product_count': product_count,
    }

    return render(request,'store/store.html',context)

# def submit_review(request,product_id):
#     url =request.META.get('HTTP_REFERER')
#     if request.method == 'POST':
#         try:
#             reviews = ReviewRating.objects.get(user__id=request.user.id,product__id=product_id)
#             form = ReviewForm(request.POST,instance=reviews)
#             form.save()
#             messages.success(request,'Thank you ! Your review has been updated .')
#             return redirect(url)

#         except ReviewRating.DoesNotExist:
#             form = ReviewForm(request.POST)
#             if form.is_valid():
#                 data = ReviewRating()
#                 data.subject = form.cleaned_data['subject']
#                 data.rating = form.cleaned_data['rating']
#                 data.review = form.cleaned_data['review']
#                 data.ip = request.META.get('REMOTE_ADDR')
#                 data.product_id=product_id
#                 data.user = request.user.id
#                 data.save()
#                 messages.success(request,"Thank you! Your review has been submitted successfully")
#                 return redirect(url)
               

def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            # Attempt to get an existing review for the user and product
            review = ReviewRating.objects.get(user=request.user, product_id=product_id)
            form = ReviewForm(request.POST, instance=review)
        except ReviewRating.DoesNotExist:
            # If no existing review, create a new one
            form = ReviewForm(request.POST)
        
        if form.is_valid():
            # Save the form data
            review = form.save(commit=False)
            review.product_id = product_id
            review.user = request.user  # Assign the user object, not just the user ID
            review.ip = request.META.get('REMOTE_ADDR')
            review.save()
            messages.success(request, 'Thank you! Your review has been submitted successfully.')
            return redirect(url)
    