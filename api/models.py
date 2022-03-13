from django.db import models


class Catalog(models.Model):
    name = models.CharField(max_length=50)
    artist = models.CharField(max_length=50)
    release_year = models.IntegerField()
    style = models.CharField(max_length=50)
    quantity = models.IntegerField(default=0)
