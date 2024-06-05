from django import forms
from django.core.exceptions import ValidationError
from .models import Account,UserProfile
import re

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter password',
        'class': 'form-control',
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter Confirm password',
        'class': 'form-control',
    }))

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter First Name'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter Last Name'})
        self.fields['phone_number'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter Phone Number'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter Email Address'})

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        # Password validation: Ensure it contains at least one special character and one digit
        if not re.search(r'^(?=.*[!@#$%^&*(),.?":{}|<>])(?=.*\d).+$', password):
            raise forms.ValidationError('Password must contain at least one special character and one digit.')

        # Password confirmation validation: Ensure passwords match
        if password != confirm_password:
            raise forms.ValidationError('Password and confirm password do not match.')

        # Additional validation for confirm password
        if not re.search(r'^(?=.*[!@#$%^&*(),.?":{}|<>])(?=.*\d).+$', confirm_password):
            raise forms.ValidationError('Confirm password must contain at least one special character and one digit.')



        # First name and last name validation: Ensure they contain only letters
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        if not first_name.isalpha():
            raise forms.ValidationError('First name must contain only letters.')
        if not last_name.isalpha():
            raise forms.ValidationError('Last name must contain only letters.')

        # Phone number validation: Ensure it contains exactly 10 digits
        phone_number = cleaned_data.get('phone_number')
        if not phone_number.isdigit() or len(phone_number) != 10:
            raise forms.ValidationError('Phone number must contain exactly 10 digits.')

        # Password confirmation validation: Ensure passwords match
        if password != confirm_password:
            raise forms.ValidationError('Password and confirm password do not match.')

        return cleaned_data

 

# class UserForm(forms.ModelForm):
#     class Meta:
#         model = Account
#         fields = ('first_name','last_name','email','phone_number')
#         def __init__(self, *args, **kwargs):
#            super(UserForm, self).__init__(*args, **kwargs)
#            for field in self.fields:
#                 self.fields[field].widget.attrs['class']='form-control'

# class UserProfileForm(forms.ModelForm):
#     profile_picture = forms.ImageField(required=False,error_messages = {'invalid':("Image files only")},widget=forms.FileInput)
#     class Meta:
#         model = UserProfile
#         fields = ('address_line_1','address_line_2','city','state','pincode','profile_picture')
#         def __init__(self, *args, **kwargs):
#            super(UserProfileForm, self).__init__(*args, **kwargs)
#            for field in self.fields:
#                 self.fields[field].widget.attrs['class']='form-control'

class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'email', 'phone_number')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not re.match(r'^[A-Za-z]+$', first_name):
            raise forms.ValidationError("First name can only contain alphabets.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not re.match(r'^[A-Za-z]+$', last_name):
            raise forms.ValidationError("Last name can only contain alphabets.")
        return last_name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
            raise forms.ValidationError("Please enter a valid email address.")
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not re.match(r'^\d{10}$', phone_number):
            raise forms.ValidationError("Phone number must be 10 digits.")
        return phone_number



# class UserProfileForm(forms.ModelForm):
#     class Meta:
#         model = UserProfile
#         fields = ('address_line_1', 'address_line_2', 'city', 'state', 'pincode', 'profile_picture')
#         widgets = {
#             'address_line_1': forms.TextInput(attrs={'class': 'form-control'}),
#             'address_line_2': forms.TextInput(attrs={'class': 'form-control'}),
#             'city': forms.TextInput(attrs={'class': 'form-control'}),
#             'state': forms.TextInput(attrs={'class': 'form-control'}),
#             'pincode': forms.TextInput(attrs={'class': 'form-control'}),
#             'profile_picture': forms.FileInput(attrs={'class': 'form-control-file'})  # Allow users to update profile picture
#         }
#     def clean_pincode(self):
#         pincode = self.cleaned_data.get('pincode')
#         if not re.match(r'^\d{6}$', pincode):
#             raise forms.ValidationError("Pincode must be 6 digits.")
#         return pincode

#     def clean_profile_picture(self):
#         profile_picture = self.cleaned_data.get('profile_picture')
        
#         # Check if a file is provided
#         if profile_picture:
#             # Check if the file is an instance of InMemoryUploadedFile or TemporaryUploadedFile
#             if hasattr(profile_picture, 'content_type'):
#                 content_type = profile_picture.content_type
#                 # Check if the file is an image
#                 if not content_type.startswith('image'):
#                     raise forms.ValidationError("Please upload a valid image file.")
#             else:
#                 # If profile_picture doesn't have content_type attribute, raise an error
#                 raise forms.ValidationError("Invalid file provided.")
            
#         return profile_picture
    

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('address_line_1', 'address_line_2', 'city', 'state', 'pincode', 'profile_picture')
        widgets = {
            'address_line_1': forms.TextInput(attrs={'class': 'form-control'}),
            'address_line_2': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'pincode': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control-file'})  # Allow users to update profile picture
        }
