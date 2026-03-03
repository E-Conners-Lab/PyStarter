"""Seed the database with initial beginner Python curriculum."""

from django.core.management.base import BaseCommand

from apps.curriculum.models import Exercise, Hint, Lesson, Module, TestCase


class Command(BaseCommand):
    help = "Seeds the database with the initial PyStarter curriculum"

    def handle(self, *args, **options):
        if Module.objects.exists():
            self.stdout.write(self.style.WARNING("Curriculum already exists. Skipping seed."))
            return

        self.stdout.write("Seeding curriculum...")

        # === MODULES ===
        modules_data = [
            ("Your First Program", "your-first-program", "Write your very first lines of Python code! Learn how to make Python talk using the print() function.", "rocket"),
            ("Variables & Data Types", "variables-and-data-types", "Learn how to store information in variables — the building blocks of every program.", "box"),
            ("Making Decisions", "making-decisions", "Teach your programs to make choices using if, elif, and else statements.", "git-branch"),
            ("Loops", "loops", "Make Python repeat things for you using for loops and while loops.", "repeat"),
            ("Functions", "functions", "Create reusable blocks of code by writing your own functions.", "code"),
            ("Lists & Tuples", "lists-and-tuples", "Store collections of items and learn to work with ordered data.", "list"),
            ("Dictionaries", "dictionaries", "Store data as key-value pairs — like a real dictionary but for your code.", "book-open"),
            ("String Magic", "string-magic", "Master text manipulation — slicing, formatting, and transforming strings.", "type"),
            ("Writing Cleaner Code", "writing-cleaner-code", "Level up your Python with ternary expressions, comprehensions, the walrus operator, and other Pythonic patterns.", "wand"),
            ("Python for Network Engineers", "python-for-network-engineers", "Apply Python to real-world networking — parse IPs, read CLI output, and work with JSON device configs.", "network"),
        ]

        modules = {}
        for i, (title, slug, desc, icon) in enumerate(modules_data, 1):
            m = Module.objects.create(title=title, slug=slug, description=desc, order=i, icon=icon)
            modules[slug] = m
            self.stdout.write(f"  Module {i}: {title}")

        # === MODULE 1: Your First Program ===
        m1 = modules["your-first-program"]

        l1 = Lesson.objects.create(
            module=m1, title="What is Python?", slug="what-is-python", order=1,
            lesson_type="concept",
            content="""# Welcome to Python!

Python is one of the most popular programming languages in the world — and for good reason. It's designed to be **easy to read** and **fun to write**.

## Why Python?

- **It reads like English.** Python code looks almost like writing instructions for a human.
- **It's used everywhere.** Web apps, data science, AI, games, automation — Python does it all.
- **Huge community.** Millions of developers use Python, so help is always available.

## What does Python code look like?

Here's your first peek at Python:

```python
print("Hello, World!")
```

That's it! One line of code, and Python will display `Hello, World!` on the screen.

## How does it work?

1. You **write** code (instructions for the computer)
2. Python **reads** your code from top to bottom
3. It **executes** each instruction one at a time
4. You see the **result** on screen

Ready to write your first program? Let's go!""",
        )

        l2 = Lesson.objects.create(
            module=m1, title="The print() Function", slug="the-print-function", order=2,
            lesson_type="interactive",
            content="""# Talking to the World with print()

The `print()` function is how Python displays information on screen.

## How it works

```python
print("Hello, World!")
```

The text inside the quotes is called a **string**. Python displays whatever string you put inside `print()`.

## You can print anything!

```python
print("My name is Alex")
print("I am learning Python")
print("2 + 2 =", 2 + 2)
```

Output:
```
My name is Alex
I am learning Python
2 + 2 = 4
```

## Important rules

- Text must be wrapped in quotes: `"like this"` or `'like this'`
- The parentheses `()` are required
- Each `print()` starts a new line

## Try it yourself!

Use the code editor below to experiment!""",
            sandbox_code='# Try it out! Change the text and click Run\nprint("Hello, World!")\nprint("Python is awesome!")',
        )

        l3 = Lesson.objects.create(
            module=m1, title="Practice: print()", slug="practice-print", order=3,
            lesson_type="exercise",
            content="""# Time to Practice!

Complete the exercises below to master the `print()` function.

Remember:
- Text goes inside quotes: `print("your text")`
- Each `print()` creates a new line
- You can print multiple things: `print("Hello", "World")`""",
        )

        # Exercises for Module 1
        e1 = Exercise.objects.create(
            lesson=l3, title="Say Hello", slug="say-hello", order=1,
            exercise_type="fill_blank", difficulty=1,
            instructions='Complete the code below to print `Hello, World!` to the screen.',
            starter_code='# Complete the code to print Hello, World!\n___("Hello, World!")',
            solution_code='print("Hello, World!")',
            xp_value=10, concepts="print",
        )
        TestCase.objects.create(exercise=e1, expected_output="Hello, World!", description="Should print Hello, World!", order=1)
        Hint.objects.create(exercise=e1, level=1, content="The blank should be filled with a function that displays text on screen...", xp_penalty_percent=0)
        Hint.objects.create(exercise=e1, level=2, content="The function is called `print`. Replace the `___` with `print`.", xp_penalty_percent=10)

        e2 = Exercise.objects.create(
            lesson=l3, title="Print Your Name", slug="print-your-name", order=2,
            exercise_type="write_code", difficulty=1,
            instructions='Write a program that prints `My name is Python` on one line, then `I love coding!` on the next line.\n\nExpected output:\n```\nMy name is Python\nI love coding!\n```',
            starter_code='# Print two lines:\n# Line 1: My name is Python\n# Line 2: I love coding!\n',
            solution_code='print("My name is Python")\nprint("I love coding!")',
            xp_value=15, concepts="print, strings",
        )
        TestCase.objects.create(exercise=e2, expected_output="My name is Python\nI love coding!", description="Should print both lines", order=1)
        Hint.objects.create(exercise=e2, level=1, content="You'll need two `print()` statements — one for each line.", xp_penalty_percent=0)
        Hint.objects.create(exercise=e2, level=2, content='Make sure the text inside the quotes matches exactly: `"My name is Python"` and `"I love coding!"`', xp_penalty_percent=10)

        e3 = Exercise.objects.create(
            lesson=l3, title="Fix the Bug", slug="fix-the-bug", order=3,
            exercise_type="fix_bug", difficulty=1,
            instructions='The code below has a bug! It should print `Python is fun!` but something is wrong. Find and fix the error.',
            starter_code='# Fix the bug in this code\nprint("Python is fun!"',
            solution_code='print("Python is fun!")',
            xp_value=15, concepts="print, syntax, debugging",
        )
        TestCase.objects.create(exercise=e3, expected_output="Python is fun!", description="Should print Python is fun!", order=1)
        Hint.objects.create(exercise=e3, level=1, content="Look carefully at the parentheses. Is something missing?", xp_penalty_percent=0)
        Hint.objects.create(exercise=e3, level=2, content="The closing parenthesis `)` is missing at the end of the line.", xp_penalty_percent=10)

        e4 = Exercise.objects.create(
            lesson=l3, title="Math Printer", slug="math-printer", order=4,
            exercise_type="write_code", difficulty=1,
            instructions='Use `print()` to display the result of `7 * 8`.\n\nHint: You can do math inside print! For example: `print(2 + 3)` outputs `5`.\n\nExpected output:\n```\n56\n```',
            starter_code='# Print the result of 7 * 8\n',
            solution_code='print(7 * 8)',
            xp_value=10, concepts="print, math operations",
        )
        TestCase.objects.create(exercise=e4, expected_output="56", description="Should print 56", order=1)
        Hint.objects.create(exercise=e4, level=1, content="You can put math directly inside `print()`. For example: `print(2 + 3)` outputs `5`.", xp_penalty_percent=0)

        # === MODULE 2: Variables & Data Types ===
        m2 = modules["variables-and-data-types"]

        Lesson.objects.create(
            module=m2, title="What Are Variables?", slug="what-are-variables", order=1,
            lesson_type="concept",
            content="""# Variables: Storing Information

Imagine you have labeled boxes where you can store things. That's exactly what **variables** are in Python — named containers for storing data.

## Creating a Variable

```python
name = "Alice"
age = 25
height = 5.6
```

No special keywords needed. Just pick a name, use `=`, and assign a value.

## The `=` Sign

In Python, `=` doesn't mean "equals" like in math. It means **"store this value"**.

```python
score = 100  # Store 100 in 'score'
```

## Using Variables

```python
name = "Alice"
print(name)        # Output: Alice
print("Hi,", name) # Output: Hi, Alice
```

## Variable Naming Rules

- Must start with a letter or underscore: `name`, `_count`
- Can contain letters, numbers, underscores: `player_1`
- **Cannot** contain spaces or start with a number
- Case-sensitive: `Name` and `name` are different""",
        )

        Lesson.objects.create(
            module=m2, title="Data Types", slug="data-types", order=2,
            lesson_type="interactive",
            content="""# Data Types: What Kind of Data?

## Strings (str) — Text
```python
name = "Alice"
greeting = 'Hello!'
```

## Integers (int) — Whole Numbers
```python
age = 25
score = 1000
```

## Floats (float) — Decimal Numbers
```python
height = 5.9
price = 19.99
```

## Checking the Type
```python
print(type("hello"))  # <class 'str'>
print(type(42))       # <class 'int'>
print(type(3.14))     # <class 'float'>
```

Try it yourself in the editor!""",
            sandbox_code='name = "Alice"\nage = 25\nheight = 5.9\n\nprint(name, "is", age, "years old")\nprint("Height:", height)\nprint(type(name))\nprint(type(age))',
        )

        l6 = Lesson.objects.create(
            module=m2, title="Practice: Variables", slug="practice-variables", order=3,
            lesson_type="exercise",
            content="# Practice Time!\n\nPut your variable knowledge to the test.",
        )

        e5 = Exercise.objects.create(
            lesson=l6, title="Create a Variable", slug="create-a-variable", order=1,
            exercise_type="write_code", difficulty=1,
            instructions='Create a variable called `message` and set it to `"Hello, Python!"`. Then print the variable.\n\nExpected output:\n```\nHello, Python!\n```',
            starter_code='# Create a variable called message and print it\n',
            solution_code='message = "Hello, Python!"\nprint(message)',
            xp_value=10, concepts="variables, print, strings",
        )
        TestCase.objects.create(exercise=e5, expected_output="Hello, Python!", description="Should print Hello, Python!", order=1)
        Hint.objects.create(exercise=e5, level=1, content='First create the variable: `message = "Hello, Python!"`. Then on the next line, print it.', xp_penalty_percent=0)

        e6 = Exercise.objects.create(
            lesson=l6, title="Math with Variables", slug="math-with-variables", order=2,
            exercise_type="write_code", difficulty=2,
            instructions='Create two variables: `width` set to `10` and `height` set to `5`. Then print their product (width times height).\n\nExpected output:\n```\n50\n```',
            starter_code='# Create width and height variables\n# Then print width * height\n',
            solution_code='width = 10\nheight = 5\nprint(width * height)',
            xp_value=15, concepts="variables, math, print",
        )
        TestCase.objects.create(exercise=e6, expected_output="50", description="Should print 50", order=1)
        Hint.objects.create(exercise=e6, level=1, content="Use `*` for multiplication in Python. For example: `print(3 * 4)` outputs `12`.", xp_penalty_percent=0)

        e7 = Exercise.objects.create(
            lesson=l6, title="Predict the Output", slug="predict-the-output", order=3,
            exercise_type="output_predict", difficulty=1,
            instructions='What will this code print?\n\n```python\nx = 5\ny = 3\nx = x + y\nprint(x)\n```',
            choices=[
                {"label": "5", "is_correct": False},
                {"label": "3", "is_correct": False},
                {"label": "8", "is_correct": True},
                {"label": "Error", "is_correct": False},
            ],
            xp_value=10, concepts="variables, reassignment, math",
        )

        e8 = Exercise.objects.create(
            lesson=l6, title="Introduction Card", slug="introduction-card", order=4,
            exercise_type="write_code", difficulty=2,
            instructions='Create three variables:\n- `name` set to `"Sam"`\n- `age` set to `20`\n- `city` set to `"Austin"`\n\nThen print them in this exact format:\n```\nName: Sam\nAge: 20\nCity: Austin\n```',
            starter_code='# Create the three variables\n\n\n# Print them in the right format\n',
            solution_code='name = "Sam"\nage = 20\ncity = "Austin"\nprint("Name:", name)\nprint("Age:", age)\nprint("City:", city)',
            xp_value=20, concepts="variables, print, strings, formatting",
        )
        TestCase.objects.create(exercise=e8, expected_output="Name: Sam\nAge: 20\nCity: Austin", description="Should print the formatted introduction card", order=1)
        Hint.objects.create(exercise=e8, level=1, content='Use commas in print to combine text and variables: `print("Label:", variable)`', xp_penalty_percent=0)
        Hint.objects.create(exercise=e8, level=2, content='You need three print statements. Each one starts with the label (like `"Name:"`) followed by a comma and the variable.', xp_penalty_percent=10)

        # === MODULE 3: Making Decisions ===
        m3 = modules["making-decisions"]

        Lesson.objects.create(
            module=m3, title="What Are Conditionals?", slug="what-are-conditionals", order=1,
            lesson_type="concept",
            content="""# Making Decisions with Code

Programs need to make decisions, just like you do every day. *If* it's raining, bring an umbrella. *Otherwise*, wear sunglasses.

## The `if` Statement

```python
temperature = 35

if temperature > 30:
    print("It's hot outside!")
```

The code inside the `if` block only runs when the condition is `True`.

## `if` / `else`

```python
age = 15

if age >= 18:
    print("You can vote!")
else:
    print("Too young to vote.")
```

## `if` / `elif` / `else`

Use `elif` (short for "else if") when you have multiple conditions:

```python
score = 85

if score >= 90:
    print("A")
elif score >= 80:
    print("B")
elif score >= 70:
    print("C")
else:
    print("F")
```

## Comparison Operators

| Operator | Meaning |
|----------|---------|
| `==` | Equal to |
| `!=` | Not equal to |
| `>` | Greater than |
| `<` | Less than |
| `>=` | Greater than or equal |
| `<=` | Less than or equal |

## Important: Indentation!

Python uses **indentation** (spaces) to group code inside `if` blocks. Always use 4 spaces:

```python
if True:
    print("This is indented")  # 4 spaces
print("This is NOT inside the if")
```""",
        )

        Lesson.objects.create(
            module=m3, title="If Statements in Action", slug="if-statements-in-action", order=2,
            lesson_type="interactive",
            content="""# Try It: Conditionals

Experiment with `if`, `elif`, and `else` below. Try changing the values and see what happens!

## Combining Conditions

You can combine conditions with `and` and `or`:

```python
age = 20
has_ticket = True

if age >= 18 and has_ticket:
    print("Welcome to the show!")
```

## Try it yourself!

Change the `score` variable in the editor and run the code to see different results.""",
            sandbox_code='score = 85\n\nif score >= 90:\n    print("Grade: A - Excellent!")\nelif score >= 80:\n    print("Grade: B - Great job!")\nelif score >= 70:\n    print("Grade: C - Not bad!")\nelse:\n    print("Grade: F - Keep trying!")\n\nprint("Your score:", score)',
        )

        l_m3 = Lesson.objects.create(
            module=m3, title="Practice: Conditionals", slug="practice-conditionals", order=3,
            lesson_type="exercise",
            content="# Practice Time!\n\nTest your conditional logic skills with these exercises.",
        )

        ex = Exercise.objects.create(
            lesson=l_m3, title="Even or Odd", slug="even-or-odd", order=1,
            exercise_type="fill_blank", difficulty=1,
            instructions='Complete the code to check if a number is even or odd. If `num` is divisible by 2, print `Even`. Otherwise, print `Odd`.\n\nThe variable `num` is set to `7`.\n\nExpected output:\n```\nOdd\n```',
            starter_code='num = 7\n\nif num ___ 2 == 0:\n    print("Even")\nelse:\n    print("Odd")',
            solution_code='num = 7\n\nif num % 2 == 0:\n    print("Even")\nelse:\n    print("Odd")',
            xp_value=10, concepts="if, else, modulo",
        )
        TestCase.objects.create(exercise=ex, expected_output="Odd", description="7 should be Odd", order=1)
        Hint.objects.create(exercise=ex, level=1, content="The `%` operator gives you the **remainder** of a division. `7 % 2` gives `1` (not even).", xp_penalty_percent=0)
        Hint.objects.create(exercise=ex, level=2, content="Replace `___` with `%`. The modulo operator checks divisibility.", xp_penalty_percent=10)

        ex = Exercise.objects.create(
            lesson=l_m3, title="Grade Checker", slug="grade-checker", order=2,
            exercise_type="write_code", difficulty=2,
            instructions='Write a program that checks a `score` variable (set to `72`) and prints the letter grade:\n- 90 or above: `A`\n- 80-89: `B`\n- 70-79: `C`\n- Below 70: `F`\n\nExpected output:\n```\nC\n```',
            starter_code='score = 72\n\n# Write your if/elif/else here\n',
            solution_code='score = 72\n\nif score >= 90:\n    print("A")\nelif score >= 80:\n    print("B")\nelif score >= 70:\n    print("C")\nelse:\n    print("F")',
            xp_value=15, concepts="if, elif, else, comparison",
        )
        TestCase.objects.create(exercise=ex, expected_output="C", description="Score 72 should be C", order=1)
        Hint.objects.create(exercise=ex, level=1, content="Start with the highest grade and work down: `if score >= 90:` then `elif score >= 80:` etc.", xp_penalty_percent=0)
        Hint.objects.create(exercise=ex, level=2, content="You need: `if score >= 90:` print A, `elif score >= 80:` print B, `elif score >= 70:` print C, `else:` print F.", xp_penalty_percent=10)

        ex = Exercise.objects.create(
            lesson=l_m3, title="Predict the If", slug="predict-the-if", order=3,
            exercise_type="output_predict", difficulty=1,
            instructions='What will this code print?\n\n```python\nx = 10\ny = 20\n\nif x > y:\n    print("x wins")\nelse:\n    print("y wins")\n```',
            choices=[
                {"label": "x wins", "is_correct": False},
                {"label": "y wins", "is_correct": True},
                {"label": "x wins y wins", "is_correct": False},
                {"label": "Error", "is_correct": False},
            ],
            xp_value=10, concepts="if, else, comparison",
        )

        ex = Exercise.objects.create(
            lesson=l_m3, title="Age Group", slug="age-group", order=4,
            exercise_type="write_code", difficulty=2,
            instructions='Write a program that classifies an `age` variable (set to `15`) into groups:\n- Under 13: print `Child`\n- 13-17: print `Teenager`\n- 18-64: print `Adult`\n- 65 and over: print `Senior`\n\nExpected output:\n```\nTeenager\n```',
            starter_code='age = 15\n\n# Classify the age into a group\n',
            solution_code='age = 15\n\nif age < 13:\n    print("Child")\nelif age <= 17:\n    print("Teenager")\nelif age <= 64:\n    print("Adult")\nelse:\n    print("Senior")',
            xp_value=20, concepts="if, elif, else, comparison",
        )
        TestCase.objects.create(exercise=ex, expected_output="Teenager", description="Age 15 should be Teenager", order=1)
        Hint.objects.create(exercise=ex, level=1, content="Use `if age < 13:` for Child, then `elif` for the other ranges. Remember that 13-17 means `age <= 17`.", xp_penalty_percent=0)
        Hint.objects.create(exercise=ex, level=2, content="`if age < 13:` Child, `elif age <= 17:` Teenager, `elif age <= 64:` Adult, `else:` Senior", xp_penalty_percent=10)

        # === MODULE 4: Loops ===
        m4 = modules["loops"]

        Lesson.objects.create(
            module=m4, title="Understanding Loops", slug="understanding-loops", order=1,
            lesson_type="concept",
            content="""# Loops: Repeating Things

Instead of writing the same code over and over, loops let you repeat actions automatically.

## The `for` Loop

A `for` loop runs code **a specific number of times**:

```python
for i in range(5):
    print(i)
```

Output: `0, 1, 2, 3, 4` (each on a new line)

## `range()` Explained

| Code | Produces |
|------|----------|
| `range(5)` | 0, 1, 2, 3, 4 |
| `range(1, 6)` | 1, 2, 3, 4, 5 |
| `range(0, 10, 2)` | 0, 2, 4, 6, 8 |

## Looping Over Lists

```python
fruits = ["apple", "banana", "cherry"]

for fruit in fruits:
    print(fruit)
```

## The `while` Loop

A `while` loop runs **as long as a condition is true**:

```python
count = 0

while count < 3:
    print(count)
    count = count + 1
```

Output: `0, 1, 2`

## `break` and `continue`

- `break` — exit the loop immediately
- `continue` — skip to the next iteration

```python
for i in range(10):
    if i == 5:
        break
    print(i)  # Prints 0, 1, 2, 3, 4
```""",
        )

        Lesson.objects.create(
            module=m4, title="For Loops in Action", slug="for-loops-in-action", order=2,
            lesson_type="interactive",
            content="""# Try It: Loops

Experiment with `for` and `while` loops below.

## Accumulating a Total

A common pattern is using a loop to build up a value:

```python
total = 0
for i in range(1, 6):
    total = total + i
print(total)  # 15
```

## Try it yourself!

Modify the code in the editor to see how loops work.""",
            sandbox_code='# Try different ranges!\nfor i in range(1, 6):\n    print("Counting:", i)\n\nprint("---")\n\n# Loop over a list\ncolors = ["red", "green", "blue"]\nfor color in colors:\n    print("Color:", color)',
        )

        l_m4 = Lesson.objects.create(
            module=m4, title="Practice: Loops", slug="practice-loops", order=3,
            lesson_type="exercise",
            content="# Practice Time!\n\nPut your loop skills to the test.",
        )

        ex = Exercise.objects.create(
            lesson=l_m4, title="Count to Five", slug="count-to-five", order=1,
            exercise_type="fill_blank", difficulty=1,
            instructions='Complete the code to print the numbers 1 through 5, each on a new line.\n\nExpected output:\n```\n1\n2\n3\n4\n5\n```',
            starter_code='for i in range(___, ___):\n    print(i)',
            solution_code='for i in range(1, 6):\n    print(i)',
            xp_value=10, concepts="for, range",
        )
        TestCase.objects.create(exercise=ex, expected_output="1\n2\n3\n4\n5", description="Should print 1 through 5", order=1)
        Hint.objects.create(exercise=ex, level=1, content="`range(start, stop)` generates numbers from `start` up to but **not including** `stop`.", xp_penalty_percent=0)
        Hint.objects.create(exercise=ex, level=2, content="Use `range(1, 6)` to get 1, 2, 3, 4, 5.", xp_penalty_percent=10)

        ex = Exercise.objects.create(
            lesson=l_m4, title="Sum of Numbers", slug="sum-of-numbers", order=2,
            exercise_type="write_code", difficulty=2,
            instructions='Write a program that calculates the sum of all numbers from 1 to 10 using a `for` loop, then prints the result.\n\nExpected output:\n```\n55\n```',
            starter_code='# Calculate the sum of 1 to 10\ntotal = 0\n\n# Write your loop here\n\nprint(total)',
            solution_code='total = 0\n\nfor i in range(1, 11):\n    total = total + i\n\nprint(total)',
            xp_value=15, concepts="for, range, accumulator",
        )
        TestCase.objects.create(exercise=ex, expected_output="55", description="Sum of 1-10 should be 55", order=1)
        Hint.objects.create(exercise=ex, level=1, content="Use `for i in range(1, 11):` and add each `i` to `total` inside the loop.", xp_penalty_percent=0)

        ex = Exercise.objects.create(
            lesson=l_m4, title="Predict the Loop", slug="predict-the-loop", order=3,
            exercise_type="output_predict", difficulty=1,
            instructions='What will this code print?\n\n```python\nfor i in range(3):\n    print(i * 2)\n```',
            choices=[
                {"label": "0 1 2", "is_correct": False},
                {"label": "0\n2\n4", "is_correct": True},
                {"label": "2\n4\n6", "is_correct": False},
                {"label": "0\n1\n2", "is_correct": False},
            ],
            xp_value=10, concepts="for, range, multiplication",
        )

        ex = Exercise.objects.create(
            lesson=l_m4, title="Multiplication Table", slug="multiplication-table", order=4,
            exercise_type="write_code", difficulty=2,
            instructions='Write a program that prints the multiplication table for `5`, from 1 to 5.\n\nExpected output:\n```\n5 x 1 = 5\n5 x 2 = 10\n5 x 3 = 15\n5 x 4 = 20\n5 x 5 = 25\n```',
            starter_code='# Print the multiplication table for 5\nnum = 5\n\n# Write your loop here\n',
            solution_code='num = 5\n\nfor i in range(1, 6):\n    print(num, "x", i, "=", num * i)',
            xp_value=20, concepts="for, range, math, string formatting",
        )
        TestCase.objects.create(exercise=ex, expected_output="5 x 1 = 5\n5 x 2 = 10\n5 x 3 = 15\n5 x 4 = 20\n5 x 5 = 25", description="Should print 5x table", order=1)
        Hint.objects.create(exercise=ex, level=1, content="Use `for i in range(1, 6):` and inside print `num, \"x\", i, \"=\", num * i`.", xp_penalty_percent=0)
        Hint.objects.create(exercise=ex, level=2, content='`print(num, "x", i, "=", num * i)` — commas in print add spaces between items.', xp_penalty_percent=10)

        # === MODULE 5: Functions ===
        m5 = modules["functions"]

        Lesson.objects.create(
            module=m5, title="What Are Functions?", slug="what-are-functions", order=1,
            lesson_type="concept",
            content="""# Functions: Reusable Code Blocks

A **function** is a named block of code you can call whenever you need it. Think of it like a recipe — you write it once and use it over and over.

## Creating a Function

```python
def greet(name):
    print("Hello,", name)

greet("Alice")  # Output: Hello, Alice
greet("Bob")    # Output: Hello, Bob
```

## The `def` Keyword

- `def` tells Python you're creating a function
- The name follows the same rules as variables
- **Parameters** go inside the parentheses
- Don't forget the colon `:`!

## Return Values

Functions can **return** a value back to you:

```python
def add(a, b):
    return a + b

result = add(3, 4)
print(result)  # Output: 7
```

## Default Parameters

```python
def greet(name, greeting="Hello"):
    print(greeting, name)

greet("Alice")             # Hello Alice
greet("Bob", "Hey")        # Hey Bob
```

## Why Use Functions?

1. **Reusability** — Write once, use many times
2. **Organization** — Break big problems into small pieces
3. **Readability** — Give meaningful names to blocks of logic""",
        )

        Lesson.objects.create(
            module=m5, title="Writing Functions", slug="writing-functions", order=2,
            lesson_type="interactive",
            content="""# Try It: Functions

Experiment with creating and calling functions below.

## Functions That Return Values

```python
def square(n):
    return n * n

print(square(5))  # 25
```

## Try it yourself!

Modify the function in the editor and see what happens.""",
            sandbox_code='def greet(name):\n    return "Hello, " + name + "!"\n\nmessage = greet("World")\nprint(message)\n\n# Try making your own function!\ndef double(n):\n    return n * 2\n\nprint(double(7))\nprint(double(21))',
        )

        l_m5 = Lesson.objects.create(
            module=m5, title="Practice: Functions", slug="practice-functions", order=3,
            lesson_type="exercise",
            content="# Practice Time!\n\nCreate your own functions and put them to work.",
        )

        ex = Exercise.objects.create(
            lesson=l_m5, title="Say Hello Function", slug="say-hello-function", order=1,
            exercise_type="fill_blank", difficulty=1,
            instructions='Complete the function so it **returns** the string `Hello, {name}!` (where `{name}` is the parameter). Then the code will print the result.\n\nExpected output:\n```\nHello, Alice!\n```',
            starter_code='def say_hello(name):\n    ___ "Hello, " + name + "!"\n\nprint(say_hello("Alice"))',
            solution_code='def say_hello(name):\n    return "Hello, " + name + "!"\n\nprint(say_hello("Alice"))',
            xp_value=10, concepts="functions, return, strings",
        )
        TestCase.objects.create(exercise=ex, expected_output="Hello, Alice!", description="Should return Hello, Alice!", order=1)
        Hint.objects.create(exercise=ex, level=1, content="Functions send values back using the `return` keyword.", xp_penalty_percent=0)
        Hint.objects.create(exercise=ex, level=2, content="Replace `___` with `return`.", xp_penalty_percent=10)

        ex = Exercise.objects.create(
            lesson=l_m5, title="Add Two Numbers", slug="add-two-numbers", order=2,
            exercise_type="write_code", difficulty=2,
            instructions='Write a function called `add` that takes two parameters `a` and `b` and **returns** their sum. Then print the result of calling `add(10, 25)`.\n\nExpected output:\n```\n35\n```',
            starter_code='# Define the add function\n\n\n# Print the result of add(10, 25)\n',
            solution_code='def add(a, b):\n    return a + b\n\nprint(add(10, 25))',
            xp_value=15, concepts="functions, return, parameters",
        )
        TestCase.objects.create(exercise=ex, expected_output="35", description="add(10, 25) should return 35", order=1)
        Hint.objects.create(exercise=ex, level=1, content="Use `def add(a, b):` and `return a + b` inside the function body.", xp_penalty_percent=0)

        ex = Exercise.objects.create(
            lesson=l_m5, title="Predict the Function", slug="predict-the-function", order=3,
            exercise_type="output_predict", difficulty=1,
            instructions='What will this code print?\n\n```python\ndef mystery(x):\n    return x * 3\n\nresult = mystery(4)\nprint(result + 1)\n```',
            choices=[
                {"label": "12", "is_correct": False},
                {"label": "13", "is_correct": True},
                {"label": "7", "is_correct": False},
                {"label": "Error", "is_correct": False},
            ],
            xp_value=10, concepts="functions, return, math",
        )

        ex = Exercise.objects.create(
            lesson=l_m5, title="Temperature Converter", slug="temperature-converter", order=4,
            exercise_type="write_code", difficulty=2,
            instructions='Write a function called `celsius_to_fahrenheit` that takes a Celsius temperature and returns the Fahrenheit equivalent.\n\nFormula: `F = C * 9/5 + 32`\n\nThen print the result of converting `0` degrees and `100` degrees.\n\nExpected output:\n```\n32.0\n212.0\n```',
            starter_code='# Define the celsius_to_fahrenheit function\n\n\n# Print the conversion of 0 and 100\n',
            solution_code='def celsius_to_fahrenheit(c):\n    return c * 9/5 + 32\n\nprint(celsius_to_fahrenheit(0))\nprint(celsius_to_fahrenheit(100))',
            xp_value=20, concepts="functions, return, math, formulas",
        )
        TestCase.objects.create(exercise=ex, expected_output="32.0\n212.0", description="0C=32F, 100C=212F", order=1)
        Hint.objects.create(exercise=ex, level=1, content="Inside the function, `return c * 9/5 + 32`. Python will handle the decimal math.", xp_penalty_percent=0)
        Hint.objects.create(exercise=ex, level=2, content="`def celsius_to_fahrenheit(c):` then `return c * 9/5 + 32`. Call it with `print(celsius_to_fahrenheit(0))`.", xp_penalty_percent=10)

        # === MODULE 6: Lists & Tuples ===
        m6 = modules["lists-and-tuples"]

        Lesson.objects.create(
            module=m6, title="Working with Lists", slug="working-with-lists", order=1,
            lesson_type="concept",
            content="""# Lists: Ordered Collections

A **list** stores multiple items in a single variable:

```python
fruits = ["apple", "banana", "cherry"]
numbers = [1, 2, 3, 4, 5]
mixed = ["hello", 42, True]
```

## Accessing Items (Indexing)

Lists are **zero-indexed** — the first item is at position `0`:

```python
fruits = ["apple", "banana", "cherry"]
print(fruits[0])   # apple
print(fruits[1])   # banana
print(fruits[-1])  # cherry (last item)
```

## Modifying Lists

```python
fruits = ["apple", "banana", "cherry"]
fruits.append("date")       # Add to end
fruits[0] = "avocado"       # Change first item
fruits.remove("banana")     # Remove by value
print(len(fruits))          # Length: 3
```

## Looping Over Lists

```python
for fruit in fruits:
    print(fruit)
```

## Useful List Methods

| Method | What it does |
|--------|-------------|
| `append(x)` | Add item to end |
| `insert(i, x)` | Insert at position |
| `remove(x)` | Remove first occurrence |
| `pop()` | Remove and return last item |
| `sort()` | Sort in place |
| `len(list)` | Get number of items |

## Tuples

Tuples are like lists, but **immutable** (can't be changed):

```python
point = (10, 20)
print(point[0])  # 10
```

Use tuples for data that shouldn't change (coordinates, RGB colors, etc.).""",
        )

        Lesson.objects.create(
            module=m6, title="List Operations", slug="list-operations", order=2,
            lesson_type="interactive",
            content="""# Try It: Lists

Experiment with list operations in the editor below.

## Slicing

Get a portion of a list:

```python
nums = [10, 20, 30, 40, 50]
print(nums[1:4])  # [20, 30, 40]
```

## Try it yourself!

Play with the list in the editor.""",
            sandbox_code='# Try list operations!\nfruits = ["apple", "banana", "cherry", "date"]\n\nprint("First:", fruits[0])\nprint("Last:", fruits[-1])\nprint("Length:", len(fruits))\n\nfruits.append("elderberry")\nprint("After append:", fruits)\n\n# Try slicing\nprint("Slice [1:3]:", fruits[1:3])',
        )

        l_m6 = Lesson.objects.create(
            module=m6, title="Practice: Lists", slug="practice-lists", order=3,
            lesson_type="exercise",
            content="# Practice Time!\n\nPut your list skills to work.",
        )

        ex = Exercise.objects.create(
            lesson=l_m6, title="First and Last", slug="first-and-last", order=1,
            exercise_type="fill_blank", difficulty=1,
            instructions='Complete the code to print the **first** and **last** items of the list.\n\nExpected output:\n```\nred\nblue\n```',
            starter_code='colors = ["red", "green", "yellow", "blue"]\n\nprint(colors[___])\nprint(colors[___])',
            solution_code='colors = ["red", "green", "yellow", "blue"]\n\nprint(colors[0])\nprint(colors[-1])',
            xp_value=10, concepts="lists, indexing",
        )
        TestCase.objects.create(exercise=ex, expected_output="red\nblue", description="Should print first and last items", order=1)
        Hint.objects.create(exercise=ex, level=1, content="The first item is at index `0`. The last item can be accessed with index `-1`.", xp_penalty_percent=0)
        Hint.objects.create(exercise=ex, level=2, content="Use `colors[0]` for first and `colors[-1]` for last.", xp_penalty_percent=10)

        ex = Exercise.objects.create(
            lesson=l_m6, title="Sum a List", slug="sum-a-list", order=2,
            exercise_type="write_code", difficulty=2,
            instructions='Write a program that calculates the sum of all numbers in the list using a `for` loop and prints the result.\n\nExpected output:\n```\n150\n```',
            starter_code='numbers = [10, 20, 30, 40, 50]\ntotal = 0\n\n# Loop through the list and add each number to total\n\nprint(total)',
            solution_code='numbers = [10, 20, 30, 40, 50]\ntotal = 0\n\nfor num in numbers:\n    total = total + num\n\nprint(total)',
            xp_value=15, concepts="lists, for loop, accumulator",
        )
        TestCase.objects.create(exercise=ex, expected_output="150", description="Sum should be 150", order=1)
        Hint.objects.create(exercise=ex, level=1, content="Use `for num in numbers:` and add each `num` to `total` inside the loop.", xp_penalty_percent=0)

        ex = Exercise.objects.create(
            lesson=l_m6, title="Predict the List", slug="predict-the-list", order=3,
            exercise_type="output_predict", difficulty=1,
            instructions='What will this code print?\n\n```python\nnums = [10, 20, 30]\nnums.append(40)\nprint(len(nums))\n```',
            choices=[
                {"label": "3", "is_correct": False},
                {"label": "4", "is_correct": True},
                {"label": "40", "is_correct": False},
                {"label": "Error", "is_correct": False},
            ],
            xp_value=10, concepts="lists, append, len",
        )

        ex = Exercise.objects.create(
            lesson=l_m6, title="Shopping List", slug="shopping-list", order=4,
            exercise_type="write_code", difficulty=2,
            instructions='Start with an empty list called `cart`. Add these items in order: `"milk"`, `"eggs"`, `"bread"`. Then print each item with its number.\n\nExpected output:\n```\n1. milk\n2. eggs\n3. bread\n```',
            starter_code='cart = []\n\n# Add items to the cart\n\n\n# Print each item with its number\n',
            solution_code='cart = []\n\ncart.append("milk")\ncart.append("eggs")\ncart.append("bread")\n\nfor i in range(len(cart)):\n    print(str(i + 1) + ". " + cart[i])',
            xp_value=20, concepts="lists, append, for loop, indexing",
        )
        TestCase.objects.create(exercise=ex, expected_output="1. milk\n2. eggs\n3. bread", description="Should print numbered shopping list", order=1)
        Hint.objects.create(exercise=ex, level=1, content="Use `cart.append(\"milk\")` etc. to add items. Then loop with `for i in range(len(cart)):` to get numbered output.", xp_penalty_percent=0)
        Hint.objects.create(exercise=ex, level=2, content='`print(str(i + 1) + ". " + cart[i])` formats each line. Remember `i` starts at 0 so add 1.', xp_penalty_percent=10)

        # === MODULE 7: Dictionaries ===
        m7 = modules["dictionaries"]

        Lesson.objects.create(
            module=m7, title="Understanding Dictionaries", slug="understanding-dictionaries", order=1,
            lesson_type="concept",
            content="""# Dictionaries: Key-Value Pairs

A **dictionary** stores data as key-value pairs — like a real dictionary where each word (key) has a definition (value).

```python
person = {
    "name": "Alice",
    "age": 25,
    "city": "Boston"
}
```

## Accessing Values

```python
print(person["name"])   # Alice
print(person["age"])    # 25
```

## Adding and Changing Values

```python
person["email"] = "alice@example.com"   # Add new key
person["age"] = 26                       # Update existing key
```

## Checking If a Key Exists

```python
if "name" in person:
    print("Name found!")
```

## Looping Over Dictionaries

```python
# Loop over keys
for key in person:
    print(key, ":", person[key])

# Loop over key-value pairs
for key, value in person.items():
    print(key, ":", value)
```

## Useful Methods

| Method | What it does |
|--------|-------------|
| `dict.keys()` | Get all keys |
| `dict.values()` | Get all values |
| `dict.items()` | Get all key-value pairs |
| `dict.get(key, default)` | Get value safely |
| `len(dict)` | Number of key-value pairs |""",
        )

        Lesson.objects.create(
            module=m7, title="Dictionary Operations", slug="dictionary-operations", order=2,
            lesson_type="interactive",
            content="""# Try It: Dictionaries

Experiment with dictionaries in the editor below.

## Building a Dictionary

You can start empty and add keys:

```python
scores = {}
scores["math"] = 95
scores["english"] = 88
```

## Try it yourself!

Modify the dictionary in the editor and see what happens.""",
            sandbox_code='# Try dictionary operations!\nperson = {\n    "name": "Alice",\n    "age": 25,\n    "city": "Boston"\n}\n\nprint("Name:", person["name"])\nprint("Keys:", list(person.keys()))\n\n# Add a new key\nperson["hobby"] = "coding"\n\n# Loop over all items\nfor key, value in person.items():\n    print(key, "->", value)',
        )

        l_m7 = Lesson.objects.create(
            module=m7, title="Practice: Dictionaries", slug="practice-dictionaries", order=3,
            lesson_type="exercise",
            content="# Practice Time!\n\nMaster dictionaries with these exercises.",
        )

        ex = Exercise.objects.create(
            lesson=l_m7, title="Access a Value", slug="access-a-value", order=1,
            exercise_type="fill_blank", difficulty=1,
            instructions='Complete the code to print the value associated with the key `"color"`.\n\nExpected output:\n```\nblue\n```',
            starter_code='car = {"brand": "Toyota", "color": "blue", "year": 2020}\n\nprint(car[___])',
            solution_code='car = {"brand": "Toyota", "color": "blue", "year": 2020}\n\nprint(car["color"])',
            xp_value=10, concepts="dictionaries, access",
        )
        TestCase.objects.create(exercise=ex, expected_output="blue", description="Should print blue", order=1)
        Hint.objects.create(exercise=ex, level=1, content='Use the key name in quotes inside square brackets: `dict["key"]`.', xp_penalty_percent=0)
        Hint.objects.create(exercise=ex, level=2, content='Replace `___` with `"color"` (include the quotes!).', xp_penalty_percent=10)

        ex = Exercise.objects.create(
            lesson=l_m7, title="Build a Profile", slug="build-a-profile", order=2,
            exercise_type="write_code", difficulty=2,
            instructions='Create a dictionary called `profile` with these keys and values:\n- `"name"`: `"Alex"`\n- `"age"`: `30`\n- `"language"`: `"Python"`\n\nThen print each key-value pair.\n\nExpected output:\n```\nname: Alex\nage: 30\nlanguage: Python\n```',
            starter_code='# Create the profile dictionary\n\n\n# Print each key-value pair\n',
            solution_code='profile = {"name": "Alex", "age": 30, "language": "Python"}\n\nfor key, value in profile.items():\n    print(str(key) + ": " + str(value))',
            xp_value=15, concepts="dictionaries, for loop, items",
        )
        TestCase.objects.create(exercise=ex, expected_output="name: Alex\nage: 30\nlanguage: Python", description="Should print all profile items", order=1)
        Hint.objects.create(exercise=ex, level=1, content='Create the dict: `profile = {"name": "Alex", ...}`. Then loop with `for key, value in profile.items():`.', xp_penalty_percent=0)
        Hint.objects.create(exercise=ex, level=2, content='Use `print(str(key) + ": " + str(value))` to format each line. `str()` converts numbers to text.', xp_penalty_percent=10)

        ex = Exercise.objects.create(
            lesson=l_m7, title="Predict the Dict", slug="predict-the-dict", order=3,
            exercise_type="output_predict", difficulty=1,
            instructions='What will this code print?\n\n```python\nd = {"a": 1, "b": 2}\nd["c"] = 3\nprint(len(d))\n```',
            choices=[
                {"label": "2", "is_correct": False},
                {"label": "3", "is_correct": True},
                {"label": "6", "is_correct": False},
                {"label": "Error", "is_correct": False},
            ],
            xp_value=10, concepts="dictionaries, len, adding keys",
        )

        ex = Exercise.objects.create(
            lesson=l_m7, title="Word Counter", slug="word-counter", order=4,
            exercise_type="write_code", difficulty=2,
            instructions='Count how many times each word appears in the list and print the counts.\n\nExpected output:\n```\nhello: 2\nworld: 1\npython: 3\n```',
            starter_code='words = ["hello", "world", "python", "hello", "python", "python"]\ncounts = {}\n\n# Count each word\n\n\n# Print the counts\n',
            solution_code='words = ["hello", "world", "python", "hello", "python", "python"]\ncounts = {}\n\nfor word in words:\n    if word in counts:\n        counts[word] = counts[word] + 1\n    else:\n        counts[word] = 1\n\nfor word, count in counts.items():\n    print(str(word) + ": " + str(count))',
            xp_value=20, concepts="dictionaries, for loop, counting",
        )
        TestCase.objects.create(exercise=ex, expected_output="hello: 2\nworld: 1\npython: 3", description="Should count word occurrences", order=1)
        Hint.objects.create(exercise=ex, level=1, content="Loop through `words`. For each word, check `if word in counts:` and increment, otherwise set it to 1.", xp_penalty_percent=0)
        Hint.objects.create(exercise=ex, level=2, content="`if word in counts: counts[word] = counts[word] + 1` else `counts[word] = 1`. Then loop `counts.items()` to print.", xp_penalty_percent=10)

        # === MODULE 8: String Magic ===
        m8 = modules["string-magic"]

        Lesson.objects.create(
            module=m8, title="String Methods", slug="string-methods", order=1,
            lesson_type="concept",
            content="""# String Magic: Manipulating Text

Strings in Python come with many built-in **methods** — functions that transform or inspect text.

## Common String Methods

```python
text = "Hello, World!"

print(text.upper())      # HELLO, WORLD!
print(text.lower())      # hello, world!
print(text.title())      # Hello, World!
print(text.strip())      # Remove leading/trailing spaces
print(text.replace("World", "Python"))  # Hello, Python!
print(text.startswith("Hello"))  # True
print(text.count("l"))   # 3
print(len(text))         # 13
```

## String Slicing

Get parts of a string using `[start:stop]`:

```python
text = "Python"
print(text[0])     # P
print(text[0:3])   # Pyt
print(text[-3:])   # hon
print(text[::-1])  # nohtyP (reversed!)
```

## f-Strings (Formatted Strings)

The modern way to build strings with variables:

```python
name = "Alice"
age = 25
print(f"My name is {name} and I am {age} years old.")
```

## Splitting and Joining

```python
sentence = "Hello World Python"
words = sentence.split()      # ["Hello", "World", "Python"]
joined = "-".join(words)      # "Hello-World-Python"
```

## String Properties

- Strings are **immutable** — you can't change individual characters
- `text[0] = "h"` will cause an error
- Methods like `.upper()` return a **new** string""",
        )

        Lesson.objects.create(
            module=m8, title="String Manipulation", slug="string-manipulation", order=2,
            lesson_type="interactive",
            content="""# Try It: String Magic

Experiment with string methods and slicing in the editor below.

## f-Strings Are Powerful

```python
name = "Alice"
print(f"Hello {name.upper()}!")  # Hello ALICE!
```

## Try it yourself!

Play with the string operations in the editor.""",
            sandbox_code='text = "Python is Amazing"\n\nprint("Upper:", text.upper())\nprint("Lower:", text.lower())\nprint("Words:", text.split())\nprint("Replace:", text.replace("Amazing", "Fun"))\n\n# Slicing\nprint("First 6:", text[:6])\nprint("Reversed:", text[::-1])\n\n# f-strings\nlang = "Python"\nversion = 3\nprint(f"{lang} version {version} is great!")',
        )

        l_m8 = Lesson.objects.create(
            module=m8, title="Practice: Strings", slug="practice-strings", order=3,
            lesson_type="exercise",
            content="# Practice Time!\n\nMaster string manipulation with these exercises.",
        )

        ex = Exercise.objects.create(
            lesson=l_m8, title="Uppercase", slug="uppercase", order=1,
            exercise_type="fill_blank", difficulty=1,
            instructions='Complete the code to print the text in all uppercase letters.\n\nExpected output:\n```\nHELLO PYTHON\n```',
            starter_code='text = "hello python"\n\nprint(text.___())',
            solution_code='text = "hello python"\n\nprint(text.upper())',
            xp_value=10, concepts="strings, methods, upper",
        )
        TestCase.objects.create(exercise=ex, expected_output="HELLO PYTHON", description="Should print HELLO PYTHON", order=1)
        Hint.objects.create(exercise=ex, level=1, content="There's a string method that converts all characters to uppercase.", xp_penalty_percent=0)
        Hint.objects.create(exercise=ex, level=2, content="The method is called `upper()`. Replace `___` with `upper`.", xp_penalty_percent=10)

        ex = Exercise.objects.create(
            lesson=l_m8, title="Extract Initials", slug="extract-initials", order=2,
            exercise_type="write_code", difficulty=2,
            instructions='Given a full name, extract and print the initials (first letter of each word, uppercase).\n\nExpected output:\n```\nJ.D.\n```',
            starter_code='name = "john doe"\n\n# Extract and print initials like "J.D."\n',
            solution_code='name = "john doe"\n\nwords = name.split()\ninitials = ""\nfor word in words:\n    initials = initials + word[0].upper() + "."\n\nprint(initials)',
            xp_value=15, concepts="strings, split, indexing, upper, loops",
        )
        TestCase.objects.create(exercise=ex, expected_output="J.D.", description="Should print J.D.", order=1)
        Hint.objects.create(exercise=ex, level=1, content="Split the name into words with `.split()`. Then loop through each word, grab `word[0]`, and uppercase it.", xp_penalty_percent=0)
        Hint.objects.create(exercise=ex, level=2, content='`for word in name.split():` then build initials with `word[0].upper() + "."`', xp_penalty_percent=10)

        ex = Exercise.objects.create(
            lesson=l_m8, title="Predict the String", slug="predict-the-string", order=3,
            exercise_type="output_predict", difficulty=1,
            instructions='What will this code print?\n\n```python\ntext = "Python"\nprint(text[0] + text[-1])\n```',
            choices=[
                {"label": "Pn", "is_correct": True},
                {"label": "Py", "is_correct": False},
                {"label": "on", "is_correct": False},
                {"label": "Error", "is_correct": False},
            ],
            xp_value=10, concepts="strings, indexing",
        )

        ex = Exercise.objects.create(
            lesson=l_m8, title="Reverse Words", slug="reverse-words", order=4,
            exercise_type="write_code", difficulty=2,
            instructions='Take the sentence and print it with the words in reverse order.\n\nExpected output:\n```\nfun is Python\n```',
            starter_code='sentence = "Python is fun"\n\n# Print the words in reverse order\n',
            solution_code='sentence = "Python is fun"\n\nwords = sentence.split()\nwords.reverse()\nprint(" ".join(words))',
            xp_value=20, concepts="strings, split, reverse, join",
        )
        TestCase.objects.create(exercise=ex, expected_output="fun is Python", description="Should reverse the word order", order=1)
        Hint.objects.create(exercise=ex, level=1, content="Split into words with `.split()`, reverse the list with `.reverse()`, then join back with `\" \".join(words)`.", xp_penalty_percent=0)
        Hint.objects.create(exercise=ex, level=2, content='`words = sentence.split()` then `words.reverse()` then `print(" ".join(words))`', xp_penalty_percent=10)

        # === MODULE 9: Writing Cleaner Code ===
        m9 = modules["writing-cleaner-code"]

        Lesson.objects.create(
            module=m9, title="Pythonic Patterns", slug="pythonic-patterns", order=1,
            lesson_type="concept",
            content="""# Writing Cleaner Code

Python has elegant shortcuts that make your code shorter **and** more readable. Let's learn the most useful ones.

## 1. Ternary Expressions

Instead of a full if/else block for simple assignments:

```python
# Long way
if score >= 60:
    result = "Pass"
else:
    result = "Fail"

# Pythonic way
result = "Pass" if score >= 60 else "Fail"
```

## 2. Multiple Assignment

Assign several variables in one line:

```python
x, y, z = 1, 2, 3

# Swap two variables
a, b = b, a
```

## 3. enumerate()

Get both the index and item when looping:

```python
colors = ["red", "green", "blue"]
for i, color in enumerate(colors, 1):
    print(f"{i}. {color}")
```

Output:
```
1. red
2. green
3. blue
```

## 4. List Comprehensions

Build a list in a single expression:

```python
# Long way
squares = []
for n in range(5):
    squares.append(n ** 2)

# Pythonic way
squares = [n ** 2 for n in range(5)]
```

You can add a filter:
```python
evens = [n for n in range(10) if n % 2 == 0]
```

## 5. f-String Tricks

f-Strings can do more than insert variables:

```python
value = 3.14159
print(f"{value:.2f}")       # 3.14  (2 decimal places)
print(f"{'hello':>10}")     # "     hello"  (right-align)
print(f"{42:05d}")          # "00042" (zero-pad)
```

## 6. The Walrus Operator `:=`

Assign a value **and** use it in the same expression:

```python
# Without walrus
n = len("hello")
if n > 3:
    print(n)

# With walrus
if (n := len("hello")) > 3:
    print(n)
```

Useful in while loops:
```python
while (line := input(">>> ")) != "quit":
    print(f"You said: {line}")
```""",
        )

        Lesson.objects.create(
            module=m9, title="Try It: Cleaner Code", slug="try-it-cleaner-code", order=2,
            lesson_type="interactive",
            content="""# Try It: Cleaner Code

Experiment with Pythonic patterns in the editor below.

## Ternary, enumerate, comprehensions, walrus

Try modifying the examples and see what happens!""",
            sandbox_code='# Ternary expression\nscore = 85\nresult = "Pass" if score >= 60 else "Fail"\nprint(f"{score} -> {result}")\n\n# Multiple assignment\nx, y = 10, 20\nx, y = y, x\nprint(f"Swapped: x={x}, y={y}")\n\n# enumerate\ncolors = ["red", "green", "blue"]\nfor i, color in enumerate(colors, 1):\n    print(f"{i}. {color}")\n\n# List comprehension\nsquares = [n ** 2 for n in range(6)]\nprint("Squares:", squares)\n\n# Walrus operator\ndata = [1, 5, 15, 3, 12]\nbig = [x for x in data if (doubled := x * 2) > 10]\nprint("Big doubled values:", big)',
        )

        l_m9 = Lesson.objects.create(
            module=m9, title="Practice: Cleaner Code", slug="practice-cleaner-code", order=3,
            lesson_type="exercise",
            content="# Practice Time!\n\nPut your Pythonic patterns to work.",
        )

        # Exercise 9-1: Quick Decision (fill_blank)
        ex = Exercise.objects.create(
            lesson=l_m9, title="Quick Decision", slug="quick-decision", order=1,
            exercise_type="fill_blank", difficulty=1,
            instructions='Complete the ternary expression so it prints `Pass` when `score` is 75.\n\nExpected output:\n```\nPass\n```',
            starter_code='score = 75\n\nresult = "Pass" ___ score >= 60 ___ "Fail"\nprint(result)',
            solution_code='score = 75\n\nresult = "Pass" if score >= 60 else "Fail"\nprint(result)',
            xp_value=10, concepts="ternary, conditional expression",
        )
        TestCase.objects.create(exercise=ex, expected_output="Pass", description="Should print Pass", order=1)
        Hint.objects.create(exercise=ex, level=1, content="A ternary expression has the form: `value_if_true if condition else value_if_false`.", xp_penalty_percent=0)
        Hint.objects.create(exercise=ex, level=2, content="Replace the first `___` with `if` and the second `___` with `else`.", xp_penalty_percent=10)

        # Exercise 9-2: Numbered List (write_code)
        ex = Exercise.objects.create(
            lesson=l_m9, title="Numbered List", slug="numbered-list", order=2,
            exercise_type="write_code", difficulty=2,
            instructions='Use `enumerate()` to print each color with a number starting at 1.\n\nExpected output:\n```\n1. red\n2. green\n3. blue\n```',
            starter_code='colors = ["red", "green", "blue"]\n\n# Use enumerate to print a numbered list\n',
            solution_code='colors = ["red", "green", "blue"]\n\nfor i, color in enumerate(colors, 1):\n    print(f"{i}. {color}")',
            xp_value=15, concepts="enumerate, f-strings, loops",
        )
        TestCase.objects.create(exercise=ex, expected_output="1. red\n2. green\n3. blue", description="Should print numbered list", order=1)
        Hint.objects.create(exercise=ex, level=1, content="`enumerate(colors, 1)` gives you `(1, 'red')`, `(2, 'green')`, etc.", xp_penalty_percent=0)
        Hint.objects.create(exercise=ex, level=2, content='`for i, color in enumerate(colors, 1):` then `print(f"{i}. {color}")`', xp_penalty_percent=10)

        # Exercise 9-3: Predict the Walrus (output_predict)
        ex = Exercise.objects.create(
            lesson=l_m9, title="Predict the Walrus", slug="predict-the-walrus", order=3,
            exercise_type="output_predict", difficulty=1,
            instructions='What will this code print?\n\n```python\ndata = [3, 7, 5]\nif (total := sum(data)) > 10:\n    print(total)\n```',
            choices=[
                {"label": "15", "is_correct": True},
                {"label": "10", "is_correct": False},
                {"label": "3", "is_correct": False},
                {"label": "Nothing (no output)", "is_correct": False},
            ],
            xp_value=10, concepts="walrus operator, sum",
        )

        # Exercise 9-4: Score Classifier (write_code)
        ex = Exercise.objects.create(
            lesson=l_m9, title="Score Classifier", slug="score-classifier", order=4,
            exercise_type="write_code", difficulty=2,
            instructions='For each score in the list, print the score and whether it\'s a `Pass` (>= 60) or `Fail` using a ternary expression.\n\nExpected output:\n```\n45 -> Fail\n82 -> Pass\n67 -> Pass\n91 -> Pass\n38 -> Fail\n```',
            starter_code='scores = [45, 82, 67, 91, 38]\n\n# For each score, print "score -> Pass" or "score -> Fail"\n',
            solution_code='scores = [45, 82, 67, 91, 38]\n\nfor score in scores:\n    result = "Pass" if score >= 60 else "Fail"\n    print(f"{score} -> {result}")',
            xp_value=20, concepts="ternary, loops, f-strings",
        )
        TestCase.objects.create(exercise=ex, expected_output="45 -> Fail\n82 -> Pass\n67 -> Pass\n91 -> Pass\n38 -> Fail", description="Should classify each score", order=1)
        Hint.objects.create(exercise=ex, level=1, content="Loop through `scores` and use a ternary expression: `\"Pass\" if score >= 60 else \"Fail\"`.", xp_penalty_percent=0)
        Hint.objects.create(exercise=ex, level=2, content='`for score in scores:` then `result = "Pass" if score >= 60 else "Fail"` then `print(f"{score} -> {result}")`', xp_penalty_percent=10)

        # === MODULE 10: Python for Network Engineers ===
        m10 = modules["python-for-network-engineers"]

        Lesson.objects.create(
            module=m10, title="Python Meets Networking", slug="python-meets-networking", order=1,
            lesson_type="concept",
            content="""# Python for Network Engineers

Python is one of the most popular languages for **network automation**. Engineers use it to manage routers, switches, and firewalls — checking configs, validating IP addresses, and parsing device output that would take forever to review by hand.

In this module you'll learn three skills that come up constantly in network engineering:

1. **IP address handling** — validate addresses, calculate subnets, and check network membership
2. **CLI output parsing** — take the text a network device spits out and extract the data you need
3. **JSON configs** — read structured device configurations and transform them into useful reports

---

## 1. The `ipaddress` Module

Python has a built-in `ipaddress` module (no install needed!) for working with IPv4/IPv6 addresses and networks.

### Creating IP address objects

```python
import ipaddress

ip = ipaddress.ip_address("192.168.1.1")
print(type(ip))        # <class 'ipaddress.IPv4Address'>
print(ip.is_private)   # True  — it's in a private range (192.168.x.x)
print(ip.is_loopback)  # False — 127.0.0.1 would be True
```

An `IPv4Address` object is smarter than a plain string — it knows whether the address is private, loopback, multicast, etc.

### Working with networks (CIDR notation)

A **network** like `10.0.0.0/24` represents a range of addresses. The `/24` means the first 24 bits are the network portion, leaving 8 bits (256 addresses) for hosts.

```python
network = ipaddress.ip_network("10.0.0.0/24")
print(network.num_addresses)    # 256
print(network.network_address)  # 10.0.0.0
print(network.broadcast_address)  # 10.0.0.255
print(network.prefixlen)        # 24
```

### Checking if an IP belongs to a network

This is one of the most common tasks — "is this IP inside my subnet?"

```python
ip = ipaddress.ip_address("10.0.0.42")
net = ipaddress.ip_network("10.0.0.0/24")
print(ip in net)  # True

outside = ipaddress.ip_address("192.168.1.1")
print(outside in net)  # False
```

### Validating user input

If someone gives you a bad IP string, `ipaddress` raises a `ValueError`:

```python
try:
    ip = ipaddress.ip_address("999.999.999.999")
except ValueError as e:
    print(f"Invalid: {e}")
# Invalid: '999.999.999.999' does not appear to be an IPv4 or IPv6 address
```

---

## 2. Parsing CLI Output

Network devices (routers, switches) respond to commands like `show interfaces` with **text tables**. Python is great at slicing this text into structured data.

### Basic approach: `split()` + loop

```python
output = \"\"\"Interface    Status
Gi0/0        up
Gi0/1        down
Gi0/2        up\"\"\"

lines = output.strip().split("\\n")  # split into lines
for line in lines[1:]:               # skip the header row
    parts = line.split()             # split on whitespace
    name, status = parts[0], parts[1]
    print(f"{name} is {status}")
```

Output:
```
Gi0/0 is up
Gi0/1 is down
Gi0/2 is up
```

**How it works step-by-step:**
1. `output.strip().split("\\n")` turns the big string into a list of lines
2. `lines[1:]` skips the header (`"Interface    Status"`)
3. `line.split()` breaks `"Gi0/0        up"` into `["Gi0/0", "up"]`
4. We grab `parts[0]` (interface name) and `parts[1]` (status)

### Using regular expressions for complex patterns

Sometimes CLI output is messier. The `re` module lets you match patterns:

```python
import re

output = "GigabitEthernet0/0 is up, line protocol is up"
match = re.search(r"(\\S+) is (\\w+)", output)
if match:
    print(f"Interface: {match.group(1)}")  # GigabitEthernet0/0
    print(f"Status: {match.group(2)}")     # up
```

- `\\S+` matches one or more non-whitespace characters (the interface name)
- `\\w+` matches one or more word characters (the status)
- Parentheses `()` create **capture groups** you can extract with `.group(1)`, `.group(2)`

---

## 3. JSON Device Configs

Modern network devices and automation tools (Ansible, Terraform, REST APIs) use **JSON** to represent configuration. Python's built-in `json` module makes it easy to work with.

### Parsing a JSON string

```python
import json

config_str = '{\"hostname\": \"SW1\", \"vlans\": [10, 20, 30]}'
config = json.loads(config_str)   # JSON string → Python dict
print(type(config))       # <class 'dict'>
print(config["hostname"]) # SW1
print(config["vlans"])    # [10, 20, 30]
```

`json.loads()` (**load s**tring) converts a JSON string into a Python dictionary. JSON objects become dicts, JSON arrays become lists.

### Looping through config data

```python
for vlan in config["vlans"]:
    print(f"VLAN {vlan} configured")
```

Output:
```
VLAN 10 configured
VLAN 20 configured
VLAN 30 configured
```

### A more realistic example

Device configs often have nested structures:

```python
import json

device_json = '{\"hostname\": \"R1\", \"role\": \"router\", \"interfaces\": [\"Gi0/0\", \"Gi0/1\", \"Lo0\"]}'
device = json.loads(device_json)

print(f"Device: {device['hostname']}")
print(f"Role: {device['role']}")
print(f"Interfaces: {len(device['interfaces'])}")
for iface in device["interfaces"]:
    print(f"  - {iface}")
```

This pattern — parse JSON, access keys, loop through lists — is the foundation of network automation scripts.

---

## Key Takeaways

| Task | Tool | Key function |
|------|------|-------------|
| Validate/inspect IPs | `ipaddress` | `ip_address()`, `ip_network()`, `in` |
| Parse text output | `str` methods + `re` | `.split()`, `.strip()`, `re.search()` |
| Read structured configs | `json` | `json.loads()` |

All three modules (`ipaddress`, `re`, `json`) are built into Python — no extra installs needed!""",
        )

        Lesson.objects.create(
            module=m10, title="Try It: Network Scripts", slug="try-it-network-scripts", order=2,
            lesson_type="interactive",
            content="""# Try It: Network Scripts

Experiment with IP addresses, CLI output parsing, and JSON configs in the editor below.

## Give it a try!

Modify the examples and see what happens.""",
            sandbox_code='import ipaddress\nimport json\nimport re\n\n# === IP Addresses ===\nip = ipaddress.ip_address("192.168.1.1")\nprint(f"{ip} is private: {ip.is_private}")\n\nnet = ipaddress.ip_network("10.0.0.0/24")\nprint(f"Network {net} has {net.num_addresses} addresses")\nprint(f"10.0.0.42 in network: {ipaddress.ip_address(\'10.0.0.42\') in net}")\n\n# === Parse CLI output ===\nshow_output = """Interface    Status\nGi0/0        up\nGi0/1        down\nGi0/2        up"""\n\nprint("\\n--- Parsed Interfaces ---")\nfor line in show_output.strip().split("\\n")[1:]:\n    parts = line.split()\n    print(f"  {parts[0]:12s} -> {parts[1]}")\n\n# === JSON Config ===\nconfig_json = \'{"hostname": "SW1", "vlans": [10, 20, 30]}\'\nconfig = json.loads(config_json)\nprint(f"\\nDevice: {config[\'hostname\']}")\nfor v in config["vlans"]:\n    print(f"  VLAN {v}")',
        )

        l_m10 = Lesson.objects.create(
            module=m10, title="Practice: Network Automation", slug="practice-network-automation", order=3,
            lesson_type="exercise",
            content="# Practice Time!\n\nApply your networking Python skills with these exercises.",
        )

        # Exercise 10-1: Check the Subnet (fill_blank)
        ex = Exercise.objects.create(
            lesson=l_m10, title="Check the Subnet", slug="check-the-subnet", order=1,
            exercise_type="fill_blank", difficulty=1,
            instructions='Complete the code to check if `10.0.0.50` is in the `10.0.0.0/24` network.\n\nExpected output:\n```\nTrue\n```',
            starter_code='import ipaddress\n\nip = ipaddress.ip_address("10.0.0.50")\nnet = ipaddress.ip_network("10.0.0.0/24")\n\nprint(ip ___ net)',
            solution_code='import ipaddress\n\nip = ipaddress.ip_address("10.0.0.50")\nnet = ipaddress.ip_network("10.0.0.0/24")\n\nprint(ip in net)',
            xp_value=10, concepts="ipaddress, network membership",
        )
        TestCase.objects.create(exercise=ex, expected_output="True", description="Should print True", order=1)
        Hint.objects.create(exercise=ex, level=1, content="To check if an item belongs to a collection in Python, you use a keyword...", xp_penalty_percent=0)
        Hint.objects.create(exercise=ex, level=2, content="Replace `___` with `in`. The expression `ip in net` checks network membership.", xp_penalty_percent=10)

        # Exercise 10-2: Parse Show Interfaces (write_code)
        ex = Exercise.objects.create(
            lesson=l_m10, title="Parse Show Interfaces", slug="parse-show-interfaces", order=2,
            exercise_type="write_code", difficulty=2,
            instructions='The variable `output` contains a table of interfaces. Parse it and print only the interface names (skip the header line).\n\nExpected output:\n```\nGi0/0\nGi0/1\nGi0/2\n```',
            starter_code='output = """Interface    Status    Speed\nGi0/0        up        1000\nGi0/1        down      100\nGi0/2        up        1000"""\n\n# Parse the output and print each interface name\n',
            solution_code='output = """Interface    Status    Speed\nGi0/0        up        1000\nGi0/1        down      100\nGi0/2        up        1000"""\n\nlines = output.strip().split("\\n")\nfor line in lines[1:]:\n    parts = line.split()\n    print(parts[0])',
            xp_value=15, concepts="string parsing, split, loops",
        )
        TestCase.objects.create(exercise=ex, expected_output="Gi0/0\nGi0/1\nGi0/2", description="Should print interface names", order=1)
        Hint.objects.create(exercise=ex, level=1, content="Split the output into lines with `.split(\"\\n\")`, then skip the first line (header) with `[1:]`.", xp_penalty_percent=0)
        Hint.objects.create(exercise=ex, level=2, content='`for line in lines[1:]:` then `parts = line.split()` and `print(parts[0])` to get the interface name.', xp_penalty_percent=10)

        # Exercise 10-3: Predict the JSON (output_predict)
        ex = Exercise.objects.create(
            lesson=l_m10, title="Predict the JSON", slug="predict-the-json", order=3,
            exercise_type="output_predict", difficulty=1,
            instructions='What will this code print?\n\n```python\nimport json\n\ndata = json.loads(\'{"ports": [22, 80, 443]}\')\nprint(len(data["ports"]))\n```',
            choices=[
                {"label": "3", "is_correct": True},
                {"label": "[22, 80, 443]", "is_correct": False},
                {"label": "ports", "is_correct": False},
                {"label": "Error", "is_correct": False},
            ],
            xp_value=10, concepts="json, len, lists",
        )

        # Exercise 10-4: Config Report (write_code)
        ex = Exercise.objects.create(
            lesson=l_m10, title="Config Report", slug="config-report", order=4,
            exercise_type="write_code", difficulty=2,
            instructions='Parse the JSON config and print a formatted report.\n\nExpected output:\n```\nDevice: R1\nRole: router\nInterfaces: 3\n  - GigabitEthernet0/0\n  - GigabitEthernet0/1\n  - Loopback0\n```',
            starter_code='import json\n\nconfig_str = \'{"hostname": "R1", "role": "router", "interfaces": ["GigabitEthernet0/0", "GigabitEthernet0/1", "Loopback0"]}\'\n\n# Parse the JSON and print the report\n',
            solution_code='import json\n\nconfig_str = \'{"hostname": "R1", "role": "router", "interfaces": ["GigabitEthernet0/0", "GigabitEthernet0/1", "Loopback0"]}\'\n\nconfig = json.loads(config_str)\nprint(f"Device: {config[\'hostname\']}")\nprint(f"Role: {config[\'role\']}")\nprint(f"Interfaces: {len(config[\'interfaces\'])}")\nfor iface in config["interfaces"]:\n    print(f"  - {iface}")',
            xp_value=20, concepts="json, f-strings, loops",
        )
        TestCase.objects.create(exercise=ex, expected_output="Device: R1\nRole: router\nInterfaces: 3\n  - GigabitEthernet0/0\n  - GigabitEthernet0/1\n  - Loopback0", description="Should print formatted config report", order=1)
        Hint.objects.create(exercise=ex, level=1, content="Use `json.loads()` to parse the string, then access keys like `config['hostname']`.", xp_penalty_percent=0)
        Hint.objects.create(exercise=ex, level=2, content='`config = json.loads(config_str)` then print each field with f-strings. Loop through `config["interfaces"]` for the list.', xp_penalty_percent=10)

        self.stdout.write(self.style.SUCCESS(
            f"\nDone! Created {Module.objects.count()} modules, "
            f"{Lesson.objects.count()} lessons, "
            f"{Exercise.objects.count()} exercises, "
            f"{TestCase.objects.count()} test cases, "
            f"{Hint.objects.count()} hints."
        ))
