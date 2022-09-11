from django.contrib import admin
from .models import Item
from .models import Offer



class OfferAdmin(admin.ModelAdmin):
     # report format 
    list_display = ('id', 'promotions_name', 'promotions_discount', 'bestselling_item', 'is_posted')
    
    # click to request record for review in the report
    list_display_links = ('id',)
        
    list_per_page = 25
    
    #disable add function
    #def has_add_permission(self, request, obj=None):
        #return False

admin.site.register(Offer,OfferAdmin)
