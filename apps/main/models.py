from django.db import models
from django.utils.translation import gettext_lazy as _
from django_resized import ResizedImageField

from apps.common.models import TimeStampedModel


class Subject(TimeStampedModel):
    title = models.CharField(_("Title"), max_length=255)
    photo = models.ImageField(_("Photo"), upload_to="subject_photos", blank=True, null=True)
    photo_webp = ResizedImageField("Photo .webp", upload_to="subject_photos", blank=True, null=True)
    order = models.IntegerField(_("Order"), default=0)

    class Meta:
        verbose_name = _("Subject")
        verbose_name_plural = _("Subjects")
        ordering = ("order", "-created_at")

    def __str__(self):
        return self.title


class Topic(TimeStampedModel):
    subject = models.ForeignKey(Subject, verbose_name=_("Subject"), on_delete=models.PROTECT, related_name="topics")
    title = models.CharField(_("Title"), max_length=255)
    description = models.TextField(_("Description"))
    photo = models.ImageField(_("Photo"), upload_to="topic_photos", blank=True, null=True)
    photo_webp = ResizedImageField("Photo .webp", upload_to="topic_photos", blank=True, null=True)
    order = models.IntegerField(_("Order"), default=0)

    class Meta:
        verbose_name = _("Topic")
        verbose_name_plural = _("Topics")
        ordering = ("order", "-created_at")

    def __str__(self):
        return self.title


class Question(TimeStampedModel):
    topic = models.ForeignKey(Topic, verbose_name=_("Topic"), on_delete=models.PROTECT, related_name="questions")
    text = models.TextField(_("Text"))
    order = models.IntegerField(_("Order"), default=0)

    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")
        ordering = ("order", "-created_at")

    def __str__(self):
        return self.text


class QuestionAnswer(TimeStampedModel):
    question = models.ForeignKey(Question, verbose_name=_("Question"), on_delete=models.CASCADE, related_name="answers")
    text = models.TextField(_("Text"))
    is_correct = models.BooleanField(_("Is correct"), default=False)
    order = models.IntegerField(_("Order"), default=0)

    class Meta:
        verbose_name = _("Question answer")
        verbose_name_plural = _("Question answers")
        ordering = ("order", "-created_at")

    def __str__(self):
        return self.text


class Content(TimeStampedModel):
    topic = models.ForeignKey(Topic, verbose_name=_("Topic"), on_delete=models.PROTECT, related_name="contents")
    text = models.TextField(_("Text"))
    photo = models.ImageField(_("Photo"), upload_to="content_photos", blank=True, null=True)
    photo_webp = ResizedImageField("Photo .webp", upload_to="content_photos", blank=True, null=True)
    three_d_url = models.URLField(_("3D URL"), blank=True, null=True)
    three_d_file = models.FileField(_("3D File"), upload_to="content_3d", blank=True, null=True)
    order = models.IntegerField(_("Order"), default=0)

    class Meta:
        verbose_name = _("Content")
        verbose_name_plural = _("Contents")
        ordering = ("order", "-created_at")

    def __str__(self):
        return f"Content for {self.topic.title}"


class UserTestProgress(TimeStampedModel):
    user = models.ForeignKey(
        "users.User", verbose_name=_("User"), on_delete=models.CASCADE, related_name="test_progress"
    )
    topic = models.ForeignKey(Topic, verbose_name=_("Topic"), on_delete=models.CASCADE, related_name="test_progress")
    is_completed = models.BooleanField(_("Is completed"), default=False)
    start_date = models.DateTimeField(_("Start date"), auto_now_add=True)
    end_date = models.DateTimeField(_("End date"), blank=True, null=True)
    duration = models.DurationField(_("Duration"), blank=True, null=True)
    correct_answers = models.IntegerField(_("Correct answers"), default=0)
    gained_points = models.IntegerField(_("Gained points"), default=0)

    class Meta:
        verbose_name = _("User test progress")
        verbose_name_plural = _("User test progresses")
        ordering = ("-created_at",)
        constraints = [models.UniqueConstraint(fields=["user", "topic"], name="unique_user_topic_test_progress")]


class UserQuestionAnswer(TimeStampedModel):
    user = models.ForeignKey(
        "users.User", verbose_name=_("User"), on_delete=models.CASCADE, related_name="question_answers"
    )
    question = models.ForeignKey(
        Question, verbose_name=_("Question"), on_delete=models.CASCADE, related_name="user_answers"
    )
    answer = models.ForeignKey(
        QuestionAnswer, verbose_name=_("Answer"), on_delete=models.CASCADE, related_name="user_answers", null=True
    )
    is_correct = models.BooleanField(_("Is correct"), default=False)

    class Meta:
        verbose_name = _("User question answer")
        verbose_name_plural = _("User question answers")
        ordering = ("-created_at",)
        constraints = [models.UniqueConstraint(fields=["user", "question"], name="unique_user_question_answer")]

    def save(self, *args, **kwargs):
        self.is_correct = self.answer.is_correct
        super().save(*args, **kwargs)
