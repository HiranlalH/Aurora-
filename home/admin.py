from django.contrib import admin
from .models import Product, Feedback, Product_cart, Contact

admin.site.register(Product)
admin.site.register(Feedback)
admin.site.register(Product_cart)
admin.site.register(Contact)
