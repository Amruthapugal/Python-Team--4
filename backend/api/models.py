from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('STUDENT', 'Student'),
        ('STAFF', 'Staff'),
        ('ADMIN', 'Admin'),
    )
    STATUS_CHOICES = (
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
    )
    
    name = models.CharField(max_length=255, default='')
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='STUDENT')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'name']

    def __str__(self):
        return self.email

class Resource(models.Model):
    TYPE_CHOICES = (
        ('LAB', 'Lab'),
        ('CLASSROOM', 'Classroom'),
        ('EVENT_HALL', 'Event Hall'),
    )
    STATUS_CHOICES = (
        ('AVAILABLE', 'Available'),
        ('UNAVAILABLE', 'Unavailable'),
    )
    
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    capacity = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='AVAILABLE')

    def __str__(self):
        return f"{self.name} ({self.type})"

class Booking(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='bookings')
    booking_date = models.DateField()
    time_slot = models.CharField(max_length=50) 
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.resource.name} ({self.booking_date} {self.time_slot})"
