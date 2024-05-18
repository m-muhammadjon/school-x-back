from rest_framework import serializers

from apps.main.models import Content, Question, QuestionAnswer, Subject, Topic


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = (
            "id",
            "title",
            "photo",
            "photo_webp",
            "updated_at",
            "created_at",
        )


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = (
            "id",
            "subject",
            "title",
            "description",
            "photo",
            "photo_webp",
            "updated_at",
            "created_at",
        )


class QuestionAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionAnswer
        fields = (
            "id",
            "text",
        )


class QuestionSerializer(serializers.ModelSerializer):
    answers = QuestionAnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = (
            "id",
            "topic",
            "text",
            "answers",
        )


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = (
            "id",
            "topic",
            "text",
            "photo",
            "photo_webp",
            "three_d_url",
            "three_d_file",
            "updated_at",
            "created_at",
        )
