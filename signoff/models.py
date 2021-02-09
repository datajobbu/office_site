from django.db import models
from django.db.models import F
from django.utils import timezone


class Signoff(models.Model):
    name = models.CharField(max_length=30)
    qnt = models.IntegerField()
    unit = models.IntegerField()
    request_date = models.DateField(default=timezone.now)