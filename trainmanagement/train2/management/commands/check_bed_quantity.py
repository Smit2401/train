# train2/management/commands/check_bed_quantity.py

from django.core.management.base import BaseCommand
from train2.utils import check_bed_quantity

class Command(BaseCommand):
    help = 'Check bed quantity and send notifications if low.'

    def handle(self, *args, **kwargs):
        check_bed_quantity()
        self.stdout.write(self.style.SUCCESS('Bed quantity check completed.'))
