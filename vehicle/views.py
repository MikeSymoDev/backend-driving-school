from django.shortcuts import render
from django.views import View
from rest_framework import permissions, status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.response import Response

from drivingSchool.permissions import IsOwnerOrReadOnly
from vehicle.models import Vehicle
from vehicle.serializers import VehicleSerializer


# Create your views here.
class VehicleListCreateAPIView(ListCreateAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(driving_instructor=self.request.user.user)


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request, so we'll always allow GET, HEAD, or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed if the requesting user is the driving instructor of the vehicle.
        return obj.driving_instructor.user == request.user


class VehicleRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    lookup_url_kwarg = "vehicle_id"
    permission_classes = [IsOwnerOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Vehicle deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

