# Generated by Django 4.1.2 on 2022-11-19 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_productgallery'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='offer_price',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='percentage',
            field=models.IntegerField(default=0),
        ),
    ]
