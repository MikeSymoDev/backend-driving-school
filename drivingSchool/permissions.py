from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow GET, HEAD, and OPTIONS requests
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True

        # Check if the requesting user is the owner of the DrivingSchool
        return obj.user == request.user