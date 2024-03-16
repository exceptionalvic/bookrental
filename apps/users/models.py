from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser
from django.conf import settings

from .manager import CustomUserManager
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.apps import apps
import uuid
from django.utils import timezone
from apps.mixins import TimeStampMixin
from django.db.models import Sum


def user_kyc_file_location(instance, filename):
    file_extension = filename.split('.')[-1]
    # generate a random name difficult to guess
    file_name = f'{uuid.uuid4()}--{timezone.now}'
    return f"user/kyc/{instance.user.email}/{file_name}.{file_extension}"


# Create your models here.
class User(TimeStampMixin, AbstractUser):
    email           = models.EmailField(unique=True)
    username        = None  # set username field to None since we are using email as primary auth
    first_name      = models.CharField(_('First Name'), max_length=150, null=True, blank=True)
    last_name       = models.CharField(_('Last Name'), max_length=150, null=True, blank=True)
    # id using UUIDField for generating user unique ID
    id            = models.UUIDField(_("ID"), primary_key=True, default=uuid.uuid4, editable=False)
    is_verified = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
    
    class Meta:
        ordering = ('date_joined',)

    def __str__(self):
        return self.email
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}" if self.first_name and self.last_name else self.email
    
    @property
    def calculate_total_fees_paid(self):
        """
        Calculate the total fees paid by the user for all rented books.
        """
        total_fees = self.user_rentals.aggregate(total_fees=Sum('calculate_rental_fee'))['total_fees']
        return total_fees if total_fees else 0

    @property
    def get_total_rented_books(self):
        """
        Get all the books rented by the user.
        """
        return self.user_rentals.all().count()
    

class KYC(TimeStampMixin):
    """Verify KYC of users"""
    ID_TYPES = (
        ('State-Issued','state-issued'),
        ('Passport','passport'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id_type = models.CharField(max_length=25, choices=ID_TYPES, default='State-Issued')
    file = models.ImageField(upload_to=user_kyc_file_location)
    is_validated = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.user} - {self.id_type}'
    
    def validate_user_kyc(self):
        self.is_validated = True
        self.save()
        # update user as verified
        user = self.user
        user.is_verified = True
        user.save()
        
