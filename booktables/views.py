from contextlib import redirect_stderr
from pydoc import classify_class_attrs
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from .models import Desk
from .models import Tablestatu
from .models import Client_booking
from django.shortcuts import get_object_or_404
from datetime import datetime
from datetime import date
from datetime import timedelta
from django.db.models import Max, Min
import pytz
from django.contrib import messages

# examples thepost = get_object_or_404(Content, name='test')

def index(request):
    template = loader.get_template('book.html')
    return HttpResponse(template.render({}, request))


# after debug, the code is OK in the following
# def run(request):
#     # Fetch all desks
#     desks = Desk.objects.all()
#     # Print info of all desks
#     for desk in desks:
#         print(desk)
#     template = loader.get_template('book.html')
#     return HttpResponse(template.render({}, request))

#after debug, the code is OK in the following
# def run(request):
#     # example : mydata = Members.objects.all().values()
#     # Fetch all desksdef run(request):
#     for desk in range(1,7):                         # for each desk
#             for i in range(1,5):                    # for each booking time
#                 Desk_id = desk
#                 timeofstatu = date(2022, 9, 4)      # update statu on that date
#                 statuoftime = date(2022, 9, 4)      # update what time of statu
#                 week_day = 1 
#                 day_time = i 
#                 is_available = True 
#                 is_reserved = False 
#                 is_released = False 
#                 is_finished = False 
#                 is_canceled = False
#                 tablestatu = Tablestatu(Desk_id=Desk_id, timeofstatu=timeofstatu, statuoftime=statuoftime, week_day=week_day, day_time=day_time, is_available=is_available, is_reserved=is_reserved, is_released=is_released, is_finished=is_finished, is_canceled=is_canceled)
#                 tablestatu.save()
                                               
#     return render(request, 'pages/book.html')

#To creat one week of statu of table
def run(request):
    
    for day in range(5,13):                             # for each day
        for desk in range(1,7):                         # for each desk
                for i in range(1,5):                    # for each booking time
                    Desk_id = desk
                    timeofstatu = date(2022, 9, 5)      # update statu on that date
                    statuoftime = date(2022, 9, day)    # update what time of statu
                    week_day = 1 
                    day_time = i 
                    is_available = True 
                    is_reserved = False 
                    is_released = False 
                    is_finished = False 
                    is_canceled = False
                    tablestatu = Tablestatu(Desk_id=Desk_id, timeofstatu=timeofstatu, statuoftime=statuoftime, week_day=week_day, day_time=day_time, is_available=is_available, is_reserved=is_reserved, is_released=is_released, is_finished=is_finished, is_canceled=is_canceled)
                    tablestatu.save()
            
    return redirect('index')

# To update statu of tables everyday because time is passed 
def run1(request): # 
    # Example: MyModel.objects.filter(pk=1).delete()
    Tablestatu.objects.filter(statuoftime=date.today()-timedelta(days=1)).delete()
    last_day = Tablestatu.objects.aggregate(Max('statuoftime'))
    last_day = last_day['statuoftime__max'] + timedelta(days=1)
    
    for desk in range(1,7):                         # for each desk
            for i in range(1,5):                    # for each booking time
                Desk_id = desk
                timeofstatu = date.today()      # update statu on that date
                statuoftime = last_day      # update what time of statu
                week_day = 1 
                day_time = i 
                is_available = True 
                is_reserved = False 
                is_released = False 
                is_finished = False 
                is_canceled = False
                tablestatu = Tablestatu(Desk_id=Desk_id, timeofstatu=timeofstatu, statuoftime=statuoftime, week_day=week_day, day_time=day_time, is_available=is_available, is_reserved=is_reserved, is_released=is_released, is_finished=is_finished, is_canceled=is_canceled)
                tablestatu.save()   
                                         
    return redirect('index')

def test(request):
    #Example: from django.db.models import Max
    #Example: Book.objects.aggregate(Max('price'))
    table_statu_reocrd = Tablestatu.objects.aggregate(Max('statuoftime'))
    print(table_statu_reocrd)   
    template = loader.get_template('book.html')
    return HttpResponse(template.render({}, request))

def booktable(request):
    if request.method == 'POST':
        client_name = request.POST["client_name"]
        client_phone = request.POST["client_phone"]
        client_email = request.POST["client_email"]
        person_num = request.POST["person_num"]
        book_date = request.POST["book_date"]
        book_time = request.POST["book_time"]
        
        test={
                
                    "client_name" : client_name,
                    "client_phone" : client_phone,
                    "client_email" : client_email,
                    "person_num" : person_num,
                    "book_date" : book_date,
                    "book_time" : book_time,
                
            }
        
        print(test)
        
        # example 
        # date_time = datetime.datetime(**date)
        # date_time = date_time.strftime("%m/%d/%Y %I:%M %p")
        IST = pytz.timezone('Asia/Hong_Kong')
        date_time = datetime.now(IST)
        date_time = date_time.strftime("%m/%d/%Y %I:%M %p")
        bookdata = Client_booking(client_name=client_name,phone=client_phone,email=client_email,person_num=person_num,
                                  book_date=book_date,book_time=book_time,is_booked=False,is_reserved=False,is_released=False,
                                  is_canceled=False,is_finished=False,request_datetime= date_time)
        
        bookdata.save()        
        messages.success(request, "Booking is rec'd and confirm later. Thank you")
        return render(request, 'pages/book.html')
    else:
        return render(request, 'pages/book.html')