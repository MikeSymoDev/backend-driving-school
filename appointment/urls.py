from django.urls import path

from appointment.views import AppointmentCreateAPIView, AppointmentRetrieveUpdateDeleteView, AppointmentByDateView, \
    SetAppointmentsUnavailableAPIView, SetSingleAppointmentUnavailableView

urlpatterns = [
    path('', AppointmentCreateAPIView.as_view(), name='booking-list'),
    path('not-available/', SetAppointmentsUnavailableAPIView.as_view(), name='not-available-many'),
    path('not-available/<int:pk>', SetSingleAppointmentUnavailableView.as_view(), name='not-available-single'),
    path('<int:pk>', AppointmentRetrieveUpdateDeleteView.as_view(), name='booking-detail'),
    path('by-date/', AppointmentByDateView.as_view())
]
