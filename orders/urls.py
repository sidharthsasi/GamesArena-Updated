from django.urls import path
from .import views

urlpatterns = [
    path('place_order/',views.place_order,name='place_order'),
    path('confirm_order/',views.confirm_order,name='confirm_order'),
    path('address/',views.address,name='address'),
    # path('paymntslct/',views.paymntslct,name='paymntslct'),
    path('ordrsuccess/',views.ordrsuccess,name='ordrsuccess'),
    path('cashondelivery/<int:val>',views.cashondelivery,name='cashondelivery'),
    path('payments/',views.payments,name='payments'),
    # path('ordr_payment//<int:id>',views.ordr_payment,name='ordr_payment'),
    path('ordercomplete/',views.ordercomplete,name='ordercomplete'),
    # path('order_payment/',views.order_payment,name='order_payment'),
    path('callback/',views.callback,name='callback'),
    path('course_changer/',views.course_changer,name='course_changer'),
    path('paypalsuccess/',views.paypalsuccess,name='paypalsuccess'),
    path('razor_success/',views.razor_success,name='razor_success'),
    path('paymentsuccessfull/',views.paymentsuccessfull,name='paymentsuccessfull'),



    path('razorpay_success/',views.razorpay_success,name='razorpay_success'),
    path('payment/<int:check>',views.ordr_payment,name='payment'),
    path("razorpay/callback/", views.callback),
    path("course", views.course_changer, ),


    # path('print_invoice',views.print_invoice,name='print_invoice'),


]
