from django.db import models
from datetime import datetime, timedelta
# for working function of twilio 
import os
from twilio.rest import Client
# signals import
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import (
post_save,
pre_save
)
import pytz

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
        #.strftime("%m/%d/%Y %I:%M %p")
        self.client_confirm_time = self.client_confirm_time+timedelta(hours=8)  
        self.client_confirm_time = self.client_confirm_time.strftime("%m/%d/%Y %I:%M %p")
        return str(self.client_booking)+" ,  Confirm on date: "+str(self.client_confirm_time)+" ,  "+str(self.tablestatu)

@receiver(post_save, sender=Reservation)
def reservation_post_save_receiver(sender, instance, created, *args, **kwargs):
	if created:
            account_sid = os.environ['TWILIO_ACCOUNT_SID']
            auth_token = os.environ['TWILIO_AUTH_TOKEN']
            client = Client(account_sid, auth_token)
            call = client.calls.create(
                                    twiml='<Response><Say>'+instance.client_booking.client_name+',your booking is confirmed</Say></Response>',
                                    to='+852'+ instance.client_booking.phone,
                                    from_='+85230013654'
                                )

            print(call.sid)


# @receiver(post_save, sender=model)
# def xxx_yyy_post_save_receiver(sender, instance, created, *args, **kwargs):
# 	if created:
# 		print("send eamil to",instance.field)
# 	else:
# 		print(instance.field, "was just saved")


# example:
# place = models.OneToOneField(
#         Place,
#         on_delete=models.CASCADE,
#         primary_key=True,
#     )