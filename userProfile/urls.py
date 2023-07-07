from django.urls import path

from userProfile.views import RetrieveUpdateDeleteUserProfile, SetupUserProfileView

urlpatterns = [
    path('setup/', SetupUserProfileView.as_view()),
    path('edit/<int:userProfile_id>', RetrieveUpdateDeleteUserProfile.as_view())
]