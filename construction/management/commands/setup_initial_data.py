from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from construction.models import Material, Project, UserProfile
from django.utils import timezone
import datetime

class Command(BaseCommand):
    help = 'Sets up initial data for the construction app'

    def handle(self, *args, **kwargs):
        self.stdout.write('Setting up initial data...')
        
        # Create superuser if it doesn't exist
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123'
            )
            UserProfile.objects.create(user=admin)
            self.stdout.write(self.style.SUCCESS('Superuser created'))
        
        # Create materials
        materials = [
            {'name': 'Cement', 'category': 'Building Materials', 'unit': 'bags', 'min_quantity': 10},
            {'name': 'Sand', 'category': 'Building Materials', 'unit': 'tons', 'min_quantity': 5},
            {'name': 'Gravel', 'category': 'Building Materials', 'unit': 'tons', 'min_quantity': 5},
            {'name': 'Steel Rods', 'category': 'Metals', 'unit': 'pieces', 'min_quantity': 20},
            {'name': 'Bricks', 'category': 'Building Materials', 'unit': 'pieces', 'min_quantity': 100},
            {'name': 'Paint', 'category': 'Finishing', 'unit': 'gallons', 'min_quantity': 5},
            {'name': 'Tiles', 'category': 'Finishing', 'unit': 'boxes', 'min_quantity': 10},
            {'name': 'Wood', 'category': 'Carpentry', 'unit': 'pieces', 'min_quantity': 15},
        ]
        
        for material_data in materials:
            Material.objects.get_or_create(
                name=material_data['name'],
                defaults={
                    'category': material_data['category'],
                    'unit': material_data['unit'],
                    'min_quantity': material_data['min_quantity']
                }
            )
        
        self.stdout.write(self.style.SUCCESS('Materials created'))
        
        # Create projects
        projects = [
            {'name': 'Residential Building A', 'location': '123 Main St', 'start_date': timezone.now().date()},
            {'name': 'Commercial Complex B', 'location': '456 Business Ave', 'start_date': timezone.now().date()},
            {'name': 'Highway Extension', 'location': 'North County', 'start_date': timezone.now().date()},
        ]
        
        for project_data in projects:
            Project.objects.get_or_create(
                name=project_data['name'],
                defaults={
                    'location': project_data['location'],
                    'start_date': project_data['start_date']
                }
            )
        
        self.stdout.write(self.style.SUCCESS('Projects created'))
        self.stdout.write(self.style.SUCCESS('Initial data setup complete!'))