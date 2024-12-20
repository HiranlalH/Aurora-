from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Cart, CartItems, Order, Product, Feedback, Contact, Shipment
from django.contrib import messages
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO
from django.utils import timezone
from django.db.models import Sum




def index(request):
    return render(request,"index.html")

def error(request):
    return render(request,"error.html")

def userlogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        print(username)
        print(password)
        print(user)
        if user is not None and user.is_active:
            login(request, user)
            # Check if the user is a super admin (superuser)
            if user.is_superuser:
                # Redirect to super admin dashboard
                return redirect('admin_dashboard')
            else:
                return redirect('index')  # Redirect to user home
        else:
            msg = "Please check the credentials carefully!"
            return render(request, 'userlogin.html', {'msg': msg})

    return render(request, "userlogin.html")

def userreg(request):
    if request.method =="POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email)
            user.set_password(password)
            user.save()
            return render(request, 'userlogin.html')
        else:
            msg = "Username already exists. Try again!"
            return render(request, 'userreg.html', {'msg':msg})
    return render(request,"userreg.html")

def userlogout(request):
    logout(request)
    return redirect('userlogin')

# def admindashboard(request):
#     sold_products = CartItems.objects.filter(cart__order__status='completed').values('product_id').annotate(total_qty_sold=Sum('total'))
#     users = User.objects.all()
#     shipment_details = Shipment.objects.all()
#     orders = Order.objects.all()
#     shipment_count = shipment_details.count()
#     total_orders = orders.count() 
#     user_count = User.objects.exclude(is_staff=True, is_superuser=True).count()  
    
#     return render(request,"admin_dashboard.html",{'users':users,'total_orders':total_orders,'shipment_count':shipment_count,'user_count':user_count,'total_sales':total_sales})


from django.db.models import Sum
from django.contrib.auth.models import User
from .models import Order, CartItems, Shipment

def admindashboard(request):
    # Get the total quantity sold for each product (completed orders only)
    sold_products = CartItems.objects.filter(cart__order__status='completed') \
                                     .values('product_id') \
                                     .annotate(total_qty_sold=Sum('product_qty')) \
                                     .order_by('product_id')

    # Count all users excluding admins
    user_count = User.objects.exclude(is_staff=True, is_superuser=True).count()

    # Count total orders
    total_orders = Order.objects.count()

    # Count total shipments
    shipment_details = Shipment.objects.all()
    shipment_count = shipment_details.count()

    # Calculate the total sales amount (sum of product_total values in CartItems)
    total_sales = CartItems.objects.filter(cart__order__status='completed') \
                                   .aggregate(total_sales=Sum('product_total'))['total_sales'] or 0
                                   
    top_selling = CartItems.objects.values('product_id__product_name') \
                                   .annotate(total_qty_sold=Sum('product_qty')) \
                                   .order_by('-total_qty_sold')[:1]
    least_purchased = CartItems.objects.values('product_id__product_name') \
                                       .annotate(total_qty_sold=Sum('product_qty')) \
                                       .order_by('total_qty_sold')[:1]
    
    # Extract product names from the query result
    least_product_names = [item['product_id__product_name'] for item in least_purchased]
    completed_orders_count = Order.objects.filter(status='completed').count()
    
    
    # Extract product names from the query result
    top_product_names = [item['product_id__product_name'] for item in top_selling]
    users = User.objects.all()
    return render(request, "admin_dashboard.html", {
        'user_count': user_count,
        'total_orders': total_orders,
        'shipment_count': shipment_count,
        'total_sales': total_sales, 
        'top_product_names':top_product_names,
        'least_product_names':least_product_names,
        'completed_orders_count':completed_orders_count,
        'users':users,
    })


def admin_userslist(request):
    shipment_details = Shipment.objects.all()
    return render(request,'admin_users.html',{'shipment_details':shipment_details})
    
def about(request):
    return render(request,"about.html")

def order_history(request, user_id):
    user = User.objects.filter(id = user_id).first()
    user_cart = cart = get_object_or_404(Cart.objects.select_related('user').prefetch_related('cartitems_set'), user=request.user, cart_status='completed')
    print(user_cart)
    return render(request, 'order_history.html', {'cart' : user_cart})


def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        ctat = Contact.objects.create(name = name, email = email, subject = subject, message = message)
        ctat.save()
        return render(request, 'contact.html')
    return render(request,"contact.html")


def feature(request):
    return render(request,"feature.html")


# def products(request):
#     products = Product.objects.all()
#     return render(request, "product.html", {'products': products})


def products(request):
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        return redirect('userlogin')  # Redirect to the login page if the user is not authenticated
    
    # If the user is authenticated, proceed to show the products
    products = Product.objects.all()
    
    return render(request, "product.html", {'products': products})


def add_to_cart(request, p_id):
    user = request.user
    product = Product.objects.get(id=p_id)
    
    # Get or create a cart for the user
    cart, created = Cart.objects.get_or_create(user=user, cart_status='pending')
    
    # Check if the product already exists in the cart
    cart_item, item_created = CartItems.objects.get_or_create(
        cart=cart,
        product_id=product,
        defaults={'product_qty': 1}
    )
    
    if not item_created:
        # If item already exists, update the quantity
        cart_item.product_qty += 1
        cart_item.save()  # `save()` will automatically update `product_total` and cart's total via `update_total`
    
    return redirect('product')



def cart(request):
    # Retrieve the user's active cart
    try:
        cart = Cart.objects.get(user=request.user, cart_status='pending')
    except Cart.DoesNotExist:
        cart = None
    
    cart_data = []
    total_amount = 0

    if cart:
        # Retrieve the items in the cart
        cart_items = CartItems.objects.filter(cart=cart)
        for item in cart_items:
            item_total = item.product_id.unit_price * item.product_qty
            cart_data.append({
                'product_name': item.product_id.product_name,
                'unit_price': item.product_id.unit_price,
                'quantity': item.product_qty,
                'item_total': item_total,
            })
            total_amount += item_total

    return render(request, 'cart.html', {
        'cart': cart_data,
        'total_amount': total_amount,
    })


def checkout(request):
    try:
        cart = Cart.objects.get(user=request.user, cart_status='pending')
    except Cart.DoesNotExist:
        cart = None

    cart_data = []
    total_amount = 0

    if cart:
        cart_items = CartItems.objects.filter(cart=cart)
        for item in cart_items:
            item_total = item.product_id.unit_price * item.product_qty
            cart_data.append({
                'product_name': item.product_id.product_name,
                'unit_price': item.product_id.unit_price,
                'quantity': item.product_qty,
                'item_total': item_total,
            })
            total_amount += item_total

    return render(request, 'checkout.html', {
        'cart': cart_data,
        'total_amount': total_amount,
    })


def payment(request):
    try:
        cart = Cart.objects.get(user=request.user, cart_status='pending')
    except Cart.DoesNotExist:
        return redirect('checkout')  # Redirect to checkout if there's no active cart

    total_amount = cart.total
    cart_data = []
    
    cart_items = CartItems.objects.filter(cart=cart)
    for item in cart_items:
        cart_data.append({
            'product_name': item.product_id.product_name,
            'unit_price': item.product_id.unit_price,
            'quantity': item.product_qty,
            'item_total': item.product_total,
        })

    return render(request, 'payment.html', {
        'cart': cart_data,
        'total_amount': total_amount,
    })

def confirm_payment(request):
    if request.method == 'POST':
        # Simulate payment processing here
        # Payment logic would typically go here
        
        # Retrieve the user's active cart
        try:
            cart = Cart.objects.get(user=request.user, cart_status='pending')
        except Cart.DoesNotExist:
            return redirect('checkout')  # Redirect to checkout if no active cart is found

        # Create an order
        order = Order.objects.create(
            cart=cart,
            status='completed',
            total=cart.total,
            order_at=timezone.now()
        )
        
        # Mark the cart as completed
        cart.cart_status = 'completed'
        cart.save()

        # Redirect to confirmation page with the order ID
        return redirect('confirmation', order_id=order.id)


def confirmation(request, order_id):
    order = Order.objects.get(id=order_id)
    cart = order.cart
    cart_items = CartItems.objects.filter(cart=cart)
    
    return render(request, "confirmation.html", {
        'cart_items': cart_items,
        'order':order,
        'order_id': order_id,
        'total_amount': order.total
    })

def cart_display_view(request):
    cart_items = request.session.get('cart_items', {})
    return render(request, 'cart.html', {'cart_items': cart_items})
  

def testimonial(request):
    return render(request,"testimonial.html")

def feedback(request):
    if request.method == "POST":
        # Get form data from POST request
        name = request.POST.get('name')
        email = request.POST.get('email')
        rating = request.POST.get('rating')
        comments = request.POST.get('comments')

        # Create a Feedback object and save it to the database
        feedbk = Feedback.objects.create(
            name=name,
            email=email,
            rating=rating,
            comments=comments
        )
        feedbk.save()

        # After saving, return the template with a success message
        return render(request, 'feedback.html', {'success': True})
    
    # Render the form if not a POST request
    return render(request, "feedback.html")

def download_invoice(request, order_id):
    # Fetch the order and associated cart items
    try:
        order = Order.objects.get(id=order_id)
        cart = order.cart
        cart_items = CartItems.objects.filter(cart=cart)
    except Order.DoesNotExist:
        return HttpResponse("Order not found", status=404)

    # Create a response object with PDF content type
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{order_id}.pdf"'

    # Create a buffer to hold the PDF data
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)

    # Static text headers for the invoice
    p.drawString(100, 800, "AURORA - Invoice")
    p.drawString(100, 780, f"Order ID: {order_id}")
    p.drawString(100, 760, "Thank you for your order!")

    # Table headers
    p.drawString(100, 730, "Product")
    p.drawString(250, 730, "Unit Price")
    p.drawString(350, 730, "Quantity")
    p.drawString(450, 730, "Total Price")

    # Draw each item from the cart
    y_position = 710
    for item in cart_items:
        if y_position < 100:  # If the page is full, create a new one
            p.showPage()
            y_position = 750  # Reset y-position for new page

        p.drawString(100, y_position, item.product_id.product_name)
        p.drawString(250, y_position, f"Rs. {item.product_id.unit_price}")
        p.drawString(350, y_position, str(item.product_qty))
        p.drawString(450, y_position, f"Rs. {item.product_total}")
        y_position -= 20

    # Draw total amount at the end of the table
    p.drawString(100, y_position - 20, f"Total Amount: Rs. {order.total}")

    # Finish the PDF and close it
    p.showPage()
    p.save()

    # Get the PDF content from the buffer
    pdf = buffer.getvalue()
    buffer.close()

    # Write the PDF content to the response
    response.write(pdf)
    return response


def clear_cart(request, user_id):
    data = Cart.objects.filter(user_id=request.user)
    data.delete()

    return redirect('cart')  # Redirect back to the cart page (make sure 'cart' is defined in your urls)


# def shipment(request):
#     if request.method == "POST":
#         fullname = request.POST.get('fullname')
#         mobile = request.POST.get('mobile')
#         pincode = request.POST.get('pincode')
#         address = request.POST.get('address')
#         address2 = request.POST.get('address2')
#         landmark = request.POST.get('landmark')
#         city = request.POST.get('city')
#         state = request.POST.get('state')
#         shipmnt = Shipment.objects.create(fullname = fullname, mobile = mobile, pincode = pincode, address1 = address, address2 = address2, landmark = landmark, city = city, state=state)
#         shipmnt.save()
#         return redirect('payment')
#     return render(request, "shipment.html")


def shipment(request):
    if request.method == 'POST':
        fullname = request.POST.get('fullname')
        mobile = request.POST.get('mobile')  # Ensure 'mobile' is retrieved correctly
        pincode = request.POST.get('pincode')
        address1 = request.POST.get('address')
        address2 = request.POST.get('address2')
        landmark = request.POST.get('landmark')
        city = request.POST.get('city')
        state = request.POST.get('state')
        
        # Check that all required fields are not None
        if mobile:  # Ensure mobile is provided before saving
            shipment = Shipment(
                fullname=fullname,
                mobile=mobile,
                pincode=pincode,
                address1=address1,
                address2=address2,
                landmark=landmark,
                city=city,
                state=state
            )
            shipment.save()
            return redirect('payment')  # Adjust to your redirect

    return render(request, 'shipment.html')

def trackshipment(request):
    return render(request,"trackshipment.html")

def admin_feedback(request):
    feedbacks = Feedback.objects.all()
    return render(request , 'admin_feedback.html',{'feedbacks':feedbacks})