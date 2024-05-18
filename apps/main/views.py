from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView, RetrieveAPIView

from apps.main import serializers
from apps.main.models import Subject, Topic, Question, Content


class SubjectListView(ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = serializers.SubjectSerializer


class SubjectRetrieveView(RetrieveAPIView):
    queryset = Subject.objects.all()
    serializer_class = serializers.SubjectSerializer


class TopicListView(ListAPIView):
    queryset = Topic.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("subject",)
    serializer_class = serializers.TopicSerializer


class TopicRetrieveView(RetrieveAPIView):
    queryset = Topic.objects.all()
    serializer_class = serializers.TopicSerializer


class QuestionListView(ListAPIView):
    queryset = Question.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("topic",)
    serializer_class = serializers.QuestionSerializer


class QuestionRetrieveView(RetrieveAPIView):
    queryset = Question.objects.all()
    serializer_class = serializers.QuestionSerializer


class ContentListView(ListAPIView):
    queryset = Content.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("topic",)
    serializer_class = serializers.ContentSerializer


class ContentRetrieveView(RetrieveAPIView):
    queryset = Content.objects.all()
    serializer_class = serializers.ContentSerializer
