from django.contrib import admin
from .models import Product, Feedback, Contact, Shipment

admin.site.register(Product)
admin.site.register(Feedback)
admin.site.register(Contact)
admin.site.register(Shipment)
