from django.db import models
from django.db.models.deletion import SET_NULL

OUTLET_NAME_CHOISES = (
    ("TM", "Flax - Todi Mills"),
    ("P", "Flax - Powai"),
    ("B", "Flax - Bandra"),
)


class POSData(models.Model):
    outlet_name = models.CharField(max_length=2, choices=OUTLET_NAME_CHOISES)
    order_date = models.DateField()
    quantity = models.IntegerField(default=0)
    net_sell = models.FloatField(default=0)
    food_item = models.ForeignKey('FoodItem', on_delete=SET_NULL, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    # super_category = models.CharField(max_length=100, blank=True)
    # category = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.outlet_name}-order-{self.food_item.item_name}"

    class Meta:
        verbose_name_plural = "POS Data List"
        ordering = ('food_item__item_number', 'order_date', 'outlet_name')


class Ingredient(models.Model):
    ingredient_name = models.CharField(max_length=100)
    measuring_unit = models.CharField(max_length=30)
    date_created = models.DateTimeField(
        auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.ingredient_name


class FoodItem(models.Model):
    item_name = models.CharField(max_length=100)
    item_number = models.IntegerField(unique=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.item_name

    class Meta:
        ordering = ('item_number', 'pk')


class MenuItemRecipe(models.Model):
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.FloatField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.food_item.item_name}-{self.ingredient.ingredient_name}"


class POSIngredientData(models.Model):
    store = models.CharField(max_length=2, choices=OUTLET_NAME_CHOISES)
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.SET_NULL, null=True)
    order_date = models.DateField()
    quantity = models.FloatField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ingredient.ingredient_name

    class Meta:
        verbose_name_plural = "POS Ingredient Data List"
        ordering = ('ingredient__pk', 'order_date', 'store', )
