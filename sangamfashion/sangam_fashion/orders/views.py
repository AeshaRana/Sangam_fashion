from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from carts.models import CartItem
from .forms import OrderForm
from .models import Order,Payment,OrderProduct
import datetime
import json
from store.models import Product
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import F


# Generate The Date Wise Report

# views.py

from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .models import Order
import datetime

def generate_datewise_report(request, year, month, day):
    year = int(year)
    month = int(month)
    day = int(day)

    date = datetime.date(year, month, day)
    orders = Order.objects.filter(created_at__date=date)

    context = {'orders': orders, 'date': date}

    template_path = 'orders/datewise_report_template.html'
    template = get_template(template_path)
    html = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="datewise_report_{year}-{month}-{day}.pdf"'
    pisa.CreatePDF(html, dest=response)

    return response



# Generate The Monthly Report

from django.shortcuts import render
from .models import Order, Payment
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import datetime  # Import datetime module to work with dates

def generate_monthly_report(request, year, month):
    # Convert year and month parameters to integers
    year = int(year)
    month = int(month)
    
    # Fetch orders for the specified year and month
    orders = Order.objects.filter(created_at__year=year, created_at__month=month)
    
    # Prepare context to pass to the template
    context = {
        'orders': orders,
    }
    
    # Render the HTML content of the report template
    template = get_template('orders/report.html')
    html = template.render(context)
    
    # Create a PDF file using the HTML content
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="monthly_report_{year}_{month}.pdf"'
    pisa.CreatePDF(html, dest=response)
    
    return response





# PDF
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .models import Order, Payment

def generate_invoice_pdf(request, order_number):
    try:
        order = Order.objects.get(order_number=order_number)
        payment = Payment.objects.get(order=order)

        context = {
            'order': order,
            'payment': payment,
        }

        template_path = 'orders/invoice_template.html'
        template = get_template(template_path)
        html = template.render(context)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="invoice_{order_number}.pdf"'

        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response
    except Order.DoesNotExist:
        return HttpResponse('Order not found')


# Create your views here.

def payments(request):
    body= json.loads(request.body)
    order=Order.objects.get(user=request.user,is_ordered=False,order_number=body['orderID'])
    print(body)
    

    # store transaction details to payment model
    payment=Payment(
        user=request.user,
        payment_id=body['transID'],
        payment_method=body['payment_method'],
        amount_paid=order.order_total,
        status=body['status'],
    )
    payment.save()

    order.payment=payment
    order.is_ordered=True
    order.status='Completed'
    order.save()

    #move the cart items to order Product table

    cart_items = CartItem.objects.filter(user=request.user)

    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()

        cart_item = CartItem.objects.get(id=item.id)
        product_variation = cart_item.variation.all()
        orderproduct = OrderProduct.objects.get(id=orderproduct.id)
        orderproduct.variation.set(product_variation)
        orderproduct.save()


    #Reduce the quantity of the sold products
        
        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()


    #clear the cart
        
    CartItem.objects.filter(user=request.user).delete()

    #send order received email to the customer

    mail_subject="Thankyou for your order."
    message=render_to_string('orders/order_received_email.html',{
            'user': request.user,
            'order':order,
    })
    to_email=request.user.email
    send_email=EmailMessage(mail_subject,message,to=[to_email])
    send_email.send()

    #send order number and transaction id back to onApprove sendData() of payment.html
    
    data={
        'order_number':order.order_number,
        'transID'     : payment.payment_id,
    }
    return JsonResponse(data)

def place_order(request,total=0,quantity=0):
    current_user = request.user

    #If the cart count is less than or equal to zero than redirect back to shop

    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')
    
    grand_total=0
    tax = 0

    for cart_item in cart_items:
        total += (cart_item.product.price*cart_item.quantity)
        quantity += cart_item.quantity
    tax=(2*total)/100
    grand_total=total+tax 

    if request.method == 'POST' :
        form = OrderForm(request.POST)
        if form.is_valid():
            #store all the billing information inside order table : 
            data = Order()
            data.user= current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.city = form.cleaned_data['city']
            data.state = form.cleaned_data['state']
            data.pincode = form.cleaned_data['pincode']
            # data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax =  tax
            data.ip  = request.META.get('REMOTE_ADDR')
            data.save()
            
            #generate order number : 
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d  = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d")  #2024 02 14
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(user=current_user,is_ordered=False,order_number=order_number)
            context = {
                'order' : order,
                'cart_items' : cart_items,
                'total' : total,
                'tax' : tax,
                'grand_total':grand_total,
            }
            return render(request,'orders/payments.html',context)
        
        else:
            return redirect('checkout')
        

def order_complete(request):
    order_number = request.GET.get('order_number') # taking from the url of order_complete .html page
    transID = request.GET.get('payment_id')  # taking from the url of order_complete .html page

    try:
        order = Order.objects.get(order_number=order_number,is_ordered = True)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)

        subtotal = 0
        for i in ordered_products:
            subtotal += i.product_price*i.quantity
        
        payment = Payment.objects.get(payment_id=transID)
        context = {
            'order': order,
            'ordered_products' : ordered_products,
            'order_number' : order.order_number,
            'transID' : payment.payment_id,
            'payment' : payment,
            'subtotal' : subtotal,
        }
        return render(request,'orders/order_complete.html',context)
    
    except(Payment.DoesNotExist,Order.DoesNotExist):
        return redirect('home')


# def change_order_status(request,pid):
#     ordered_products = Order.objects.get(order_number=pid)
#     status=request.GET.get('status')
    
#     if status:
#         ordered_products.status=status
#         ordered_products.save()
#         messages.success(request,"status updated successfully")
#     return render(request,'orders/cancel_order.html')


def cancel_order(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    if request.method == 'POST':
        # Handle cancellation confirmation
        order.status = 'Cancelled'
        order.cancel_date = timezone.now()  # Save cancellation date and time
        order.is_ordered = False
        order.save()


        # Increase the quantity of each product in the order
        for order_product in order.orderproduct_set.all():
            product = order_product.product
            Product.objects.filter(pk=product.pk).update(stock=F('stock') + 1)

       
        # Redirect to a success page or appropriate URL
        return redirect('order_cancelled_success')  # Adjust as needed
    return render(request, 'orders/cancel_order.html', {'order': order})

def order_cancelled_success(request):
    return render(request, 'orders/confirm_cancel_order.html')