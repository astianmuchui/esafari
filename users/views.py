from django.shortcuts import render

def loginpage(request):
    return render(request, "login.html")

def homepage(request):
    return render(request, "home.html")
