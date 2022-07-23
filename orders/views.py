from cProfile import Profile
import email
from multiprocessing import context
from django.shortcuts import redirect, render
from django.http import HttpResponse,JsonResponse
from accounts.models import Account,UserProfile
from carts.models import Cart, CartItemm,Coupon,Paymentrazor
from carts.views import _cart_id
from jersey.views import home, product
from orders.models import order
from .forms import OrderForm
import datetime
from store.models import Product
from orders.models import OrderProduct
import json
from .models import Payment, order,RazorPay
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import razorpay
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import JsonResponse
import json
import tempfile


# Create your views here.
@login_required(login_url='signin')
def place_order(request):

    if request.user.is_authenticated:
        cart_items=CartItemm.objects.filter(user=request.user)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items=CartItemm.objects.filter(cart=cart)
    
    cart_count = cart_items.count()
    total = 0
    tax = 0
    quantity=0
    
    for cart_item in cart_items:
        total +=(cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    print(total)

    # adrs = UserProfile.objects.filter(user=request.user)
    # print(adrs)    
    # adr ={
    #     'adrs':adrs
    # }

    val = request.POST.get('selection')
    print(val)

    if request.method == "POST":
        if val == "typeadrs":

            plc = order()
            plc.first_name= request.POST.get('first_name')
            plc.last_name = request.POST.get('last_name')
            plc.email = request.POST.get('email')
            plc.phone = request.POST.get('phone')
            plc.address_line_1 = request.POST.get('addres_line_1')
            plc.address_line_2 = request.POST.get('addres_line_2')
            plc.city = request.POST.get('city')
            plc.state = request.POST.get('state')
            plc.country = request.POST.get('country')
            plc.zip = request.POST.get('zip')
            use = request.user
            print(use)
            user = Account.objects.get(email=use)
            plc.user=user
            print(plc.user)
            print("00000000")
            plc.order_total = total
            plc.ip = request.META.get('REMOTE_ADDR')
       
            order_id_generated = str(int(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
            plc.order_number = order_id_generated
            plc.save()
            print('6')
            request.session['order_id'] = plc.order_number

       
            order_id = plc.order_number
            orders = order.objects.get(user=plc.user,order_number=order_id)
            print("hiiii")
       
            adrs=UserProfile.objects.filter(user=request.user)
            print(order_id)
            plc.save()
        
            context= {
                'orders' : orders,
                'cart_items': cart_items,
                'tax' : tax,
                'total' : total,
                'adrs':adrs,
                'val':val,
            
            }           
         
         
            #generate order number

            # yr = int(datetime.date.today().strftime('%Y'))
            # dt = int(datetime.date.today().strftime('%d'))
            # mt = int(datetime.date.today().strftime('%m'))
            # d = datetime.date(yr,mt,dt)
            # current_date = d.strftime("%Y%m%d")
            # order_number = current_date + str(data.id)
            
            # print("8888")
            # return render(request,'paymenyselect.html',context)
            return redirect(payments)
        else:
            
            add = UserProfile.objects.get(user=request.user)
            # b=request.user.first_name
            # a=add.State


            plc = order()
            plc.first_name= request.user.first_name
            plc.last_name = request.user.last_name
            plc.address_line_1 = add.address_line_1
            plc.address_line_2 = add.address_line_2
            plc.city = add.city
            plc.state = add.State
            plc.country = add.country
            
            use = request.user
            print(use)
            user = Account.objects.get(email=use)
            plc.user=user
            print(plc.user)
           
            plc.order_total = total
            plc.ip = request.META.get('REMOTE_ADDR')
       
            order_id_generated = str(int(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
            plc.order_number = order_id_generated
            plc.save()
            
            request.session['order_id'] = plc.order_number

    #    paypal start
            order_id = plc.order_number
            orders = order.objects.get(user=plc.user,order_number=order_id)
            print("hiiii")
       
            adrs=UserProfile.objects.filter(user=request.user)
            print(order_id)
            plc.save()


            order_id = order.order_number
            print("10101010101")
            print(order_id)
            print(order.order_number)
            orders = order.objects.filter(user=user,order_number=order_id)
            
            request.session['order_id'] = order.order_number
            context = {
                        'order_id' :order_id,
                        'total' : total,
                        'order':order,
                        'cart_items' : cart_items
                        
                    }
            print( total)
            print(cart_items)
            
            return redirect('paypalsuccess')

# end paypal


            order_data      = order.objects.get(user=request.user, is_ordered=False, order_number=order_id)
            adrs            = UserProfile.objects.filter(user=request.user)
            if request.session:
                coupon_id = request.session.get('coupon_id')
                print(coupon_id)
                try:
                    final_price=0
                    deduction=0
                    coupon=None
                    coupon = Coupon.objects.get(id=coupon_id)
                    deduction = coupon.discount_amount(total)
                    final_price = total-deduction
                    print(final_price)
                    grand_total = tax + final_price
                    print(grand_total)
                    print('SHOWNG APPLIED COUPON GRAND TOTAL')
                    
                except:
                    pass
        
            else:
        


                grand_total = grand_total






            razorpay_client = razorpay.Client(
            auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
            print("hoooiiriiririridirir")

            currency = 'INR'
            amount = total

            #create order

            razorpay_order = razorpay_client.order.create(  {"amount": int(amount) * 100, "currency": "INR", "payment_capture": "1"})


            # order id of newly created order.
        
            razorpay_order_id = razorpay_order['id']
            callback_url = 'http://127.0.0.1:8000/orders/razor_success/'  
            print("hiiisisfof")
            print(final_price)  

            context= {
                'orders' : orders,
                'cart_items': cart_items,
                'tax' : tax,
                'total' : total,
                'adrs':adrs,
                'val':val,
                'callback_url' : callback_url,
                'razorpay_order_id' : razorpay_order_id,
                'razorpay_merchant_key' : settings.RAZOR_KEY_ID,
                'razorpay_amount' : amount,
                'currency' : currency ,
                'final_price': final_price,
                'deduction':deduction,
                'coupon': coupon,

            
            }           
         
            razor_model =RazorPay()
            razor_model.order = orders
            razor_model.razor_pay = razorpay_order_id
            razor_model.save()

            return render(request,'orders/paymenyselect.html',context)
        # else:
        #     print("222")
        #     return render (request,'address.html')
    else:
            adrs =UserProfile.objects.filter(user=request.user)
            context = {
                'adrs': adrs

             }

            print("paypal here")
    

            return render (request,'orders/address.html',context)






def confirm_order(request):
   
    total = 0
    quantity = 0
    print('1')
    cart_items = CartItemm.objects.filter(user=request.user)
    cart_count = cart_items.count()

    if (cart_count <= 0):
        print('2')
        return redirect('cart')
    for cart_item in cart_items:
        total += (cart_item.product.offer_price * cart_item.quantity)
        quantity += cart_item.quantity
    total = total + 40

    print('sathyam paray')
    print(total)
    
    global val
    val = request.POST.get("address")
    print(val)
    if request.method == "POST": 
            profile = UserProfile.objects.get(user=request.user,id=val)
            print("inside confirm order")  
            cart_itm = Cart.objects.get(user = request.user)
            cart_itms = Cart.objects.filter(user = request.user)

            if cart_itm.final_offer_price > 0 :
                
                cart_i = cart_itm.final_offer_price  + 40
                print("ENTERING FINAL PRICE")
                print(cart_i)
                cart_itms.final_offer_price = cart_i
                total = cart_itms.final_offer_price
                print(total)
                print("total")
                print("vayyayyeeee")
            else :
                cart_itms.update(final_offer_price = total)



            
            razorpay_client = razorpay.Client(
            auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
            print("hoooiiriiririridirir")

            currency = 'INR'
            amount = total

            #create order

            razorpay_order = razorpay_client.order.create(  {"amount": int(amount) * 100, "currency": "INR", "payment_capture": "1"})


            # order id of newly created order.
        
            razorpay_order_id = razorpay_order['id']
            callback_url = 'http://127.0.0.1:8000/orders/razor_success/'  


            context = {
                        
                        'total' : total,
                        'val': val,
                        'cart_items' : cart_items,
                        'profile' : profile ,
                        'razorpay_order_id' : razorpay_order_id,
                        'razorpay_merchant_key' : settings.RAZOR_KEY_ID,
                        'razorpay_amount' : amount,
                        'currency' : currency ,
                       
                        
                    }
            return render(request,'orders/paymenyselect.html',context)
    else:
            # adrs =UserProfile.objects.filter(user=request.user)
         profile = UserProfile.objects.filter(user = request.user)
        
         if UserProfile.objects.filter(user = request.user).exists():
             profile_avl = 1
         else:
             profile_avl = 0

         print(profile_avl)
       
         if Cart.objects.filter(user=request.user).exists():
            cart_item = Cart.objects.get(user=request.user)
            
            users=cart_item.user
            if cart_item.final_offer_price > 0 :
                total = cart_item.final_offer_price  + 40  
            context = {
                # 'adrs': adrs,
                'total':total,
                'profile' : profile,
                'profile_avl' : profile_avl,
                 }
       
            return render(request,'orders/address.html',context)

          
 

# def paymntslct(request):
#     adrs = UserProfile.objects.filter(user=request.user)
#     if request.method == "POST":
#         if adrs =="typeadrs":
#             adrs2 =order.objects.get(user=request.user)
#             context = {
#                 'adrs2': adrs2
#             }
#         else:
#             context= {
#                 'adrs' : adrs
#             }


    
#     return render (request,'paymenyselect.html',context)


def address(request):
    user = request.user
   
    if request.method == "POST":
      
            first_name = request.POST['fname']
            last_name = request.POST['lname']
            # Phone_number = request.POST['Phone_number']
            Email = request.POST['email']
            # gender = request.POST['gender']
            # house = request.POST['house']
            Address1 = request.POST['addres_line_1']
            Address1 = request.POST['addres_line_1']
            Address2 = request.POST['addres_line_2']
            city = request.POST['city']
            state = request.POST['state']
            country = request.POST['country']
            pin = request.POST['pin']
            pro=UserProfile.objects.create(user=user,first_name=first_name,last_name=last_name,email=Email,address_line_1=Address1,address_line_2=Address2,city=city,State=state,country=country,pin=pin)
            pro.save()

            profile = UserProfile.objects.filter(user = user)
            
            return redirect('confirm_order')

         
    else:
        return render(request,'orders/adr.html')











def cashondelivery(request,val):
    if request.user.is_authenticated:
        cart_items=CartItemm.objects.filter(user=request.user)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items=CartItemm.objects.filter(cart=cart)
    user = request.user
    cart_items = CartItemm.objects.filter(user=user)
    carrt = Cart.objects.get(user=request.user)
    print(carrt)
    profile = UserProfile.objects.get(user=user,id=val)
    countt =1
   
    user = request.user
    first_name = profile.first_name
    last_name = profile.last_name
    address_1 = profile.address_line_1
    address_2 = profile.address_line_2
    city = profile.city
    state = profile.State
    country = profile.country
    state = profile.State
    pin = profile.pin
    order_total =  carrt.final_offer_price
    print(order_total)
    ip = request.META.get('REMOTE_ADDR')
    Order=order.objects.create(user=user,first_name=first_name,
                                last_name=last_name,
                                 address_line_1=address_1,
                                 address_line_2=address_2,city=city,state=state,
                                country=country,zip=pin, 
                                order_total = order_total)
    Order.save()        
    order_id_generated = str(int(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
    Order.order_number = order_id_generated
    Order.save()
    print(Order)
    order_id_generated = str(int(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
    Order.order_number = order_id_generated
    print('6')
    # request.session['order_id'] = Order.order_number
    print("ivdeyano session")
    Order.save()
    order_id = Order.order_number   
    print(order_id)       
    orders = order.objects.get(user=request.user,order_number=order_id)
            
    # request.session['order_id'] = order.order_number
    print("session undoo")
    payment = Payment()
    payment.user = user
    payment.payment_id = order_id
    payment.payment_method = 'COD'
    payment.amount_paid=order.order_total
    print("111111111")
 
    payment.status = 'Pending'
    payment.save()
    Order.payment=payment
    Order.is_ordered =True
    Order.save()
    cart_itm = cart_items

    for item in cart_items:
        order_product = OrderProduct()
        order_product.order = Order
        order_product.payment = payment
        order_product.user = item.user
        order_product.product = item.product
        order_product.quantity =  item.quantity
        order_product.product_price = item.product.price
        order_product.ordered = True
        order_product.save()

        product =  Product.objects.get(id = item.product.id)
        product.stock = product.stock - item.quantity
        print(product.stock)
        print("100000000001")

        if product.stock <=0:
            product.Is_available = False
        product.save()
        item.delete()
    order_product = OrderProduct.objects.filter(user=user,payment = payment )
    print("ivide kittiyo")
    print(order_product)
    total = order.order_total
    if Cart.objects.filter(user=request.user).exists():
            cart_item = Cart.objects.get(user=request.user)
            users=cart_item.user
            if cart_item.final_offer_price > 0 :
                total = cart_item.final_offer_price 
                ct = Cart.objects.filter(user=request.user)
                print("updTE aayoo")
                c = ct.update(final_offer_price=0)

    context ={ 
        'order_product':order_product,
        'cart_itm':cart_itm,
        'order':Order,
        'total': total,    
    }
    return render(request,'orders/ordercomplete.html',context)







def ordr_payment(request,check):
    request.session['check']  = check
    user =request.user
    print(user,'jjjjjjjjjjjjjjjj')
    user_o = Account.objects.get(id=user.id)
    
    request.session['user']  = user_o.id
    cart = Cart.objects.get(user=request.user)
    amount = cart.final_offer_price
        
        
    client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
   
    razorpay_order = client.order.create(
            {"amount": int(amount) * 100, "currency": "INR", "payment_capture": "1"}
        )
    print(razorpay_order['id'])
    payment = Paymentrazor.objects.create(
            user=user_o, total_amount=amount, order_id=razorpay_order['id']
        )
    payment.save()
    return render(
            request,
            "orders/razorpymnt.html",
            {
                "callback_url": "http://" + "127.0.0.1:8000" + "/orders/razorpay/callback/",
                "razorpay_key": settings.RAZOR_KEY_ID,
                "order": payment,
            },
        )



  
@csrf_exempt
def callback(request):
    
    if  request.method == 'POST':
        
        payment_id = request.POST.get("razorpay_payment_id", "")
        
        provider_order_id = request.POST.get("razorpay_order_id", "")
       
        signature_id = request.POST.get("razorpay_signature", "")
        try:
            order = Paymentrazor.objects.get(order_id = provider_order_id)
        except:
            
            # payment_id = json.loads(request.POST.get("error[metadata]")).get("payment_id")
            provider_order_id = json.loads(request.POST.get("error[metadata]")).get(
            "order_id")
           
            order = Paymentrazor.objects.get(order_id=provider_order_id)

            print('going through here')
            return render(request, "callback.html", context={"status": "FAILED"})

        # order.transaction_id = payment_idclient = razorpay.Client(auth=("YOUR_ID", "YOUR_SECRET"))
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        result = client.utility.verify_payment_signature({
        'razorpay_order_id': provider_order_id,
        'razorpay_payment_id': payment_id,
        'razorpay_signature': signature_id
        })

        order.payment_id = payment_id
        order.signature_id = signature_id    
        order.save()
        if result:
        
            order.status = 'ACCEPTED'
            order.save()
            
            return redirect(course_changer)
        else:
            order.status = 'FAILED'
            order.save()
            print('going through here')
            return render(request, "orders/callback.html", context={"status": order.status})
    else:
        print("yyyyyyyyyyyyyyyy")
        payment_id = json.loads(request.POST.get("error[metadata]")).get("payment_id")
        provider_order_id = json.loads(request.POST.get("error[metadata]")).get(
            "order_id"
        )
        order = order.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.status = 'FAILED'
        order.save()
        return render(request, "callback.html", context={"status": order.status})
    

    
def course_changer(request):
    check = request.session.get('check')
    print(check,'ffffffffffffffffffff')
  
    return redirect(razorpay_success)



def razorpay_success(request):
    user = request.user
   
   
    total = 0
    quantity = 0
    
    cart_items = CartItemm.objects.filter(user=user)
    cart_count = cart_items.count()

    if (cart_count <= 0):
        print('111111')
        return redirect('cart')
    for cart_item in cart_items:
        total += (cart_item.product.offer_price * cart_item.quantity)
        quantity += cart_item.quantity
   
    if UserProfile.objects.filter(user= request.user).exists():
            count =1
            profile = UserProfile.objects.get(user=request.user)   
            # id=val
            print(profile)
            user = request.user
            first_name = profile.first_name
            last_name = profile.last_name
            address_1 = profile.address_line_1
            address_2 = profile.address_line_2
            city = profile.city
            state = profile.State
            country = profile.country
            state = profile.State
            pin = profile.pin
   
            order_total = total
            ip = request.META.get('REMOTE_ADDR')
            Order=order.objects.create(user=user,first_name=first_name,
                                         last_name=last_name,
                                         address_line_1=address_1,
                                        address_line_2=address_2,city=city,state=state,
                                         country=country,zip=pin, 
                                        order_total = order_total)
            Order.save()
            
            order_id_generated = str(int(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
            Order.order_number = order_id_generated

            Order.save()
            print(Order)
            order_id_generated = str(int(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
            Order.order_number = order_id_generated

            print('6')
            request.session['order_id'] = Order.order_number

            Order.save()

            order_id = Order.order_number
            print("10101010101")
            print(order_id)
            print(order.order_number)
            orders = order.objects.filter(user=user,order_number=order_id)
            
            request.session['order_id'] = Order.order_number
            print('before')
            order_id = request.session.get('order_id')
            print(order_id)
            print('after')
            Order = order.objects.get(order_number = order_id) #get changed to filter then changed to get wrking
            cart_items = CartItemm.objects.filter(user=request.user)
        
            payment = Payment()
            payment.user = user
            payment.payment_id = order_id
            print(payment.payment_id)
            payment.payment_method = 'RAZORPAY'
            payment.amount_paid=order_total  #Order.order_total changed to order_total
            print("111111111")
            print(order.order_total)
            payment.status = 'COMPLETED'
            payment.save()
            Order.payment=payment
            Order.is_ordered =True
            Order.save()
            for item in cart_items:
                order_product = OrderProduct()
                order_product.order = Order
                order_product.payment = payment
                order_product.user = item.user
                order_product.product = item.product
                order_product.quantity =  item.quantity
                order_product.product_price = item.product.price
                print('item.price')
                order_product.ordered = True
                order_product.save()

                product =  Product.objects.get(id = item.product.id)
                product.stock = product.stock - item.quantity
                print(product.stock)
                print("paypal here")

                if product.stock <=0:
                    product.Is_available = False
                product.save()
        
                print("last ")
                return redirect(paymentsuccessfull)




def paymentsuccessfull(request):
    cart_item = CartItemm.objects.filter(user=request.user)
    order_id = request.session.get('order_id')
    print(order_id)
    order_product = OrderProduct.objects.filter(user=request.user , order_id = order_id)
    print("1234567890")
    cart_itm = cart_item
    Order = order.objects.get(order_number = order_id)
    print(cart_itm)
    cart_item.delete()
    total = Order.order_total
    if Cart.objects.filter(user=request.user).exists():
            cart_item = Cart.objects.get(user=request.user)
            users=cart_item.user
            if cart_item.final_offer_price > 0 :
                total = cart_item.final_offer_price 
                ct = Cart.objects.filter(user=request.user)
                c = ct.update(final_offer_price=0)
    context ={ 
        'order_product':order_product,
        'cart_itm':cart_itm,
        'order':Order,
        'total':total
    }
  
    return render(request,'orders/ordercomplete.html',context)


























def payments(request):
    users  = request.user
    user = Account.objects.get(email=users)
    print(user)
    
    body = json.loads(request.body)
    print('GOING TO ORDER')
    print(body['orderID'])
    orders = order.objects.get(user=user, is_ordered=False, order_number=body['orderID'])
    print(body)
    print(orders)
    print("yessssssssssś")

    payment = Payment(
        user = request.user,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        amount_paid = order.order_total,
        status = body['status'],
    )
    payment.save()
    print("hiiaiosfjoifjo")
    orders.payment = payment
    orders.is_ordered = True
    print('ordersave')
    orders.save()
    
    cart_items = CartItemm.objects.filter(user=request.user)

    # for item in cart_items:
    #     orderproduct = OrderProduct()
    #     orderproduct.order_id = order.id
    #     orderproduct.payment = payment
    #     orderproduct.user_id = request.user.id
    #     orderproduct.product_id = item.product_id
    #     orderproduct.quantity = item.quantity
    #     orderproduct.product_price = item.product.price
    #     orderproduct.ordered = True
    #     orderproduct.save()


    #     cart_item = CartItemm.objects.get(id=item.id)
    #     product_variation = cart_item.variations.all()
    #     orderproduct = OrderProduct.objects.get(id=orderproduct.id)
    #     # orderproduct.variations.set(product_variations)
    #     orderproduct.save()

    for item in cart_items:
       
        OrderProduct.objects.create(
        order = orders,
        product = item.product,
        user = request.user,
        quantity = item.quantity,
        product_price = item.product.price,
        payment = payment,
        ordered = True,
        )
    #decrease the product quantity from product
    orderproduct = Product.objects.filter(id=item.product_id).first()
    orderproduct.stock = orderproduct.stock-item.quantity
    orderproduct.save()




    CartItemm.objects.filter(user=request.user).delete()
    print(order.order_number)
    print(payment.payment_id)
    data={
        'order_number':orders.order_number,
        'transID' :payment.payment_id
    }
    return JsonResponse(data)
  


def ordercomplete(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')


    try:
        orders = order.objects.get(user=request.user, order_number = order_number , is_ordered=True)
        print(orders)
        ordered_product = OrderProduct.objects.filter(order_id=orders.id)
        print(ordered_product)
        payment = Payment.objects.get(payment_id = transID)

        subtotal = 0
        for i in ordered_product:
            subtotal += i.product_price * i.quantity


        context={
            'orders':orders,
            'ordered_product':ordered_product,
            'order_number' : orders.order_number,
            'transID' : payment.payment_id,
            'subtotal' :subtotal,
            'payment' : payment,
        }   

        return render(request,'ordercomplete.html',context)
    except (Payment.DoesNotExist,order.DoesNotExist):
        return redirect(home)



def paypalsuccess(request):
    print("ivide ethiyoooo")
    user = request.user
    order_id = request.session.get('order_id')
    print(order_id)
 
    orders = order.objects.get(order_number = order_id)
    cart_items = CartItemm.objects.filter(user=user)
        
    payment = Payment()
    payment.user = user
    payment.payment_id = order_id
    payment.payment_method = 'PAYPAL'
    payment.amount_paid=order.order_total
    print("111111111")
    print(order.order_total)
    payment.status = 'COMPLETED'
    payment.save()
    order.payment=payment
    order.is_ordered =True
    order.save()
    for item in cart_items:
        order_product = OrderProduct()
        order_product.order = orders
        order_product.payment = payment
        order_product.user = item.user
        order_product.product = item.product
        order_product.quantity =  item.quantity
        order_product.product_price = item.product.price
        print('item.price')
        order_product.ordered = True
        order_product.save()

        product =  Product.objects.get(id = item.product.id)
        product.stock = product.stock - item.quantity
        print(product.stock)
        print("paypal here")

        if product.stock <=0:
            product.Is_available = False
        product.save()
        
    print("last ")
    return JsonResponse({'completed':'success'})


   




@csrf_exempt
def razor_success(request):
    
    transID = request.POST.get('razorpay_payment_id')
    razorpay_order_id = request.POST.get('razorpay_order_id')
    signature = request.POST.get('razorpay_signature')
    current_user = request.user
    print(current_user)
        #transaction details store

    razor = RazorPay.objects.get(razor_pay=razorpay_order_id)
    orders = order.objects.get(order_number = razor)
    print('razor success page')
    payment = Payment()
    payment.user= current_user
    payment.payment_id = transID
    payment.payment_method = "Razorpapy"
    payment.amount_paid = order.order_total
    payment.status = "Completed"
    payment.save()

    orders.payment=payment
    orders.is_ordered = True
    orders.save()

    cart_item = CartItemm.objects.filter(user=current_user)
    
    
    # Invoice Generating by using order_id

    
   
    for item in cart_item:
       
        OrderProduct.objects.create(
        order = orders,
        product = item.product,
        user = current_user,
        quantity = item.quantity,
        product_price = item.product.price,
        payment = payment,
        ordered = True,
        )

        #decreasing products from stock after order

        orderproduct = Product.objects.filter(id=item.product_id).first()
        orderproduct.stock = orderproduct.stock-item.quantity
        orderproduct.save()

        #deleting Cart items after order


        CartItemm.objects.filter(user=current_user).delete()


    orders = order.objects.get(order_number = razor )
    order_product = OrderProduct.objects.filter(order=order)
    transID = OrderProduct.objects.filter(order=order).first()
    context = {
        'orders':orders,
        'order_product':order_product,
        'transID':transID
    }

    return render(request,'orders/ordercomplete.html', context)





def print_invoice(request):
    response = HttpResponse(content_type = 'application/pdf')
    response['Content-Disposition'] = 'inline; attachement; filename=Invoice' +'.pdf'

    response['Content-Transfer-Encoding'] = 'binary'

    order_product = OrderProduct.objects.filter(user=request.user)
    cart_item = CartItemm.objects.filter(user=request.user)
    order_id = request.session.get('order_id')
    print(order_id)
    cart_itm = cart_item
    ordr = order.objects.get(order_number = order_id)
    print(cart_itm)
    cart_item.delete()
    total = order.order_total
    if Cart.objects.filter(user=request.user).exists():
            cart_item = Cart.objects.get(user=request.user)
            users=cart_item.user
            if cart_item.final_offer_price > 0 :
                total = cart_item.final_offer_price 
                ct = Cart.objects.filter(user=request.user)
                ct.update(final_offer_price=0)
    context ={ 
        'order_product':order_product,
        'cart_itm':cart_itm,
        'ordr':ordr,
        'total':total
    }

    html_string = render_to_string('orders/pdf_invoice.html',context)

    html=HTML(string=html_string)

    result = html.write_pdf()

    with tempfile.NamedTemporaryFile(delete=True) as output : 
        output.write(result)
        output.flush()


        output=open(output.name,'rb')

        response.write(output.read())

    return response




# def order_payment(request,check):
#     request.session['check']  = check
#     user =request.user

#     user_o = Account.objects.get(id=user.id)
    
#     request.session['user']  = user_o.id
#     cart = Cart.objects.get(user=request.user)
#     amount = cart.final_offer_price
        
        
#     client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
#     razorpay_order = client.order.create(
#             {"amount": int(amount) * 100, "currency": "INR", "payment_capture": "1"}
#         )
#     print(razorpay_order['id'])
#     payment = Paymentrazor.objects.create(
#             user=user_o, total_amount=amount, order_id=razorpay_order['id']
#         )
#     payment.save()
#     return render(
#             request,
#             "orders/razorpayment.html",
#             {
#                 "callback_url": "http://" + "127.0.0.1:8000" + "/orders/razorpay/callback/",
#                 "razorpay_key": settings.RAZORPAY_KEY_ID,
#                 "order": payment,
#             },
#         )
  



# @csrf_exempt
# def callback(request):
    
#     if  request.method == 'POST':
        
#         payment_id = request.POST.get("razorpay_payment_id", "")
        
#         provider_order_id = request.POST.get("razorpay_order_id", "")
       
#         signature_id = request.POST.get("razorpay_signature", "")
#         try:
#             order = Paymentrazor.objects.get(order_id=provider_order_id)
#         except:
            
#             # payment_id = json.loads(request.POST.get("error[metadata]")).get("payment_id")
#             provider_order_id = json.loads(request.POST.get("error[metadata]")).get(
#             "order_id")
           
#             order = Paymentrazor.objects.get(order_id=provider_order_id)

#             print('going through here')
#             return render(request, "orders/callback.html", context={"status": "FAILED"})

#         # order.transaction_id = payment_idclient = razorpay.Client(auth=("YOUR_ID", "YOUR_SECRET"))
#         client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
#         result = client.utility.verify_payment_signature({
#         'razorpay_order_id': provider_order_id,
#         'razorpay_payment_id': payment_id,
#         'razorpay_signature': signature_id
#         })

#         order.payment_id = payment_id
#         order.signature_id = signature_id    
#         order.save()
#         if result:
        
#             order.status = 'ACCEPTED'
#             order.save()
            
#             return redirect(course_changer)
#         else:
#             order.status = 'FAILED'
#             order.save()
#             print('going through here')
#             return render(request, "orders/callback.html", context={"status": order.status})
#     else:
  
#         payment_id = json.loads(request.POST.get("error[metadata]")).get("payment_id")
#         provider_order_id = json.loads(request.POST.get("error[metadata]")).get(
#             "order_id"
#         )
#         order = order.objects.get(provider_order_id=provider_order_id)
#         order.payment_id = payment_id
#         order.status = 'FAILED'
#         order.save()
#         return render(request, "orders/callback.html", context={"status": order.status})



        
    
# def course_changer(request):
#     check = request.session.get('check')
   
#     return redirect(razorpay_success)





# def razorpay_success(request):
#     user = request.user
#     print(val)
   
#     total = 0
#     quantity = 0
#     print('1')
   
#     cart_items = CartItemm.objects.filter(user=user)
#     cart_count = cart_items.count()

#     if (cart_count <= 0):
#         print('2')
#         return redirect('cart')
#     for cart_item in cart_items:
#         total += (cart_item.product.offer_price * cart_item.quantity)
#         quantity += cart_item.quantity
   
#     if Profile.objects.filter( id = val ).exists():
#             countt =1
#             profile = Profile.objects.get(user=user,id=val)
#             print(profile.house)
#             user = request.user
#             first_name = profile.first_name
#             last_name = profile.last_name
#             phone_number = profile.Phone_number
#             email = user.email
#             town = profile.town
#             house = profile.house
#             country = profile.country
#             state = profile.state
#             zip = profile.zip
#             order_total = total
#             ip = request.META.get('REMOTE_ADDR')
#             order=order.objects.create(user=user,first_name=first_name,last_name=last_name,phone_number=phone_number,town=town,house=house,country=country,state=state,zip=zip,ip=ip, order_total = order_total, email=email)
#             order.save()
            
#             order_id_generated = str(int(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
#             order.order_number = order_id_generated
#             order.save()

#             order_id_generated = str(int(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
#             order.order_number = order_id_generated

#             request.session['order_id'] = order.order_number

#             order.save()

#             order_id = order.order_number
#             print(order_id)
#             print(order.order_number)
#             orders = Order.objects.get(user=user,order_number=order_id)
            
#             request.session['order_id'] = order.order_number
    
#             order_id = request.session.get('order_id')
#             print(order_id)
 
#             order = order.objects.get(order_number = order_id)
#             cart_items = CartItemm.objects.filter(user=user)
        
#             payment = Payment()
#             payment.user = user
#             payment.payment_id = order_id
#             payment.payment_method = 'RAZORPAY'
#             payment.amount_paid=order.order_total

#             payment.status = 'COMPLETED'
#             payment.save()
#             order.payment=payment
#             order.is_ordered =True
#             order.save()
#             for item in cart_items:
#                 order_product = OrderProduct()
#                 order_product.order = order
#                 order_product.payment = payment
#                 order_product.user = item.user
#                 order_product.product = item.product
#                 order_product.quantity =  item.quantity
#                 order_product.product_price = item.product.price
#                 print('item.price')
#                 order_product.ordered = True
#                 order_product.save()

#                 product =  Product.objects.get(id = item.product.id)
#                 product.stock = product.stock - item.quantity
#                 print(product.stock)
#                 print("paypal here")

#                 if product.stock <=0:
#                     product.Is_available = False
#                 product.save()
        
#                 print("last ")
#                 return redirect(paymentsuccessfull)














def ordrsuccess(request):
    return render(request,"orders/success.html")
