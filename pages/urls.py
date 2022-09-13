# load path
# load views from the same directory

from django.urls import path
from . import views
# set the / api, as variable=index to callback function
urlpatterns = [
    path('',views.index, name='index'),
    path('index/',views.index,name='index'),
    path('about/',views.about, name='about'),
    path('menu/',views.menu, name='menu'),
    path('book/',views.book, name='book'),
    path('pdf_view/', views.pdf_view, name='pdf_view')
]
