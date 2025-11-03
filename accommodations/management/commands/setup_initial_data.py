from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from accommodations.models import Location

class Command(BaseCommand):
    help = 'Setup initial data for StudentPA'
    
    def handle(self, *args, **options):
        # Create Landlords group
        landlord_group, created = Group.objects.get_or_create(name='Landlords')
        if created:
            self.stdout.write(self.style.SUCCESS('Successfully created Landlords group'))
        else:
            self.stdout.write(self.style.WARNING('Landlords group already exists'))
        
        # Create initial locations
        locations = [
            'Campus District', 'City Center', 'North Dlangville', 
            'South Dlangville', 'East Side', 'West End'
        ]
        
        for location_name in locations:
            loc, created = Location.objects.get_or_create(name=location_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created location: {location_name}'))
        
        self.stdout.write(self.style.SUCCESS('Successfully created initial locations'))