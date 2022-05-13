from django.forms import ModelForm
from django import forms
from .models import Customer, Business, Guarantor


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        widgets = {
            'Dob': forms.TextInput(attrs={
                'placeholder': "yyyy/mm/dd",
            })}


class BusinessForm(ModelForm):
    class Meta:
        model = Business
        exclude = ['customer']


class GuarantorForm(ModelForm):
    class Meta:
        model = Guarantor
        exclude = ['customer']
