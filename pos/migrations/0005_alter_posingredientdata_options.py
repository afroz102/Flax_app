# Generated by Django 3.2.6 on 2021-08-31 23:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pos', '0004_auto_20210830_1631'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='posingredientdata',
            options={'ordering': ('ingredient__pk', 'order_date', 'store'), 'verbose_name_plural': 'POS Ingredient Data List'},
        ),
    ]
