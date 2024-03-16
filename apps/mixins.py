"""Mixins for reuse accross models"""
from datetime import timedelta, datetime
from django.db import models
from django.db.models import Q


class TimeStampMixin(models.Model):
    """Add date created and date updated to models"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True