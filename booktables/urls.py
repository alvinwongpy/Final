from django.urls import path
from . import views
# set the / api, as variable=index to callback function
# / accounts/ all the accounrs api
# setup all the possible accounts route

urlpatterns = [
    path('booktable', views.booktable, name='booktable'), 
    path('run/',views.run, name='run'),
    path('run1/',views.run1, name='run1'),    
]