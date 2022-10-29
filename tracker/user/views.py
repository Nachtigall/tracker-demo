from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer


class UserDetailsView(APIView):
    permission_classes = (IsAuthenticated,)
    http_method_names = ["get"]

    def get(self, request):
        """
        Get all user details.
        """
        user = User.objects.get(pk=request.user.id)
        serializer = UserSerializer(user)
        return Response(serializer.data)
