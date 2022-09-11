from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from menu_items.models import Type
from menu_items.models import Item
from slider.models import Slider
from opinions.models import Opinion
from offers.models import Offer
from django.http import FileResponse, Http404



def index(request):
               
    # example: entry = Entry.objects.get(pk=1)
    # slider panel content control
    slider1 = Slider.objects.get(pk=1)
    slider2 = Slider.objects.get(pk=2)
    slider3 = Slider.objects.get(pk=3)
    
    slider1=str(slider1.slider)
    slider2=str(slider2.slider)
    slider3=str(slider3.slider)
    
    # example : desks = Desk.objects.all()
    # example : items = Item.objects.filter(is_displayed=True).all()
     # opinions panel content control
    opinions = Opinion.objects.filter(is_published=True).all()     
    
    # offer panel content control
    offers = Offer.objects.filter(is_posted=True).all()

    #call function to get types data and items data
    types, items = generate_data()
    
    #collect all data for sending to the webage 
    context = {
            'types': types,
            'items': items,
            'slider1' : slider1,
            'slider2' : slider2,
            'slider3' : slider3,
            'opinions' : opinions,
            'offers': offers,
           
    }
    print(context) 
    return render(request, 'pages/index.html', context)


def about(request):
    template = loader.get_template('pages/about.html')
    return HttpResponse(template.render({}, request))

def book(request):
    #template = loader.get_template('pages/book.html')
    #return HttpResponse(template.render({}, request))
    return render(request, 'pages/book.html')



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


# open pdf function ref : https://thewebdev.info/2022/04/04/how-to-show-a-pdf-file-in-a-python-django-view/  
def pdf_view(request):
    try:
        return FileResponse(open('foobar.pdf', 'rb'), content_type='application/pdf')
    except FileNotFoundError:
        raise Http404()
    