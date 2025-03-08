from . import views
from django.urls import path

urlpatterns = [
    # login
    path('', views.homepage, name="homepage"),
    path('login/', views.loginpage, name="loginpage"),
]
