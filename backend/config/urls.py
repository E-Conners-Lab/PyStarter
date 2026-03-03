from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/accounts/", include("apps.accounts.urls")),
    path("api/v1/curriculum/", include("apps.curriculum.urls")),
    path("api/v1/submissions/", include("apps.submissions.urls")),
    path("api/v1/ai/", include("apps.ai.urls")),
]
