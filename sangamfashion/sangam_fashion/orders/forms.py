from django import forms
from django.core.exceptions import ValidationError
from .models import Order

class OrderForm(forms.ModelForm):
    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if any(char.isdigit() or not char.isalnum() for char in first_name):
            raise ValidationError("First name cannot contain special symbols or digits.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if any(char.isdigit() or not char.isalnum() for char in last_name):
            raise ValidationError("Last name cannot contain special symbols or digits.")
        return last_name

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not phone.isdigit() or len(phone) != 10:
            raise ValidationError("Phone number must be a 10-digit integer.")
        return phone

    def clean_pincode(self):
        pincode = self.cleaned_data['pincode']
        if not pincode.isdigit() or len(pincode) != 6:
            raise ValidationError("Pincode must be a 6-digit integer.")
        return pincode

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone', 'email', 'address_line_1', 'address_line_2', 'city', 'state', 'pincode']

