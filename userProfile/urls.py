from django.urls import path

from userProfile.views import RetrieveUpdateDeleteUserProfile, SetupUserProfileView, InstructorListView, \
    InstructorDetailView

urlpatterns = [
    path('setup/', SetupUserProfileView.as_view()),
    path('me/edit/', RetrieveUpdateDeleteUserProfile.as_view()),
    path('instructors/', InstructorListView.as_view()),
    path('instructors/<int:userProfile_id>', InstructorDetailView.as_view()),
]