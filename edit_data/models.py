from django.db import models

class Countrie(models.Model):
    iso = models.CharField(verbose_name='ISO format name', max_length=10, unique=True)
    name = models.CharField(verbose_name='Countrie name', max_length=100, unique=True)

class City(models.Model):
    name = models.CharField(verbose_name='City name', max_length=100)
    country = models.ForeignKey(Countrie, on_delete=models.CASCADE)
