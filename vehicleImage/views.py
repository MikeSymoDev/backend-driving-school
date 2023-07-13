from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from vehicle.models import Vehicle
from vehicleImage.models import VehicleImage
from vehicleImage.serizalizers import VehicleImageSerializer


# Create your views here.
class VehicleImageListCreateView(ListCreateAPIView):
    serializer_class = VehicleImageSerializer
    permission_classes = []

    def get_queryset(self):
        vehicle_id = self.kwargs['vehicle_id']
        return VehicleImage.objects.filter(vehicle_id=vehicle_id)

    def perform_create(self, serializer):
        vehicle_id = self.kwargs['vehicle_id']
        vehicle = Vehicle.objects.get(id=vehicle_id)
        serializer.save(vehicle=vehicle)


class VehicleImageRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = VehicleImage.objects.all()
    serializer_class = VehicleImageSerializer
    permission_classes = []

    def get_object(self):
        vehicle_id = self.kwargs['vehicle_id']
        image_id = self.kwargs['image_id']
        return VehicleImage.objects.get(vehicle_id=vehicle_id, id=image_id)