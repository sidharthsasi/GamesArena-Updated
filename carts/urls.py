from . import views
from django.urls import path


urlpatterns = [
    path('add_cart/<int:product_id>/',views.add_cart,name='add_cart'),
    path('',views.cart ,name='cart'),
    path('remove_cart/<int:product_id>/',views.remove_cart,name='remove_cart'),
    path('remove_cart_item/<int:product_id>/',views.remove_cart_item,name='remove_cart_item'),
   
   
    path('update_cart',views.update_cart,name='update_cart'),

    path('buy_now/<int:id>',views.buy_now ,name='buy_now'),
    # path('address/',views.address,name='adrs'),
    path('review_cart',views.review_cart ,name='review_cart'),
    path('cartadd',views.cartadd,name='cartadd'),
    path('cartminus',views.cartminus,name='cartminus'),
    
]
