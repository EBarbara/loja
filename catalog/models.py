from django.db import models


class Disk(models.Model):
    """
    Modelo de cada CD vendido na loja.
    Por questões de tempo hábil não foram implementadas validações de banco, o que significa
    que podemos ter ano de lançamento no futuro, ou quantidades negativas.
    """
    name = models.CharField(max_length=50)
    artist = models.CharField(max_length=50)
    release_year = models.IntegerField()
    style = models.CharField(max_length=50)
    quantity = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
