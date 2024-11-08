from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', index, name='index'),
    path('error/',error,name='error'),
    path('userlogin/',userlogin,name='userlogin'),
    path('userlogout/',userlogout, name='userlogout'),
    path('userreg/',userreg,name='userreg'),
    path('admin_dashboard/',admindashboard,name='admin_dashboard'),
    path('about/',about,name='about'),
    path('contact/',contact,name='contact'),
    path('feature/',feature,name='feature'),
    path('product/',products,name='product'),
    path('testimonial/',testimonial,name='testimonial'),
    path('feedback/',feedback,name='feedback'),
    path('checkout/', checkout, name='checkout'), 
    path('payment/',payment,name='payment'),
    path('confirm-payment/',confirm_payment,name='confirm_payment'),
    path('confirmation/<int:order_id>',confirmation,name='confirmation'),
    path('add_to_cart/<int:p_id>', add_to_cart, name="add_to_cart"),
    path('cart', cart, name='cart'),  # Ensure user_id is part of the path
    path('clear_cart/<int:user_id>/', clear_cart, name='clear_cart'),
    path('download_invoice/<int:order_id>/', download_invoice, name='download_invoice'),
    path('trackshipment/', trackshipment, name='trackshipment'), 
    path('shipment/',shipment, name='shipment'),
    path('admin_userslist',admin_userslist,name = 'admin_userslist'),
    path('admin_feedback/',admin_feedback, name='admin_feedback'),
    path('order_history/<int:user_id>',order_history, name='order_history'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)