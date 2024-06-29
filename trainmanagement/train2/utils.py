# utils.py

from .models import Bed, Notification
from django.utils import timezone

def check_bed_quantity():
    low_quantity_threshold = 5
    beds_below_threshold = Bed.objects.filter(quantity__lt=low_quantity_threshold, is_available=True)
    
    if beds_below_threshold.exists():
        message = f"Attention: There are only {beds_below_threshold.count()} beds left with quantity less than {low_quantity_threshold}."
        Notification.objects.create(message=message)
