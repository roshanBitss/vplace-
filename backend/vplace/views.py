# vplace/views.py

from django.shortcuts import render

def login_page(request):
    return render(request, "login.html")

def home_page(request):
    return render(request, "home.html")

def job_page(request):
    return render(request, "job.html")

def event_page(request):
    return render(request, "event.html")

def test_page(request):
    return render(request, "test.html")

def profile_page(request):
    return render(request, "profile.html")

def logout(request):
    return render(request, "login.html")