# Generated by Django 3.2.6 on 2021-08-28 13:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FoodItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=100)),
                ('item_number', models.IntegerField(unique=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ingredient_name', models.CharField(max_length=100)),
                ('measuring_unit', models.CharField(max_length=30)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='MenuItemRecipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField(default=0)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('food_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pos.fooditem')),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pos.ingredient')),
            ],
        ),
    ]