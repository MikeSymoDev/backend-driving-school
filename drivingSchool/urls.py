from django.urls import path

from drivingSchool.views import ListCreateDrivingSchoolView, RetrieveUpdateDeleteDrivingSchool

urlpatterns = [
    path('', ListCreateDrivingSchoolView.as_view()),
    path('<int:driving_school_id>', RetrieveUpdateDeleteDrivingSchool.as_view()),
]