from django.db import models
from datetime import datetime

class CartOrder(models.Model):
   user_id = models.IntegerField()
   selection_date = models.DateTimeField(default=datetime.now, blank=True)

class CartOrderDetail(models.Model):
    cartorder_id = models.IntegerField()
    item_id = models.IntegerField()
    qty = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_confirmed = models.BooleanField(default=False)
    
    def qty_increment(self):
        self.qty = self.qty + 1


