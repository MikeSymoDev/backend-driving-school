from rest_framework import serializers

from drivingSchool.serializers import DrivingSchoolSerializer
from user.serializers import UserSerializer
from userProfile.models import UserProfile
from vehicle.serializers import VehicleSerializer


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["user"] = UserSerializer(instance.user, many=False).data
        representation["driving_school"] = DrivingSchoolSerializer(instance.driving_school, many=False).data
        # representation["liked_by_user"] = ThingsUserLikeSerializer(instance.liked_by_user, many=True).data
        return representation