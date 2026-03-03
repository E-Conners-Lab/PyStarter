from rest_framework import serializers

from .models import Exercise, Hint, Lesson, Module, TestCase


class HintSerializer(serializers.ModelSerializer):
    level_name = serializers.SerializerMethodField()

    class Meta:
        model = Hint
        fields = ("id", "level", "level_name", "content", "xp_penalty_percent")

    def get_level_name(self, obj):
        names = {1: "Nudge", 2: "Concept", 3: "Approach", 4: "Walkthrough", 5: "Solution"}
        return names.get(obj.level, "Unknown")


class TestCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCase
        fields = ("id", "input_data", "expected_output", "description", "is_hidden")


class ExerciseListSerializer(serializers.ModelSerializer):
    is_completed = serializers.SerializerMethodField()

    class Meta:
        model = Exercise
        fields = (
            "id",
            "title",
            "slug",
            "order",
            "exercise_type",
            "difficulty",
            "xp_value",
            "concepts",
            "is_completed",
        )

    def get_is_completed(self, obj):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return False
        return obj.user_progress.filter(user=request.user, is_completed=True).exists()


class ExerciseDetailSerializer(serializers.ModelSerializer):
    test_cases = serializers.SerializerMethodField()
    hints_available = serializers.SerializerMethodField()
    is_completed = serializers.SerializerMethodField()
    user_attempts = serializers.SerializerMethodField()

    class Meta:
        model = Exercise
        fields = (
            "id",
            "title",
            "slug",
            "order",
            "exercise_type",
            "difficulty",
            "instructions",
            "starter_code",
            "choices",
            "xp_value",
            "concepts",
            "test_cases",
            "hints_available",
            "is_completed",
            "user_attempts",
        )

    def get_test_cases(self, obj):
        visible = obj.test_cases.filter(is_hidden=False)
        return TestCaseSerializer(visible, many=True).data

    def get_hints_available(self, obj):
        return obj.hints.count()

    def get_is_completed(self, obj):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return False
        return obj.user_progress.filter(user=request.user, is_completed=True).exists()

    def get_user_attempts(self, obj):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return 0
        progress = obj.user_progress.filter(user=request.user).first()
        return progress.attempts if progress else 0


class LessonListSerializer(serializers.ModelSerializer):
    exercise_count = serializers.SerializerMethodField()
    is_completed = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = (
            "id",
            "title",
            "slug",
            "order",
            "lesson_type",
            "exercise_count",
            "is_completed",
        )

    def get_exercise_count(self, obj):
        return obj.exercises.count()

    def get_is_completed(self, obj):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return False
        return obj.user_progress.filter(user=request.user, is_completed=True).exists()


class LessonDetailSerializer(serializers.ModelSerializer):
    exercises = ExerciseListSerializer(many=True, read_only=True)
    is_completed = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = (
            "id",
            "title",
            "slug",
            "order",
            "lesson_type",
            "content",
            "sandbox_code",
            "exercises",
            "is_completed",
        )

    def get_is_completed(self, obj):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return False
        return obj.user_progress.filter(user=request.user, is_completed=True).exists()


class ModuleListSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    total_xp = serializers.IntegerField(read_only=True)
    is_unlocked = serializers.SerializerMethodField()
    is_completed = serializers.SerializerMethodField()
    progress_percent = serializers.SerializerMethodField()

    class Meta:
        model = Module
        fields = (
            "id",
            "title",
            "slug",
            "description",
            "order",
            "icon",
            "lesson_count",
            "total_xp",
            "is_unlocked",
            "is_completed",
            "progress_percent",
        )

    def get_lesson_count(self, obj):
        return obj.lessons.count()

    def get_is_unlocked(self, obj):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return obj.order == 1  # First module always shown as unlocked
        return obj.user_progress.filter(user=request.user, is_unlocked=True).exists()

    def get_is_completed(self, obj):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return False
        return obj.user_progress.filter(user=request.user, is_completed=True).exists()

    def get_progress_percent(self, obj):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return 0
        total_exercises = sum(
            lesson.exercises.filter(is_published=True).count()
            for lesson in obj.lessons.filter(is_published=True)
        )
        if total_exercises == 0:
            return 0
        completed = sum(
            1
            for lesson in obj.lessons.filter(is_published=True)
            for exercise in lesson.exercises.filter(is_published=True)
            if exercise.user_progress.filter(user=request.user, is_completed=True).exists()
        )
        return round((completed / total_exercises) * 100)


class ModuleDetailSerializer(serializers.ModelSerializer):
    lessons = LessonListSerializer(many=True, read_only=True)
    is_unlocked = serializers.SerializerMethodField()
    is_completed = serializers.SerializerMethodField()
    next_module = serializers.SerializerMethodField()

    class Meta:
        model = Module
        fields = (
            "id",
            "title",
            "slug",
            "description",
            "order",
            "icon",
            "lessons",
            "is_unlocked",
            "is_completed",
            "next_module",
        )

    def get_is_unlocked(self, obj):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return obj.order == 1
        return obj.user_progress.filter(user=request.user, is_unlocked=True).exists()

    def get_is_completed(self, obj):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return False
        return obj.user_progress.filter(user=request.user, is_completed=True).exists()

    def get_next_module(self, obj):
        next_mod = (
            Module.objects.filter(is_published=True, order__gt=obj.order)
            .order_by("order")
            .values("slug", "title")
            .first()
        )
        return next_mod
