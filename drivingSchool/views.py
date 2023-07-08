from rest_framework.generics import ListCreateAPIView

from drivingSchool.models import DrivingSchool
from drivingSchool.serializers import DrivingSchoolSerializer


# Create your views here.
class ListCreateDrivingSchoolView(ListCreateAPIView):
    queryset = DrivingSchool.objects.all()
    serializer_class = DrivingSchoolSerializer