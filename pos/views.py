import math

import time
import datetime
import csv
import json
import concurrent.futures  # for threading

from django.core.serializers import serialize
from django.core.paginator import Paginator

# To help with pagination
from django.http.response import Http404, HttpResponseForbidden, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, ListView
from django.contrib.auth.decorators import login_required
from pos.forms import IngredientModelForm
from .models import (
    OUTLET_NAME_CHOISES,
    Ingredient, MenuItemRecipe, FoodItem, POSData, POSIngredientData
)


# Helper function
def dateListSeperator(start_date_filter, end_date_filter):
    # TODO--Convert all date related operations to a seperate funcion
    start_date = datetime.date.fromisoformat(start_date_filter)
    end_date = datetime.date.fromisoformat(end_date_filter)
    noOfDays = (end_date - start_date).days + 1
    # print("noOfDays: ", noOfDays)

    dateList = []
    count_week = math.ceil(noOfDays/7)
    # Breaking no. of days to multiple of weeks
    for i in range(1, count_week+1):
        new_start_date = start_date + datetime.timedelta(days=(i-1)*7)
        new_end_date = start_date + datetime.timedelta(days=i*7-1)
        # print(new_end_date)
        if new_end_date < end_date:
            # print("new end date")
            dateStr = f"{new_start_date} - {new_end_date}"
        else:
            # print("end date")
            dateStr = f"{new_start_date} - {end_date}"

        dateList.append(dateStr)
    return [count_week, dateList]


class HomeView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        # # For tracking time
        # t1 = time.perf_counter()
        # t2 = time.perf_counter()
        # print(f'Finished in {t2-t1} seconds')
        context = {}
        # context['range'] = range(31)
        return render(self.request, 'pos/home_page.html', context)


# Food Item(menu item recipe) Point of sell data representation
class FoodItemPOSView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        start_date_filter = self.request.GET.get('start_date')
        end_date_filter = self.request.GET.get('end_date')
        store_filter = self.request.GET.get('store')

        if (start_date_filter is None or start_date_filter == "") or (
            end_date_filter is None or end_date_filter == "") or (
                store_filter is None or store_filter == ""):
            context = {
                "store_filter": store_filter,
                "start_date_filter": start_date_filter,
                "end_date_filter": end_date_filter,
                "dateList": [],  # for header
                "final_list": [],  # Food Item list
            }
            return render(self.request, 'pos/food_item_tab.html', context)

        start_date = datetime.date.fromisoformat(start_date_filter)
        # end_date = datetime.date.fromisoformat(end_date_filter)

        if end_date_filter:
            end_date_filter = end_date_filter.split('/')[0]

        dateListArr = dateListSeperator(start_date_filter, end_date_filter)
        dateList = dateListArr[1]
        count_week = dateListArr[0]
        # print(dateList)

        # posData = POSData.objects.all()
        x = POSData.objects.all()
        posData = []
        for i in range(10):
            posData.append(x[i])

        prevItemNumber = None
        final_list = []
        count = 0
        # print([0]*count_week)
        for orderItem in posData:
            store = orderItem.outlet_name
            if store_filter and store_filter != "" and store_filter != 'A':
                if store_filter != store:
                    continue

            currItemName = orderItem.food_item.item_name
            currItemNumber = orderItem.food_item.item_number
            ordered_date = orderItem.order_date
            item_qty = orderItem.quantity

            # list, size of count_week, initialize with 0
            valuesObjList = [0]*count_week
            # index to place in valueObjList
            noOfDayIndex = math.ceil(
                ((ordered_date - start_date).days + 1)/7) - 1

            # first case at index 0
            if prevItemNumber is None:
                final_list.append(
                    [currItemNumber, currItemName, valuesObjList])

                final_list[count][2][noOfDayIndex] += item_qty

                prevItemNumber = currItemNumber
            elif currItemNumber == prevItemNumber:
                final_list[count][2][noOfDayIndex] += item_qty
                prevItemNumber = currItemNumber
            else:
                count += 1
                final_list.append(
                    [currItemNumber, currItemName, valuesObjList])
                final_list[count][2][noOfDayIndex] += item_qty
                prevItemNumber = currItemNumber
        context = {
            "store_filter": store_filter,
            "start_date_filter": start_date_filter,
            "end_date_filter": end_date_filter,
            "dateList": dateList,  # for header
            "final_list": final_list,  # Food Item list
        }
        # print(final_list)
        return render(self.request, 'pos/food_item_tab.html', context)


# Ingredient Point of sell data representation
class IngredientPOSView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        start_date_filter = self.request.GET.get('start_date')
        end_date_filter = self.request.GET.get('end_date')
        store_filter = self.request.GET.get('store')

        if (start_date_filter is None or start_date_filter == "") or (
            end_date_filter is None or end_date_filter == "") or (
                store_filter is None or store_filter == ""):
            context = {
                "store_filter": store_filter,
                "start_date_filter": start_date_filter,
                "end_date_filter": end_date_filter,
                "dateList": [],  # for header
                "ingredient_list": [],  # Food Item list
            }
            return render(self.request, 'pos/ingredient_item_tab.html', context)

        start_date = datetime.date.fromisoformat(start_date_filter)
        # end_date = datetime.date.fromisoformat(end_date_filter)

        if (start_date_filter is None or end_date_filter is None) or (
                start_date_filter) == "" or end_date_filter == "":
            return redirect('pos:home')

        if end_date_filter:
            end_date_filter = end_date_filter.split('/')[0]

        posIngredientData = POSIngredientData.objects.all()

        # y = POSIngredientData.objects.all()
        # posIngredientData = []
        # for i in range(10):
        #     posIngredientData.append(y[i])

        dateListArr = dateListSeperator(start_date_filter, end_date_filter)
        # print(dateList)
        dateList = dateListArr[1]
        count_week = dateListArr[0]

        """ For Ingredient Item List """
        # ingredient qty according to order
        # Order of list/matrix len(posData)*len(allIngredientItem)
        # [[{"pk": 1, "name": "ham",...},{}, ...], [...], ...]
        ingredient_list = []
        prevIngredientPk = None
        count_x = 0

        for ingredientItem in posIngredientData:
            store = ingredientItem.store

            if store_filter and store_filter != "" and store_filter != 'A':
                if store_filter != store:
                    continue

            currIngredientName = ingredientItem.ingredient.ingredient_name
            currIngredientPk = ingredientItem.ingredient.pk
            ordered_date = ingredientItem.order_date
            ingredient_qty = ingredientItem.quantity

            valuesObjList = [0]*count_week
            # index to place in valueObjList
            noOfDayIndex = math.ceil(
                ((ordered_date - start_date).days + 1)/7) - 1

            # first case at index 0
            if prevIngredientPk is None:
                ingredient_list.append([
                    currIngredientPk,
                    currIngredientName,
                    store,
                    valuesObjList
                ])

                ingredient_list[count_x][3][noOfDayIndex] += ingredient_qty

                prevIngredientPk = currIngredientPk
            elif currIngredientPk == prevIngredientPk:
                ingredient_list[count_x][3][noOfDayIndex] += ingredient_qty
                prevIngredientPk = currIngredientPk
            else:
                count_x += 1
                ingredient_list.append([
                    currIngredientPk,
                    currIngredientName,
                    store,
                    valuesObjList
                ])
                ingredient_list[count_x][3][noOfDayIndex] += ingredient_qty
                prevIngredientPk = currIngredientPk
        # print("ingredient_list: ", ingredient_list)

        context = {
            "store_filter": store_filter,
            "start_date_filter": start_date_filter,
            "end_date_filter": end_date_filter,
            "dateList": dateList,  # for header
            "ingredient_list": ingredient_list,  # ingredient Item list
        }

        return render(self.request, 'pos/ingredient_item_tab.html', context)


class MenuItemRecipeView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        food_items = FoodItem.objects.all()
        ingredients = Ingredient.objects.all()
        # paginator = Paginator(food_items, 25)  # Show 25 contacts per page.

        # page_number = self.request.GET.get('page')

        # food item is menu items in restaurants
        # foodItems = paginator.get_page(page_number)

        context = {
            "foodItems": food_items,
            "ingredients": ingredients,
        }
        return render(self.request, 'pos/recipes.html', context)

    def post(self, *args, **kwargs):
        data = json.loads(self.request.body)
        # print("data: ", data)

        food_item_name = data.get('item_name')
        food_item_number = data.get('item_number')
        ingredient_list = data.get('ingredient_list')
        # print(f"{food_item_name}- {food_item_number}")
        newFoodItemObj = FoodItem.objects.create(
            item_name=food_item_name,
            item_number=food_item_number,
        )
        for ingredient_item in ingredient_list:
            ingredient_obj = Ingredient.objects.get(
                id=ingredient_item['ingridient_id'])
            MenuItemRecipe.objects.create(
                food_item=newFoodItemObj,
                ingredient=ingredient_obj,
                quantity=ingredient_item['quantity']
            )

        return JsonResponse({"msg": "Menu Item created successfully!!"})


class OrderListView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        orders = POSData.objects.all().order_by('-order_date')
        paginator = Paginator(orders, 50)  # Show 25 contacts per page.

        page_number = self.request.GET.get('page')

        orderItems = paginator.get_page(page_number)
        foodItems = FoodItem.objects.all()
        context = {
            "orders": orderItems,
            "stores": OUTLET_NAME_CHOISES,
            "foodItems": foodItems,
        }
        return render(self.request, 'pos/order_list.html', context)
    # template_name = 'pos/order_list.html'
    # queryset = POSData.objects.all().order_by('-order_date')
    # paginate_by = 50
    # # context_object_name Just works as context in FBV
    # # Or you have to change the name in template as context_obj
    # context_object_name = "orders"


# Retrieve order detail and update and delete order
class OrderView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        order_pk = kwargs.get('order_pk')
        try:
            order = POSData.objects.get(id=order_pk)
        except POSData.DoesNotExist:
            raise Http404()
        order_data = json.loads(serialize('json', [order]))

        return JsonResponse({
            "order_data": order_data,
            "stores": OUTLET_NAME_CHOISES,
        })

    def post(self, *args, **kwargs):
        order_pk = kwargs.get('order_pk')
        is_delete_request = self.request.GET.get('is_del')

        if is_delete_request:
            is_delete_request = is_delete_request.split('/')[0]

        try:
            order = POSData.objects.get(id=order_pk)
        except POSData.DoesNotExist:
            raise Http404()

        if is_delete_request is not None:
            if is_delete_request == '1':
                # print("deleted")
                order.delete()
                return redirect('pos:orders')
            else:
                return HttpResponseForbidden()
        else:  # update order
            order.outlet_name = self.request.POST.get('store_name')
            order.order_date = self.request.POST.get('order_date')
            order.quantity = self.request.POST.get('quantity')
            order.net_sell = self.request.POST.get('net_sell')

            order.save()
            # print("updated")

        return redirect('pos:orders')


# Display list of Ingredients and add a new ingredient
class IngredientListView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):  # Get ingredient list
        ingredients = Ingredient.objects.all()
        form = IngredientModelForm()
        context = {
            "ingredients": ingredients,
            "form": form,
        }
        return render(self.request, 'pos/ingredient_list.html', context)

    def post(self, *args, **kwargs):  # Add new ingredient
        # print("Post method")
        form = IngredientModelForm(self.request.POST)
        if form.is_valid():
            # print("form is valid")
            form.save()
        else:
            print("form is not valid")
        return redirect('pos:ingredients_list')


# Update/delete/retrieve ingredient data
class IngredientView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):  # fetch data of ingredients
        ingredient_pk = kwargs.get('ingredient_pk')
        # print("pk: ", ingredient_pk)
        try:
            ingredient = Ingredient.objects.get(id=ingredient_pk)
            data = serialize('json', [ingredient])

        except Ingredient.DoesNotExist:
            return JsonResponse({
                "Success": False,
                "msg": "Ingredient does not exists."
            }, 403)

        return JsonResponse({"Success": True, "ingredient_data": json.loads(data)})

    # Delete and update
    def post(self, *args, **kwargs):
        ingredient_pk = kwargs.get('ingredient_pk')
        is_delete_request = self.request.GET.get('is_del')

        newIngredientName = self.request.POST.get('ingredient_name')
        newUnit = self.request.POST.get('measuring_unit')

        try:
            ingredient = Ingredient.objects.get(id=ingredient_pk)
        except Ingredient.DoesNotExist:
            raise Http404()
        if is_delete_request:
            ingredient.delete()
        else:
            ingredient.ingredient_name = newIngredientName
            ingredient.measuring_unit = newUnit
            ingredient.save()
        return redirect('pos:ingredients_list')


# Retrieve Item recipe from MenuItem Model for View recipe function
def getItemRecipe(request, food_item_pk):
    if request.method == 'POST':
        # print("food_item_pk: ", food_item_pk)
        menuItemRecipeQS = MenuItemRecipe.objects.filter(
            food_item=food_item_pk)  # .values('ingredient', 'quantity')
        data = {
            "food_item": json.loads(serialize(
                'json', [menuItemRecipeQS[0].food_item])),
            'ingredients': []
        }
        for menuItemRecipe in menuItemRecipeQS:
            ingredientItem = json.loads(serialize(
                'json', [menuItemRecipe.ingredient]
                # .values('pk', 'ingredient_name', 'measuring_unit')
            ))

            data['ingredients'].append({
                "item": ingredientItem,
                "recipe_item": {
                    "pk": menuItemRecipe.pk,
                    "quantity": menuItemRecipe.quantity
                }
            })
        # print("data: ", data)
        # menuItemRecipe = serialize('json', menuItemRecipeQS)
        # json.loads(menuItemRecipe)

        return JsonResponse(data)


# update and delete menu item recipe
class IngredientInMenuItemRecipeView(LoginRequiredMixin, View):
    def post(self, *args, **kwargs):
        menu_item_pk = kwargs['menu_item_pk']
        is_delete_request = self.request.GET.get('is_del')

        try:
            menuItemObj = MenuItemRecipe.objects.get(id=menu_item_pk)
        except MenuItemRecipe.DoesNotExist:
            raise Http404()

        if is_delete_request:
            # print("deleted")
            menuItemObj.delete()
        else:
            ingredient_qty = json.loads(self.request.body).get('quantity')

            menuItemObj.quantity = ingredient_qty
            menuItemObj.save()

        return redirect('pos:recipes')


# def updateIngredientQuantity(request, menu_item_pk):
#     if request.method == 'POST':
#         # print("food_item_pk: ", food_item_pk)
#         # ingredient_pk = request.POST.get('ingredient')
#         ingredient_qty = json.loads(request.body).get('quantity')
#
#         menuItemObj = MenuItemRecipe.objects.get(id=menu_item_pk)
#
#         menuItemObj.quantity = ingredient_qty
#         menuItemObj.save()
#
#     return redirect('pos:recipes')
#
#     # return JsonResponse({"msg": "Ingredient Quantity updated"})

@login_required
def addIngredientToExistingMenu(request, food_item_pk):
    if request.method == 'POST':
        # print("POST DATA: ", request.POST)
        ingredient_pk = request.POST.get('ingredient')
        ingredient_qty = request.POST.get('quantity')
        # print(f"{ingredient_pk} - {ingredient_qty }")

        foodItem = FoodItem.objects.get(id=food_item_pk)
        ingredient_obj = Ingredient.objects.get(id=ingredient_pk)

        MenuItemRecipe.objects.create(
            food_item=foodItem,
            ingredient=ingredient_obj,
            quantity=ingredient_qty,
        )
    return redirect('pos:recipes')
    # return JsonResponse({"msg": "ingredient added"})


@login_required
def uploadOrderCsvFile(request):
    t3 = time.perf_counter()
    file_path = 'Enterprise_Daily_Item_Sales_Report.csv'
    with open(file_path, 'r') as csvfile:
        objList = []
        # creating a csv dictionary reader object
        csvDictReader = csv.DictReader(csvfile, delimiter=',')
        count = 0
        for obj in csvDictReader:
            objElem = {}
            objElem['order_date'] = obj['Date']
            objElem['item_number'] = obj['Item Number']
            if count <= 2716:
                objElem['outlet_name'] = "TM"
            elif count > 2716 and count <= 4751:
                objElem['outlet_name'] = "P"
            else:
                objElem['outlet_name'] = "B"
            if len(obj) == 10:
                objElem['quantity'] = list(obj.values())[7]
                objElem['net_sell'] = list(obj.values())[8]
                objElem['item_name'] = f"{list(obj.values())[6]},{list(obj.values())[6]}"
            else:
                objElem['quantity'] = obj['Qty']
                objElem['net_sell'] = obj['Net Sale']
                objElem['item_name'] = list(obj.values())[5]
            # print(net_sell)
            # if len(obj) == 10:
            # else:
            count += 1
            objList.append(objElem)

            # print(">>>>>>>>>>>>: ", count)
        print("All item saved: ", objList)
    t4 = time.perf_counter()
    print(f'Finished in {t4-t3} seconds')
    # item_number, item_name, outlet_name, order_date, quantity, net_sell

    def uploadDoc(objEl):
        t8 = time.perf_counter()
        c = 0
        try:
            food_item = FoodItem.objects.get(item_number=objEl['item_number'])
        except FoodItem.DoesNotExist:
            food_item = FoodItem.objects.create(
                item_number=objEl['item_number'],
                item_name=objEl['item_name']
            )
        POSData.objects.create(
            outlet_name=objEl['outlet_name'],
            order_date=objEl['order_date'],
            quantity=objEl['quantity'],
            net_sell=objEl['net_sell'],
            food_item=food_item,
        )
        menuRecipes = MenuItemRecipe.objects.filter(food_item=food_item)
        for menuRecipe in menuRecipes:
            POSIngredientData.objects.create(
                store=objEl['outlet_name'],
                ingredient=menuRecipe.ingredient,
                order_date=objEl['order_date'],
                quantity=int(objEl['quantity'])*menuRecipe.quantity,
            )
        t9 = time.perf_counter()
        print(f'count-{c}_Finished in {t9-t8} seconds')
        c += 1

    t1 = time.perf_counter()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(uploadDoc, objList)
    t2 = time.perf_counter()
    print(f'Finished in {t2-t1} seconds')
    return redirect('/')


@login_required
def deleteFoodMenu(request, food_menu_pk):
    if request.method == 'POST':
        try:
            foodItem = FoodItem.objects.get(id=food_menu_pk)
        except FoodItem.DoesNotExist:
            raise Http404()

        foodItem.delete()
        print("deleted")
        return redirect('pos:recipes')
