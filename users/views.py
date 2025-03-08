from django.shortcuts import render

def tenant_signuppage(request):
    return render(request, "tenant_signup.html")

def homepage(request):
    return render(request, "home.html")
def tenant_dashboard(request):
    return render(request, "tenant_dashboard.html")

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .models import User, TenantProfile, ProviderProfile
from .forms import (
    UserRegistrationForm, TenantProfileForm, 
    ProviderProfileForm, LoginForm
)

def home(request):
    return render(request, 'home.html')

def register_view(request):
    return render(request, 'register.html')

def register_user(request):
    if request.method == 'POST':
        role = request.POST.get('role')
        user_form = UserRegistrationForm(request.POST)
        
        if role == User.TENANT:
            profile_form = TenantProfileForm(request.POST)
        elif role == User.PROVIDER:
            profile_form = ProviderProfileForm(request.POST)
        else:
            # Invalid role
            return redirect('register')
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.role = role
            user.save()
            
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            
            # Log the user in
            login(request, user)
            
            # Redirect to appropriate dashboard
            if role == User.TENANT:
                return redirect('tenant_dashboard')
            elif role == User.PROVIDER:
                return redirect('provider_dashboard')
        
    else:
        role = request.GET.get('role', User.TENANT)
        user_form = UserRegistrationForm()
        
        if role == User.TENANT:
            profile_form = TenantProfileForm()
        else:
            profile_form = ProviderProfileForm()
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'selected_role': role
    }
    
    return render(request, 'register_user.html', context)

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            
            if user is not None:
                login(request, user)
                
                # Redirect based on user role
                if user.role == User.TENANT:
                    return redirect('tenant_dashboard')
                elif user.role == User.PROVIDER:
                    return redirect('provider_dashboard')
                elif user.role == User.ADMIN:
                    return redirect('admin_dashboard')
            else:
                form.add_error(None, "Invalid email or password")
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})

@login_required
def tenant_dashboard(request):
    if request.user.role != User.TENANT:
        return redirect('home')
    
    tenant = request.user.tenant_profile
    reservations = tenant.reservations.all()
    
    context = {
        'tenant': tenant,
        'reservations': reservations,
    }
    
    return render(request, 'tenant_dashboard.html', context)

@login_required
def provider_dashboard(request):
    if request.user.role != User.PROVIDER:
        return redirect('home')
    
    provider = request.user.provider_profile
    vehicles = provider.vehicles.all()
    
    context = {
        'provider': provider,
        'vehicles': vehicles,
    }
    
    return render(request, 'provider_dashboard.html', context)

@login_required
def admin_dashboard(request):
    if request.user.role != User.ADMIN:
        return redirect('home')
    
    tenants = TenantProfile.objects.all()
    providers = ProviderProfile.objects.all()
    
    context = {
        'tenants': tenants,
        'providers': providers,
    }
    
    return render(request, 'admin_dashboard.html', context)