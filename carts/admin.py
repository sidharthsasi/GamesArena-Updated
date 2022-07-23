from django.contrib import admin
from .models import Cart,CartItemm,Coupon
# Register your models here.


admin.site.register(Coupon)
admin.site.register(CartItemm)
admin.site.register(Cart)



