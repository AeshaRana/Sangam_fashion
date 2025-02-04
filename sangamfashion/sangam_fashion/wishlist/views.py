from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product
from .models import Wishlist, WishlistItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required 
# Create your views here.



def _wishlist_id(request):
    wishlist = request.session.session_key
    if not wishlist:
        wishlist = request.session.create()
    return wishlist


def add_wishlist(request,product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id) #to get the product

    # if the user is authenticated : 
    if current_user.is_authenticated:
        try:
            wishlist = Wishlist.objects.get(wishlist_id=_wishlist_id(request))
        except Wishlist.DoesNotExist:
            wishlist = Wishlist.objects.create(wishlist_id=_wishlist_id(request))
            pass
    
        is_wishlist_item_exists = WishlistItem.objects.filter(product=product, user=current_user).exists()
    
        if is_wishlist_item_exists:
            wishlist_item = WishlistItem.objects.get(product=product, user=current_user)
            # wishlist_item.quantity += 1  # Increment quantity
            wishlist_item.save()
        else:
            wishlist_item = WishlistItem.objects.create(
                product=product,
                wishlist=wishlist,
                user=current_user
            )

        return redirect('wishlist')

    
    # if the user is authenticated :
    else:
        
        try:
            wishlist = Wishlist.objects.get(wishlist_id=_wishlist_id(request))#to get wishlist using wishlist_id present in the session
        except Wishlist.DoesNotExist:
            wishlist = Wishlist.objects.create(
                wishlist_id=_wishlist_id(request)
            )
        wishlist.save()

        try:
            wishlist_item = WishlistItem.objects.get(product=product,wishlist=wishlist)
            # wishlist_item.quantity += 1 #wishlist_item.quantity = wishlist_item.quantity+1
            wishlist_item.save()
        except WishlistItem.DoesNotExist:
            wishlist_item = WishlistItem.objects.create(
                product = product,
                # quantity = 1,
                wishlist = wishlist,
            )
            wishlist_item.save()
        return redirect('wishlist')
    

def remove_wishlist_item(request,product_id):
    
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        wishlist_item = WishlistItem.objects.get(product=product,user=request.user)
    else:
        wishlist = Wishlist.objects.get(wishlist_id=_wishlist_id(request))
        wishlist_item = WishlistItem.objects.get(product=product,wishlist=wishlist)
    wishlist_item.delete()
    return redirect('wishlist')


@login_required(login_url='login')
def wishlist(request,wishlist_items=None):
    try:
        if request.user.is_authenticated:
            wishlist_items = WishlistItem.objects.filter(user=request.user,is_active=True)

        else:
            wishlist = Wishlist.objects.get(wishlist_id=_wishlist_id(request))
            wishlist_items = WishlistItem.objects.filter(wishlist=wishlist,is_active=True)
        # for wishlist_item in wishlist_items:
        #     total += (wishlist_item.product.price * wishlist_item.quantity)
        #     quantity +=wishlist_item.quantity
    except ObjectDoesNotExist:
        pass #just ignore
    
    context = {
        # 'total' : total,
        # 'quantity' : quantity,
        'wishlist_items' :wishlist_items,
    }
    return render(request,'store/wishlist.html',context)



