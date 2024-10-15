from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Product, Product_cart, Feedback, Contact
from django.contrib import messages



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

def admindashboard(request):
    return render(request,"admin_dashboard.html")
    
def about(request):
    return render(request,"about.html")
    
def blog(request):
    return render(request,"blog.html")

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

def Prediction(request):
    return render(request,"Prediction.html")

def products(request):
    products = Product.objects.all()
    return render(request, "product.html", {'products': products})

def add_to_cart(request, p_id):
    user = request.user
    product = Product.objects.get(id = p_id)
    if Product_cart.objects.filter(user_id = user).exists():
        if Product_cart.objects.filter(product_id = product).exists():
            crt = Product_cart.objects.get(user_id = user, product_id = product)
            crt.product_qty += 1
            crt.save()
            return redirect(products)
        elif not Product_cart.objects.filter(product_id = product).exists():
            crt = Product_cart.objects.create(user_id = user, product_id = product, product_qty = 1, cart_status = True)
            crt.save()
            return redirect(products)
    crt = Product_cart.objects.create(user_id = user, product_id = product, product_qty = 1, cart_status = True)
    crt.save()
    return redirect(products)


def cart(request):
    # Retrieve the cart items for the user
    cart = Product_cart.objects.filter(user_id=request.user)
    total_amount = 0
    cart_data = []
    for item in cart:
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
    cart = Product_cart.objects.filter(user_id=request.user)
    total_amount = 0
    cart_data = []
    for item in cart:
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
    cart = Product_cart.objects.filter(user_id=request.user)
    total_amount = 0
    cart_data = []
    for item in cart:
        item_total = item.product_id.unit_price * item.product_qty
        cart_data.append({
            'product_name': item.product_id.product_name,
            'unit_price': item.product_id.unit_price,
            'quantity': item.product_qty,
            'item_total': item_total,
        })
        total_amount += item_total
    return render(request,"payment.html",{'total_amount':total_amount})


def confirmation(request):
    cart = Product_cart.objects.filter(user_id=request.user)
    total_amount = 0
    cart_data = []
    for item in cart:
        item_total = item.product_id.unit_price * item.product_qty
        cart_data.append({
            'product_name': item.product_id.product_name,
            'unit_price': item.product_id.unit_price,
            'quantity': item.product_qty,
            'item_total': item_total,
        })
        total_amount += item_total
    return render(request,"confirmation.html")

def cart_display_view(request):
    cart_items = request.session.get('cart_items', {})
    return render(request, 'cart.html', {'cart_items': cart_items})
  

def testimonial(request):
    return render(request,"testimonial.html")

def feedback(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        rating = request.POST.get('rating')
        comments = request.POST.get('comments')
        feedbk = Feedback.objects.create(name = name, email = email, rating = rating, comments = comments)
        feedbk.save()
        return render(request, 'feedback.html')
    return render(request,"feedback.html")


def clear_cart(request, user_id):
    data = Product_cart.objects.filter(user_id=request.user)
    data.delete()

    return redirect('cart')  # Redirect back to the cart page (make sure 'cart' is defined in your urls)




# def cart_view(request):
#     if request.method == 'POST':
#         cart_items = {}
#         body_lotion_qty = int(request.POST.get('body_lotion', 0))
#         if body_lotion_qty > 0:
#             cart_items['Body Lotion'] = {'qty': body_lotion_qty, 'price': 500}

#         # Repeat for other products
#         face_cream_qty = int(request.POST.get('face_cream', 0))
#         if face_cream_qty > 0:
#             cart_items['Face Cream'] = {'qty': face_cream_qty, 'price': 410}

#         # Add more products similarly...

#         # Save cart_items in session or pass to context
#         request.session['cart_items'] = cart_items
        
#         return redirect('cart_display')  # Redirect to the cart display page

#     return render(request, 'cart.html')



# def clear_cart(request, user_id):
#     products = Product_cart.objects.filter(user_id = user_id)
#     usr = User.objects.get(id = user_id)
#     for product in products:
#         product.cart_status = False
#         product.save()
#     return redirect(cart, usr.id)




