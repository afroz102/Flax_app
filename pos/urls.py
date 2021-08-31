from django.urls import path
from .views import (
    HomeView,
    IngredientView,
    MenuItemRecipeView,
    FoodItemPOSView,
    IngredientPOSView,
    OrderListView,
    IngredientListView,
    IngredientInMenuItemRecipeView,
    OrderView,
    deleteFoodMenu,
    getItemRecipe,
    addIngredientToExistingMenu,
    # updateIngredientQuantity,
    uploadOrderCsvFile,
    deleteFoodMenu,
)

app_name = 'pos'

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('pos/items/', FoodItemPOSView.as_view(), name="items_pos"),

    path(
        'pos/ingredients/',
        IngredientPOSView.as_view(),
        name="ingredients_pos"
    ),

    path('orders/', OrderListView.as_view(), name="orders"),

    path(
        'order-detail/<int:order_pk>/',
        OrderView.as_view(),
        name="order_detail"
    ),

    path(
        'ingredients-list/',
        IngredientListView.as_view(),
        name="ingredients_list"
    ),
    path(
        'ingredient-details/<int:ingredient_pk>/',
        IngredientView.as_view(),
        name="get_ingredient_details"
    ),

    path(
        'ingredient-in-menu-item-recipe/<int:menu_item_pk>/',
        IngredientInMenuItemRecipeView.as_view(),
        name="ingredient_in_menu_item_recipe"
    ),

    path('recipes/', MenuItemRecipeView.as_view(), name="recipes"),
    path('recipe/<int:food_item_pk>/', getItemRecipe, name="recipe"),

    path(
        'add-ingredient-to-menu/<int:food_item_pk>/',
        addIngredientToExistingMenu,
        name="add_ingredient_to_menu"
    ),
    #     path('update-ingredient-quantity/<int:menu_item_pk>/',
    #          updateIngredientQuantity, name="update_ingredient_quantity"),
    path('bulk-order-upload/', uploadOrderCsvFile, name="bulk_order_upload"),
    path('delete-food-menu/<int:food_menu_pk>/',
         deleteFoodMenu, name="delete_food_menu"),
]
