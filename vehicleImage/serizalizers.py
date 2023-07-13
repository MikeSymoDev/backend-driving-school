from rest_framework import serializers

from vehicleImage.models import VehicleImage


class VehicleImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleImage
        fields = ['id', 'image', 'created', 'vehicle']