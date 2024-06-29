from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import logout
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from xhtml2pdf import pisa 
from io import BytesIO
from decimal import Decimal
from django.utils import timezone
from datetime import datetime
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from train2.models import Passenger, staff
import logging
from .forms import TicketForm
# from .forms import RoomForm
import os
import json
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from .models import Ticket
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        x = User.objects.create_user(username=username, first_name=firstname, last_name=lastname, email=email, password=password)
        x.save()
        print("user created successfully")
                
        subject = "welcome to Indianrail🚃"
        message = "Hello " + x.first_name + "!\n" + "Thank You for joining us!"
        from_email = settings.EMAIL_HOST_USER
        to_list = [x.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)
        
        return redirect('/')
    else:
        return render(request, 'login.html')

def loginform(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(request.method)
        print(username)
        print(password)
        
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect('/')  
        else:
            messages.error(request, 'Invalid email or password')
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')
    
# def profile(request):
#     if not request.user.is_authenticated:
#         return redirect('loginform')
#     return render(request, 'profile.html', {'user': request.user})

from django.shortcuts import render, redirect
from .models import Passenger
from .forms import PassengerForm

def passenger_register(request):
    if request.method == 'POST':
        form = PassengerForm(request.POST)
        if form.is_valid():
            passenger = form.save(commit=False)
            passenger.user = request.user  
            passenger.save()
            
            subject = "Welcome to Indianrail🚃"
            message = f"Hello {passenger.fullname}!\nThank you for register!❤️"
            from_email = settings.EMAIL_HOST_USER
            to_list = [passenger.email]
            send_mail(subject, message, from_email, to_list, fail_silently=True)
            
            return redirect('home') 
    else:
        form = PassengerForm()
    
    return render(request, 'passenger_registration.html', {'form': form})


def service(request):
    
    return render(request, 'service.html')

def ticketbooking(request):
    
    return render(request, 'ticket.html')

def price(request):
    return render(request, 'price.html')   


from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import staff
from .forms import StaffForm, UserForm

def staff_register(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        staff_form = StaffForm(request.POST)
        
        if user_form.is_valid() and staff_form.is_valid():
            # Create a new User instance
            user = user_form.save()
            
            # Create a new Staff instance linked to the user
            staff = staff_form.save(commit=False)
            staff.user = user  # Link the Staff instance to the User instance
            staff.save()
            
            return redirect('home')  # Redirect to a success page or another relevant page
    
    else:
        user_form = UserForm()
        staff_form = StaffForm()
    
    return render(request, 'staff_form.html', {'user_form': user_form, 'staff_form': staff_form})


@login_required
def book_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user  
            ticket.save()
            
            # Decrease the quantity of bed rolls booked
            bedroll_type = form.cleaned_data.get('bedroll')  # Assuming 'bedroll' is a field in TicketForm
            number_of_bedrolls = form.cleaned_data.get('number_of_bedrolls')  # Assuming 'number_of_bedrolls' is a field in TicketForm
            
            # Update the quantity in the Bed model
            bed = Bed.objects.get(bed_type=bedroll_type)
            if bed.quantity >= number_of_bedrolls:
                bed.quantity -= number_of_bedrolls
                bed.save()
            
            return redirect('home')  
    else:
        form = TicketForm()
    
    return render(request, 'ticket.html', {'form': form})

# views.py

from django.shortcuts import render
from .models import Notification

def message(request):
    unread_notifications_count = Notification.objects.filter(is_read=False).count()
    context = {
        'unread_notifications_count': unread_notifications_count
    }
    return render(request, 'home.html', context)


def profile(request, user_id):
    passenger = get_object_or_404(Passenger, user_id=user_id)
    tickets = Ticket.objects.filter(user_id=user_id)
    available_beds = Bed.objects.filter(is_available=True)  # Query available beds
    return render(request, 'profile.html', {'passenger': passenger, 'tickets': tickets, 'available_beds': available_beds})


def logout_view(request):
    logout(request)
    return redirect('/')



from django.shortcuts import render, redirect
from .models import Bed
from .forms import BedForm

def add_bed(request):
    if request.method == 'POST':
        form = BedForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bed_list')  # Redirect to a bed list page or another relevant page after adding bed
    else:
        form = BedForm()
    
    return render(request, 'add_bed.html', {'form': form})

@csrf_exempt
def update_bedroll(request, ticket_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            bedroll_count = data.get('number_of_bedrolls')
            if bedroll_count is None:
                return JsonResponse({'success': False, 'error': 'Bedroll count is missing'})

            ticket = Ticket.objects.get(id=ticket_id)
            ticket.number_of_bedrolls = bedroll_count
            ticket.save()
            return JsonResponse({'success': True})
        except Ticket.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Ticket not found'})
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})