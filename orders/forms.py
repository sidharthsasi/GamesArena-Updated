from dataclasses import field
from django import forms
from . models import order


class OrderForm(forms.ModelForm):
    class Meta:
        model = order
        fields = ['first_name','last_name','phone','email','address_line_1','address_line_2','country','state','city','order_note']
