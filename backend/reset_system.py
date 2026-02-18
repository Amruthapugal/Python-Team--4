import os
import django
import sys
from django.core.management import call_command

# Add project root to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'campus_backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campus_backend.settings')
django.setup()

from api.models import User, Resource, Booking

def reset_system():
    print("WARNING: This will wipe all data from the database.")
    print("Flushing database...")
    call_command('flush', interactive=False)
    print("Database flushed.")

    print("Seeding initial data...")
    
    # Create Admin/Staff
    staff = User.objects.create_user(
        username='staff', 
        email='staff@test.com', 
        password='password123', 
        role='STAFF',
        name='Staff Member'
    )
    
    # Create Student
    student = User.objects.create_user(
        username='student', 
        email='student@test.com', 
        password='password123', 
        role='STUDENT',
        name='Test Student'
    )

    # Create Resources
    Resource.objects.create(name='Innovation Lab', type='LAB', capacity=30, status='AVAILABLE')
    Resource.objects.create(name='Main Auditorium', type='EVENT_HALL', capacity=200, status='AVAILABLE')
    Resource.objects.create(name='Conference Room A', type='CLASSROOM', capacity=15, status='AVAILABLE')

    print("\n--- System Reset Complete ---")
    print(f"Student User: {student.email} / password123")
    print(f"Staff User:   {staff.email} / password123")
    print("Resources created: 3")

if __name__ == '__main__':
    reset_system()
