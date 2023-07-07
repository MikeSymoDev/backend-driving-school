from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from user.serializers import UserSerializer


# Create your views here.
class SignUpView(GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = []
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # Perform any additional tasks after user creation
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
