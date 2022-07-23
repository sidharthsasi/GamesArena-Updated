from atexit import register
from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.register,name='register'),
    path('phone_number_verification/', views.phone_number_verification, name='phone_number_verification'),
    path('otp_verification/<int:Phone_number>/', views.otp_verification, name='otp_verification'),
    path('signin/',views.signin,name='signin'),
    path('signout/',views.signout,name='signout'),
    path('otplogin/',views.loginotp,name='otplogin'),
    path('login_otp1/',views.login_otp1,name='login_otp1'),
    path('my_orders/',views.my_orders,name='my_orders'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('userprfl/',views.userprfl,name='userprfl'),
    path('wallet/', views.wallet, name='wallet'),
    path('referel/', views.referel, name='referel'),
    path('refrlcod/', views.refrlcod, name='refrlcod'),
    path('couponshow/', views.couponshow, name='couponshow'),
    path('myordr/',views.myordr,name='myordr'),
    path('canclordr/<int:id>',views.canclordr,name='canclordr'),
    path('returnordr/<int:id>',views.returnordr,name='returnordr'),
    path('edituserprfl/',views.edituserprfl,name='edituserprfl'),
    path('changpswrd/',views.changpswrd,name='changpswrd'),
    path('deleteaddress/<int:id>',views.deleteaddress,name='deleteaddress'),
   
]
