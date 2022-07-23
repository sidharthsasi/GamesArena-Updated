from django.urls import path,include
from.import views 


urlpatterns = [


path('',views.admin_signin,name='admin_signin'),
path('hii',views.hii,name='hii'),
path('admin_page/',views.admin_page,name='admpage'),
# path('admin_page/',views.admin_page,name='page'),
path('admin_product',views.admin_product,name='admin_product'),
path('admin_signout',views.admin_signout),
path('admin_user',views.admin_user,name='admin_user'),
path('block/<int:id>',views.block),
path('delete/<int:id>',views.delete),
path('edit/<int:id>',views.edit),
path('cart/',views.cart),

path('prodedit/<int:id>',views.prodedit),
path('prodadd/',views.prodadd,name='prodadd'),
path('proddlt/<int:id>',views.proddlt),

path('cat/',views.cat,name='cat'),
path('catdlt/<int:id>',views.catdlt,name='catdlt'),
path('addcat/',views.addcat,name='addcat'),

path('admordr/',views.admordr,name='admordr'),
path('ordrctrl/<int:id>/<str:val>/',views.ordrctrl,name='ordrctrl'),


path('adm_dashboard',views.adm_dashboard,name='adm_dashboard'),

path('offers',views.offers,name='offers'),
path('productoffer',views.productoffer,name='productoffer'),
path('category_offr_disable/<int:id>',views.category_offr_disable,name='category_offr_disable'),

path('category_offr',views.category_offr,name='category_offr'),
path('edit_catoffr/<int:id>',views.edit_catoffr,name='edit_catoffr'),



path('salesreport',views.salesreport,name='salesreport'),
path('fullreport',views.fullreport,name='fullreport'),
path('showresult',views.showresult,name='showresult'),
path('weeklyreport/<int:date>',views.weeklyreport,name='weeklyreport'),
path('monthlyreport/<int:date>',views.monthlyreport,name='monthlyreport'),
path('yearlyreport/<int:date>',views.yearlyreport,name='yearlyreport'),

path('productoffer',views.productoffer,name='productoffer'),
path('productoffer_disable/<int:id>',views.productoffer_disable,name='productoffer_disable'),
path('productoffer_edit/<int:id>',views.productoffer_edit,name='productoffer_edit'),


path('couponlist',views.couponlist,name='couponlist'),
path('add_coupon',views.add_coupon,name='add_coupon'),
path('edit_coupon/<int:id>',views.edit_coupon,name='edit_coupon'),
path('disable_coupon/<int:id>',views.disable_coupon,name='disable_coupon'),

path('banner',views.banner,name='banner'),
path('add_banner',views.add_banner,name='add_banner'),
path('select_banner/<int:id>',views.select_banner,name='select_banner'),
path('deselect_banner/<int:id>',views.deselect_banner,name='deselect_banner'),
path('remove_banner/<int:id>',views.remove_banner,name='remove_banner'),

]
