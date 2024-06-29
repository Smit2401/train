from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Passenger(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    fullname = models.CharField(max_length=100)
    birth_date = models.DateField()
    email = models.EmailField(max_length=30)
    gender = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=15)
    occupation =  models.CharField(max_length=30, null=True, blank=True)
    nationality = models.CharField(max_length=20, null=True, blank=True)
    city = models.TextField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return self.fullname 

from django.contrib.auth.models import User

class Ticket(models.Model):
    JOURNEY_TYPE_CHOICES = [
        ('single', 'Single Journey'),
        ('return', 'Return Journey'),
    ]

    CLASS_CHOICES = [
        ('first_class', 'First Class'),
        ('second_class', 'Second Class'),
        ('third_class', 'Third Class'),
        ('sleeper_class', 'Sleeper Class'),
    ]

    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    BEDROLL_CHOICES = [
        ('standard', 'Standard Bed Roll'),
        ('deluxe', 'Deluxe Bed Roll'),
        ('premium', 'Premium Bed Roll'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    journey_type = models.CharField(max_length=10, choices=JOURNEY_TYPE_CHOICES)
    departure_station = models.CharField(max_length=100)
    arrival_station = models.CharField(max_length=100)
    departure_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    travel_class = models.CharField(max_length=20, choices=CLASS_CHOICES)
    number_of_passengers = models.PositiveIntegerField()
    full_name = models.CharField(max_length=100)
    dob = models.DateField()
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    address = models.TextField()
    bedroll = models.CharField(max_length=20, choices=BEDROLL_CHOICES)
    number_of_bedrolls = models.PositiveIntegerField()
    bed = models.ForeignKey('Bed', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.full_name} - {self.departure_station} to {self.arrival_station}"

    
class staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    staff_type = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=15)
    experience = models.IntegerField()
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    languages = models.CharField(max_length=255)
    submission_date = models.DateField()
    submitted_registration = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.username
    
class Notification(models.Model):
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message

    
class Bed(models.Model):
    BEDROLL_CHOICES = [
        ('standard', 'Standard Bed Roll'),
        ('deluxe', 'Deluxe Bed Roll'),
        ('premium', 'Premium Bed Roll'),
    ]

    bed_type = models.CharField(max_length=20, choices=BEDROLL_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.bed_type} - {self.quantity} available"

