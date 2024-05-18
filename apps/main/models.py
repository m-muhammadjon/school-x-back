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
