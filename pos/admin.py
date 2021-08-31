from django.contrib import admin
from . import models

admin.site.register(models.POSData)
admin.site.register(models.Ingredient)
admin.site.register(models.FoodItem)
admin.site.register(models.MenuItemRecipe)
admin.site.register(models.POSIngredientData)
