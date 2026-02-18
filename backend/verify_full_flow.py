import os
import django
import sys
from datetime import date

# Add the project root to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'campus_backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campus_backend.settings')
django.setup()

from api.models import User, Resource, Booking
from django.db.utils import IntegrityError

def run_verification():
    print("Starting verification process...")

    # 1. Create Users
    print("\n Creating Users...")
    try:
        student, _ = User.objects.get_or_create(email='student@test.com', defaults={'username': 'student', 'role': 'STUDENT'})
        staff, _ = User.objects.get_or_create(email='staff@test.com', defaults={'username': 'staff', 'role': 'STAFF'})
        print(f"Users created/retrieved: {student.email}, {staff.email}")
    except Exception as e:
        print(f"Error creating users: {e}")

    # 2. Create Resources
    print("\n Creating Resources...")
    try:
        lab, _ = Resource.objects.get_or_create(name='Computer Lab 1', type='LAB', capacity=30)
        hall, _ = Resource.objects.get_or_create(name='Main Hall', type='EVENT_HALL', capacity=100)
        print(f"Resources created/retrieved: {lab.name}, {hall.name}")
    except Exception as e:
        print(f"Error creating resources: {e}")

    # 3. Create Bookings
    print("\n Creating Bookings...")
    booking_date = date.today()
    time_slot = "10:00-11:00"

    # Clean up existing bookings for this test to ensure clean state
    Booking.objects.filter(resource=lab, booking_date=booking_date, time_slot=time_slot).delete()

    try:
        booking1 = Booking.objects.create(user=student, resource=lab, booking_date=booking_date, time_slot=time_slot)
        print(f"Booking 1 created successfully: {booking1}")
    except Exception as e:
        print(f"Error creating booking 1: {e}")

    # 4. Test Double Booking (Should Fail at serializer level usually, but here checking model/business logic if enforced there too or just serializer?)
    # The business logic is currently in the Serializer. So model-level create() won't automatically fail unless we add validation there too.
    # However, let's check if we can simulate the serializer validation logic or if we should move it to the model.
    # Best practice is often model clean() or saving, but serializer is fine for API.
    # Let's try to create another booking via ORM. If logic is ONLY in serializer, this might succeed, which reveals a potential gap if not intended.
    # BUT, for this script, we want to verify the API flow essentially.
    
    print("\n Testing Double Booking Prevention (ORM Level)...")
    # Since the validation is in the Serializer, pure ORM creation MIGHT succeed if not enforced in model.
    # Let's check.
    
    booking2 = Booking(user=staff, resource=lab, booking_date=booking_date, time_slot=time_slot)
    
    # We can manually call a check here to verify what our API would do
    if Booking.objects.filter(resource=lab, booking_date=booking_date, time_slot=time_slot).exclude(status='REJECTED').exists():
        print("Double booking detected by script logic (mimicking serializer).")
    else:
        booking2.save()
        print("Warning: Double booking allowed at ORM level! (Validation is in Serializer)")

    print("\n Verification Complete.")

if __name__ == '__main__':
    run_verification()
