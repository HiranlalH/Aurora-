from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

# Create your views here.
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

def admindashboard(request):
    return render(request,"admin_dashboard.html")
    

def userlogout(request):
    logout(request)
    return redirect('userlogin')

def about(request):
    return render(request,"about.html")
    
def blog(request):
    return render(request,"blog.html")

def contact(request):
    return render(request,"contact.html")

def feature(request):
    return render(request,"feature.html")

def Prediction(request):
    return render(request,"Prediction.html")

def product(request):
    return render(request,"product.html")

def testimonial(request):
    return render(request,"testimonial.html")

def feedback(request):
    return render(request,"feedback.html")

def payment(request):
    return render(request,"payment.html")

def cart(request):
    return render(request,"cart.html")

def checkout(request):
    return render(request,"checkout.html")

def confirmation(request):
    return render(request,"confirmation.html")


def cart_view(request):
    if request.method == 'POST':
        cart_items = {}
        body_lotion_qty = int(request.POST.get('body_lotion', 0))
        if body_lotion_qty > 0:
            cart_items['Body Lotion'] = {'qty': body_lotion_qty, 'price': 500}

        # Repeat for other products
        face_cream_qty = int(request.POST.get('face_cream', 0))
        if face_cream_qty > 0:
            cart_items['Face Cream'] = {'qty': face_cream_qty, 'price': 410}

        # Add more products similarly...

        # Save cart_items in session or pass to context
        request.session['cart_items'] = cart_items
        
        return redirect('cart_display')  # Redirect to the cart display page

    return render(request, 'cart.html')

def cart_display_view(request):
    cart_items = request.session.get('cart_items', {})
    return render(request, 'cart.html', {'cart_items': cart_items})
