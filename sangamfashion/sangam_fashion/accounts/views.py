from django.shortcuts import render,redirect,get_object_or_404
from .forms import RegistrationForm,UserForm,UserProfileForm
from .models import Account,UserProfile
from django.contrib import messages,auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile

#verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

from carts.models import Cart,CartItem
from carts.views import _cart_id
from wishlist.models import Wishlist,WishlistItem
from wishlist.views import _wishlist_id
from orders.models import Order,OrderProduct
import requests



# Create your views here.

def register(request):
    if request.method =='POST':
        form=RegistrationForm(request.POST)
        if form.is_valid():
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            email=form.cleaned_data['email']
            phone_number=form.cleaned_data['phone_number']
            password=form.cleaned_data['password']
            username=email.split("@")[0]

            user=Account.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username,password=password)
            user.phone_number=phone_number
            user.save()

            #user activation
            current_site=get_current_site(request)
            mail_subject="please activate your account."
            message=render_to_string('accounts/account_verification_email.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),

            })
            to_email=email
            send_email=EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
            # messages.success(request,'Thank you for registering with us we have sent you an verification email to email id please verify it..!')
            return redirect('/accounts/login/?command=verification&email='+email)

            

    else:
        form=RegistrationForm()
    
    context={
        'form':form,

    }
    return render(request,'accounts/register.html',context)





def login(request):
    if request.method == 'POST':
        email=request.POST['email']
        password=request.POST['password']

        user=auth.authenticate(email=email,password=password)

        if user is not None:
            try:
                cart=Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists=CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item=CartItem.objects.filter(cart=cart)

                    #Product Variation by cart id  
                    product_variation=[]
                    for item in cart_item:
                        variation = item.variation.all()
                        product_variation.append(list(variation))

                    # Get The Cart Items from the user To Access his product variations
                    cart_item=CartItem.objects.filter(user=user)
                        
                    ex_var_list=[]
                    id=[]
                    for item in cart_item:
                            existing_variation=item.variation.all()
                            ex_var_list.append(list(existing_variation))
                            id.append(item.id)

                    for pr in product_variation:
                        if  pr in ex_var_list:
                              index=ex_var_list.index(pr)
                              item_id=id[index]
                              item=CartItem.objects.get(id=item_id)
                              item.quantity+=1
                              item.user=user
                              item.save()  
                        else:
                            cart_item=CartItem.objects.filter(cart=cart)
                            for item in cart_item:
                                item.user=user
                                item.save()
                        
                    
            except:
                pass

            try:
                wishlist = Wishlist.objects.get(wishlist_id=_wishlist_id(request))
                is_wishlist_item_exists = WishlistItem.objects.filter(wishlist=wishlist).exists()

                if is_wishlist_item_exists:
                    wishlist_item = WishlistItem.objects.filter(wishlist=wishlist)
                    
                    for item in wishlist_item:
                        # Check if the product is already in the user's wishlist
                        if not WishlistItem.objects.filter(wishlist=wishlist, product=item.product).exists():
                            # Add the product to the user's wishlist
                            new_item = WishlistItem.objects.create(wishlist=wishlist, product=item.product, user=user)
                            new_item.save()
                else:
                    # No wishlist items exist, so no need to check duplicates
                    wishlist_item = WishlistItem.objects.filter(wishlist=wishlist)
                    for item in wishlist_item:
                        item.user = user
                        item.save()
            except Wishlist.DoesNotExist:
                pass

            auth.login(request,user)
            messages.success(request,"You are logged in..")
            url = request.META.get('HTTP_REFERER') #get the previous url
            try:
                query = requests.utils.urlparse(url).query
                #next=/cart/checkout
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)
                
            except:
               return redirect('home')
        else:
            messages.error(request,'Invalid login cridential')
            return redirect('login')

    
    return render(request,'accounts/login.html')



@login_required(login_url='login')
def logout(request):
   auth.logout(request)
   messages.success(request,'You are logged out')
   return redirect('login')


def activate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user =None

    if user is not None and default_token_generator.check_token(user,token):
        user.is_active=True
        user.save()
        messages.success(request,"your account is activated")

        return redirect('login')
    else:
        messages.error(request,'Invalid activation link')
        return redirect('register')
    
    
@login_required(login_url='login')
def dashboard(request):
    orders = Order.objects.order_by('-created_at').filter(user_id=request.user.id,is_ordered=True)
    orders_count = orders.count()
    userprofile = UserProfile.objects.get(user_id=request.user.id)
    context={
        'orders_count':orders_count,
        'userprofile':userprofile,
    }
    return render(request,'accounts/dashboard.html',context)


def forgotPassword(request):
    if request.method == "POST":
        email=request.POST["email"]

        if Account.objects.filter(email=email).exists():
            user=Account.objects.get(email__exact=email)

            #Reset password email
            current_site=get_current_site(request)
            mail_subject="Reset your password."
            message=render_to_string('accounts/reset_password_email.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),

            })
            to_email=email
            send_email=EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()

            messages.success(request,"password reset has been sent to your email address.")
            return redirect ('login')
        else:
            messages.error(request,"Account does not exists.!")
            return redirect('forgotPassword')
        
    return render(request,'accounts/forgotpassword.html')


def resetpassword_validate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user =None

    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid']=uid
        messages.success(request,'Please reset your password')
        return redirect('resetPassword')
    else:
        messages.error(request,'This link has been expired')
        return redirect('login')
    

def resetPassword(request):
    if request.method =="POST":
        password=request.POST['password']
        confirm_password=request.POST['confirm_password']

        if password == confirm_password:
            uid=request.session.get('uid')
            user=Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request,'Your password reseted successfully.')
            return redirect('login')
        else:
            messages.error(request,"Password and confirm password doen't match")
            return redirect('resetPassword')
    else:
        return render(request,'accounts/resetpassword.html')
    



@login_required(login_url='login')
def my_orders(request):
    orders = Order.objects.filter(user=request.user,is_ordered=True).order_by('-created_at') # '-' to get the order in descending order
    context = {
        'orders' : orders,
    }
    return render(request,'accounts/my_orders.html',context)


#fully confirmed
@login_required(login_url='login')
def edit_profile(request):
    userprofile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = request.user  # Ensure the UserProfile is linked to the current user
            profile.save()
            messages.success(request, 'Your profile has been updated')
            return redirect('edit_profile')
        else:
            messages.error(request, 'There was an error updating your profile. Please check the form data.')

    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'userprofile': userprofile,
    }
    return render(request, 'accounts/edit_profile.html', context)


import re

@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = Account.objects.get(username__exact=request.user.username)

        # Password validation rules
        if len(new_password) < 6:
            messages.error(request, 'Password must be at least 6 characters long.')
            return redirect('change_password')
        
        if not re.search("[0-9]", new_password):
            messages.error(request, 'Password must contain at least one digit.')
            return redirect('change_password')
        
        if not re.search("[A-Za-z]", new_password):
            messages.error(request, 'Password must contain at least one letter.')
            return redirect('change_password')
        
        if not re.search("[!@#$%^&*()_+=\-{}[\]:;',.<>?]", new_password):
            messages.error(request, 'Password must contain at least one special character.')
            return redirect('change_password')
        
        if new_password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('change_password')

        # Validate current password
        success = user.check_password(current_password)
        if not success:
            messages.error(request, 'Please enter a valid current password.')
            return redirect('change_password')

        # Update password
        user.set_password(new_password)
        user.save()
        auth.logout(request)
        messages.success(request, 'Password updated successfully.')
        return redirect('change_password')
        
    return render(request, 'accounts/change_password.html')


@login_required(login_url='login')
def order_detail(request,order_id):
    # print("---->",order_id)
    order_detail=OrderProduct.objects.filter(order__order_number=order_id)
    # print(order_detail)
    order=Order.objects.get(order_number=order_id)
    subtotal = 0
    for i in order_detail:
        subtotal +=i.product_price * i.quantity
    context = {
        'order_detail': order_detail,
        'order': order,
        'subtotal':subtotal,
     }
    return render(request,'accounts/order_detail.html',context)



# about us page

def aboutus(request):
   previous_page = request.META.get('HTTP_REFERER')
   context = {
        'previous_page': previous_page
        }
   return render(request,'accounts/aboutus.html',context)


#contact us

def contact(request):
    # previous_page = request.META.get('HTTP_REFERER')
    # if request.method == 'POST':
    #     form = ContactForm(request.POST)
    #     if form.is_valid():
    #         contact = form.save()
    #         subject = 'Thank you for contacting us'
    #         message = f'Dear {contact.name},\nThank you for contacting us. We will get back to you as soon as possible.'
    #         email_from = settings.EMAIL_HOST_USER
    #         email_to = [contact.email, ]
    #         send_mail(subject, message, email_from, email_to)
    #         return redirect('Seeker:index')
    # else:
    #     form = ContactForm()
    return render(request, 'accounts/contactus.html')