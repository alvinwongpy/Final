from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from menu_items.models import Type
from menu_items.models import Item


def index(request):
    
    #call function to get types data and items data
    types, items = generate_data()
    
    #collect all data for sending to the webage 
    context = {
        'types': types,
        'items': items,
    }
        
    return render(request, 'pages/index.html', context)


def about(request):
    template = loader.get_template('pages/about.html')
    return HttpResponse(template.render({}, request))

def book(request):
    template = loader.get_template('pages/book.html')
    return HttpResponse(template.render({}, request))


def menu(request):
    
    #call function to get types data and items data
    types, items = generate_data()
    
    #collect all data for sending to the webage 
    context = {
        'types': types,
        'items': items,
    }
        
    return render(request, 'pages/menu.html', context)

def test(request):
    
    types, items = generate_data()
    
    context = {
        'types': types,
        'items': items,
    }
    
    return render(request, 'pages/test.html', context)


#function to generate types data and items data
def generate_data():
    
    types = Type.objects.all()
    items = Item.objects.filter(is_displayed=True).all()
    
    for type in types:
        lowercase = type.type_name
        lowercase = lowercase.lower()
        setattr(type, 'lowercase', lowercase)
    
    for item in items:
        lowercase = item.type.type_name
        lowercase = lowercase.lower()
        setattr(item, 'lowercase', lowercase)
  
    
    return types,items
