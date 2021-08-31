from django import forms
from pos.models import Ingredient


class IngredientModelForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['ingredient_name', 'measuring_unit']

        widgets = {
            'ingredient_name': forms.TextInput(attrs={
                'type': 'text',
                'class': "form-control",
                'autofocus': 'autofocus',
            }),
            'measuring_unit': forms.TextInput(attrs={
                'type': 'text',
                'class': "form-control",
            }),
        }
