from rest_framework import serializers

from apps.main.models import (Content, Question, QuestionAnswer, Subject,
                              Topic, UserQuestionAnswer, UserTestProgress)


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
    chosen_answer = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = (
            "id",
            "topic",
            "text",
            "chosen_answer",
            "answers",
        )

    def get_chosen_answer(self, obj):
        request = self.context.get("request")
        if request:
            user = request.user
            user_question_answer = UserQuestionAnswer.objects.filter(user=user, question=obj).first()
            if user_question_answer:
                return {
                    "id": user_question_answer.answer.id,
                    "is_correct": user_question_answer.answer.is_correct,
                }
        return None


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = (
            "id",
            "topic",
            "title",
            "text",
            "photo",
            "photo_webp",
            "three_d_url",
            "three_d_file",
            "updated_at",
            "created_at",
        )


class UserTestProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTestProgress
        fields = (
            "user",
            "topic",
            "is_completed",
            "start_date",
            "end_date",
            "duration",
            "correct_answers",
            "gained_points",
            "updated_at",
            "created_at",
        )
        extra_kwargs = {
            "user": {"read_only": True},
            "topic": {"read_only": True},
            "is_completed": {"read_only": True},
            "end_date": {"read_only": True},
            "duration": {"read_only": True},
            "correct_answers": {"read_only": True},
            "gained_points": {"read_only": True},
        }


class UserQuestionAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserQuestionAnswer
        fields = (
            "user",
            "question",
            "answer",
        )
        extra_kwargs = {
            "user": {"read_only": True},
            "answer": {"required": True},
        }
