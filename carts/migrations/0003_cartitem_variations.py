# Generated by Django 4.1.2 on 2022-11-01 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_rename_varation_variation_and_more'),
        ('carts', '0002_cartitem_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='Variations',
            field=models.ManyToManyField(blank=True, to='store.variation'),
        ),
    ]
