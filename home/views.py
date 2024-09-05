from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,"index.html")

def error(request):
    return render(request,"error.html")

def about(request):
    return render(request,"about.html")
    
def blog(request):
    return render(request,"blog.html")

def contact(request):
    return render(request,"contact.html")

def feature(request):
    return render(request,"feature.html")

def how_to_use(request):
    return render(request,"how_to_use.html")

def product(request):
    return render(request,"product.html")

def testimonial(request):
    return render(request,"testimonial.html")