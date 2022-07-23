from ast import Pass
import email
from importlib.metadata import packages_distributions
from multiprocessing import context
from pickle import FALSE
from turtle import update
from unicodedata import category
from venv import create
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.models import Account
from accounts.models import Account
import os
import datetime
from carts.models import Cart
from category.models import Category,Category_Offer
from category.forms import category_form
from orders.models import Payment, order,OrderProduct
from store.models import Product
from slugify import slugify
from django.db.models import Sum,Count
from django.db.models.functions import TruncDate
from django.core.paginator import Paginator,EmptyPage
from carts.models import Coupon
from jersey.models import Banner
from django.db.models.functions import ExtractMonth,ExtractDay
import calendar

# Create your views here.

def admin_signin(request):
    
    if request.user.is_authenticated and request.user.is_admin:
        return redirect('adm_dashboard')
    if request.method == "POST":
        username = request.POST.get('useremail')
        password = request.POST.get('password')
        user=authenticate(username=username ,password=password)
        if username == '' and password == '':
            messages.error(request,"Please enter credentials")
            return redirect(admin_signin)
        if user is not None:
            if user.is_admin==True:
                login(request,user)
                return redirect(admin_page)
            else:
                messages.error(request,"You are not authorized")
                return redirect(admin_signin)
        else:
            messages.error(request,"Invalid Username or Password")
            return redirect(admin_signin)
    else:
        return render(request,'admins/admin_signin.html')    
   


@login_required(login_url=admin_signin)   



def admin_user(request):
    user = Account.objects.exclude(is_admin =True).order_by('date_joined')
    return render(request,'admins/users.html', {'users':user})

    

def admin_page(request):
    return render(request,'admins/admin_dashboard.html')






def admin_product(request):
    prod=Product.objects.all()

    p = Paginator(prod,5)

    print('Number of pages')
    print(p.num_pages)

    page_num = request.GET.get('page',1)

    try:

        page = p.page(page_num)
    except EmptyPage:
         page = p.page(1)
    
    context = {
       
        'prod': page ,
        
    }

    return render(request,'admins/admin_product.html',context)



def admin_signout(request):
    logout(request)
    messages.success(request,"logout successfully")
    return redirect(admin_signin)


def block(request,id):
    user = Account.objects.get(pk=id)
    if user.is_active:
        user.is_active= False
    else:
        user.is_active= True
    user.save()
    return redirect(admin_user)



def delete(request,id):
    Account.objects.get(pk=id).delete()
    return redirect(admin_user)



def edit(request,id):
    user = Account.objects.get(pk=id)
    if request.method =="POST":
        username=request.POST['username']
        firstname=request.POST['firstname']
        lastname=request.POST['lastname']
        email=request.POST['email']
        phone=request.POST['phoneno']
        user.username=username
        user.first_name=firstname
        user.last_name=lastname
        user.email=email
        user.phone_number=phone
        user.save()
        
        
        return redirect(admin_user)   
    
    return render(request,'admins/edit.html', {'user':user})



def cart(request):
    return render(request,'admins/admincart.html')



def prodedit(request,id):
    user = Product.objects.get(id=id)
    if request.method =="POST":
        product_name=request.POST.get('name')
        description=request.POST.get('description')
        price=request.POST.get('price')
        stock=request.POST.get('stock')
        category=request.POST.get('category')
        image=request.FILES.get('image')
        image2=request.FILES.get('image2')
        image3=request.FILES.get('image3')
        cate = Category.objects.get(category_name = category)

        user.category_id =cate
        if len(product_name)>0:
            user.product_name=product_name
        if len(description)>0:    
            user.description=description
        if len(price)>0:
            user.price=price
        if len(stock)>0:
            user.stock=stock
        
        
        if len(request.FILES)>0:
            user.images =image
       
            user.images2 =image2
        
            user.images3 =image3
        
            user.save()

        return redirect(admin_product)
    user = Product.objects.get(pk=id)
    cate = Category.objects.all()

    return render(request,'admins/prodedit.html', {'user':user, 'cate':cate})


def prodadd(request):
    if request.method == "POST":
        prod = Product()
        prod.product_name = request.POST.get('prodname')
        prod.description = request.POST.get('proddes')
        prod.price = request.POST.get('prodprice')
        prod.stock = request.POST.get('prodstock')
        categ     = request.POST.get('prodcat')
        
        prod.slug  = slugify(prod.product_name) 

        if len(prod.product_name) == 0 or len(categ) == 0:
            messages.error(request,'fields cannot be blank')
            return redirect(prodadd)

            
        prod.category = Category.objects.get(id=categ)
        if len(request.FILES) != 0:
            print('IMAGE UPLOADED')
            prod.images = request.FILES.get('images')
            prod.images2 = request.FILES.get('images2')
            prod.images3 = request.FILES.get('images3')

            prod.save()
        
        else:
            messages.error(request, "Please insert an image ")
            print('please insert an image')
            return redirect(prodadd)


        messages.success(request,'Product Added Successfully')
        return redirect(admin_product)
    else:
        cate = Category.objects.all()
        return render(request,'admins/prodadd.html', {'cate': cate})


def proddlt(request,id):
    prd=get_object_or_404(Product,id=id)
    prd.delete()
    return redirect(admin_product)


def cat(request):
    catgry=Category.objects.all()
    return render(request,'admins/admin_cat.html',{'catgry':catgry})


def catdlt(request,id):
   cat=get_object_or_404(Category,id=id)
   cat.delete()
   return redirect(cat)


def addcat(request):
    
    form = category_form(request.POST,request.FILES)
    if form.is_valid():
        print("ffff")
        form.save()
        messages.info(request,'Category added successfully')
        return redirect('cat')
    context = {'form':form}
    return render(request,'admins/addcat.html',context)
   



def admordr(request):
    ordr=order.objects.all().order_by('-created_at')
    
    p = Paginator(ordr,15)

    print('Number of pages')
    print(p.num_pages)

    page_num = request.GET.get('page',1)

    try:

        page = p.page(page_num)
    except EmptyPage:
         page = p.page(1)
    
   
    context={
        'ordr':page
    }
    return render(request,'admins/adminorder.html',context)



def ordrctrl(request,id,val):
    print("hashiuhivbaibiravbavibrbrievab")
    ordr = order.objects.get(id=id)
    ordr.status = val
    ordr.save()    
    return redirect(admordr)



    



def productoffer(request):
    return render(request,'admins/productoffer.html')




def salesreport(request):
    return render(request,'admins/salesreport.html')



def fullreport(request):
    
    salesreports = order.objects.all().order_by('-id')
    
    total = 0
    total= salesreports.aggregate(Sum('order_total'))

    p = Paginator(salesreports,15)

    print('Number of pages')
    print(p.num_pages)

    page_num = request.GET.get('page',1)

    try:

        page = p.page(page_num)
    except EmptyPage:
         page = p.page(1)
    
    context = {
       
        'salesreports': page ,
        'total':    total
    }
    return render(request,'admins/fullreport.html',context)   



def showresult(request):
    orders = order.objects.all()
    if request.method == "POST":
        fromdate =request.POST.get('fromdate')
        todate =request.POST.get('todate')
        if len(fromdate) > 0 and len(todate) > 0 :
            frm = fromdate.split("-")
            tod = todate.split("-")

            fm = [int(x) for x in frm]
            todt = [int(x) for x in tod]
            print(fm)
            print("didnt get table")
                
            salesreports = order.objects.filter(created_at__gte=datetime.date(fm[0],fm[1],fm[2]), created_at__lte=datetime.date(todt[0],todt[1],todt[2])).annotate(day=TruncDate('created_at')).values('day').annotate(count=Count('id')).annotate(sum=Sum('order_total')).order_by('-day')
            print(salesreports)
            p = Paginator(salesreports,15)

            print('Number of pages')
            print(p.num_pages)

            page_num = request.GET.get('page',1)

            try:

                 page = p.page(page_num)
            except EmptyPage:
                 page = p.page(1)
            context = {

                'salesreports' : page ,   

            }
            
         
            return render(request,'admins/salesreport.html',context)

        else:
            salesreports = order.objects.all()
            context = {
                'salesreports': salesreports ,

             }
            return render(request,'admins/salesreport.html',context)

    else:
        salesreports = order.objects.all()
        context = {
            'salesreports': salesreports ,
        

        }
        return render(request,'admins/salesreport.html',context)



def monthlyreport(request,date):
    frmdate = date
    print(frmdate)
    fm = [ 2022 , frmdate , 1 ]
    todt = [2022 , frmdate , 28 ]
    
    print(fm)
            
    salesreports = order.objects.filter(created_at__gte=datetime.date(fm[0],fm[1],fm[2]), created_at__lte=datetime.date(todt[0],todt[1],todt[2])).annotate(day=TruncDate('created_at')).values('day').annotate(count=Count('id')).annotate(sum=Sum('order_total')).order_by('-day')
    p = Paginator(salesreports,10)

    print('Number of pages')
    print(p.num_pages)

    page_num = request.GET.get('page',1)

    try:
      page = p.page(page_num)
    except EmptyPage:
      page = p.page(1)
    
    if len(salesreports) > 0 :   
        context = {
                'salesreports' : page ,   
            }
        print(salesreport)
        print("111")
        return render(request,'admins/salesreport.html',context)
    else:
        messages.error(request,"No Orders")
        return render(request,'admins/salesreport.html')
    


def yearlyreport(request,date):
   
    frmdate = date
    print(frmdate)
    fm = [ frmdate , 1 , 1 ]
    todt = [frmdate , 12 , 30 ]
    
    print(fm)
            
    salesreports = order.objects.filter(created_at__gte=datetime.date(fm[0],fm[1],fm[2]), created_at__lte=datetime.date(todt[0],todt[1],todt[2])).annotate(day=TruncDate('created_at')).values('day').annotate(count=Count('id')).annotate(sum=Sum('order_total')).order_by('-day')
    p = Paginator(salesreports,10)

    print('Number of pages')
    print(p.num_pages)

    page_num = request.GET.get('page',1)

    try:
      page = p.page(page_num)
    except EmptyPage:
      page = p.page(1)
    
    
    if len(salesreports) > 0 :   
        context = {
                'salesreports' : page ,   
            }
        print(salesreport)
        print("111")
        return render(request,'admins/salesreport.html',context)
    else:
        messages.error(request,"No Orders")
        return render(request,'admins/salesreport.html')


def weeklyreport(request,date):
   
    frmdate = date
    print(frmdate)
    fm = [ frmdate , 1 , 1 ]
    
    todt = [frmdate , 12 , 30 ]
    
    print(fm)
            
    salesreports = order.objects.filter(created_at__gte=datetime.date(fm[0],fm[1],fm[2]), created_at__lte=datetime.date(todt[0],todt[1],todt[2])).annotate(day=TruncDate('created_at')).values('day').annotate(count=Count('id')).annotate(sum=Sum('order_total')).order_by('-day')
    if len(salesreports) > 0 :   
        context = {
                'salesreports' : salesreports ,   
            }
        print(salesreport)
        print("111")
        return render(request,'admins/salesreport.html',context)
    else:
        messages.error(request,"No Orders")
        return render(request,'admins/salesreport.html')


def offers(request):

    return render(request,'admins/offers.html')


def productoffer(request):

    if request.method == 'POST':
        search = request.POST["product_search"] 
        context = Product.objects.filter(product_name__icontains = search)
        return render(request,'admins/productoffer.html',{'products': context })
    context= Product.objects.all().order_by('product_name')
    return render( request,'admins/productoffer.html',{'products':context})
   


def productoffer_disable(request,id):

    product_off = Product.objects.get(id=id)
    print(product_off)
    if product_off.Is_offer_active == True:
        product_of = Product.objects.filter(id=id)
        product_of.update(Is_offer_active = False)
    elif product_off.Is_offer_active == False:
        product_of = Product.objects.filter(id=id)
        product_of.update(Is_offer_active = True)
    return redirect('productoffer')



def productoffer_edit(request,id):
    
    product = Product.objects.get(id=id)
    
    if request.method == "POST":
        if Product.objects.filter(id=id).exists():

            offr = Product.objects.filter(id=id)
            print(offr)
            
            print("ivide ethiyooooo")
            offer = request.POST['offers']
            # prices=offr.category
            # print(prices)

            if int(offer) <= 71 and int(offer) >= 0 :
                offr.update(product_offer=offer)
                
                # offr.update(offer_price=prices)
                return redirect('productoffer')
            else :
                messages.error(request,"offer must be between 0% to 70%")
                return render(request,'admins/productofferedit.html',{'product':product, 'id':id})

        else:
            return redirect('product_offer')
    else:
        
        return render(request,'admins/productofferedit.html',{'product':product, 'id':id})







def category_offr(request):

    cat=Category.objects.all().order_by("id")
    
    context={
        'cat':cat
    }

    return render(request,'admins/category_offer.html',context)






def edit_catoffr(request,id):
    cat_id =id
    val = request.POST.get("offer")
    category = Category.objects.get(id = cat_id)
    if request.method == "POST":
        if Category_Offer.objects.filter(category_id=cat_id).exists():
            offr = Category_Offer.objects.filter(category_id=cat_id)
            offer = request.POST['offers']
            if int(offer) <= 71 and int(offer) >= 0 :
                print(offer)
                category = val
                offr.update(discount = offer)
                
                return redirect('category_offr')
            else :
                messages.error(request,"Offer must be between 0% to 70%")
                offr = Category_Offer.objects.get(category_id=cat_id)
                discount = offr.discount
                return render(request,'admins/edit_catoffr.html',{'cat_id':cat_id , 'category':category ,'discount':discount})

        else:
            offer = request.POST['offers']
            print(offer)
            category = val
            offr = Category_Offer.objects.create(category_id=cat_id,category=val,discount = offer)
            offr.save()
            return redirect('category_offr')


    if Category_Offer.objects.filter(category_id=cat_id).exists():
        offr = Category_Offer.objects.get(category_id=cat_id)
        discount = offr.discount
      
        return render(request,'admins/edit_catoffr.html',{'cat_id':cat_id , 'category':category ,'discount':discount})
    else:
        return render(request,'admins/edit_catoffr.html',{'cat_id':cat_id , 'category':category })




def category_offr_disable(request,id):
    
    cat = Category.objects.get(id=id)
    cat_off = Category_Offer.objects.get(category = cat)
    print(cat_off)
    if cat_off.active == True:
        cat_off.active = False
    elif cat_off.active == False:
        cat_off.active = True
    cat_off.save()
    return redirect('category_offr')







def couponlist(request):
    coupons = Coupon.objects.all()
    context={ 
        'coupons':coupons
    }
    return render(request,'admins/couponlist.html',context)





def add_coupon(request):
    if request.method == 'POST':
       
        offer = request.POST.get('discount')
        coupon_code = request.POST.get('coupon_code') 
        valid_from = request.POST.get('valid_from')
        valid_to = request.POST.get('valid_to')

        print(offer)
            
        coupon = Coupon.objects.create(discount = offer, coupon_code = coupon_code, valid_from=valid_from,valid_to=valid_to )
        coupon.save() 
        return redirect('couponlist')
    else : 
        return render(request,'admins/add-coupon.html')





def edit_coupon(request,id):
    coupon_id = id
    if request.method == 'POST':
        if Coupon.objects.filter(id=coupon_id).exists():
            offr = Coupon.objects.filter(id=coupon_id)
            offer = request.POST['discount']
            coupon_code = request.POST['coupon_code']
            valid_from = request.POST['valid_from']
            valid_to = request.POST['valid_to'] 
            print(offer)
            
            offr.update(discount = offer, coupon_code = coupon_code, valid_from=valid_from, valid_to=valid_to )
            
            return redirect('couponlist')
    else:
        coupon = Coupon.objects.get(id=coupon_id)
        context = { 
            'coupon_id' : coupon_id,
            'coupon': coupon
        }
        return render(request,'admins/edit-coupon.html',context)






def disable_coupon(request,id):
    
    coupon = Coupon.objects.get(id=id)
    print(coupon)
    if coupon.active == True:
        coupons = Coupon.objects.filter(id=id)
        coupons = coupons.update(active = False)
        
        return redirect('couponlist')
    
    elif coupon.active == False:
         coupons = Coupon.objects.filter(id=id)
         coupons = coupons.update(active = True)
        
         return redirect('couponlist')




















def adm_dashboard(request):

    orderbyday = order.objects.annotate(day=ExtractDay('created_at')).values('day').annotate(count=Count('id'))
    print(orderbyday)
    dayday =[]
    orderperday =[]
    for o in orderbyday:
        dayday.append(o['day'])
        orderperday.append(o['count'])
    orders = order.objects.annotate(month=ExtractMonth('created_at')).values('month').annotate(count=Count('id')).values('month','count')
    monthNumber = []
    totalOrder = []
    for ord in orders:
        monthNumber.append(calendar.month_name[ord['month']])
        totalOrder.append(ord['count'])



    ordr=order.objects.all()
    revenue=0
    orders = OrderProduct.objects.all()
    for item in orders:
        revenue = revenue + item.product_price

    #total order
    ordercount = order.objects.all().count()

    completed_order = order.objects.filter(status='Completed').count()
    pending_order = order.objects.filter(status='Confirmed').count()
    accepted_order = order.objects.filter(status='Accepted').count()
    cancelled_order = order.objects.filter(status='Cancelled').count()
    returned_order = order.objects.filter(status='Returned').count()
    order_status = []
    order_status.append(completed_order)
    order_status.append(accepted_order)
    order_status.append(pending_order)
    order_status.append(cancelled_order)
    order_status.append(returned_order)
    print(order_status)
    recent_order = order.objects.all().order_by('-created_at')[:5]
    orders_list = order.objects.all().order_by('-id')
    active_users = Account.objects.all().count()
    order_count = order.objects.all().count()
    paymt=Payment.objects.all()

    context= {
        'ordr': ordr,
        'ordercount': ordercount,
        'order_status':order_status,
        'recent_order':recent_order,
        'orders_list':orders_list,
        'active_users':active_users,
        'order_count':order_count,
        'revenue':revenue,
        'paymt':paymt,
        'monthNumber':monthNumber,
        'totalOrder':totalOrder,
        'dayday':dayday,
        'orderperday':orderperday,
        
    }

    return render(request,'admins/admin_dashboard.html',context)





@login_required(login_url=admin_signin)  
def banner(request):
    bannr = Banner.objects.all()
    return render(request,'admins/banner.html',{'bannr':bannr})


@login_required(login_url=admin_signin)  
def add_banner(request):
    if request.method == "POST":
        banr=Banner()
        if len(request.FILES) != 0:
            print('IMAGE UPLOADED')
            banr.banner_image = request.FILES.get('image')
            banr.save()
            return redirect('banner')
    else:
        
        return render(request,'admins/addbanner.html')




@login_required(login_url=admin_signin)  
def select_banner(request,id):
    bannr = Banner.objects.all()
    bannr.update(is_selected = False )
    banners = Banner.objects.filter(id = id)
    banners.update(is_selected = True)
    return redirect('banner')



def deselect_banner(request,id):
    bannr = Banner.objects.all()
    bannr.update(is_selected = True )
    banners = Banner.objects.filter(id = id)
    banners.update(is_selected = False)
    return redirect('banner')




@login_required(login_url=admin_signin)  
def remove_banner(request , id):
    bannr = Banner.objects.filter(id= id)
    bannr.delete()
    return redirect(banner)










def hii(request):
    return render(request,'admins/sample.html')



def hoii(request,id,val):
    return render(request,'admins/hooiiii.html')
   
