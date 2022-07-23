from crypt import methods
import email
from genericpath import exists
from itertools import accumulate
from multiprocessing import context
from unicodedata import name
from django.forms import PasswordInput
from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from jersey.views import home
from orders.models import Payment, order,OrderProduct
from store.models import Product
from .models import Account,Wallet
from .mixins import MessHandler
from twilio.rest import Client
import random
from django.contrib.auth.models import User
from django.contrib import auth
from accounts.models import Account,UserProfile
from orders import models
from django.contrib.auth.hashers import check_password

from carts.views import _cart_id
from carts.models import Cart,CartItemm,Coupon
from django.core.paginator import Paginator,EmptyPage

# Create your views here.


def register(request):

     if request.method == "POST":
        username = request.POST.get('username')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        myuser = Account.objects.create_user(username=username, email=email, password=pass1, first_name=fname,
                                          last_name=lname,phone_number=phone)
        
        myuser.save()

        user_name = myuser
        context = { 
                'user_name':user_name
            }
        return render(request,'accounts/phonenumber_verify.html',context)




        # messages.success(request, "Your account successfully registered")

        # return redirect(signin)

     return render(request,'accounts/register.html')



def phone_number_verification(request):
    user_name = request.GET.get('user_name')
    print(user_name)
    if request.method == 'POST':

        count =0
        phone_number = request.POST['Phone_number']
        phone_no="+91" + phone_number


        for i in phone_number:
            count=count+1

        
        if count == 10 :
            
            if Account.objects.filter(phone_number=phone_number).exists():
                user1= Account.objects.filter(email = user_name)
                user1.delete()
                messages.info(request,'number already exist ! !')
                return redirect('register')
            else:
                # Your Account SID twilio
                account_sid = "AC5a28393fd89fd7b5bb6b7732e04397b0"
                # Your Auth Token twilio
                auth_token  = "cc8f637a9e4d925d4706b6bbd47e507d"

                client = Client(account_sid, auth_token)

               

                verification = client.verify \
                        .services("VA8098d010414b64c73f2534d6c8b20771") \
                        .verifications \
                        .create(to=phone_no,channel='sms')
                print("1234")
                
                context = {
                    'phone_number': phone_number,
                    'user_name':user_name,

                }
                return render (request, 'accounts/phone_verification.html',context)

        
        else :  
            
            if Account.objects.filter(email = user_name).exists():
                user1= Account.objects.filter(email = user_name)
                user1.delete()
                messages.success(request,'entered phone number is not correct !')
                return redirect('register')
           
            else : 
                messages.success(request,'entered phone number is not correct !')
                return redirect('register')

    else : 
            
            messages.success(request,'Please enter correct phone number !')
            return redirect('register')



def otp_verification(request,Phone_number):
    user_name = request.GET.get('name')
    print(Phone_number)
    print(user_name)

    if request.method=='POST':
        fir = request.POST["first"]
        print(fir)
        otp3 =  request.POST['first']+ request.POST['second']+request.POST['third']+request.POST['fourth']
        print(otp3)
       
        phone_no = "+91" + str(Phone_number)

    if request.method=='POST':

        otp_input =  request.POST['first']+ request.POST['second']+request.POST['third']+request.POST['fourth']
        account_sid = "AC5a28393fd89fd7b5bb6b7732e04397b0"
        auth_token = "cc8f637a9e4d925d4706b6bbd47e507d"
        client = Client(account_sid, auth_token)
        verification_check = client.verify \
                                .services("VA8098d010414b64c73f2534d6c8b20771") \
                                .verification_checks \
                                .create(to= phone_no, code= otp_input)
           
        
        if verification_check.status == "approved":
            messages.success(request,"OTP verified successfully.")
            user = Account.objects.get(email=user_name)
            user.is_active = True   
            user.Phone_number = Phone_number        
            user.save()          
            messages.success(request,"registered successfully")
            return redirect ('signin')
        else:
            if Account.objects.filter( username = user_name).exists():
                print("''''''''''''''''''''''''''''")
                user = Account.objects.filter(username = user_name)
                user.delete()
                messages.success(request,"register unsuccessfull")
                return redirect ('register')
            else :
                print("Entering else statementt")
                messages.success(request,"register unsuccessfull")
                return redirect ('register')

    else:
        return render (request, 'accounts/phone_verification.html')








def signin(request):

    if not request.user.is_authenticated:
        if request.method == "POST":
            email = request.POST.get('email')
            pass1 = request.POST.get('pass1')
            
            
            user = authenticate(username=email,password=pass1)


            if user is not None:
                login(request,user)
            
                return redirect(home)
            else:
                messages.error(request, "Bad credentials")
                return redirect(signin)
        else:
            return render(request, "accounts/signin.html")
    else:
        return redirect(home)


    


def loginotp(request):
    if request.method=='POST':
        mobile='9567917717'
        phone_number = request.POST['phone_number']
        if mobile==phone_number:
            #  Account SID twilio
            account_sid = "AC5a28393fd89fd7b5bb6b7732e04397b0"
            #  Auth Token twilio    
            auth_token  = "cc8f637a9e4d925d4706b6bbd47e507d"

            client = Client(account_sid, auth_token)
            global otp
            otp = str(random.randint(1000,9999))
            message = client.messages.create(
                to="+919567917717", 
                from_="'+1 937 932 1563'",
                body="Hello there! Your Login OTP is"+otp)
            messages.success(request,'OTP has been sent & enter OTP')
            return render (request,'otp.html')

        else:
            
            messages.info(request,'invalid mobile number ! !')
            return render (request, 'accounts/otplogin.html')
    
    return render (request,'accounts/otplogin.html')



def login_otp1(request):
    if request.method=='POST':
       
       if Account.objects.filter(phone_number= 9567917717).exists():
          user = Account.objects.get(phone_number= 9567917717)
          otpvalue = request.POST['otp']
          otp=otpvalue
          if len(otpvalue)>0:
             if otpvalue == otp:
                print('123')
                auth.login(request,user)
                messages.success(request,'You are logged in')
                return redirect(home)
             else:   
                messages.error(request,'Invalid OTP')
                return redirect('login_otp1')
          else:
            messages.error(request,'Invalid OTP')
            return redirect('login_otp1')
            
       else:
            messages.error(request,'Invalid OTP')
            return redirect('login_otp1')
    else:
        return render(request, 'accounts/otp.html')

def my_orders(request):
    
    orders =order.objects.filter(user = request.user,is_ordered=True).order_by('-created_at')
    
    context={
        'orders':orders,
    }
    
    return render(request,'myorders.html',context)



@login_required(login_url='signin')
def dashboard(request):
    # print("12223445")
    # if UserProfile.objects.filter(user=request.user).exists():
    #     u=UserProfile.objects.filter(user=request.user)
    #     print(u)
    # else:
    #     print("nnnnnn")
    # orders =order.objects.filter(user = request.user)
    # ordr={
    #     'order':order
    # }
    orders = order.objects.order_by('-created_at').filter(user_id=request.user.id,is_ordered=True)
    orders_count = orders.count()
    adrs=UserProfile.objects.filter(user=request.user)

    context ={
        'orders_count': orders_count,
        'adrs':adrs,
       
    }

    return render(request,'accounts/dashboard.html',context)


def userprfl(request):
     if request.method == "POST":
        prfl = UserProfile()
        prfl.first_name=request.POST.get('fname')
        prfl.last_name=request.POST.get('lname')
        prfl.email=request.POST.get('email')
        prfl.address_line_1 = request.POST.get('addres_line_1')
        prfl.address_line_2 = request.POST.get('addres_line_2')
        prfl.city = request.POST.get('city')
        prfl.State = request.POST.get('state')
        prfl.country = request.POST.get('country')
        prfl.pin = request.POST.get('pin')
        prfl.user=request.user
        prfl.save()
       
        return redirect(dashboard)
     else:
        return render(request,'accounts/usrprfl_adrs.html')

def myordr(request):
    print('hoiiiii')
    ordr=order.objects.all().order_by('-created_at')
    item = CartItemm.objects.filter(user=request.user)

    p=Paginator(ordr,15)
    print('Number of pages')
    print(p.num_pages)

    page_num = request.GET.get('page',1)

    try:

         page = p.page(page_num)
    except EmptyPage:
         page = p.page(1)
   


    context={
        'ordr' : page,
        'item' : item
    }




    




    return render(request,'accounts/myorders.html',context)
  

def canclordr(request,id):
    # messages.warning(request, 'Do you want to cancel order')
    # ordr = order.objects.filter(id=id)
    # ordr.update(status="Cancelled")

    user = request.user
    ordr = order.objects.get(id=id,user=user)
    
    paymnt = ordr.payment.payment_method
    print(paymnt)
    if paymnt == 'COD' : 
        ordr.status = 'Cancelled'
        ordr.save()
    elif paymnt == 'Paypal' or paymnt == 'RAZORPAY' : 
        if Wallet.objects.filter(user = user).exists:
            wallet = Wallet.objects.get(user = user)
            bal = wallet.balance + ordr.order_total
            wallt = Wallet.objects.filter(user = user)
            wallt.update(balance = bal)
            ordr.status = 'Cancelled'
            ordr.save()
        else:
            wallet = Wallet.objects.create(
                user = user,
                balance = ordr.order_total
                )
            
            wallet.save()
            ordr.status = 'Cancelled'
            ordr.save()
    return redirect(myordr)


def returnordr(request,id):
    # messages.warning(request, 'Do you want to cancel order')
    # ordr = order.objects.filter(id=id)
    # ordr.update(status="Cancelled")

    print("hashiuhivbaibiravbavibrbrievab")
    ordr = order.objects.get(id=id)
    ordr.status = "Returned"
    ordr.save()    
    
    return redirect(myordr)


def edituserprfl(request):
    user = UserProfile.objects.filter(user=request.user)
    # prfl = Account.objects.get(email=request.user)
    print(user)
    # print(prfl)
    # val=request.POST.get("selection")
  
    # print(val)
    if request.method == 'POST':
        print("12324")
       
        fname=request.POST['fname']
        lname=request.POST['lname']
        adrs1 = request.POST['address1']
        adrs2 = request.POST['address2']
        city  = request.POST['city']
        state = request.POST['state']
        country  = request.POST['country']
        user.first_name = fname
        user.last_name = lname
        user.address_line_1 = adrs1
        user.address_line_2 = adrs2
        user.city = city
        user.State = state
        user.country = country
        # prfl.save()
        user.update()
        return redirect(dashboard)
    else:
        user = UserProfile.objects.filter(user = request.user)
        # prfl = Account.objects.get(email=request.user)
        context = {
            'user':user,
            # 'prfl':prfl
        }
        return render(request,'accounts/edituserprfl.html',context)
     


def changpswrd(request):
    print("jjjjjj")

    user = Account.objects.get( email = request.user)
    print(user)
    a = request.user.password    
    print(a)
    print(user)
    print("6666")
    if request.method == 'POST':
        oldpswrd = request.POST['oldpaswrd']
        print(oldpswrd)
        newpswrd = request.POST['newpswrd1']
        confrmpswrd = request.POST['newpswrd2']
        pswrd = user.check_password(oldpswrd)
        print(len(newpswrd),newpswrd)

        if newpswrd == confrmpswrd:
            if pswrd:
                print("111")
                user.set_password(newpswrd)
                user.save()
                messages.success(request,'Password changed successfully')
                return redirect('dashboard')

            else:
                messages.error(request,"password doesnt exist !")
                return redirect('changpswrd')
        else:
                messages.error(request,"password doesnt match !")
                return redirect('changpswrd')
    return render(request,'accounts/pswrdchange.html')





def deleteaddress(request,id):
    UserProfile.objects.filter(pk=id).delete()
    return redirect(dashboard)

    

# def coupons(request):
#     coupons = Coupon.objects.filter(active = True)
#     context = {
#         'coupons':coupons
#     }
#     return render(request,'accounts/coupons.html', context)



def signout(request):
    logout(request)
    
    messages.success(request, "logout successfully")
    return redirect('home')

    

    
def order_view(request,id):
    user =  request.user
    if order.objects.filter(id=id).exists():
        orders = order.objects.get(id=id )
        order_items = OrderProduct.objects.filter(order_id=id)
        print(orders)
        print(order_items.count())
        
        context ={
            'order_items':order_items,
            'orders':orders
        }


        return render(request,'orders/order_view_list.html',context)
    else :
        messages.success(request,'no order found')
        return redirect('accounts/my_orders')



def order_cancel(request,id):
    
    user = request.user
    orders = order.objects.get(id=id,user=user)
    
    paymnt = orders.payment.payment_method
    print(paymnt)
    if paymnt == 'COD' : 
        orders.status = 'cancelled'
        orders.save()
    elif paymnt == 'PAYPAL' or paymnt == 'RAZORPAY' : 
        if Wallet.objects.filter(user = user).exists:
            wallet = Wallet.objects.get(user = user)
            bal = wallet.balance + orders.order_total
            wallt = Wallet.objects.filter(user = user)
            wallt.update(balance = bal)
            orders.status = 'cancelled'
            orders.save()
        else:
            wallet = Wallet.objects.create(
                user = user,
                balance = orders.order_total
                )
            
            wallet.save()
            orders.status = 'cancelled'
            orders.save()

    return redirect('accounts/my_orders')



def order_return(request,id):
    user = request.user
    orders = order.objects.get(id=id,user=user)
    orders.status = 'Returned'
    orders.save()
    return redirect('order_view',id)



def wallet(request):
    wl = Wallet.objects.all()
    users = request.user
    wall = 0
    count=0
    wallet = 0
    if Wallet.objects.filter(user = users).exists():
        wallet = Wallet.objects.get(user = users)
    else :
       wall = Wallet.objects.create(user = users)
       wall.save()
    return render(request, 'accounts/wallet.html', {'wallet': wall, 'wallet': wallet, 'wl':wl})



def referel(request):
    user = request.user
    cod = request.POST['code']
    print(cod)
    if user.referel_code != cod :
        print("R")
        if Account.objects.filter(referel_code = cod).exists():
            usr = Account.objects.filter(referel_code = cod)
            print(usr)
            use = Wallet.objects.get(user = user)
            wall = use.balance + 250
            print(wall)
            
            userr = Wallet.objects.filter(user = user)
            userr.update(balance = wall)
            A  = Account.objects.filter(email = user)
            print(A)
            A.update(referel_activated = True)
            messages.success(request,"Referel Successfull. 250 /-  Added to your Wallet, Happy Shopping !")
            return redirect('wallet') 
        else:
        
            print("j")
            messages.error(request,"Referel code is wrong !")
            return redirect('wallet') 
    else:
        print("j")
        messages.error(request,"Referel code is wrong !")
        return redirect('dashboard') 
        

    
def refrlcod(request):
    user = request.user.id
    usr =  Account.objects.get(id=user)
    print(usr)
    context = {
        'usr': usr
    }
    return render(request, 'accounts/referal.html', context)



def couponshow(request):
    cpn=Coupon.objects.all()
    context={
        'cpn':cpn
    }
    return render(request,'accounts/couponshow.html',context)
    