from django.db import models

# Create your models here.


class User(models.Model):
    Id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=100)
    Email = models.EmailField(unique=True)
    AddressPostcode = models.CharField(max_length=100)
    StateName = models.CharField(max_length=100)