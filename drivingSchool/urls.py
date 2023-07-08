from django.urls import path

from drivingSchool.views import ListCreateDrivingSchoolView

urlpatterns = [
    path('', ListCreateDrivingSchoolView.as_view())
]