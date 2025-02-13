import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class UserProfile(models.Model):
    birth_date = models.DateField(null=True, blank=True)