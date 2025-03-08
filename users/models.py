# models.py
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', User.ADMIN)
        
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    # User roles
    TENANT = 'tenant'
    PROVIDER = 'provider'
    ADMIN = 'admin'
    
    ROLE_CHOICES = [
        (TENANT, 'Tenant'),
        (PROVIDER, 'Provider'),
        (ADMIN, 'Admin'),
    ]
    
    username = None
    email = models.EmailField(_('email address'), unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=TENANT)
    
    # Common fields for all users
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    
    # Modify the groups and user_permissions fields to avoid conflicts
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='user_set_custom',  # Custom related_name
        blank=True,
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='user_set_custom',  # Custom related_name
        blank=True,
    )
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()
    
    def __str__(self):
        return self.email

class TenantProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='tenant_profile')
    driver_license_number = models.CharField(max_length=50)
    license_expiry_date = models.DateField()
    payment_method = models.CharField(max_length=50)
    
    def __str__(self):
        return f"Tenant: {self.user.email}"

class ProviderProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='provider_profile')
    company_name = models.CharField(max_length=100)
    business_license = models.CharField(max_length=50)
    tax_id = models.CharField(max_length=50)
    
    def __str__(self):
        return f"Provider: {self.company_name}"

class ElectricVehicle(models.Model):
    provider = models.ForeignKey(ProviderProfile, on_delete=models.CASCADE, related_name='vehicles')
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.IntegerField()
    license_plate = models.CharField(max_length=20)
    charge_capacity = models.FloatField()  # in kWh
    range = models.IntegerField()  # in miles/km
    hourly_rate = models.DecimalField(max_digits=6, decimal_places=2)
    is_available = models.BooleanField(default=True)
    location = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.year} {self.make} {self.model} - {self.license_plate}"

class Reservation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    tenant = models.ForeignKey(TenantProfile, on_delete=models.CASCADE, related_name='reservations')
    vehicle = models.ForeignKey(ElectricVehicle, on_delete=models.CASCADE, related_name='reservations')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_cost = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    
    def __str__(self):
        return f"{self.tenant.user.email} - {self.vehicle} - {self.start_time.date()}"
    
    def calculate_total_cost(self):
        duration = (self.end_time - self.start_time).total_seconds() / 3600  # in hours
        self.total_cost = self.vehicle.hourly_rate * duration
        return self.total_cost