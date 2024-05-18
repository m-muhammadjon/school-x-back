from django.utils.crypto import get_random_string
from rest_framework import status
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from . import serializers
from .models import User


class AuthView(GenericAPIView):
    serializer_class = serializers.AuthSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        name = serializer.validated_data["name"]
        user, _ = User.objects.get_or_create(first_name=name, defaults={"username": get_random_string(length=32)})
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        return Response(
            {
                "user_id": user.id,
                "name": user.first_name,
                "refresh": refresh_token,
                "access": access_token,
            },
            status=status.HTTP_200_OK,
        )


class UserRetrieveAPIView(RetrieveAPIView):
    serializer_class = serializers.UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user
