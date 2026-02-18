import os
import django
import sys
import json
# Add the project root to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'campus_backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campus_backend.settings')
django.setup()

from api.models import User
from rest_framework.test import APIRequestFactory
from rest_framework_simplejwt.views import TokenObtainPairView

def verify_login():
    print("Starting login verification...")
    
    # Ensure test user exists
    email = 'verify_login@test.com'
    password = 'password123'
    if not User.objects.filter(email=email).exists():
        User.objects.create_user(username=email, email=email, password=password)
        print(f"Created test user: {email}")
    else:
        # Reset password to ensure it matches
        u = User.objects.get(email=email)
        u.set_password(password)
        u.save()
        print(f"Reset password for: {email}")

    factory = APIRequestFactory()
    view = TokenObtainPairView.as_view()

    # Test 1: Sending 'username' key
    print("\nTest 1: Sending 'username' key")
    data_username = {
        'username': email, # Even though it's an email, we send it as 'username' key
        'password': password
    }
    request = factory.post('/api/token/', data_username, format='json')
    response = view(request)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("Success with 'username' key")
    else:
        print("Failed with 'username' key")
        print(response.data)

    # Test 2: Sending 'email' key
    print("\nTest 2: Sending 'email' key")
    data_email = {
        'email': email,
        'password': password
    }
    request = factory.post('/api/token/', data_email, format='json')
    response = view(request)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("Success with 'email' key")
    else:
        print("Failed with 'email' key")
        print(response.data)

if __name__ == '__main__':
    verify_login()
