from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from userProfile.serializers import UserProfileSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Include additional data in the token payload
        profile = user.user
        token['loggedUser'] = UserProfileSerializer(profile).data

        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        profile = user.user
        data['loggedUser'] = UserProfileSerializer(profile).data
        return data
