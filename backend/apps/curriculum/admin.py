from django.contrib import admin

from .models import Exercise, Hint, Lesson, Module, TestCase


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 0
    fields = ("title", "slug", "order", "lesson_type", "is_published")


class ExerciseInline(admin.TabularInline):
    model = Exercise
    extra = 0
    fields = ("title", "slug", "order", "exercise_type", "difficulty", "xp_value", "is_published")


class TestCaseInline(admin.TabularInline):
    model = TestCase
    extra = 0
    fields = ("input_data", "expected_output", "description", "is_hidden", "order")


class HintInline(admin.TabularInline):
    model = Hint
    extra = 0
    fields = ("level", "content", "xp_penalty_percent")


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ("order", "title", "slug", "is_published")
    list_editable = ("is_published",)
    prepopulated_fields = {"slug": ("title",)}
    inlines = [LessonInline]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "module", "order", "lesson_type", "is_published")
    list_filter = ("module", "lesson_type", "is_published")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ExerciseInline]


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ("title", "lesson", "order", "exercise_type", "difficulty", "xp_value")
    list_filter = ("exercise_type", "difficulty", "lesson__module")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [TestCaseInline, HintInline]


@admin.register(TestCase)
class TestCaseAdmin(admin.ModelAdmin):
    list_display = ("exercise", "description", "is_hidden", "order")
    list_filter = ("is_hidden",)


@admin.register(Hint)
class HintAdmin(admin.ModelAdmin):
    list_display = ("exercise", "level", "xp_penalty_percent")
    list_filter = ("level",)
