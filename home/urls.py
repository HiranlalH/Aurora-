from django.urls import path
from .views import index,error,about,blog,contact,feature,Prediction,product,testimonial,userlogin,userreg,feedback,payment

urlpatterns = [
    path('', index, name='index'),
    path('error/',error,name='error'),
    path('userlogin/',userlogin,name='userlogin'),
    path('userreg/',userreg,name='userreg'),
    
    path('about/',about,name='about'),
    path('blog/',blog,name='blog'),
    path('contact/',contact,name='contact'),
    path('feature/',feature,name='feature'),
    path('Prediction/',Prediction,name='Prediction'),
    path('product/',product,name='product'),
    path('testimonial/',testimonial,name='testimonial'),
    path('feedback/',feedback,name='feedback'),
    path('payment/',payment,name='payment')
    

]