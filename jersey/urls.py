
from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.home,name='home'),

    path('products/',views.product,name='products'),
    path('productdtl/<int:id>',views.prddtl,name='productdtl'),  
    path('<slug:category_slug>/',views.product,name='products_by_category'),
    path('cart/<int:id>',views.cart),
]
