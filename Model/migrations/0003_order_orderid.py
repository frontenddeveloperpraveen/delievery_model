# Generated by Django 4.2.1 on 2023-09-25 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Model', '0002_order_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='orderid',
            field=models.CharField(default='Nul', max_length=50, unique=True),
        ),
    ]
