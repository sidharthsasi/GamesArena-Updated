from cmath import e
from multiprocessing import context
from tkinter import E
from tokenize import single_quoted
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from jersey.models import Banner
from store.models import Product
from category.models import Category,Category_Offer
from django.core.paginator import Paginator,EmptyPage



# Create your views here.
def home(request):
    
    products = Product.objects.all().filter(is_available = True)
    products = Product.objects.all().filter(is_available=True)[:4]
    product_count = products.count()
    banner=Banner.objects.all()
    context = {
        'products' : products,
        'product_count' : product_count,
        'banner' : banner,
    }
    return render(request,'jersey/index.html',context)


def product(request,category_slug=None):
    categories = None
    products = None


    products = Product.objects.all().filter(is_available=True)
    cat_offer = Category_Offer.objects.all()
    
    for cat in cat_offer:
        for product in products: 
            if product.category == cat.category and product.product_offer >=  0 and cat.discount >= 0 and cat.discount <= product.product_offer :
                off =  product.product_offer 
                if off <70 and off > 0 :
                    
                    product.offer_price = product.price-(product.price*off/100)
                    product.offer_perc = product.product_offer
                    product.save()
                else: pass
            elif  product.category == cat.category and product.product_offer >= 0  and cat.discount >= 0  and cat.discount >= product.product_offer :
                if cat.discount < 70 and cat.discount > 0 :
                    product.offer_price = product.price-(product.price*cat.discount/100)

                    product.offer_perc = cat.discount
                    product.save()
            elif product.category != cat.category and product.product_offer > 0 :
                if product.product_offer > 0 and product.product_offer < 70 :
                    product.offer_price = product.price-(product.price*product.product_offer/100)
                    product.save()
            else:
                pass
    

                
    # banners = banner.objects.filter(is_selected =True).order_by('id')
    # user = request.user
    # if user.is_active == True:
    #     cart_count = CartItem.objects.filter(user=request.user,is_active=True).count()
    # else:
    #     cart_count = 0

    # context = {

        
        
    #     'products': products,
    #     'banners':banners,
    #     'cart_count':cart_count,

    # }

    if category_slug != None: 
        categories = get_object_or_404(Category,slug =category_slug)
        # products = Product.objects.all().filter(is_available = True)
        products = Product.objects.filter(category=categories,is_available = True)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True)
        product_count = products.count()
    context = {
        'products' : products,
        'product_count' : product_count,
        'cat_offer':cat_offer,  
    }
    return render(request,'jersey/product.html',context)





def prddtl(request,id):
    try:
        single_product = Product.objects.get(id=id)
        products = Product.objects.all().filter(is_available=True)
    except Exception as e:
        raise e

    print(single_product.product_name)

    return render(request,'jersey/product-detail.html',{'single_product':single_product,'products':products})


def relatedprdct(request):
    products = Product.objects.all()

     
    p = Paginator(products,2)

    print('Number of pages')
    print(p.num_pages)

    page_num = request.GET.get('page',1)

    try:
         page = p.page(page_num)
    except EmptyPage:
         page = p.page(1)
    context = {

        'product' : page ,   

    }


    return render(request,'jersey/product-detail.html',context)


def cart(request):
    return render (request,'cart/cart.html')