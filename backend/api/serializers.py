from rest_framework import serializers
from .models import User, Resource, Booking
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # Trim email/username and password before validation
        if 'email' in attrs:
            attrs['email'] = attrs['email'].strip()
        if 'password' in attrs:
            attrs['password'] = attrs['password'].strip()
            
        data = super().validate(attrs)
        
        # Add custom claims to the response data
        data['role'] = self.user.role
        data['name'] = self.user.name
        data['email'] = self.user.email
        
        return data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'email', 'phone', 'role', 'status', 'created_at', 'password']
        read_only_fields = ['id', 'created_at']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        # Trim inputs
        if 'email' in attrs:
            attrs['email'] = attrs['email'].strip().lower() # Normalize email
            attrs['username'] = attrs['email'] # Ensure username matches email
        if 'name' in attrs:
            attrs['name'] = attrs['name'].strip()
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    resource_name = serializers.CharField(source='resource.name', read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_name = serializers.CharField(source='user.name', read_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'user', 'user_email', 'user_name', 'resource', 'resource_name', 'booking_date', 'time_slot', 'status', 'created_at']
        read_only_fields = ['id', 'created_at', 'user', 'status', 'resource_name', 'user_email', 'user_name']

    def validate(self, data):
        # Business Rule: A resource cannot be double-booked for the same date and time slot.
        resource = data.get('resource')
        booking_date = data.get('booking_date')
        time_slot = data.get('time_slot')

        if Booking.objects.filter(resource=resource, booking_date=booking_date, time_slot=time_slot).exclude(status='REJECTED').exists():
            raise serializers.ValidationError("This resource is already booked for the selected date and time slot.")
        
        return data
