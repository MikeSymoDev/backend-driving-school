from django.urls import path

from vehicleImage.views import VehicleImageListCreateView, VehicleImageRetrieveUpdateDestroyView

urlpatterns = [
    path('<int:vehicle_id>', VehicleImageListCreateView.as_view(), name='vehicle-image-list-create'),
    path('vehicle/<int:vehicle_id>/image/<int:image_id>', VehicleImageRetrieveUpdateDestroyView.as_view(), name='vehicle-image-retrieve-update-destroy'),
]