from django.urls import path

from . import views

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("token/refresh/", views.token_refresh, name="token-refresh"),
    path("me/", views.me, name="me"),
    path("progress/", views.progress_summary, name="progress-summary"),
    path("leaderboard/", views.leaderboard, name="leaderboard"),
    path("password-reset/", views.password_reset_request, name="password-reset"),
    path("password-reset-confirm/", views.password_reset_confirm, name="password-reset-confirm"),
]
