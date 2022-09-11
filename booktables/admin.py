from django.contrib import admin
from .models import Desk
from .models import Reservation
from .models import Tablestatu
from .models import Client_booking


admin.site.register(Client_booking)


class DeskAdmin(admin.ModelAdmin):
    readonly_fields = ('seats',)
    #readonly_fields = ()
admin.site.register(Desk,DeskAdmin)

class TablestatuAdmin(admin.ModelAdmin):
    readonly_fields = ('Desk', 'week_day','day_time',)
    search_fields = ('id', 'statuoftime',)
        
    # Example:
    # list_display = ('name', 'age')
    # search_fields = ('name',)

    # def get_search_results(self, request, queryset, search_term):
    #     queryset, may_have_duplicates = super().get_search_results(
    #         request, queryset, search_term,
    #     )
    #     try:
    #         search_term_as_int = int(search_term)
    #     except ValueError:
    #         pass
    #     else:
    #         queryset |= self.model.objects.filter(age=search_term_as_int)
    #     return queryset, may_have_duplicates
    
admin.site.register(Tablestatu,TablestatuAdmin)
admin.site.register(Reservation)
