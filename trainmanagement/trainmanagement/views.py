from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404

def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def registration_form(request):
    return render(request, 'doctor_reg.html')

def contact(request):
    return render(request, 'contact.html')

def service(request):
    return render(request, 'service.html')

def price(request):
    return render(request, 'index.html') 