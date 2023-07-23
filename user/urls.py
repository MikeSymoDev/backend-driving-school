from django.urls import path

from user.views import SignUpView, UpdateUserView

urlpatterns = [
    path('', SignUpView.as_view()),
]