from django.urls import path, include
from . import views

urlpatterns = [
    path('home/', views.home, name="Routes_Home"),
    path('street/', views.streetmap_api, name="Routes_Streetmap_API"),

]
