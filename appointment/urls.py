from django.urls import path

from appointment.views import AppointmentCreateAPIView, AppointmentRetrieveUpdateDeleteView, AppointmentByDateView, \
    SetAppointmentsUnavailableAPIView, SetSingleAppointmentUnavailableView, StudentAppointmentsView, \
    CancelAppointmentView, InstructorAppointmentsView

urlpatterns = [
    path('', AppointmentCreateAPIView.as_view(), name='booking-list'),
    path('not-available/', SetAppointmentsUnavailableAPIView.as_view(), name='not-available-many'),
    path('not-available/<int:pk>', SetSingleAppointmentUnavailableView.as_view(), name='not-available-single'),
    path('<int:pk>', AppointmentRetrieveUpdateDeleteView.as_view(), name='booking-detail'),
    path('by-date/<int:instructor_id>/', AppointmentByDateView.as_view()),
    path('mybookings/', StudentAppointmentsView.as_view()),
    path('cancellation/<int:pk>', CancelAppointmentView.as_view(), name='cancel-booking'),
    path('me/instructor/', InstructorAppointmentsView.as_view(), name='instructor-appointments')
]
