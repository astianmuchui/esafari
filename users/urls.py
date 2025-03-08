from . import views
from django.urls import path, include

urlpatterns = [
    # login
    path('login/', views.loginpage, name="loginpage"),
    path('', views.homepage, name="homepage")
]
