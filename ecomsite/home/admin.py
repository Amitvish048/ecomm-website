from django.contrib import admin
from. models import product,Cart,Order
# Register your models here.
class products_admin(admin.ModelAdmin):
    list_display = ['id','name','price','pdetails','category','is_active']
    
    

admin.site.register(product,products_admin)
admin.site.register(Cart)
admin.site.register(Order)
