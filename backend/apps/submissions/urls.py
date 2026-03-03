from django.urls import path

from . import views

urlpatterns = [
    path("sandbox/", views.sandbox_run, name="sandbox-run"),
    path("run/<int:exercise_id>/", views.run_code, name="run-code"),
    path("submit/<int:exercise_id>/", views.submit_code, name="submit-code"),
    path("history/<int:exercise_id>/", views.submission_history, name="submission-history"),
]
