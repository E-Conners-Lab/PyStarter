from django.urls import path

from . import views

urlpatterns = [
    path("hint/<int:exercise_id>/", views.ai_hint, name="ai-hint"),
    path("critique/<int:exercise_id>/", views.ai_critique, name="ai-critique"),
    path("explain-error/<int:exercise_id>/", views.explain_error, name="explain-error"),
]
