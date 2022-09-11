from django.db import models
from datetime import datetime
from twilio.rest import Client

class Desk(models.Model):
    desk_id = models.AutoField(primary_key=True)
    seats = models.IntegerField()
    
    def __str__(self):
        return "Desk# :"+str(self.pk)+", Seat number: "+str(self.seats)
    
class Tablestatu(models.Model):
    Desk = models.ForeignKey(Desk, on_delete=models.DO_NOTHING)
    timeofstatu = models.DateField(blank=True) 
    statuoftime = models.DateField(blank=True) 
    week_day = models.PositiveSmallIntegerField(
    choices=(
        (1, "Monday"),
        (2, "Tuesday"),
        (3, "Wednesday"),
        (4, "Thursday "),
        (5, "Friday"),
        (6, "Saturday"),
        (7, "Sunday") 
        )
    )
    day_time =  models.PositiveSmallIntegerField(
    choices=(
        (1, "6:00PM"),
        (2, "7:00PM"),
        (3, "8:00PM"),
        (4, "9:00PM")
        )
    )
    is_available = models.BooleanField(default=False)
    is_reserved = models.BooleanField(default=False)
    is_released = models.BooleanField(default=False)
    is_finished = models.BooleanField(default=False)
    is_canceled = models.BooleanField(default=False)
        
    def __str__(self):        
        list_time = ["6:00PM","7:00PM","8:00PM","9:00PM"]
        day_time=list_time[self.day_time-1]
        if self.is_available == False and self.is_reserved == True:
            return "Desk: No."+str(self.Desk.pk)+" , Seat No.: "+str(self.Desk.seats)+"  , the desk statu by that date and time: "+str(self.statuoftime)+"  , "+str(day_time)+"      (RESERVED)"
        else:
            
            available = "Yes"
            return "Desk: No."+str(self.Desk.pk)+" , Seat No.: "+str(self.Desk.seats)+"  , the desk statu by that date and time: "+str(self.statuoftime)+"  , "+str(day_time)+"  , Available: "+available 
       
    
class Client_booking(models.Model):
    client_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    person_num = models.IntegerField()
    book_date = models.DateField(blank=True)
    book_time =  models.PositiveSmallIntegerField(
    choices=(
        (1, "6:00PM"),
        (2, "7:00PM"),
        (3, "8:00PM"),
        (4, "9:00PM")
        )
    )
    is_booked = models.BooleanField(default=False)
    is_reserved = models.BooleanField(default=False)
    is_released = models.BooleanField(default=False)
    is_canceled = models.BooleanField(default=False)
    is_finished = models.BooleanField(default=False)
    # request_datetime = models.DateTimeField(blank=True)
    request_datetime = models.CharField(max_length=200)
    
    def __str__(self):
        print(str(self.request_datetime))
        list_time = ["6:00PM","7:00PM","8:00PM","9:00PM"]
        book_time=list_time[self.book_time-1]
        #return "client name:"+self.client_name+","+"person num:"+str(self.person_num)+","+"booking datetime:"+str(self.book_datetime)
        return str(self.client_name)+" requested  "+ str(self.person_num)+ " persons of desk, booking date: "+str(self.book_date)+" , booking time: "+ str(book_time)+" , the request on datetime: "+str(self.request_datetime)

class Reservation(models.Model):
    client_booking = models.OneToOneField(Client_booking, on_delete=models.DO_NOTHING)
    tablestatu = models.OneToOneField(Tablestatu, on_delete=models.DO_NOTHING)
    client_confirm_time = models.DateTimeField(blank=True)
    is_OK = models.BooleanField(default=False)
    
    def __str__(self):                
        return str(self.client_booking)+" ,  Confirm on date: "+str(self.client_confirm_time)+" ,  "+str(self.tablestatu)

# example:
# place = models.OneToOneField(
#         Place,
#         on_delete=models.CASCADE,
#         primary_key=True,
#     )