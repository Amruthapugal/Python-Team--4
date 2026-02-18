import os
import django
import sys
# Add the project root to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'campus_backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campus_backend.settings')
django.setup()

from api.models import User
from rest_framework.test import APIRequestFactory
from rest_framework_simplejwt.views import TokenObtainPairView
from api.views import UserViewSet

def verify_auth_flow():
    print("Starting Auth Flow Verification (Register -> Login)...")
    
    email = 'authtest@test.com'
    password = 'password123'
    username = 'authtest' # Since we use email as username in frontend logic often, but let's be distinct here to see.

    # 1. Cleanup
    User.objects.filter(email=email).delete()

    # 2. Register
    print("\n[Step 1] Registering User...")
    factory = APIRequestFactory()
    register_view = UserViewSet.as_view({'post': 'create'})
    
    reg_data = {
        'username': username,
        'email': email,
        'password': password,
        'name': 'Auth Test User',
        'role': 'STUDENT'
    }
    
    req = factory.post('/api/users/', reg_data, format='json')
    resp = register_view(req)
    
    if resp.status_code != 201:
        print(f"Registration Failed: {resp.status_code} - {resp.data}")
        return
    print("Registration Successful.")

    # 3. Login
    print("\n[Step 2] Logging in...")
    login_view = TokenObtainPairView.as_view()
    
    # Payload matching what verified_login.py found works (email key)
    login_data = {
        'email': email,
        'password': password
    }
    
    req = factory.post('/api/token/', login_data, format='json')
    resp = login_view(req)
    
    if resp.status_code == 200:
        print("Login Successful!")
        print(f"Token received: {resp.data.get('access')[:20]}...")
    else:
        print(f"Login Failed: {resp.status_code} - {resp.data}")
        
        # Debug: Check user in DB
        u = User.objects.get(email=email)
        print(f"User check: Email={u.email}, Username={u.username}, PasswordEncoded={u.password[:20]}...")
        print(f"Check password: {u.check_password(password)}")

if __name__ == '__main__':
    verify_auth_flow()
