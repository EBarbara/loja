from django.db import models


class Disk(models.Model):
    name = models.CharField(max_length=50)
    artist = models.CharField(max_length=50)
    release_year = models.IntegerField()
    style = models.CharField(max_length=50)
    quantity = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
