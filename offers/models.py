from unicodedata import name
from django.db import models
from menu_items.models import Item

class Offer(models.Model):
    promotions_name = models.CharField(max_length=200)
    promotions_discount = models.IntegerField()
    promotions_photo = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True)
    bestselling_item = models.ForeignKey(Item, on_delete=models.DO_NOTHING)
    bestselling_music = models.FileField(upload_to='music/%Y/%m/%d/')
    is_posted = models.BooleanField(default=False)

    def __str__(self):
        return "Promotions :" + self.promotions_name +"  Bestselling item:  " + self.bestselling_item.item_name