from django.contrib import admin
from .models import (Section, Customer, Row, Seat)


class SeatAdmin(admin.ModelAdmin):
    """
    Add needed columns to Seat admin section
    """
    list_display = ['__str__', 'section', 'customer_name', 'is_blocked',
                    'is_allocated']

    def section(self, obj):
        return obj.row.section.name

    def customer_name(self, obj):
        if obj.customer:
            return obj.customer.reserve_name

        return '-'

    def is_allocated(self, obj):
        if obj.customer:
            return True

        return False

    is_allocated.boolean = True


class RowAdmin(admin.ModelAdmin):
    """
    Add needed columns to Row admin section
    """
    list_display = ['__str__', 'section']


admin.site.register(Section)
admin.site.register(Row, RowAdmin)
admin.site.register(Seat, SeatAdmin)
admin.site.register(Customer)
