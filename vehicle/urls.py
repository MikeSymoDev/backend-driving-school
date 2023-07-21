from django.urls import path, include

from vehicle.views import VehicleListCreateAPIView, VehicleRetrieveUpdateDeleteView, MyVehiclesListView

urlpatterns = [
    path('', VehicleListCreateAPIView.as_view()),
    path('<int:vehicle_id>', VehicleRetrieveUpdateDeleteView.as_view()),
    path('vehicle-image/', include('vehicleImage.urls')),
    path('my-vehicles/', MyVehiclesListView.as_view(), name='my-vehicles-list'),
]