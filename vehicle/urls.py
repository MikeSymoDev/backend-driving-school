from django.urls import path, include

from vehicle.views import VehicleListCreateAPIView, VehicleRetrieveUpdateDeleteView

urlpatterns = [
    path('', VehicleListCreateAPIView.as_view()),
    path('<int:vehicle_id>', VehicleRetrieveUpdateDeleteView.as_view()),
    path('vehicle-image/', include('vehicleImage.urls'))
]