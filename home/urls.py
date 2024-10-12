from django.urls import path
from .views import index,error,about,blog,contact,feature,Prediction,products,testimonial,userlogin,userlogout,userreg,feedback,cart,checkout,payment,confirmation, add_to_cart
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', index, name='index'),
    path('error/',error,name='error'),
    path('userlogin/',userlogin,name='userlogin'),
    path('userlogout/',userlogout, name='userlogout'),
    path('userreg/',userreg,name='userreg'),
    path('about/',about,name='about'),
    path('blog/',blog,name='blog'),
    path('contact/',contact,name='contact'),
    path('feature/',feature,name='feature'),
    path('Prediction/',Prediction,name='Prediction'),
    path('product/',products,name='product'),
    path('testimonial/',testimonial,name='testimonial'),
    path('feedback/',feedback,name='feedback'),
    path('cart/',cart,name='cart'),
    path('checkout/',checkout,name='checkout'),
    path('payment/',payment,name='payment'),
    path('confirmation/',confirmation,name='confirmation'),
    path('add_to_cart/<int:p_id>', add_to_cart, name="add_to_cart")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)