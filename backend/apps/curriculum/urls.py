from django.urls import path

from . import views

urlpatterns = [
    path("modules/", views.ModuleListView.as_view(), name="module-list"),
    path("modules/<slug:slug>/", views.ModuleDetailView.as_view(), name="module-detail"),
    path(
        "modules/<slug:module_slug>/lessons/<slug:lesson_slug>/",
        views.LessonDetailView.as_view(),
        name="lesson-detail",
    ),
    path(
        "modules/<slug:module_slug>/lessons/<slug:lesson_slug>/exercises/<slug:exercise_slug>/",
        views.ExerciseDetailView.as_view(),
        name="exercise-detail",
    ),
    path("exercises/<int:exercise_id>/hint/", views.reveal_hint, name="reveal-hint"),
    path(
        "exercises/<int:exercise_id>/hints/",
        views.revealed_hints,
        name="revealed-hints",
    ),
    path(
        "lessons/<int:lesson_id>/complete/",
        views.mark_lesson_complete,
        name="mark-lesson-complete",
    ),
]
