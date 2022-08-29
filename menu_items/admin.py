from django.contrib import admin
from .models import Type
from .models import Item

class TypeAdmin(admin.ModelAdmin):
     # report format 
    list_display = ('id', 'type_name')
    
    # click to request record for review in the report
    list_display_links = ('id',)
        
    list_per_page = 25
    
    #disable add function
    #def has_add_permission(self, request, obj=None):
        #return False
        
admin.site.register(Type, TypeAdmin)

class ItemAdmin(admin.ModelAdmin):
    # report format 
    list_display = ('id', 'type','item_name','item_photo','is_displayed')
    
     # click to request record for review in the report
    list_display_links = ('id',)
    
    # disable add function
    #def has_add_permission(self, request, obj=None):
        #return False
    
admin.site.register(Item, ItemAdmin)

