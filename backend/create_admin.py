import os
import django
import sys

# Add project root to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'campus_backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campus_backend.settings')
django.setup()

from api.models import User

def create_admin_user():
    email = 'admin@test.com'
    password = 'password123'
    name = 'System Admin'
    
    # Check if user exists
    if User.objects.filter(email=email).exists():
        print(f"User {email} already exists.")
        # Optional: ensure role is ADMIN
        u = User.objects.get(email=email)
        if u.role != 'ADMIN':
            u.role = 'ADMIN'
            u.save()
            print("Updated role to ADMIN.")
        return

    print(f"Creating admin user: {email}")
    user = User.objects.create_user(
        username=email,
        email=email,
        password=password,
        name=name,
        role='ADMIN'
    )
    user.is_staff = True
    user.is_superuser = True
    user.save()
    print("Admin user created successfully.")

if __name__ == '__main__':
    create_admin_user()
