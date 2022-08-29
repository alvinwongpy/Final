from django.urls import path
from . import views
# set the / api, as variable=index to callback function
# / accounts/ all the accounrs api
# setup all the possible accounts route

urlpatterns = [
    path('', views.cart, name='cart'),
    path('test',views.test, name="test"),       
]