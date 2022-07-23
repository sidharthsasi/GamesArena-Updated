from django import forms
from .models import Category

class category_form(forms.ModelForm):
    
    class Meta:
        model = Category
        fields = ['category_name', 'slug', 'descriptions']