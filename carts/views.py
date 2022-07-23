from math import prod
from multiprocessing import context
from operator import imod
from django.http import HttpResponse
from django.shortcuts import redirect,render,get_object_or_404 
from django.contrib.auth.decorators import login_required
from . models import Cart, CartItemm
from store.models import Product
from orders.models import order
from accounts.models import Account, UserProfile
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login
from django.contrib import messages
from carts.models import Coupon
from django.http import JsonResponse
from accounts.models import Wallet
import json

# Create your views here.
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart
 

def add_cart(request, product_id):
    print("111")
    product = Product.objects.get(id=product_id)
    current =request.session.session_key
    print(product_id)
    try:
        cart = Cart.objects.get( cart_id = _cart_id(request))   

    except Cart.DoesNotExist: 
        print("222")
        if request.user.is_authenticated: 
            cart = Cart.objects.create(
             cart_id = _cart_id(request),
             user = request.user.email
          )

        else:
            cart = Cart.objects.create(
                
                cart_id = _cart_id(request),
            )
    cart.save()

    if request.user.is_authenticated:
        print("333")
        try:
            cart_item = CartItemm.objects.get(product=product, user=request.user)
            cart_item.quantity +=1
            cart_item.save()
        except CartItemm.DoesNotExist:
            cart_item = CartItemm.objects.create(
                product = product,
                quantity = 1,
                user = request.user,
                cart = cart,
                
            )
            cart_item.save()
        if CartItemm.objects.filter(user = request.user).exists():
            item =  CartItemm.objects.filter(user = request.user)
            item.update(cart = cart.id)
            if Cart.objects.filter(cart_id = current, user= request.user).exists():
                crt =Cart.objects.get(cart_id = current, user= request.user)
               
            
            if Cart.objects.filter( user= request.user  ).exclude(cart_id = current).exists():
                crt = Cart.objects.filter( user= request.user  ).exclude(cart_id = current)
                crt.delete()
            pass
        


    else:
        try:
            cart_item = CartItemm.objects.get(product=product, cart=cart)
            cart_item.quantity +=1
            cart_item.save()
        except CartItemm.DoesNotExist: 
            cart_item = CartItemm.objects.create(
                product = product,
                quantity = 1,
               
                cart = cart
            )
            cart_item.save()

    return redirect('cart')



def update_cart(request):
   
    if request.method == 'POST':
        prod_id = int(request.POST.get('product_id'))
        if CartItemm.objects.filter(user=request.user , product_id = prod_id ):
            prod_qty = int(request.POST.get('quantity'))
            cart = CartItemm.objects.get(product_id = prod_id , user = request.user)
            cart.quantity = prod_qty
            cart.save()
            return JsonResponse({ 'status': "Updated Successfully"})



def remove_cart(request,product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_item=CartItemm.objects.get(product=product, user=request.user)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item=CartItemm.objects.get(product=product, cart=cart)
    if cart_item.quantity >1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')


def remove_cart_item(request,product_id):
    product = get_object_or_404(Product,id=product_id)
    if request.user.is_authenticated:
        cart_item=CartItemm.objects.get (product=product, user=request.user)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item=CartItemm.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cart')



  
def cart(request,total=0,quantity=0,cart_items=None):


    # grand_total=0
    # try:
    #     if request.user.is_authenticated:
    #         cart_items = CartItemm.objects.filter( user=request.user).order_by('product')

    #     else:
    #         cart = Cart.objects.get(user = request.user)
    #         cart_items = CartItemm.objects.filter(cart=cart)
    #     for cart_item in cart_items:
    #         total += (cart_item.product.offer_price * cart_item.quantity)
    #         quantity += cart_item.quantity
    #     grand_total = grand_total + total

    # except ObjectDoesNotExist:
    #     pass


    # if request.method=="POST":
    #         name = request.POST['coupon']
    #         if len(name) == 0 :
    #             name="none" 
    #         cart_offer = Cart.objects.filter(carts_id = _cart_id(request))
            
    #         if Coupon.objects.filter(coupon_code = name, active=True).exists():
    #             user = request.user
    #             coupon = Coupon.objects.get(coupon_code = name)
    #             offer = coupon.discount
    #             if grand_total > 1500 : 
    #                 price = grand_total - (grand_total*offer / 100)
    #                 print(grand_total)
    #                 cart_items = cart_offer.update(coupon_applied=offer, final_offer_price = price, user=user.email )
    #                 print(offer)
                
    #                 messages.success(request,'Coupon Added Succesfully')
    #             else: 
    #                 messages.error(request,'Sorry   , Coupon Applicable Only for Order above 1500 ')
    #                 context ={ 
    #                 'offer' : offer,
    #                 'grand_total':grand_total,
    #                 'cart_items': cart_items,
    #             }
    #             return render(request,'carts/cart.html',context)
    #         else:
    #             messages.error(request,'No Coupon Available')
                
    #             context = {
                    
    #                 'grand_total':grand_total,
    #                 'cart_items': cart_items,
    #             }
    #             return render(request,'carts/cart.html',context)

    # else:
            
    #         context = {
                
    #             'grand_total':grand_total,
    #             'cart_items': cart_items,
    #             'total' : total,
    #             'quantity' : quantity,
    #             'cart_items':cart_items,
    #         }

    if request.user.is_authenticated:
        
        cart_items = CartItemm.objects.filter(user=request.user).order_by('product')
        
        context = {
            'cart_items' : cart_items,
        }
        return render(request,'carts/cart.html',context)
    else : 

        try: 
            carts = Cart.objects.get(carts_id = _cart_id(request))
            print(carts)
            
            carts.save()

            cart_items = CartItemm.objects.filter( cart = carts)
            
            context = {
                'cart_items' : cart_items,
             }

            return render(request,'carts/cart.html',context)
        except:
            
            pass

            return render(request,'carts/cart.html')


    




def review_cart(request):
 
    if request.user.is_authenticated:
        final_price = 0
        carrt = Cart.objects.filter(user = request.user)
        carrt.final_offer_price = 0
        cart_items = CartItemm.objects.filter(user = request.user)
        for cart_item in cart_items :
            total = (cart_item.product.offer_price * cart_item.quantity)
            final_price = final_price + total
        print(final_price)
        carrt.update(final_offer_price = final_price)
        # if Wallet.objects.filter(user = request.user).exists():
        #     wallet = Wallet.objects.get(user = request.user)
        # else:
        #     wallet = "0"
            
        print("trouble")
        if request.method == 'POST':
            print("something fishy")
            name = request.POST['coupon']
            print(name)
            if len(name) == 0 :
                name="none" 
            cart_offer = Cart.objects.filter(cart_id = _cart_id(request))
            
            if Coupon.objects.filter(coupon_code = name, active=True).exists():
                user = request.user
                coupon = Coupon.objects.get(coupon_code = name)
                offer = coupon.discount
                if final_price > 1500 : 
                    price = final_price - (final_price*offer / 100)
                    print(final_price)
                    cartitem = cart_offer.update(coupon_applied=offer, final_offer_price = price, user=user.email )
                    print(offer)
                
                    messages.success(request,'Coupon Added Succesfully')
                else: 
                    messages.error(request,'Sorry   , Coupon Applicable Only for Order above 1500 ')


                context ={ 
                    'offer' : offer,
                    'final_price':final_price,
                    'cart_items': cart_items,
                }
                return render(request,'carts/reviewcart.html',context)
            else:
                messages.error(request,'No Coupon Available')
                
                context = {
                    
                    'final_price':final_price,
                    'cart_items': cart_items,
                }
                return render(request,'carts/reviewcart.html',context)

        else:
            
            context = {
                
                'final_price':final_price,
                'cart_items': cart_items,
                
            }
            return render(request,'carts/reviewcart.html',context)


    else:
        messages.error(request,'you need to Login !')
        try:
            cart = Cart.objects.get(carts_id = _cart_id(request))
            
            print(cart)
            return render(request,'accounts/signin.html',{'cart':cart})
        except:
            print("omg")
            
            return render(request,'accounts/signin.html')




















def offer_check_function(item):
    product = Product.objects.get(product_name=item)
  
    print("OFFER CHECK ACTIVE")
    if Product.objects.filter(product=product,active=True).exists():
        if product.pro_offer:
            off_total = product.price - product.price*product.pro_offer.discount/100
    else:
        off_total = product.price
        print(off_total)
    return off_total









    # user=Account.objects.get(user=request.user)
    # if user is not None:
    #     login(request, user)
    #     print('LOGIN SUCCESSFUL')
    #     cart = Cart.objects.filter(user=request.user).exists()
    #     print('CART USER GETTING CREATED')
    #     print(cart)
    #     if not cart:
    #         cart        = Cart.objects.create(user=request.user)
    #         cart.save()
    # else:
    #     print('CART USER EXIST')
    #     cart= Cart.objects.get(user=request.user)


    # context = {
    #     'total' : total,
    #     'quantity' : quantity,
    #     'cart_items':cart_items,
    #     'grandtotal': grand_total,
        

    # }
    # return render(request,'cart.html',context)

@login_required()
def buy_now(request,id):
    
    user = request.user
    if CartItemm.objects.filter(user=user).exists:
        items = CartItemm.objects.filter(user=user)

        for item in items:
            item.delete()
    
    product_id = id
    product = Product.objects.get(id=product_id)
    try:
       
        carts = Cart.objects.get(cart_id = _cart_id(request))
    except Cart.DoesNotExist:
       
        carts = Cart.objects.create(
           
            cart_id = _cart_id(request)
        ) 
    
    carts.save()

    if request.user.is_authenticated:
       
        if CartItemm.DoesNotExist:
            cart_item = CartItemm.objects.create(
                product=product,
                quantity = 1,
                cart = carts,
                user = request.user,
                
                
            )
            cart_item.save()

        return redirect('place_order')

    else : 

        messages.error(request,'you need to Login !')
        return redirect('login')




def cartadd(request):
    body = json.loads(request.body)
    product_id = body['product']

    user = request.user
    cart = Cart.objects.get(user=user)
    cartitm = CartItemm.objects.get(cart=cart , product_id = product_id)
    cartitm.quantity += 1
    cartitm.save()
    data = {"quantity":cartitm.quantity,"prod":product_id}
    return JsonResponse(data)


def cartminus(request):
    body = json.loads(request.body)
    product_id = body['product']

    user = request.user
    cart = Cart.objects.get(user=user)
    cartitm = CartItemm.objects.get(cart=cart , product_id = product_id)
    if cartitm.quantity > 1:
        cartitm.quantity -= 1
        cartitm.save()
    data = {"quantity":cartitm.quantity,"prod":product_id}
    return JsonResponse(data)