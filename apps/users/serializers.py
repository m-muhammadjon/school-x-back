from django.db.models import Sum
from rest_framework import serializers

from apps.main.models import UserTestProgress

from .models import User


class AuthSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    quiz_activity = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "coin",
            "date_joined",
            "quiz_activity",
        )

    def get_quiz_activity(self, obj):
        activity = UserTestProgress.objects.filter(user=obj, is_completed=True).aggregate(Sum("duration"))[
            "duration__sum"
        ]
        return activity
