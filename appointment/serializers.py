from rest_framework import serializers

from appointment.models import Appointment
from userProfile.models import UserProfile


class CustomTimeField(serializers.TimeField):
    def to_representation(self, value):
        if value is None:
            return None
        return value.strftime('%H:%M:%S')


class AppointmentSerializer(serializers.ModelSerializer):
    instructor = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    student = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all(), required=False, allow_null=True)
    start_date = serializers.DateField(read_only=True)
    start_time = CustomTimeField(read_only=True)

    class Meta:
        model = Appointment
        fields = '__all__'

    def get_instructor(self, instance):
        instructor = instance.instructor
        return {
            'email': instructor.email,
            'first_name': instructor.user.first_name,
            'last_name': instructor.user.last_name,
            'driving_school': {
                'companyName': instructor.driving_school.companyName,
                'address': instructor.driving_school.address,
                'postal_code': instructor.driving_school.postal_code,
                'location_city': instructor.driving_school.location_city,
                'country': instructor.driving_school.country
        }
        }

    def get_student(self, instance):
        student = instance.student
        if student is None:
            return None
        return {
            'email': student.user.email,
            'first_name': student.user.first_name,
            'last_name': student.user.last_name,
        }

    def to_representation(self, instance):
        print(instance.instructor.id)
        representation = super().to_representation(instance)
        representation["instructor"] = self.get_instructor(instance)
        representation["student"] = self.get_student(instance)
        return representation
