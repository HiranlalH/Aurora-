from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Product, Product_cart, Feedback, Contact
from django.contrib import messages
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO



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
        if Product_cart.objects.filter(user_id = request.user,product_id = product).exists():
            crt = Product_cart.objects.filter(user_id = request.user, product_id = product).first()
            crt.product_qty += 1
            crt.product_total = crt.product_qty*product.unit_price
            crt.save()
            return redirect(products)
        elif not Product_cart.objects.filter(product_id = product).exists():
            crt = Product_cart.objects.create(user_id = user, product_id = product, product_qty = 1, cart_status = True)
            crt.save()
            return redirect(products)
    crt = Product_cart.objects.create(user_id = user, product_id = product, product_qty = 1, product_total = product.unit_price, cart_status = True)
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
    
    return render(request,"confirmation.html", {'cart': cart})

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

def download_invoice(request, user_id):
    # Create a response object with PDF content type
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'

    # Create a buffer to hold the PDF data
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)

    # Fetch cart data from session or database as needed
    cart = Product_cart.objects.filter(user_id = user_id) # Assuming cart data is stored in session
    print(cart)

    # Draw static text headers for the invoice
    p.drawString(100, 800, "AURORA - Invoice")
    p.drawString(100, 780, "Thank you for your order!")

    # Table headers
    p.drawString(100, 750, "Product")
    p.drawString(250, 750, "Unit Price")
    p.drawString(350, 750, "Quantity")
    p.drawString(450, 750, "Total Price")

    # Draw each item from the cart with dynamic data
    y_position = 730
    for item in cart:
        p.drawString(100, y_position, item.product_id.product_name)
        p.drawString(250, y_position, f"Rs. {item.product_id.unit_price}")
        p.drawString(350, y_position, str(item.product_qty))
        p.drawString(450, y_position, f"Rs. {item.product_total}")
        y_position -= 20

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
    data = Product_cart.objects.filter(user_id=request.user)
    data.delete()

    return redirect('cart')  # Redirect back to the cart page (make sure 'cart' is defined in your urls)


def order_hist(request):
    return render(request, 'orderhistory.html')

def trackshipment(request):
    return render(request, 'trackshipment.html')