from django.contrib import admin
from .models import Rental, Book, AdminLogs


class RentalAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'start_date', 'end_date', 'calculate_rental_fee')

admin.site.register(Rental)
admin.site.register(Book)
admin.site.register(AdminLogs)
