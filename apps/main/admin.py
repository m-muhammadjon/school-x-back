from django.contrib import admin
from unfold.admin import ModelAdmin, StackedInline, TabularInline

from apps.main import models


class TopicInline(StackedInline):
    model = models.Topic
    fields = (
        "title",
        "description",
        "photo",
        "photo_webp",
        "order",
    )
    extra = 0
    show_change_link = True


class ContentInline(StackedInline):
    model = models.Content
    fields = ("text", "photo", "photo_webp", "three_d_url", "three_d_file", "order")
    extra = 0
    show_change_link = True


class QuestionInline(StackedInline):
    model = models.Question
    fields = ("text", "order")
    extra = 0
    show_change_link = True


class QuestionAnswerInline(TabularInline):
    model = models.QuestionAnswer
    fields = ("text", "is_correct", "order")
    extra = 0
    show_change_link = True


@admin.register(models.Subject)
class SubjectAdmin(ModelAdmin):
    list_display = ("id", "title", "order")
    list_display_links = ("id", "title")
    list_editable = ("order",)
    inlines = (TopicInline,)


@admin.register(models.Topic)
class TopicAdmin(ModelAdmin):
    list_display = ("id", "subject", "title", "order")
    list_display_links = ("id", "subject")
    inlines = (QuestionInline, ContentInline)


@admin.register(models.Question)
class QuestionAdmin(ModelAdmin):
    list_display = ("id", "topic", "text", "order")
    list_display_links = ("id", "topic")
    list_editable = ("order",)
    inlines = (QuestionAnswerInline,)


@admin.register(models.Content)
class ContentAdmin(ModelAdmin):
    list_display = ("id", "topic", "order")
    list_display_links = ("id", "topic")
    list_editable = ("order",)
