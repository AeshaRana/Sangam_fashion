from django.urls import path
from . import views

urlpatterns = [
    path('place_order/',views.place_order,name='place_order'),
    path('payments/',views.payments,name='payments'),
    path('order_complete/',views.order_complete,name='order_complete'),
    # cancel order
    path('cancel_order/<str:order_number>/', views.cancel_order, name='cancel_order'),
    path('order_cancelled_success/', views.order_cancelled_success, name='order_cancelled_success'),

    # path('change-order-status/<int:pid>/',views.change_order_status,name="change_order_status"),
    # path('generate_pdf_bill/',views.generate_pdf_bill,name='generate_pdf_bill'),
    path('generate_invoice_pdf/<str:order_number>/', views.generate_invoice_pdf, name='generate_invoice_pdf'),
    path('generate_monthly_report/<int:year>/<int:month>/', views.generate_monthly_report, name='generate_monthly_report'),
    path('generate_datewise_report/<int:year>/<int:month>/<int:day>/', views.generate_datewise_report, name='generate_datewise_report'),
]