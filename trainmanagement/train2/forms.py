from django import forms
from .models import Passenger, Ticket

class PassengerForm(forms.ModelForm):
    class Meta:
        model = Passenger
        fields = ['fullname', 'birth_date', 'email', 'gender', 'phone_number', 'occupation', 'nationality', 'city']

from django import forms
from .models import Ticket

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = [
            'journey_type', 'departure_station', 'arrival_station', 'departure_date', 'return_date', 
            'travel_class', 'number_of_passengers', 'full_name', 'dob', 'email', 'phone_number', 
            'gender', 'address', 'bedroll', 'number_of_bedrolls'
        ]
        widgets = {
            'journey_type': forms.Select(attrs={'id': 'journey_type', 'onchange': 'toggleJourneyDates()'}),
            'departure_station': forms.TextInput(attrs={'id': 'departure'}),
            'arrival_station': forms.TextInput(attrs={'id': 'arrival'}),
            'departure_date': forms.DateInput(attrs={'type': 'date', 'id': 'departure_date'}),
            'return_date': forms.DateInput(attrs={'type': 'date', 'id': 'return_date'}),
            'travel_class': forms.Select(attrs={'id': 'class'}),
            'number_of_passengers': forms.NumberInput(attrs={'id': 'number_of_passengers'}),
            'full_name': forms.TextInput(attrs={'id': 'full_name'}),
            'dob': forms.DateInput(attrs={'type': 'date', 'id': 'dob'}),
            'email': forms.EmailInput(attrs={'id': 'email'}),
            'phone_number': forms.TextInput(attrs={'id': 'phone_number'}),
            'gender': forms.Select(attrs={'id': 'gender'}),
            'address': forms.TextInput(attrs={'id': 'address'}),
            'bedroll': forms.Select(attrs={'id': 'bedroll'}),
            'number_of_bedrolls': forms.NumberInput(attrs={'id': 'number_of_bedrolls'}),
        }


from django.contrib.auth.models import User
from .models import staff

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

class StaffForm(forms.ModelForm):
    class Meta:
        model = staff
        fields = ['staff_type', 'phone_number', 'experience', 'country', 'city', 'languages', 'submission_date', 'submitted_registration']
        
from .models import Bed

class BedForm(forms.ModelForm):
    class Meta:
        model = Bed
        fields = ['bed_type', 'price', 'quantity', 'is_available']
