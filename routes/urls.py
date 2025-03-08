from django.urls import path, include
from . import views


urlpatterns = [
    path('home/', views.home, name="Routes_Home"),
    path('street/', views.streetmap_api, name="Routes_Streetmap_API"),
    path('optimize/', views.optimization, name="Routes_Optimization"),
    path('geocode/', views.forward_geocode, name="Routes_Geocode"),

]

