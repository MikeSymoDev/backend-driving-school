from django.shortcuts import render
from django.views import View
from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView, GenericAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from user.models import User
from userProfile.models import UserProfile
from userProfile.serializers import UserProfileSerializer
from vehicle.serializers import VehicleSerializer

from math import sin, cos, sqrt, atan2, radians


# Create your views here.

# View to Setup a Profile
class SetupUserProfileView(GenericAPIView):
    permission_classes = []
    serializer_class = UserProfileSerializer

    def patch(self, request):
        email = request.data.get('email')

        user = User.objects.filter(email=email).first()
        if not user:
            return Response({'error': 'Invalid email'}, status=status.HTTP_400_BAD_REQUEST)

        user_profile = UserProfile.objects.filter(user=user).first()
        if not user_profile:
            return Response({'error': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)

        user_profile.email = email
        user_profile.gender = request.data.get('gender')
        user_profile.type = request.data.get('type')
        user_profile.address = request.data.get('address')
        user_profile.postal_code = request.data.get('postal_code')
        user_profile.location_city = request.data.get('location_city')
        user_profile.country = request.data.get('country')
        user_profile.about = request.data.get('about')
        user_profile.profile_image = request.data.get('profile_image')
        user_profile.instructor_license = request.data.get('instructor_license')
        user_profile.driving_school = request.data.get('driving_school')
        user_profile.has_learner_permit = request.data.get('has_learner_permit')
        user_profile.phone = request.data.get('phone')
        user_profile.save()

        return Response(self.get_serializer(user_profile).data)


# View to Edit the UserProfile
class RetrieveUpdateDeleteUserProfile(RetrieveUpdateDestroyAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.user

    def destroy(self, request, *args, **kwargs):
        user_profile = self.get_object()

        # Delete the related User instance
        user = user_profile.user
        user.delete()

        # Delete the UserProfile instance
        self.perform_destroy(user_profile)

        return Response(status=status.HTTP_204_NO_CONTENT)


# Get all the Instructors
class InstructorListView(ListAPIView):
    queryset = UserProfile.objects.filter(type='I')
    serializer_class = UserProfileSerializer
    permission_classes = []


# Get certain Instructor
class InstructorDetailView(RetrieveAPIView):
    queryset = UserProfile.objects.filter(type='I')
    serializer_class = UserProfileSerializer
    lookup_url_kwarg = 'userProfile_id'
    permission_classes = []

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data

        # Retrieve the associated vehicles
        vehicles = instance.vehicle.all()
        vehicle_serializer = VehicleSerializer(vehicles, many=True)
        data['vehicles'] = vehicle_serializer.data

        return Response(data)


class NearestInstructorsView(ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = []

    def get_queryset(self):
        search = self.request.query_params.get('search')


        if search is not None:
            # Filter appointments by date and instructor ID
            return UserProfile.objects.filter(postal_code__icontains=search, type="I")

        return UserProfile.objects.all()