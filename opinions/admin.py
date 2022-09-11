from django.contrib import admin
from .models import Opinion


class OpinionAdmin(admin.ModelAdmin):
     # report format 
    list_display = ('id', 'customer_name', 'is_published')
    
    # click to request record for review in the report
    list_display_links = ('id',)
        
    list_per_page = 25
    
    #disable add function
    #def has_add_permission(self, request, obj=None):
        #return False

admin.site.register(Opinion,OpinionAdmin)
