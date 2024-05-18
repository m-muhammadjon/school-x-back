from django.db.models import Sum
from django.http import Http404
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError
from rest_framework.generics import (GenericAPIView, ListAPIView,
                                     RetrieveAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from . import serializers
from .models import (Content, Question, Subject, Topic, UserQuestionAnswer,
                     UserTestProgress)


class SubjectListView(ListAPIView):
    queryset = Subject.objects.all().order_by("order", "created_at")
    serializer_class = serializers.SubjectSerializer


class SubjectRetrieveView(RetrieveAPIView):
    queryset = Subject.objects.all()
    serializer_class = serializers.SubjectSerializer


class TopicListView(ListAPIView):
    queryset = Topic.objects.all().order_by("order", "created_at")
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("subject",)
    serializer_class = serializers.TopicSerializer


class TopicRetrieveView(RetrieveAPIView):
    queryset = Topic.objects.all()
    serializer_class = serializers.TopicSerializer


class QuestionListView(ListAPIView):
    queryset = Question.objects.all().order_by("order", "created_at")
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("topic",)
    serializer_class = serializers.QuestionSerializer


class QuestionRetrieveView(RetrieveAPIView):
    queryset = Question.objects.all()
    serializer_class = serializers.QuestionSerializer


class ContentListView(ListAPIView):
    queryset = Content.objects.all().order_by("order", "created_at")
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("topic",)
    serializer_class = serializers.ContentSerializer


class ContentRetrieveView(RetrieveAPIView):
    queryset = Content.objects.all()
    serializer_class = serializers.ContentSerializer


class UserTestProgressView(RetrieveAPIView):
    serializer_class = serializers.UserTestProgressSerializer
    queryset = UserTestProgress.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        user = self.request.user
        topic = self.kwargs.get("topic_id")
        return UserTestProgress.objects.filter(user=user, topic=topic).first()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance is None:
            raise Http404
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class UserTestProgressStartEndView(GenericAPIView):
    serializer_class = serializers.UserTestProgressSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = request.user
        topic_id = kwargs.get("topic_id")
        status = kwargs.get("status")
        if status == "start":
            if UserTestProgress.objects.filter(user=user, topic_id=topic_id).exists():
                instance = UserTestProgress.objects.filter(user=user, topic_id=topic_id).first()
            else:
                instance = UserTestProgress.objects.create(user=user, topic_id=topic_id)
        elif status == "finish":
            if not UserTestProgress.objects.filter(user=user, topic_id=topic_id).exists():
                raise Http404
            elif UserTestProgress.objects.filter(user=user, topic_id=topic_id, is_completed=True).exists():
                instance = UserTestProgress.objects.filter(user=user, topic_id=topic_id).first()
            else:
                instance = UserTestProgress.objects.filter(user=user, topic_id=topic_id).first()
                correct_answers = UserQuestionAnswer.objects.filter(
                    user=user, question__topic_id=topic_id, is_correct=True
                ).count()
                gained_points = correct_answers * 2
                now = timezone.now()
                duration = now - instance.start_date
                instance.is_completed = True
                instance.end_date = now
                instance.duration = duration
                instance.correct_answers = correct_answers
                instance.gained_points = gained_points
                instance.save()

                user.coin = UserTestProgress.objects.filter(user=user, is_completed=True).aggregate(
                    Sum("gained_points")
                )["gained_points__sum"]
                user.save()
        else:
            raise Http404
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class UserQuestionAnswerSubmitView(GenericAPIView):
    serializer_class = serializers.UserQuestionAnswerSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        question = serializer.validated_data["question"]
        answer = serializer.validated_data["answer"]
        if answer not in question.answers.all():
            raise Http404
        if not UserTestProgress.objects.filter(user=user, topic=question.topic).exists():
            raise ValidationError("User has not started the test yet.")
        if UserTestProgress.objects.filter(user=user, topic=question.topic, is_completed=True).exists():
            raise ValidationError("User has already finished the test.")
        obj, _ = UserQuestionAnswer.objects.update_or_create(
            user=user, question=question, defaults={"answer": answer, "is_correct": answer.is_correct}
        )
        return Response(self.get_serializer(obj).data)
