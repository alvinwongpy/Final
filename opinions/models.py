from unicodedata import name
from django.db import models

class Opinion(models.Model):
    customer_name = models.CharField(max_length=200)
    advise = models.CharField(max_length=200)
    client_photo = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True)
    
    def __str__(self):
        return "Client : "+self.customer_name