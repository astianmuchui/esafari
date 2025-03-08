# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, TenantProfile, ProviderProfile, ElectricVehicle

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, required=True)
    phone_number = forms.CharField(max_length=15, required=True)
    address = forms.CharField(widget=forms.Textarea, required=True)
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone_number', 
                  'address', 'password1', 'password2')

class TenantProfileForm(forms.ModelForm):
    driver_license_number = forms.CharField(max_length=50, required=True)
    license_expiry_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True)
    payment_method = forms.CharField(max_length=50, required=True)
    
    class Meta:
        model = TenantProfile
        fields = ('driver_license_number', 'license_expiry_date', 'payment_method')

class ProviderProfileForm(forms.ModelForm):
    company_name = forms.CharField(max_length=100, required=True)
    business_license = forms.CharField(max_length=50, required=True)
    tax_id = forms.CharField(max_length=50, required=True)
    
    class Meta:
        model = ProviderProfile
        fields = ('company_name', 'business_license', 'tax_id')

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    
class ElectricVehicleForm(forms.ModelForm):
    class Meta:
        model = ElectricVehicle    
        fields = ['make', 'model', 'year', 'license_plate', 'charge_capacity', 'range', 'hourly_rate', 'is_available', 'location']