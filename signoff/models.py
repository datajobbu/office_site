from django.db import models

# Create your models here.
class Signoff(models.Model):
    name = models.CharField(max_length=30)
    qnt = models.IntegerField()
    unit = models.IntegerField()
    request_date = models.DateField(auto_now_add=True)