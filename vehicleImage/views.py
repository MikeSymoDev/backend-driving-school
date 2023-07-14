from rest_framework import permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.response import Response

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

        # Check if the current user is the driving instructor of the vehicle
        user = self.request.user.user
        if user != vehicle.driving_instructor:
            raise PermissionDenied("You are not allowed to upload images for this vehicle.")

        serializer.save(vehicle=vehicle)


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request, so we'll always allow GET, HEAD, or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed if the requesting user is the driving instructor of the vehicle.
        return obj.driving_instructor.user == request.user


class VehicleImageRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = VehicleImage.objects.all()
    serializer_class = VehicleImageSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_object(self):
        vehicle_id = self.kwargs['vehicle_id']
        image_id = self.kwargs['image_id']
        return VehicleImage.objects.get(vehicle_id=vehicle_id, id=image_id)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # Check if the requesting user is the owner of the vehicle
        vehicle_owner = instance.vehicle.driving_instructor.user
        if request.user != vehicle_owner:
            return Response({"message": "You are not authorized to delete this vehicle image."}, status=status.HTTP_403_FORBIDDEN)

        self.perform_destroy(instance)
        return Response({"message": "Vehicle image deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
