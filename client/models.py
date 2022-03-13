from django.db import models


class Client(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    cpf = models.CharField(max_length=11)
    email = models.EmailField(unique=True)
    birthday = models.DateField()
    is_active = models.BooleanField(default=True)
