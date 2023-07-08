from rest_framework import serializers

from drivingSchool.models import DrivingSchool


class DrivingSchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = DrivingSchool
        fields = '__all__'
        # fields = ['id', 'title', 'cookbooks']
        read_only_fields = ['user']