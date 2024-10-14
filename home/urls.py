from django.urls import path
from .views import *
urlpatterns = [
    path('', index, name='index'),
    path('error/',error,name='error'),
    path('userlogin/',userlogin,name='userlogin'),
    path('userlogout/',userlogout, name='userlogout'),
    path('userreg/',userreg,name='userreg'),
    path('admin_dashboard/',admindashboard,name='admin_dashboard'),
    path('about/',about,name='about'),
    path('blog/',blog,name='blog'),
    path('contact/',contact,name='contact'),
    path('feature/',feature,name='feature'),
    path('Prediction/',Prediction,name='Prediction'),
    path('product/',product,name='product'),
    path('testimonial/',testimonial,name='testimonial'),
    path('feedback/',feedback,name='feedback'),
    path('cart/',cart,name='cart'),
    path('checkout/',checkout,name='checkout'),
    path('payment/',payment,name='payment'),
    path('confirmation/',confirmation,name='confirmation')
    
    

]