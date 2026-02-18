from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User, Resource, Booking
from .serializers import UserSerializer, ResourceSerializer, BookingSerializer, CustomTokenObtainPairSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = User.objects.all()
        status_param = self.request.query_params.get('status', None)
        if status_param is not None:
            queryset = queryset.filter(status=status_param.upper())
        return queryset

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

class ResourceViewSet(viewsets.ModelViewSet):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            from .permissions import IsAdminOrStaffUser
            return [IsAdminOrStaffUser()]
        return [permissions.IsAuthenticated()]

from rest_framework.decorators import action
from .permissions import IsStaffUser

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Staff can see all bookings, Students only see their own
        # Staff/Admin can see all bookings, Students only see their own
        if user.role in ['STAFF', 'ADMIN'] or user.is_staff:
            return Booking.objects.all()
        return Booking.objects.filter(user=user)

    def perform_create(self, serializer):
        # Automatically assign the booking to the logged-in user
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsStaffUser])
    def approve(self, request, pk=None):
        booking = self.get_object()
        if booking.status != 'PENDING':
             return Response({'error': 'Booking is not pending'}, status=status.HTTP_400_BAD_REQUEST)
        
        booking.status = 'APPROVED'
        booking.save()
        return Response({'status': 'approved'})

    @action(detail=True, methods=['post'], permission_classes=[IsStaffUser])
    def reject(self, request, pk=None):
        booking = self.get_object()
        booking.status = 'REJECTED'
        booking.save()
        return Response({'status': 'rejected'})
