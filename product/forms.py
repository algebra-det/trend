from django import forms
from .models import Product, ProductCategory, ProductRequest

from django.forms.models import inlineformset_factory

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class ProductCategoryForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = '__all__'

class ProductFullfillForm(forms.ModelForm):
    class Meta:
        model = ProductRequest
        fields = ['fullfilled']