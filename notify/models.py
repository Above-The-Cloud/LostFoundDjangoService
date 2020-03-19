import datetime

from django.db import models

# Create your models here.
from django.utils import timezone


class Notify(models.Model):
    user_id = models.BigIntegerField()
    dynamic_id = models.IntegerField()
    read = models.IntegerField(default=0)
    status = models.IntegerField(default=1)
    ctime = models.DateTimeField(default = timezone.now)
    mtime = models.DateTimeField(auto_now = True)