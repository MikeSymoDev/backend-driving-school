from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from drivingSchool.models import DrivingSchool
from drivingSchool.permissions import IsOwnerOrReadOnly
from drivingSchool.serializers import DrivingSchoolSerializer


# Create your views here.
class ListCreateDrivingSchoolView(ListCreateAPIView):
    queryset = DrivingSchool.objects.all()
    serializer_class = DrivingSchoolSerializer
    permission_classes = []


class RetrieveUpdateDeleteDrivingSchool (RetrieveUpdateDestroyAPIView):
    queryset = DrivingSchool.objects.all()
    serializer_class = DrivingSchoolSerializer
    lookup_url_kwarg = "driving_school_id"
    permission_classes = []
