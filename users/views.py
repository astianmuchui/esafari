from django.shortcuts import render

def loginpage(request):
    return render("login.html")

def homepage(request):
    return render(request, "home.html")
