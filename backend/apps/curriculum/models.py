from django.db import models


class Module(models.Model):
    """
    A top-level unit in the curriculum. Modules are strictly ordered
    and must be completed sequentially.

    Example modules:
    1. Your First Program
    2. Variables & Data Types
    3. Making Decisions (if/else)
    4. Loops
    5. Functions
    6. Lists & Tuples
    7. Dictionaries
    8. String Magic
    9. Writing Cleaner Code
    10. Python for Network Engineers
    11. Handling Errors
    12. User Input & While Loops
    13. Regular Expressions
    14. Building a Network Toolkit
    """

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    order = models.PositiveIntegerField(unique=True)
    icon = models.CharField(max_length=50, default="book")
    is_published = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.order}. {self.title}"

    @property
    def total_xp(self):
        return sum(e.xp_value for lesson in self.lessons.all() for e in lesson.exercises.all())

    @property
    def total_exercises(self):
        return sum(lesson.exercises.count() for lesson in self.lessons.all())


class Lesson(models.Model):
    """
    A lesson within a module. Each lesson teaches a concept and contains
    exercises for practice. Lessons are ordered within their module.

    Lesson types:
    - concept: Teaching content with examples (read-only, no code editor)
    - interactive: Teaching content with a live code sandbox to experiment
    - exercise: A graded exercise the user must complete
    """

    LESSON_TYPES = [
        ("concept", "Concept Lesson"),
        ("interactive", "Interactive Example"),
        ("exercise", "Exercise"),
    ]

    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    order = models.PositiveIntegerField(db_index=True)
    lesson_type = models.CharField(max_length=20, choices=LESSON_TYPES, default="concept")

    # Teaching content (Markdown)
    content = models.TextField(
        help_text="Markdown content for the lesson. Use code blocks for examples."
    )

    # Optional sandbox code for interactive lessons
    sandbox_code = models.TextField(
        blank=True,
        default="",
        help_text="Pre-loaded code for the interactive sandbox.",
    )

    is_published = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["module__order", "order"]
        unique_together = ("module", "slug")

    def __str__(self):
        return f"{self.module.title} > {self.title}"


class Exercise(models.Model):
    """
    A coding exercise within a lesson. Exercises are the graded components
    that users must pass to progress.

    Exercise types:
    - fill_blank: Code with blanks (___) the user fills in
    - fix_bug: Buggy code the user must fix
    - write_code: Write code from scratch to solve a problem
    - output_predict: Predict what the code will output (multiple choice)
    """

    EXERCISE_TYPES = [
        ("fill_blank", "Fill in the Blank"),
        ("fix_bug", "Fix the Bug"),
        ("write_code", "Write Code"),
        ("output_predict", "Predict the Output"),
    ]

    DIFFICULTY_CHOICES = [
        (1, "Starter"),
        (2, "Easy"),
        (3, "Medium"),
        (4, "Challenging"),
    ]

    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="exercises")
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    order = models.PositiveIntegerField(db_index=True)
    exercise_type = models.CharField(max_length=20, choices=EXERCISE_TYPES, default="write_code")
    difficulty = models.PositiveSmallIntegerField(choices=DIFFICULTY_CHOICES, default=1)

    # The problem description shown to the user
    instructions = models.TextField()

    # Starter code loaded into the editor
    starter_code = models.TextField(
        blank=True,
        default="",
        help_text="Code pre-loaded in the editor. Use # TODO comments for guidance.",
    )

    # The reference solution (not shown to user unless they use max hints)
    solution_code = models.TextField(
        blank=True,
        default="",
        help_text="The reference solution for this exercise.",
    )

    # For output_predict exercises: JSON list of choices
    choices = models.JSONField(
        null=True,
        blank=True,
        help_text='For output_predict: [{"label": "42", "is_correct": true}, ...]',
    )

    # XP and progression
    xp_value = models.PositiveIntegerField(default=10)
    concepts = models.CharField(
        max_length=300,
        blank=True,
        default="",
        help_text="Comma-separated Python concepts (e.g., 'variables, print, strings')",
    )

    is_published = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["lesson__module__order", "lesson__order", "order"]
        unique_together = ("lesson", "slug")

    def __str__(self):
        return f"{self.lesson.title} > {self.title}"


class TestCase(models.Model):
    """Test cases for validating exercise submissions."""

    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name="test_cases")
    input_data = models.TextField(
        blank=True,
        default="",
        help_text="Input to pass to the code (simulated stdin or function args).",
    )
    expected_output = models.TextField(
        help_text="Expected output (stdout or return value).",
    )
    is_hidden = models.BooleanField(
        default=False,
        help_text="Hidden test cases aren't shown to the user before submission.",
    )
    description = models.CharField(
        max_length=200,
        blank=True,
        default="",
        help_text="Human-readable description of what this test checks.",
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"Test for {self.exercise.title}: {self.description or self.expected_output[:50]}"


class Hint(models.Model):
    """Progressive hints for exercises, with increasing detail and XP penalties."""

    HINT_LEVELS = [
        (1, "Nudge", 0),       # No penalty - just a gentle push
        (2, "Concept", 10),    # 10% XP penalty - remind them of the concept
        (3, "Approach", 25),   # 25% - suggest an approach
        (4, "Walkthrough", 50),  # 50% - step by step walkthrough
        (5, "Solution", 100),  # 100% - show the answer
    ]

    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name="hints")
    level = models.PositiveSmallIntegerField(
        help_text="1=Nudge, 2=Concept, 3=Approach, 4=Walkthrough, 5=Solution"
    )
    content = models.TextField(help_text="Markdown hint content.")
    xp_penalty_percent = models.PositiveSmallIntegerField(
        default=0,
        help_text="Percentage of XP deducted when this hint is revealed.",
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["exercise", "level"]
        unique_together = ("exercise", "level")

    def __str__(self):
        level_name = dict((l, n) for l, n, _ in self.HINT_LEVELS).get(self.level, "Unknown")
        return f"{self.exercise.title} - {level_name}"
