from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model for PyStarter."""

    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True, default="")
    total_xp = models.PositiveIntegerField(default=0)
    current_streak = models.PositiveIntegerField(default=0)
    longest_streak = models.PositiveIntegerField(default=0)
    last_activity_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Belt progression thresholds
    BELT_THRESHOLDS = [
        (0, "white", "White Belt"),
        (200, "yellow", "Yellow Belt"),
        (600, "orange", "Orange Belt"),
        (1500, "green", "Green Belt"),
        (3000, "blue", "Blue Belt"),
        (6000, "purple", "Purple Belt"),
        (10000, "brown", "Brown Belt"),
        (18000, "black", "Black Belt"),
    ]

    @property
    def current_belt(self):
        belt = "white"
        for threshold, belt_key, _ in self.BELT_THRESHOLDS:
            if self.total_xp >= threshold:
                belt = belt_key
        return belt

    @property
    def current_belt_display(self):
        for threshold, belt_key, display in self.BELT_THRESHOLDS:
            if self.total_xp >= threshold:
                result = display
        return result

    @property
    def next_belt_xp(self):
        for threshold, _, _ in self.BELT_THRESHOLDS:
            if self.total_xp < threshold:
                return threshold
        return None

    def award_xp(self, amount):
        self.total_xp += amount
        self.save(update_fields=["total_xp"])

    def update_streak(self):
        from django.utils import timezone

        today = timezone.now().date()
        if self.last_activity_date == today:
            return
        if self.last_activity_date and (today - self.last_activity_date).days == 1:
            self.current_streak += 1
        elif self.last_activity_date != today:
            self.current_streak = 1
        self.longest_streak = max(self.longest_streak, self.current_streak)
        self.last_activity_date = today
        self.save(update_fields=["current_streak", "longest_streak", "last_activity_date"])

    def __str__(self):
        return self.username


class UserModuleProgress(models.Model):
    """Tracks a user's progress through a curriculum module."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="module_progress")
    module = models.ForeignKey(
        "curriculum.Module", on_delete=models.CASCADE, related_name="user_progress"
    )
    is_unlocked = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("user", "module")

    def __str__(self):
        return f"{self.user.username} - {self.module.title}"


class UserLessonProgress(models.Model):
    """Tracks a user's progress through a lesson."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="lesson_progress")
    lesson = models.ForeignKey(
        "curriculum.Lesson", on_delete=models.CASCADE, related_name="user_progress"
    )
    is_completed = models.BooleanField(default=False)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("user", "lesson")

    def __str__(self):
        return f"{self.user.username} - {self.lesson.title}"


class UserExerciseProgress(models.Model):
    """Tracks a user's progress on an exercise."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="exercise_progress")
    exercise = models.ForeignKey(
        "curriculum.Exercise", on_delete=models.CASCADE, related_name="user_progress"
    )
    is_completed = models.BooleanField(default=False)
    best_code = models.TextField(blank=True, default="")
    xp_earned = models.PositiveIntegerField(default=0)
    attempts = models.PositiveIntegerField(default=0)
    hints_used = models.PositiveIntegerField(default=0)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("user", "exercise")

    def __str__(self):
        return f"{self.user.username} - {self.exercise.title}"
