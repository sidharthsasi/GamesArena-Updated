from django import forms
from .models import Account,UserProfile


class Userform(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('first_name','last_name','phone_number')

class UserProfileForm(form.modelForm):
    class Meta:
        model = UserProfile
        fields = ('address_line_1','address_line_1','city','state','country','prifile_picture')
