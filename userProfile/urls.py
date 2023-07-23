from django.urls import path

from user.views import UpdateUserView
from userProfile.views import RetrieveUpdateDeleteUserProfile, SetupUserProfileView, InstructorListView, \
    InstructorDetailView, NearestInstructorsView

urlpatterns = [
    path('setup/', SetupUserProfileView.as_view()),
    path('me/edit/', RetrieveUpdateDeleteUserProfile.as_view()),
    path('instructors/', InstructorListView.as_view()),
    path('instructors/<int:userProfile_id>', InstructorDetailView.as_view()),
    path('nearest-instructors/', NearestInstructorsView.as_view(), name='nearest-instructors'),
    path('update-user/', UpdateUserView.as_view(), name='update_user'),
]