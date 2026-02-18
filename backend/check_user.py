import os
import django
import sys
from django.contrib.auth import authenticate

# Add project root to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'campus_backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campus_backend.settings')
django.setup()

from api.models import User

def check_user():
    email = 'student@test.com'
    password = 'password123'
    
    print(f"Checking user: {email}")
    
    try:
        user = User.objects.get(email=email)
        print(f"User found: {user.username} (ID: {user.id})")
        print(f"Is active: {user.is_active}")
        
        # Check password manually
        if user.check_password(password):
            print("Password check: PASSED")
        else:
            print("Password check: FAILED")
            
        # Try full authentication
        auth_user = authenticate(email=email, password=password)
        if auth_user:
             print("Django Authentication: SUCCESS")
        else:
             print("Django Authentication: FAILED (authenticate returned None)")

    except User.DoesNotExist:
        print("User NOT FOUND in database.")

if __name__ == '__main__':
    check_user()
