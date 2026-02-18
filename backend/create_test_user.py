import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campus_backend.settings')
django.setup()

from api.models import User

if not User.objects.filter(email='test@example.com').exists():
    User.objects.create_user(username='testuser', email='test@example.com', password='password123', role='STUDENT')
    print("Test user created: test@example.com / password123")
else:
    print("Test user already exists.")
