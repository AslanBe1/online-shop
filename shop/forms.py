from django import forms
from phonenumber_field.modelfields import PhoneNumberField

from shop.models import Product


class OrderForm(forms.Form):
    full_name = forms.CharField()
    phone_number = PhoneNumberField(region='UZ')
    quantity = forms.IntegerField()

class OrderModelForm(forms.ModelForm):
    pass


class CommentForm(forms.Form):
    full_name = forms.CharField()
    email = forms.EmailField()
    comment = forms.CharField(widget=forms.Textarea)

class CommentModelForm(forms.ModelForm):
    pass


class ProductModelForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
