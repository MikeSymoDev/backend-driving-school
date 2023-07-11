from rest_framework import serializers

from drivingSchool.serializers import DrivingSchoolSerializer
from user.serializers import UserSerializer
from userProfile.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    driving_school = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = '__all__'

    def get_driving_school(self, instance):
        if instance.type == 'I':
            return DrivingSchoolSerializer(instance.driving_school, many=False).data
        else:
            return None

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["user"] = UserSerializer(instance.user, many=False).data
        representation["driving_school"] = self.get_driving_school(instance)
        return representation
