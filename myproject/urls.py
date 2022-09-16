"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url
from django.urls import path, include
from django.conf import settings
#from django.conf.urls.static import static
from django.views.static import serve
from django.conf.urls import handler404, handler500



admin.site.site_header  =  "DRAGONBURG admin"  
admin.site.site_title  =  "DRAGONBURG admin site"
admin.site.index_title  =  "Welcome to DRAGONBURG Admin"

urlpatterns = [
    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
    path("", include('pages.urls')),
    path("book/", include('booktables.urls')),
    path("cart/", include('cart.urls')),
    path("accounts/", include('accounts.urls')),
    path("admin/", admin.site.urls),
]

#handler404 = "myproject.views.page_not_found_view"
handler404 = 'myproject.views.error_404_view'