from django.urls import path

from userProfile.views import RetrieveUpdateDeleteUserProfile, SetupUserProfileView, InstructorListView

urlpatterns = [
    path('setup/', SetupUserProfileView.as_view()),
    path('me/edit/', RetrieveUpdateDeleteUserProfile.as_view()),
    path('instructors/', InstructorListView.as_view())
]