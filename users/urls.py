from . import views
from django.urls import path

urlpatterns = [
    # login
    path('', views.home, name="home"),
    path('register/', views.register_view, name='register'),
    path('register/user/', views.register_user, name='register_user'),
    path('login/', views.login_view, name='login'),
    path('dashboard/tenant/', views.tenant_dashboard, name='tenant_dashboard'),
    path('add_vehicle/', views.add_vehicle, name='add_vehicle'),
    path('dashboard/provider/', views.provider_dashboard, name='provider_dashboard'),
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard')
]
