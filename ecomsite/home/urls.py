from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('',views.home),
    path('products/<pid>',views.viewproduct),
    path('cartfilter/<cid>',views.catfilter),
    path('sort/<sid>',views.sort),
    path('register/',views.registration),
    path('Login/',views.user_login),
    path('logout/',views.user_logout),
    path('addtocart/<pid>',views.addtocart),
    path('viewcart',views.viewcart),
    path('remove/<cid>',views.removeFromCart),
    path('update/<qv>/<cid>',views.updateqty),
    path('placeorder',views.placeorder),
    path('pay',views.pay),
    path('range',views.range),
    path('senduseremail/',views.senduseremail)



]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)