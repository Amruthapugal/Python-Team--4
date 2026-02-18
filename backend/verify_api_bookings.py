import os
import django
import sys
# Add the project root to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'campus_backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campus_backend.settings')
django.setup()

from api.models import User, Resource, Booking
from rest_framework.test import APIRequestFactory, force_authenticate
from api.views import UserViewSet, BookingViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

def verify_api_bookings():
    print("Starting Booking API Verification...")
    
    # 1. Setup Data
    email = 'bookingtest@test.com'
    password = 'password123'
    # Clean up
    User.objects.filter(email=email).delete()
    Resource.objects.filter(name='Test Lab').delete()

    user = User.objects.create_user(username='bookingtest', email=email, password=password, role='STUDENT')
    resource = Resource.objects.create(name='Test Lab', type='LAB', capacity=10)
    
    print("User and Resource created.")

    # 2. Login to get token (simulating frontend)
    factory = APIRequestFactory()
    login_view = TokenObtainPairView.as_view()
    req = factory.post('/api/token/', {'email': email, 'password': password}, format='json')
    resp = login_view(req)
    
    if resp.status_code != 200:
        print(f"Login failed: {resp.data}")
        return
    
    token = resp.data['access']
    print("Login successful, token obtained.")

    # 3. Create Booking via API
    print("\n[Step 1] Creating Booking via API...")
    booking_view = BookingViewSet.as_view({'post': 'create'})
    booking_data = {
        'resource': resource.id,
        'booking_date': '2026-03-01',
        'time_slot': '10:00-11:00'
    }
    req = factory.post('/api/bookings/', booking_data, format='json')
    force_authenticate(req, user=user) # Use force_authenticate for simplicity with ViewSet
    resp = booking_view(req)

    if resp.status_code != 201:
        print(f"Booking creation failed: {resp.status_code} - {resp.data}")
    else:
        print(f"Booking created: ID {resp.data['id']}")

    # 4. List Bookings via API
    print("\n[Step 2] Listing Bookings via API...")
    list_view = BookingViewSet.as_view({'get': 'list'})
    req = factory.get('/api/bookings/')
    force_authenticate(req, user=user)
    resp = list_view(req)

    if resp.status_code == 200:
        print(f"Bookings found: {len(resp.data)}")
        if len(resp.data) == 1 and resp.data[0]['resource'] == resource.id:
            print("SUCCESS: Retrieved specific user booking.")
        else:
            print(f"FAILURE: Unexpected booking data: {resp.data}")
    else:
        print(f"Listing failed: {resp.status_code}")

if __name__ == '__main__':
    verify_api_bookings()
