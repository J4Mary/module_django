import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    cash = models.FloatField(blank=True, null=True, default=1000)
