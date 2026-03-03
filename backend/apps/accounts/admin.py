from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, UserExerciseProgress, UserLessonProgress, UserModuleProgress


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("username", "email", "total_xp", "current_belt", "current_streak")
    list_filter = ("is_staff", "is_active")
    fieldsets = BaseUserAdmin.fieldsets + (
        ("PyStarter", {"fields": ("bio", "total_xp", "current_streak", "longest_streak")}),
    )


@admin.register(UserModuleProgress)
class UserModuleProgressAdmin(admin.ModelAdmin):
    list_display = ("user", "module", "is_unlocked", "is_completed")
    list_filter = ("is_unlocked", "is_completed")


@admin.register(UserLessonProgress)
class UserLessonProgressAdmin(admin.ModelAdmin):
    list_display = ("user", "lesson", "is_completed")
    list_filter = ("is_completed",)


@admin.register(UserExerciseProgress)
class UserExerciseProgressAdmin(admin.ModelAdmin):
    list_display = ("user", "exercise", "is_completed", "xp_earned", "attempts")
    list_filter = ("is_completed",)
