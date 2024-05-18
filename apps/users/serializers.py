from rest_framework import serializers


class AuthSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
