from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    product_name = models.CharField(max_length=255)
    product_qty = models.IntegerField()
    unit_price = models.IntegerField()
    product_image = models.ImageField(upload_to='products/', blank=True, null=True)
    product_status = models.BooleanField(default=True)
    
class Product_cart(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_qty = models.IntegerField()
    cart_status = models.BooleanField(default=True)
    
    
class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    rating = models.CharField(max_length=100)
    comments = models.TextField()
    
    


    
    
