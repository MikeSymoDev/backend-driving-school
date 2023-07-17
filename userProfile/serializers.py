from rest_framework import serializers

from user.serializers import UserSerializer
from userProfile.models import UserProfile
from vehicle.serializers import VehicleSerializer


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


    def get_driving_school(self, instance):
        if instance.type == 'I':
            driving_school = instance.driving_school
            if driving_school is not None:
                return {
                    'id': driving_school.id,
                    'companyName': driving_school.companyName,
                    'address': driving_school.address,
                    'postal_code': driving_school.postal_code,
                    'location_city': driving_school.location_city,
                    'country': driving_school.country,
                }
        return None

    def get_vehicles(self, instance):
        if instance.type == 'I':
            vehicles = instance.vehicle.all()
            vehicle_serializer = VehicleSerializer(vehicles, many=True)
            return vehicle_serializer.data
        return []
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["user"] = UserSerializer(instance.user, many=False).data
        representation["driving_school"] = self.get_driving_school(instance)
        representation["vehicles"] = self.get_vehicles(instance)
        return representation
