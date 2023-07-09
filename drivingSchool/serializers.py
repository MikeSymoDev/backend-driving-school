from rest_framework import serializers

from drivingSchool.models import DrivingSchool


class DrivingSchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = DrivingSchool
        fields = '__all__'
        read_only_fields = ['user']
