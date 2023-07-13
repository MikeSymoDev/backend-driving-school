from rest_framework import serializers

from vehicle.models import Vehicle
from vehicleImage.serizalizers import VehicleImageSerializer


class VehicleSerializer(serializers.ModelSerializer):
    vehicle_image = VehicleImageSerializer(many=True, read_only=True)

    class Meta:
        model = Vehicle
        fields = ['id', 'driving_instructor', 'make', 'model', 'year', 'transmission', 'fuel_type', 'vehicle_image']
        read_only_fields = ['driving_instructor']

