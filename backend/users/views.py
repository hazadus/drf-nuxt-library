from rest_framework import authentication, permissions
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CustomUser
from .serializers import CustomUserDetailSerializer


class AuthenticatedUserDetailView(APIView):
    """
    Return logged in user's detailed info.
    """

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def get(request: Request) -> Response:
        """
        Return logged in user's detailed info.
        """
        user = CustomUser.objects.filter(pk=request.user.pk).first()
        serializer = CustomUserDetailSerializer(user, many=False)
        return Response(serializer.data)
