from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Customer)
admin.site.register(Burger)
admin.site.register(Order)
admin.site.register(OrderBurger)
admin.site.register(Address)
