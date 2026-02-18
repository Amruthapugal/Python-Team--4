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
from api.views import UserViewSet

def verify_registration():
    print("Starting registration verification...")
    
    # Cleanup previous test user if exists
    User.objects.filter(email='newuser@test.com').delete()

    factory = APIRequestFactory()
    view = UserViewSet.as_view({'post': 'create'})

    data = {
        'username': 'newuser',
        'email': 'newuser@test.com',
        'password': 'password123',
        'name': 'New User',
        'role': 'STUDENT'
    }

    request = factory.post('/api/users/', data, format='json')
    response = view(request)

    print(f"Response Status Code: {response.status_code}")
    if response.status_code == 201:
        print("Registration Successful!")
        user = User.objects.get(email='newuser@test.com')
        print(f"User created: {user.email}, Role: {user.role}")
    else:
        print("Registration Failed!")
        print(response.data)

if __name__ == '__main__':
    verify_registration()
