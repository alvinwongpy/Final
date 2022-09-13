from django.contrib import admin
from .models import Slider

class SliderAdmin(admin.ModelAdmin):
       
    #disable add function
    def has_add_permission(self, request, obj=None):
        return False
    #disable delete function
    def has_delete_permission(self, request, obj=None):
        return False
       
admin.site.register(Slider, SliderAdmin)
