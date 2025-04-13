# ecommerce_app/views.py
from django.shortcuts import render

def homepage_view(request):
    return render(request, 'homepage.html')  

def login_view(request):
    return render(request, 'login.html') 

def logout_view(request):
    return render(request, 'logout.html')

def loggedout_view(request):
    return render(request, 'loggedout.html')
