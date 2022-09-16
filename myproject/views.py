# from django.shortcuts import render
# def page_not_found_view(request, exception):
#     return render(request, '404.html', status=404)

from django.conf import settings
from django.shortcuts import render,redirect
 
 
def error_404_view(request, exception):
   
    # we add the path to the the 404.html file
    # here. The name of our HTML file is 404.html
    return render(request, '404.html')