from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    product_name = models.CharField(max_length=255)
    product_qty = models.IntegerField()
    unit_price = models.IntegerField()
    product_image = models.ImageField(upload_to='products/', blank=True, null=True)
    product_status = models.BooleanField(default=True)
    

    
from django.db import models
from django.contrib.auth.models import User

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    cart_status = models.TextField(default='pending')

    def update_total(self):
        self.total = sum(item.product_total for item in self.cartitems_set.all())
        self.save()

class CartItems(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cartitems_set")
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_qty = models.IntegerField(default=1)
    product_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
        self.product_total = self.product_qty * self.product_id.unit_price
        super().save(*args, **kwargs)
        # Update the cart's total after saving
        self.cart.update_total()

class Order(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    status = models.TextField(default='pending')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    order_at = models.DateTimeField(auto_now_add=True)
    
    
class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    rating = models.CharField(max_length=100)
    comments = models.TextField()

    
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=50)
    message = models.TextField()

class Shipment(models.Model):
    fullname = models.CharField(max_length=100)
    mobile = models.IntegerField()
    pincode = models.IntegerField()
    address1 = models.TextField(max_length=100)
    address2 = models.TextField(max_length=100)
    landmark = models.TextField(max_length=100)
    city = models.TextField(max_length=100)
    state = models.TextField(max_length=100)
    
    
    

           
        

    
    
