from django.urls import path
from .views import index,error,about,blog,contact,feature,how_to_use,product,testimonial

urlpatterns = [
    path('', index, name='index'),
    path('error/',error,name='error'),
    path('about/',about,name='about'),
    path('blog/',blog,name='blog'),
    path('contact/',contact,name='contact'),
    path('feature/',feature,name='feature'),
    path('how_to_use/',how_to_use,name='how_to_use'),
    path('product/',product,name='product'),
    path('testimonial/',testimonial,name='testimonial')

]