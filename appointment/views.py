from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.response import Response

from rest_framework.views import APIView
from datetime import datetime, time, timedelta
from django.utils.timezone import make_aware
from rest_framework.generics import CreateAPIView
from .serializers import AppointmentSerializer
from .models import Appointment
from rest_framework.permissions import IsAuthenticated
from dateutil.relativedelta import relativedelta


# Create your views here.
class AppointmentCreateAPIView(CreateAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(instructor=self.request.user.user)

        start_date = serializer.initial_data['start_date']
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()

        # Get the logged-in user as the instructor
        instructor = self.request.user.user

        # Location is the Location of the logged user
        location = f'{instructor.address}, {instructor.postal_code} {instructor.location_city}, {instructor.country}'

        end_date = self.request.data.get('end_date')
        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        else:
            end_date = start_date + relativedelta(months=3)

        # Create appointments until the end date, ignoring dates with existing appointments for the instructor
        current_date = start_date
        while current_date <= end_date:
            if current_date.weekday() != 6:  # Exclude Sundays
                # Check if the instructor already has an appointment on the current date
                if not Appointment.objects.filter(instructor=instructor, date=current_date).exists():
                    start_time = datetime.combine(current_date, time(hour=8, minute=0))
                    end_time = datetime.combine(current_date, time(hour=17, minute=0))
                    time_slot = start_time

                    while time_slot <= end_time:
                        start_datetime = make_aware(time_slot)  # Convert start_time to aware datetime

                        # Check if an appointment already exists for the current date and time slot
                        if not Appointment.objects.filter(instructor=instructor, date=current_date,
                                                          start_time=start_datetime).exists():
                            # Create a new appointment instance
                            appointment = Appointment(
                                instructor=instructor,
                                location=location,
                                date=current_date,
                                start_time=start_datetime
                            )
                            appointment.save()  # Save the appointment

                        # Move to the next time slot
                        time_slot += timedelta(hours=1)

            # Move to the next day
            current_date += timedelta(days=1)

        # Delete appointments with null date field
        Appointment.objects.filter(date__isnull=True).delete()


class SetAppointmentsUnavailableAPIView(APIView):
    def post(self, request):
        # Get the instructor from the request user
        instructor = request.user.user

        # Get the start and end dates from the request data
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')

        # Get the appointments within the specified date range
        appointments = Appointment.objects.filter(
            instructor=instructor,
            date__range=[start_date, end_date]
        )

        updated_count = 0
        not_updated_count = 0
        booked_count = 0
        not_available_count = 0

        # Update the appointments to 'NA' (Not Available) status
        for appointment in appointments:
            if appointment.state == 'B':
                not_updated_count += 1
                booked_count += 1
            elif appointment.state == 'NA':
                not_updated_count += 1
                not_available_count += 1
            else:
                appointment.state = 'NA'
                appointment.save()
                updated_count += 1

        # Create the response message
        response_msg = f"{updated_count} appointments were set to not available."

        if not_updated_count > 0:
            response_msg += f" {not_updated_count} appointments could not be changed ({booked_count} already booked " \
                            f"and {not_available_count} already set to not available)."

        return Response({"message": response_msg}, status=status.HTTP_200_OK)


class SetSingleAppointmentUnavailableView(APIView):
    def patch(self, request, pk):
        try:
            appointment = Appointment.objects.get(pk=pk)
            instructor = appointment.instructor

            # Check if the appointment belongs to the instructor
            if instructor != request.user.user:
                return Response("You are not authorized to perform this action.", status=status.HTTP_401_UNAUTHORIZED)

            if appointment.state == 'NA':
                appointment.state = 'O'  # Set the appointment state to 'Open'
                appointment.save()
                return Response("Appointment set to 'Open'.", status=status.HTTP_200_OK)

            elif appointment.state == 'O':
                appointment.state = 'NA'  # Set the appointment state to 'Not Available'
                appointment.save()
                return Response("Appointment set to 'Not Available'.", status=status.HTTP_200_OK)

            return Response("Invalid appointment state.", status=status.HTTP_400_BAD_REQUEST)

        except Appointment.DoesNotExist:
            return Response("Appointment not found.", status=status.HTTP_404_NOT_FOUND)


class AppointmentRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

    def update(self, request, *args, **kwargs):
        # Get the appointment instance
        instance = self.get_object()

        # Check if the appointment is already booked
        if instance.state == 'B':
            return Response({"message": "Appointment is already booked."}, status=status.HTTP_400_BAD_REQUEST)

        # Get the student from the request user
        student = request.user.user

        # Check if the student is allowed to update the appointment
        if instance.student and instance.student != student:
            return Response({"message": "You are not authorized to update this appointment."},
                            status=status.HTTP_403_FORBIDDEN)

        else:
            instance.student = student
        # Update the appointment status to 'B' (Booked)
        instance.state = 'B'

        # Get the note from the request data
        notes = request.data.get('notes')
        if notes:
            instance.notes = notes

        # Save the updated appointment
        instance.save()

        return Response({"message": "Appointment status set to booked.", "data": AppointmentSerializer(instance).data},
                        status=status.HTTP_200_OK)


class AppointmentByDateView(ListAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        search = self.request.query_params.get('search')
        instructor_id = self.kwargs.get('instructor_id')  # Get the instructor ID from the URL

        if search is not None:
            # Filter appointments by date and instructor ID
            return Appointment.objects.filter(date__exact=search, instructor_id=instructor_id)

        return Appointment.objects.all()


class StudentAppointmentsView(ListAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user.user
        return Appointment.objects.filter(student=user, state='B')


class CancelAppointmentView(APIView):
    def patch(self, request, pk):
        try:
            appointment = Appointment.objects.get(pk=pk)
            student = appointment.student

            # Check if the appointment belongs to the student
            if student != request.user.user:
                return Response("You are not authorized to perform this action.",status=status.HTTP_401_UNAUTHORIZED)

            if appointment.state == 'B':
                appointment.state = 'O'  # Set the appointment state to 'Open'
                appointment.save()
                return Response(f"your Appointment (ID: {appointment.id}) with {appointment.instructor.email} is cancelled", status=status.HTTP_200_OK)

            return Response("Invalid appointment state.", status=status.HTTP_400_BAD_REQUEST)

        except Appointment.DoesNotExist:
            return Response("Appointment not found.", status=status.HTTP_404_NOT_FOUND)

class InstructorAppointmentsView(ListAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        instructor = self.request.user.user
        return Appointment.objects.filter(instructor=instructor)
