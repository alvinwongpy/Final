from django.db import models
from datetime import datetime

class Type(models.Model):
    type_name = models.CharField(max_length=200)
    type_desciption = models.TextField(blank=True)
    
    def __str__(self):
        return self.type_name

class Item(models.Model):
    type = models.ForeignKey(Type, on_delete=models.DO_NOTHING)
    item_name = models.CharField(max_length=200)
    item_desciption = models.TextField(blank=True)
    item_photo = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_displayed = models.BooleanField(default=False)
    
    def __str__(self):
        return self.item_name
    