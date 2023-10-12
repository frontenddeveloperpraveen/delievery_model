from django.db import models

class Order(models.Model):

    sno = models.AutoField(primary_key=True)

    orderid = models.IntegerField(default=0, unique=True)

    name = models.CharField(max_length=85)

    email = models.CharField(max_length=60)

    price = models.IntegerField(default=0)

    verified = models.BooleanField(default=False)
