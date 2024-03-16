import datetime
from django.utils import timezone
from decimal import Decimal
from django.db import models
from apps.mixins import TimeStampMixin
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_save
import math

User = get_user_model()

# Create your models here.
class Book(TimeStampMixin):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=125)
    number_of_pages = models.IntegerField()
    
    def __str__(self):
        return self.title
    

class Rental(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_rentals')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    book_return_date = models.DateField(null=True, blank=True)
    is_book_returned = models.BooleanField(default=False)
    
    # handle book rental extension logics
    is_extended = models.BooleanField(default=False)
    # extension_count tracks how many times extensions was done
    extension_count = models.IntegerField(default=0, editable=False) 
    extension_duration_in_months = models.IntegerField(default=0)
    extention_end_date = models.DateField(null=True, blank=True)
        
    @property
    def calculate_rental_fee(self):
        """Calculate rental fee."""
        days_rented = (datetime.datetime.now().date() - self.start_date).days
        if days_rented <= 30:
            return Decimal(0)
        else:
            # Calculate the number of months beyond the initial free month
            # round up to nearest whole number
            months_rented = math.ceil((days_rented - 30) / 30)
            # Calculate the fee based on number of pages
            fee = self.book.number_of_pages / 100 * 3
            # Calculate the amount due considering the fee and rental period
            amount_due = Decimal(fee) * Decimal(months_rented)
            return round(amount_due, 2) # round up to 2 decimals
        
    def extend_rental(self, admin_user, extension_duration_in_months):
        """Extend book rental."""
        # Convert months to days using a rough approximation (assuming 30 days per month)
        extension_duration_in_days = extension_duration_in_months * 30
        self.extention_end_date = self.end_date + datetime.timedelta(days=extension_duration_in_days)
        self.extension_duration_in_months += extension_duration_in_months
        self.extension_count += 1
        self.is_extended = True
        self.save()
        
        # log admin action
        AdminLogs.objects.create(admin=admin_user, 
                                 book_rental=self, 
                                 duration=extension_duration_in_months)
        
    def close_rental(self):
        """Close book rental and mark as returned."""
        self.book_return_date = datetime.datetime.now().today()
        self.is_book_returned = True
        self.save()
    
    def __str__(self):
        return f'{self.book.title}'

class AdminLogs(TimeStampMixin):
    """Log rental extension activities of a Book Keeper or Admin.
    
    This is necessary to track rental extensions created by each admin for
    future reference."""
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    book_rental = models.ForeignKey(Rental, on_delete=models.CASCADE)
    duration = models.IntegerField(null=True, blank=True)
    action_description = models.TextField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.action_description:
            self.action_description = f'{self.admin.get_full_name()} extended the due date of {self.book_rental.book.title} rented by {self.book_rental.user.get_full_name()} by {self.duration} months'
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.book_rental}'
    
    

@receiver(post_save, sender=Rental)
def update_end_date(sender, instance, created, *args, **kwargs):
    # ensure signal fires at initial creation only
    if created:
        # update start and end date
        instance.start_date = datetime.datetime.now().date()
        instance.end_date = instance.start_date + datetime.timedelta(days=30)
        instance.save()