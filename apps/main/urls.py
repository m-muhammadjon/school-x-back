from django.urls import path

from apps.main import views

app_name = "main"

urlpatterns = [
    path("subjects/", views.SubjectListView.as_view(), name="subject-list"),
    path("subjects/<int:pk>/", views.SubjectRetrieveView.as_view(), name="subject-retrieve"),
    path("topics/", views.TopicListView.as_view(), name="topic-list"),
    path("topics/<int:pk>/", views.TopicRetrieveView.as_view(), name="topic-retrieve"),
    path("questions/", views.QuestionListView.as_view(), name="question-list"),
    path("contents/", views.ContentListView.as_view(), name="content-list"),
    path("contents/<int:pk>/", views.ContentRetrieveView.as_view(), name="content-retrieve"),
]
