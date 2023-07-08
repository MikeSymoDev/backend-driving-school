from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from user.models import User
from userProfile.models import UserProfile
from userProfile.serializers import UserProfileSerializer


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

        user.email = email
        user.gender = request.data.get('gender')
        user.type = request.data.get('type')
        user.address = request.data.get('address')
        user.postal_code = request.data.get('postal_code')
        user.location_city = request.data.get('location_city')
        user.country = request.data.get('country')
        user.about = request.data.get('about')
        user.profile_image = request.data.get('profile_image')
        user.instructor_license = request.data.get('instructor_license')
        user.driving_school = request.data.get('driving_school')
        user.has_learner_permit = request.data.get('has_learner_permit')
        user.phone = request.data.get('phone')
        user.save()

        return Response(self.get_serializer(user).data)


# View to Edit the UserProfile
class RetrieveUpdateDeleteUserProfile(RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = "userProfile_id"

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)

    def api_response(self, message, status_code=status.HTTP_200_OK):
        return Response({"message": message}, status=status_code)

    def destroy(self, request, *args, **kwargs):
        user_profile = self.get_object()

        # Delete the related DjangoUser instance
        django_user = user_profile.userprofile
        django_user.delete()

        # Delete the related RegistrationProfile instance if it exists
        registration_profile = django_user.registration_validation
        if registration_profile is not None:
            registration_profile.delete()

        # Delete the UserProfile instance
        self.perform_destroy(user_profile)

        return self.api_response("Profile deleted successfully", status.HTTP_204_NO_CONTENT)
