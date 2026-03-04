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
            ("Handling Errors", "handling-errors", "Learn to catch and handle errors gracefully so your scripts don't crash on bad data.", "shield"),
            ("User Input & While Loops", "user-input-and-while-loops", "Build interactive CLI tools that read user input and loop until the job is done.", "terminal"),
            ("Regular Expressions", "regular-expressions", "Master pattern matching with regex to parse device logs, extract IPs, and search text like a pro.", "search"),
            ("Building a Network Toolkit", "building-a-network-toolkit", "Combine everything you've learned into realistic network automation scripts.", "wrench"),
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

## What Is Programming?

Programming is just writing instructions for a computer. Think of it like writing a recipe: you list the steps in order, and the computer follows them exactly. The difference is that a computer needs **very precise** instructions — it can't guess what you mean.

Python is the language we use to write those instructions. It's one of the closest programming languages to plain English, which makes it a great first language.

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

### Why the parentheses and quotes?

- The **parentheses** `()` tell Python "I'm calling a function" — in this case, the `print` function
- The **quotes** `""` tell Python "this is text, not a command" — without quotes, Python would think `Hello` is a variable name

This will feel natural very quickly. Every `print()` call follows the same pattern: `print("your text here")`.

## How does it work?

When you click **Run** in the editor, here's what happens behind the scenes:

1. You **write** code (instructions for the computer)
2. Python **reads** your code from top to bottom
3. It **executes** each instruction one at a time
4. You see the **result** on screen

Python runs your code **line by line**, in order. If you have three `print()` lines, it runs the first, then the second, then the third.

## Comments: Notes for Humans

You can add notes to your code using `#`. Python ignores everything after `#` on that line:

```python
# This is a comment — Python skips this line
print("Hello!")  # This comment is after the code
```

Comments are for **you** (and other humans reading your code). Use them to explain *why* you did something, not *what* you did.

## Errors Are Normal!

When you're learning, you **will** see error messages. Everyone does — even experienced programmers. An error doesn't mean you're bad at this. It means Python is telling you exactly what went wrong so you can fix it.

Common early mistakes:
- Forgetting the closing parenthesis: `print("Hello"` → add the `)`
- Forgetting the quotes: `print(Hello)` → add quotes around the text
- Misspelling `print`: `prnt("Hello")` → check the spelling

When you see an error, read the message. Python usually tells you the line number and what it expected. You'll get faster at fixing these with practice.

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

        # Try It Yourself: Print
        Lesson.objects.create(
            module=m1, title="Try It Yourself: Print", slug="try-it-yourself-print", order=4,
            lesson_type="interactive",
            content="# Try It Yourself: Print\n\n"
                "Time for creative challenges! Use `print()` to build something cool.\n\n"
                "## Challenge 1 — ASCII Art\n\n"
                "Create a 3-line ASCII art picture using only `print()` statements. Here's an example of a simple house:\n\n"
                "```\n"
                "   /\\\\\n"
                "  /  \\\\\n"
                " /____\\\\\n"
                " |    |\n"
                " |____|\n"
                "```\n\n"
                "Try making a cat, a rocket, a tree, or anything you like!\n\n"
                "## Challenge 2 — Receipt Printer\n\n"
                "Print a formatted receipt like this:\n\n"
                "```\n"
                "===== RECEIPT =====\n"
                "Coffee        $4.50\n"
                "Sandwich      $8.99\n"
                "Cookie        $2.50\n"
                "-------------------\n"
                "TOTAL        $15.99\n"
                "===== THANK YOU ===\n"
                "```\n\n"
                "Use spaces to align the prices on the right side.\n\n"
                "## Challenge 3 — Business Card\n\n"
                "Print a business card with borders:\n\n"
                "```\n"
                "============================\n"
                "|      JANE SMITH          |\n"
                "|      Python Developer    |\n"
                "|      jane@example.com    |\n"
                "============================\n"
                "```\n\n"
                "Use `=` for top/bottom borders and `|` for side borders.",
            sandbox_code='',
        )

        # === MODULE 2: Variables & Data Types ===
        m2 = modules["variables-and-data-types"]

        Lesson.objects.create(
            module=m2, title="What Are Variables?", slug="what-are-variables", order=1,
            lesson_type="concept",
            content="""# Variables: Storing Information

Imagine you have labeled boxes where you can store things. That's exactly what **variables** are in Python — named containers for storing data.

## Why Do Variables Exist?

Without variables, you'd have to repeat values everywhere:

```python
print("Alice")
print("Alice is learning Python")
print("Go Alice!")
```

If the name changes, you'd have to update every single line. With a variable, you change it in **one place**:

```python
name = "Alice"
print(name)
print(name, "is learning Python")
print("Go", name + "!")
```

Variables save you from repeating yourself and make your code easy to update.

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

**Important:** Variables don't display themselves — you still need `print()` to see the value. Just writing `name` on a line by itself won't show anything in a script.

## Reassignment: Variables Can Change

```python
score = 100
print(score)   # 100
score = 200
print(score)   # 200
```

When you reassign a variable, the old value is **gone**. Python doesn't remember it — the variable just points to the new value now.

## Common Mistake: Using a Variable Before Creating It

```python
print(greeting)        # NameError!
greeting = "Hello"
```

Python reads top to bottom. If you try to use a variable before the line that creates it, you'll get a `NameError`. The fix is simple: move the creation **above** the first use.

## Type Conversion

Sometimes you need to convert between types. Python gives you built-in functions for this:

```python
age = 25
print("I am " + str(age) + " years old")  # str() converts number to text

text_number = "42"
real_number = int(text_number)  # int() converts text to whole number
print(real_number + 8)          # 50

price = float("19.99")  # float() converts text to decimal number
print(price)             # 19.99
```

You'll use `str()`, `int()`, and `float()` constantly — especially when mixing text and numbers.

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

        # Try It Yourself: Variables
        Lesson.objects.create(
            module=m2, title="Try It Yourself: Variables", slug="try-it-yourself-variables", order=4,
            lesson_type="interactive",
            content="# Try It Yourself: Variables & Data Types\n\n"
                "Put your variable skills to work with these fun calculation challenges!\n\n"
                "## Challenge 1 — Road Trip Calculator\n\n"
                "Plan a road trip! Store these values in variables and calculate the total fuel cost:\n\n"
                "- Distance: 350 miles\n"
                "- Fuel efficiency: 25 miles per gallon\n"
                "- Gas price: $3.50 per gallon\n\n"
                "Print: `\"Trip cost: $XX.XX\"`\n\n"
                "## Challenge 2 — Age Calculator\n\n"
                "Given an age in years, calculate and print how many **days**, **hours**, and **minutes** old someone is (approximately):\n\n"
                "```\n"
                "Age: 25 years\n"
                "Days: 9125\n"
                "Hours: 219000\n"
                "Minutes: 13140000\n"
                "```\n\n"
                "(Assume 365 days per year, 24 hours per day, 60 minutes per hour.)\n\n"
                "## Challenge 3 — Mad Libs Story\n\n"
                "Create variables for: an animal, a color, a food, and a number. Then print a silly story using those variables:\n\n"
                "```\n"
                "The <color> <animal> ate <number> plates of <food> and fell asleep.\n"
                "```\n\n"
                "Make it as silly as you want!",
            sandbox_code='',
        )

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

## How Python Evaluates Conditions

When Python sees `temperature > 30`, it evaluates that expression and gets either `True` or `False`. These are called **booleans** — a data type with only two possible values.

```python
print(10 > 5)    # True
print(10 > 20)   # False
print(type(True)) # <class 'bool'>
```

You can think of every `if` condition as a question that Python answers with yes (`True`) or no (`False`).

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

Python checks conditions **top to bottom** and runs the **first** block that matches. Once it finds a match, it skips the rest — even if later conditions would also be true.

## Comparison Operators

| Operator | Meaning                |
|----------|------------------------|
| `==`     | Equal to               |
| `!=`     | Not equal to           |
| `>`      | Greater than           |
| `<`      | Less than              |
| `>=`     | Greater than or equal  |
| `<=`     | Less than or equal     |

## Common Mistake: `=` vs `==`

This is the #1 beginner mistake with conditionals:

```python
# WRONG — this assigns, not compares!
if x = 10:    # SyntaxError!

# RIGHT — double equals for comparison
if x == 10:
    print("x is ten")
```

- `=` means **"store this value"** (assignment)
- `==` means **"is this equal to?"** (comparison)

## Combining Conditions: `and` / `or`

You can combine conditions using `and` and `or`:

```python
age = 20
has_ticket = True

if age >= 18 and has_ticket:
    print("Welcome!")  # Both must be True
```

```python
is_student = True
is_senior = False

if is_student or is_senior:
    print("Discount!")  # At least one must be True
```

**How they work:**
- `and` → `True` only when **both** sides are `True`
- `or` → `True` when **at least one** side is `True`
- `not` → flips `True` to `False` and vice versa

## Nested `if` Blocks

You can put an `if` inside another `if`:

```python
has_account = True
age = 20

if has_account:
    if age >= 18:
        print("Full access")
    else:
        print("Limited access")
```

This works, but often `and` is cleaner: `if has_account and age >= 18:`

## Important: Indentation!

Python uses **indentation** (spaces) to group code inside `if` blocks. Always use 4 spaces:

```python
if True:
    print("This is indented")  # 4 spaces
print("This is NOT inside the if")
```

If your indentation is wrong, Python raises an `IndentationError`. This is Python's way of saying "I can't tell which lines belong inside the `if` block." Make sure every line inside an `if` is indented the same amount.""",
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

        # Exercise 3-5: Logical And (fill_blank)
        ex = Exercise.objects.create(
            lesson=l_m3, title="Logical And", slug="logical-and", order=5,
            exercise_type="fill_blank", difficulty=2,
            instructions='Complete the code so it prints `Access granted` only when both `age` is 18 or older **and** `has_id` is `True`.\n\nExpected output:\n```\nAccess granted\n```',
            starter_code='age = 21\nhas_id = True\n\nif age >= 18 ___ has_id:\n    print("Access granted")\nelse:\n    print("Access denied")',
            solution_code='age = 21\nhas_id = True\n\nif age >= 18 and has_id:\n    print("Access granted")\nelse:\n    print("Access denied")',
            xp_value=10, concepts="and, boolean logic, if",
        )
        TestCase.objects.create(exercise=ex, expected_output="Access granted", description="Should print Access granted", order=1)
        Hint.objects.create(exercise=ex, level=1, content="You need a keyword that requires **both** conditions to be true.", xp_penalty_percent=0)
        Hint.objects.create(exercise=ex, level=2, content="Replace `___` with `and`. Both conditions must be True for the block to run.", xp_penalty_percent=10)

        # Exercise 3-6: Fix the Condition (fix_bug)
        ex = Exercise.objects.create(
            lesson=l_m3, title="Fix the Condition", slug="fix-the-condition", order=6,
            exercise_type="fix_bug", difficulty=2,
            instructions='The code below should print `Equal` when `x` and `y` are the same, but it has a bug. Find and fix it.\n\nExpected output:\n```\nEqual\n```',
            starter_code='x = 10\ny = 10\n\nif x = y:\n    print("Equal")\nelse:\n    print("Not equal")',
            solution_code='x = 10\ny = 10\n\nif x == y:\n    print("Equal")\nelse:\n    print("Not equal")',
            xp_value=15, concepts="comparison, equality, debugging",
        )
        TestCase.objects.create(exercise=ex, expected_output="Equal", description="Should print Equal", order=1)
        Hint.objects.create(exercise=ex, level=1, content="Look at the comparison operator in the `if` statement. Is it the right one for checking equality?", xp_penalty_percent=0)
        Hint.objects.create(exercise=ex, level=2, content="Use `==` (double equals) for comparison, not `=` (single equals, which is assignment).", xp_penalty_percent=10)

        # Try It Yourself: Conditionals
        Lesson.objects.create(
            module=m3, title="Try It Yourself: Conditionals", slug="try-it-yourself-conditionals", order=4,
            lesson_type="interactive",
            content="# Try It Yourself: Making Decisions\n\n"
                "Test your conditional logic with these real-world scenarios!\n\n"
                "## Challenge 1 — Shipping Calculator\n\n"
                "Build a shipping cost calculator based on package weight:\n\n"
                "| Weight | Cost |\n"
                "|--------|------|\n"
                "| Under 1 kg | $5.00 |\n"
                "| 1 - 5 kg | $10.00 |\n"
                "| 5 - 20 kg | $20.00 |\n"
                "| Over 20 kg | $50.00 |\n\n"
                "Test with weights: `0.5`, `3`, `15`, `25`\n\n"
                "## Challenge 2 — Weather Advisor\n\n"
                "Given a temperature (in °F), print what to wear:\n\n"
                "- Below 32°F → `\"Brrr! Stay inside if you can!\"`\n"
                "- 32-50°F → `\"Wear a heavy coat and gloves\"`\n"
                "- 50-70°F → `\"A light jacket should do\"`\n"
                "- Above 70°F → `\"T-shirt weather!\"`\n\n"
                "## Challenge 3 — Password Validator\n\n"
                "Check a password against these rules and print which ones pass or fail:\n\n"
                "1. Length is at least 8 characters\n"
                "2. Contains at least one digit\n"
                "3. Contains at least one uppercase letter\n\n"
                "Print the result of each check, then `\"Password accepted!\"` if all pass or `\"Password rejected.\"` if any fail.",
            sandbox_code='',
        )

        # === MODULE 4: Loops ===
        m4 = modules["loops"]

        Lesson.objects.create(
            module=m4, title="Understanding Loops", slug="understanding-loops", order=1,
            lesson_type="concept",
            content="""# Loops: Repeating Things

Instead of writing the same code over and over, loops let you repeat actions automatically.

## The "Copy-Paste 100 Times" Problem

Imagine you need to print the numbers 1 through 100. Without loops, you'd write:

```python
print(1)
print(2)
print(3)
# ... 97 more lines?!
```

That's tedious and error-prone. Loops solve this — they let you say "do this thing N times" in just two lines.

## The `for` Loop

A `for` loop runs code **a specific number of times**:

```python
for i in range(5):
    print(i)
```

Output: `0, 1, 2, 3, 4` (each on a new line)

### How the loop variable changes

Let's trace through this step by step:
- **Iteration 1:** `i` is `0`, prints `0`
- **Iteration 2:** `i` is `1`, prints `1`
- **Iteration 3:** `i` is `2`, prints `2`
- **Iteration 4:** `i` is `3`, prints `3`
- **Iteration 5:** `i` is `4`, prints `4`
- Loop ends (no more values from `range`)

The variable `i` takes on a new value each time through the loop. You can name it anything — `i` is just a convention.

## `range()` Explained

`range()` generates numbers on the fly — it doesn't create a list in memory. It just produces the next number each time the loop asks for one.

| Code               | Produces        |
|--------------------|-----------------|
| `range(5)`         | 0, 1, 2, 3, 4  |
| `range(1, 6)`      | 1, 2, 3, 4, 5  |
| `range(0, 10, 2)`  | 0, 2, 4, 6, 8  |

### Common mistake: off-by-one

If you want numbers 1 through 5, you might write `range(5)` — but that gives you `0, 1, 2, 3, 4`. The stop value is **excluded**. Use `range(1, 6)` to get `1, 2, 3, 4, 5`.

Think of it as: `range(start, stop)` means "from start, up to **but not including** stop."

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

### Infinite loop warning

If the condition never becomes `False`, the loop runs forever:

```python
# DON'T DO THIS (infinite loop!)
while True:
    print("Help!")
```

Always make sure your `while` loop has a way to stop — either the condition eventually becomes `False`, or you use `break` to exit.

## The Accumulator Pattern

One of the most common loop patterns is building up a result:

```python
total = 0
for i in range(1, 6):
    total = total + i
    # Step by step: 0+1=1, 1+2=3, 3+3=6, 6+4=10, 10+5=15
print(total)  # 15
```

Start with an initial value (like `0`), then update it each iteration. You'll use this pattern constantly.

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

        # Exercise 4-5: Countdown (write_code)
        ex = Exercise.objects.create(
            lesson=l_m4, title="Countdown", slug="countdown", order=5,
            exercise_type="write_code", difficulty=2,
            instructions='Write a `while` loop that counts down from 5 to 1, printing each number, then prints `Go!` after the loop.\n\nExpected output:\n```\n5\n4\n3\n2\n1\nGo!\n```',
            starter_code='# Write a while loop that counts down from 5 to 1\n# Then print "Go!"\n',
            solution_code='n = 5\n\nwhile n >= 1:\n    print(n)\n    n = n - 1\n\nprint("Go!")',
            xp_value=15, concepts="while loop, countdown",
        )
        TestCase.objects.create(exercise=ex, expected_output="5\n4\n3\n2\n1\nGo!", description="Should count down then print Go!", order=1)
        Hint.objects.create(exercise=ex, level=1, content="Start a variable at 5, use `while n >= 1:`, print `n`, then decrease it by 1 each iteration.", xp_penalty_percent=0)
        Hint.objects.create(exercise=ex, level=2, content='`n = 5` then `while n >= 1:` with `print(n)` and `n = n - 1` inside. After the loop: `print("Go!")`', xp_penalty_percent=10)

        # Exercise 4-6: Break on Target (fill_blank)
        ex = Exercise.objects.create(
            lesson=l_m4, title="Break on Target", slug="break-on-target", order=6,
            exercise_type="fill_blank", difficulty=1,
            instructions='Complete the code so the loop stops when it finds `"cherry"` in the list. It should print each fruit until it hits the target, then print `Found it!`.\n\nExpected output:\n```\napple\nbanana\nFound it!\n```',
            starter_code='fruits = ["apple", "banana", "cherry", "date"]\n\nfor fruit in fruits:\n    if fruit == "cherry":\n        print("Found it!")\n        ___\n    print(fruit)',
            solution_code='fruits = ["apple", "banana", "cherry", "date"]\n\nfor fruit in fruits:\n    if fruit == "cherry":\n        print("Found it!")\n        break\n    print(fruit)',
            xp_value=10, concepts="for, break",
        )
        TestCase.objects.create(exercise=ex, expected_output="apple\nbanana\nFound it!", description="Should stop at cherry", order=1)
        Hint.objects.create(exercise=ex, level=1, content="There's a keyword that immediately exits a loop...", xp_penalty_percent=0)
        Hint.objects.create(exercise=ex, level=2, content="Replace `___` with `break`. It exits the `for` loop immediately.", xp_penalty_percent=10)

        # Try It Yourself: Loops
        Lesson.objects.create(
            module=m4, title="Try It Yourself: Loops", slug="try-it-yourself-loops", order=4,
            lesson_type="interactive",
            content="# Try It Yourself: Loops\n\n"
                "These challenges give you hands-on practice with for loops, while loops, and range()!\n\n"
                "## Challenge 1 — Star Triangle\n\n"
                "Print a right triangle pattern of stars. Row 1 has 1 star, row 2 has 2 stars, etc., up to 7 rows.\n\n"
                "```\n"
                "*\n"
                "**\n"
                "***\n"
                "****\n"
                "*****\n"
                "******\n"
                "*******\n"
                "```\n\n"
                "## Challenge 2 — FizzBuzz\n\n"
                "Print numbers from 1 to 30, but:\n"
                "- For multiples of 3, print `Fizz` instead\n"
                "- For multiples of 5, print `Buzz` instead\n"
                "- For multiples of both 3 and 5, print `FizzBuzz`\n\n"
                "## Challenge 3 — Even Sum\n\n"
                "Calculate and print the sum of all even numbers from 2 to 100 (inclusive) using a loop.\n\n"
                "The answer should be `2550`.\n\n"
                "## Challenge 4 — Number Pyramid\n\n"
                "Print a number pyramid where each row shows numbers from 1 up to the row number:\n\n"
                "```\n"
                "1\n"
                "1 2\n"
                "1 2 3\n"
                "1 2 3 4\n"
                "1 2 3 4 5\n"
                "```\n\n"
                "Hint: Use a nested loop or `range()` with `print(..., end=\" \")`.",
            sandbox_code='',
        )

        # === MODULE 5: Functions ===
        m5 = modules["functions"]

        Lesson.objects.create(
            module=m5, title="What Are Functions?", slug="what-are-functions", order=1,
            lesson_type="concept",
            content="""# Functions: Reusable Code Blocks

A **function** is a named block of code you can call whenever you need it. Think of it like a machine: you put something in (the **input**), the machine does its work, and something comes out (the **output**).

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

## `print()` vs `return` — The #1 Confusion

This trips up almost every beginner:

```python
def add_print(a, b):
    print(a + b)    # Shows the value on screen, but doesn't send it back

def add_return(a, b):
    return a + b    # Sends the value back to the caller

# With print:
result = add_print(3, 4)   # Displays 7 on screen
print(result)               # None! The function didn't return anything

# With return:
result = add_return(3, 4)  # Nothing displayed, but result is 7
print(result)               # 7
```

- `print()` **shows** a value on screen — it's for humans to read
- `return` **sends** a value back to the code that called the function — it's for your program to use

If your function needs to give a value back (so you can use it later, do math with it, etc.), use `return`. If you just want to display something, use `print()`.

## What Happens When You Forget `return`?

If a function doesn't have a `return` statement, it returns `None` by default:

```python
def broken_add(a, b):
    a + b  # This calculates the sum but doesn't do anything with it!

result = broken_add(3, 4)
print(result)  # None
```

## Scope: Variables Inside Functions Stay Inside

Variables created inside a function **don't exist** outside of it:

```python
def my_function():
    secret = "hello"
    print(secret)  # Works fine

my_function()
print(secret)  # NameError! 'secret' doesn't exist here
```

This is called **scope**. The function is like a room — what happens inside stays inside.

## Default Parameters

```python
def greet(name, greeting="Hello"):
    print(greeting, name)

greet("Alice")             # Hello Alice
greet("Bob", "Hey")        # Hey Bob
```

## When to Create a Function

A good rule of thumb: if you're writing the same (or very similar) code **three or more times**, wrap it in a function. Also use functions when a block of code does one clear task — giving it a name makes your code easier to read.

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

        # Exercise 5-5: Default Greeting (fill_blank)
        ex = Exercise.objects.create(
            lesson=l_m5, title="Default Greeting", slug="default-greeting", order=5,
            exercise_type="fill_blank", difficulty=1,
            instructions='Complete the function so it uses a **default parameter** of `"Hello"` for `greeting`. When called without a second argument, it should use the default.\n\nExpected output:\n```\nHello, Alice!\nHey, Bob!\n```',
            starter_code='def greet(name, greeting___):\n    print(f"{greeting}, {name}!")\n\ngreet("Alice")\ngreet("Bob", "Hey")',
            solution_code='def greet(name, greeting="Hello"):\n    print(f"{greeting}, {name}!")\n\ngreet("Alice")\ngreet("Bob", "Hey")',
            xp_value=10, concepts="functions, default parameters",
        )
        TestCase.objects.create(exercise=ex, expected_output="Hello, Alice!\nHey, Bob!", description="Should use default and explicit greeting", order=1)
        Hint.objects.create(exercise=ex, level=1, content="Default parameters are set with `=` in the function definition: `def func(param=default_value):`.", xp_penalty_percent=0)
        Hint.objects.create(exercise=ex, level=2, content='Replace `___` with `="Hello"`. The full parameter becomes `greeting="Hello"`.', xp_penalty_percent=10)

        # Exercise 5-6: Fix the Return (fix_bug)
        ex = Exercise.objects.create(
            lesson=l_m5, title="Fix the Return", slug="fix-the-return", order=6,
            exercise_type="fix_bug", difficulty=2,
            instructions='This function should **return** the doubled value so it can be printed, but it has a common beginner bug. Fix it.\n\nExpected output:\n```\n14\n```',
            starter_code='def double(n):\n    print(n * 2)\n\nresult = double(7)\nprint(result)',
            solution_code='def double(n):\n    return n * 2\n\nresult = double(7)\nprint(result)',
            xp_value=15, concepts="functions, return, print vs return",
        )
        TestCase.objects.create(exercise=ex, expected_output="14", description="Should print 14", order=1)
        Hint.objects.create(exercise=ex, level=1, content="The function uses `print()` inside but the caller expects a value back. What keyword sends a value back?", xp_penalty_percent=0)
        Hint.objects.create(exercise=ex, level=2, content="Replace `print(n * 2)` with `return n * 2`. Functions need `return` to send values back to the caller.", xp_penalty_percent=10)

        # Try It Yourself: Functions
        Lesson.objects.create(
            module=m5, title="Try It Yourself: Functions", slug="try-it-yourself-functions", order=4,
            lesson_type="interactive",
            content="# Try It Yourself: Functions\n\n"
                "Practice writing reusable functions that solve practical problems!\n\n"
                "## Challenge 1 — Max of Three\n\n"
                "Write a `max_of_three(a, b, c)` function that returns the largest of three numbers **without** using the built-in `max()` function. Use if/elif/else logic.\n\n"
                "Test with: `max_of_three(10, 25, 17)` → `25`\n\n"
                "## Challenge 2 — Even Filter\n\n"
                "Write an `is_even(n)` function that returns `True` if `n` is even, `False` otherwise. Then use it to filter a list, printing only the even numbers.\n\n"
                "```python\n"
                "numbers = [1, 4, 7, 10, 13, 16, 19, 22]\n"
                "```\n\n"
                "## Challenge 3 — Tip Calculator\n\n"
                "Write a `calculate_tip(bill, percent)` function that returns the tip amount. Then print a mini receipt:\n\n"
                "```\n"
                "Subtotal: $85.50\n"
                "Tip (18%): $15.39\n"
                "Total:     $100.89\n"
                "```\n\n"
                "Round the tip to 2 decimal places using `round()`.",
            sandbox_code='',
        )

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

Lists are **zero-indexed** — the first item is at position `0`, not `1`. This is a convention in most programming languages.

```python
fruits = ["apple", "banana", "cherry"]
print(fruits[0])   # apple
print(fruits[1])   # banana
print(fruits[-1])  # cherry (last item)
```

### Negative indexing

Negative indices count backwards from the end. `-1` is the last item, `-2` is second-to-last, and so on:

```python
colors = ["red", "green", "blue", "yellow"]
print(colors[-1])   # yellow (last)
print(colors[-2])   # blue (second from end)
```

This is handy when you don't know (or don't care) how long the list is.

### Common mistake: IndexError

If you try to access an index that doesn't exist, Python raises an `IndexError`:

```python
fruits = ["apple", "banana"]
print(fruits[5])  # IndexError: list index out of range
```

Always make sure your index is within bounds. You can check with `len()`.

## Modifying Lists

```python
fruits = ["apple", "banana", "cherry"]
fruits.append("date")       # Add to end
fruits[0] = "avocado"       # Change first item
fruits.remove("banana")     # Remove by value
print(len(fruits))          # Length: 3
```

## Slicing

Get a portion of a list using `[start:stop]`. This means "from start up to **but not including** stop":

```python
nums = [10, 20, 30, 40, 50]
print(nums[1:4])   # [20, 30, 40]  — indices 1, 2, 3
print(nums[:3])    # [10, 20, 30]  — from the beginning
print(nums[2:])    # [30, 40, 50]  — to the end
```

## Looping Over Lists

```python
for fruit in fruits:
    print(fruit)
```

## `sort()` vs `sorted()`

These two look similar but behave differently:

```python
nums = [3, 1, 2]

# sort() changes the list itself (returns None)
nums.sort()
print(nums)  # [1, 2, 3]

# sorted() returns a NEW list (original unchanged)
nums = [3, 1, 2]
new_list = sorted(nums)
print(new_list)  # [1, 2, 3]
print(nums)      # [3, 1, 2] — still the original order
```

## Useful List Methods

| Method          | What it does                |
|-----------------|-----------------------------|
| `append(x)`     | Add item to end             |
| `insert(i, x)`  | Insert at position          |
| `remove(x)`     | Remove first occurrence     |
| `pop()`          | Remove and return last item |
| `sort()`         | Sort in place               |
| `len(list)`      | Get number of items         |

## Tuples

Tuples are like lists, but **immutable** (can't be changed after creation):

```python
point = (10, 20)
print(point[0])  # 10
```

Use tuples for data that shouldn't change — coordinates, RGB colors, fixed configurations, or dictionary keys. If you try to modify a tuple, Python raises a `TypeError`.""",
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

        # Exercise 6-5: Unpack the Tuple (fill_blank)
        ex = Exercise.objects.create(
            lesson=l_m6, title="Unpack the Tuple", slug="unpack-the-tuple", order=5,
            exercise_type="fill_blank", difficulty=1,
            instructions='Complete the code to **unpack** the tuple into three variables and print them.\n\nExpected output:\n```\nAlice is 25 from Boston\n```',
            starter_code='person = ("Alice", 25, "Boston")\n\n___, ___, ___ = person\nprint(f"{name} is {age} from {city}")',
            solution_code='person = ("Alice", 25, "Boston")\n\nname, age, city = person\nprint(f"{name} is {age} from {city}")',
            xp_value=10, concepts="tuples, unpacking",
        )
        TestCase.objects.create(exercise=ex, expected_output="Alice is 25 from Boston", description="Should unpack and print tuple", order=1)
        Hint.objects.create(exercise=ex, level=1, content="Tuple unpacking lets you assign each element to a variable in one line: `a, b, c = my_tuple`.", xp_penalty_percent=0)
        Hint.objects.create(exercise=ex, level=2, content="Replace the three `___` with `name`, `age`, `city` to match the tuple's three elements.", xp_penalty_percent=10)

        # Exercise 6-6: Sort and Slice (write_code)
        ex = Exercise.objects.create(
            lesson=l_m6, title="Sort and Slice", slug="sort-and-slice", order=6,
            exercise_type="write_code", difficulty=2,
            instructions='Sort the list of scores in descending order and print the top 3.\n\nExpected output:\n```\n95\n88\n76\n```',
            starter_code='scores = [42, 88, 65, 95, 76, 33]\n\n# Sort descending and print the top 3\n',
            solution_code='scores = [42, 88, 65, 95, 76, 33]\n\nscores.sort(reverse=True)\nfor s in scores[:3]:\n    print(s)',
            xp_value=15, concepts="lists, sort, slicing",
        )
        TestCase.objects.create(exercise=ex, expected_output="95\n88\n76", description="Should print top 3 scores", order=1)
        Hint.objects.create(exercise=ex, level=1, content="Use `.sort(reverse=True)` to sort descending, then `scores[:3]` to get the first 3.", xp_penalty_percent=0)
        Hint.objects.create(exercise=ex, level=2, content='`scores.sort(reverse=True)` then `for s in scores[:3]: print(s)`', xp_penalty_percent=10)

        # Try It Yourself: Lists
        Lesson.objects.create(
            module=m6, title="Try It Yourself: Lists & Tuples", slug="try-it-yourself-lists", order=4,
            lesson_type="interactive",
            content="# Try It Yourself: Lists & Tuples\n\n"
                "These challenges will strengthen your ability to work with collections of data!\n\n"
                "## Challenge 1 — Even/Odd Splitter\n\n"
                "Take this list of numbers and split it into two separate lists — one for even numbers and one for odd numbers. Print both lists.\n\n"
                "```python\n"
                "numbers = [14, 7, 22, 3, 18, 9, 30, 11, 6, 25]\n"
                "```\n\n"
                "## Challenge 2 — Stats Without Built-ins\n\n"
                "Find the minimum, maximum, and average of a list of numbers **without** using `min()`, `max()`, or `sum()`. Use loops only!\n\n"
                "```python\n"
                "scores = [85, 92, 78, 95, 88, 73, 91]\n"
                "```\n\n"
                "Print: `Min: 73`, `Max: 95`, `Average: 86.0`\n\n"
                "## Challenge 3 — Student Scores Filter\n\n"
                "Create a list of tuples, each containing a student name and their score. Print only the students who scored above 80.\n\n"
                "```python\n"
                "students = [(\"Alice\", 92), (\"Bob\", 65), (\"Charlie\", 88), (\"Diana\", 71), (\"Eve\", 95)]\n"
                "```\n\n"
                "Print: `Alice: 92` etc. for passing students only.",
            sandbox_code='',
        )

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

## When to Use a Dict vs a List

- **List** → when you have a collection of similar items and access them by position (index 0, 1, 2...)
- **Dict** → when you want to look up items by name (like "hostname", "ip", "status")

Think of it like this: a list is a numbered list, a dict is a phone book. You'd never look up someone's number by saying "give me entry #47" — you look it up by name.

## Accessing Values

```python
print(person["name"])   # Alice
print(person["age"])    # 25
```

### Common mistake: KeyError

If you access a key that doesn't exist, Python crashes with a `KeyError`:

```python
print(person["phone"])  # KeyError: 'phone'
```

Three ways to avoid this:

```python
# 1. Check first
if "phone" in person:
    print(person["phone"])

# 2. Use .get() with a default
print(person.get("phone", "N/A"))  # N/A (no crash!)

# 3. Use try/except
try:
    print(person["phone"])
except KeyError:
    print("Key not found")
```

The `.get()` method is the most common approach — it returns a default value instead of crashing.

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

## Nested Dictionaries

Dicts can contain other dicts — this is extremely common in real-world data:

```python
device = {
    "hostname": "R1",
    "interfaces": {
        "Gi0/0": {"ip": "10.0.0.1", "status": "up"},
        "Gi0/1": {"ip": "10.0.1.1", "status": "down"}
    }
}

# Access nested values by chaining keys
print(device["interfaces"]["Gi0/0"]["ip"])  # 10.0.0.1
```

Real-world analogy: think of a network device config. The device has a hostname, and inside it has interfaces, each with their own settings.

## Useful Methods

| Method                   | What it does              |
|--------------------------|---------------------------|
| `dict.keys()`            | Get all keys              |
| `dict.values()`          | Get all values            |
| `dict.items()`           | Get all key-value pairs   |
| `dict.get(key, default)` | Get value safely          |
| `len(dict)`              | Number of key-value pairs |""",
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

        # Try It Yourself: Dictionaries
        Lesson.objects.create(
            module=m7, title="Try It Yourself: Dictionaries", slug="try-it-yourself-dictionaries", order=4,
            lesson_type="interactive",
            content="# Try It Yourself: Dictionaries\n\n"
                "These challenges go beyond basic lookups — you'll build real data structures with dicts!\n\n"
                "## Challenge 1 — Contact Book\n\n"
                "Build a simple contact book using a dictionary:\n\n"
                "1. Start with 3 contacts: `{\"Alice\": \"555-0101\", \"Bob\": \"555-0102\", \"Charlie\": \"555-0103\"}`\n"
                "2. Look up Bob's number and print it\n"
                "3. Add a new contact: `\"Diana\": \"555-0104\"`\n"
                "4. Delete Charlie's entry\n"
                "5. Print the final contact book\n\n"
                "## Challenge 2 — Inventory System\n\n"
                "Manage a store inventory:\n\n"
                "```python\n"
                "inventory = {\"apples\": 50, \"bananas\": 30, \"oranges\": 25, \"grapes\": 10}\n"
                "```\n\n"
                "1. Restock bananas by 20\n"
                "2. Sell 15 apples\n"
                "3. Print items with quantity below 20 (low stock warning)\n"
                "4. Print the final inventory\n\n"
                "## Challenge 3 — Nested Network Switch\n\n"
                "Create a nested dictionary representing a network switch:\n\n"
                "```python\n"
                "switch = {\n"
                "    \"hostname\": \"SW-CORE-01\",\n"
                "    \"model\": \"Cisco 3850\",\n"
                "    \"interfaces\": [\n"
                "        {\"name\": \"Gi0/0\", \"status\": \"up\", \"speed\": \"1Gbps\"},\n"
                "        {\"name\": \"Gi0/1\", \"status\": \"down\", \"speed\": \"1Gbps\"},\n"
                "        {\"name\": \"Gi0/2\", \"status\": \"up\", \"speed\": \"10Gbps\"},\n"
                "    ]\n"
                "}\n"
                "```\n\n"
                "Print the switch hostname, count of `up` interfaces, and details of each interface.",
            sandbox_code='',
        )

        # === MODULE 8: String Magic ===
        m8 = modules["string-magic"]

        Lesson.objects.create(
            module=m8, title="String Methods", slug="string-methods", order=1,
            lesson_type="concept",
            content="""# String Magic: Manipulating Text

Strings in Python come with many built-in **methods** — functions that transform or inspect text.

## Strings Are Immutable

This is the most important thing to understand about strings: you **cannot change them in place**. Every string method returns a **new** string — the original stays the same.

```python
text = "hello"
text.upper()       # Returns "HELLO", but text is still "hello"!
print(text)        # hello — unchanged!

text = text.upper()  # NOW text is "HELLO" (reassigned)
print(text)          # HELLO
```

### Common mistake

Thinking `.upper()` changes the original string:

```python
name = "alice"
name.upper()    # This does nothing useful! The result is thrown away
print(name)     # alice — still lowercase!

name = name.upper()  # Fix: save the result back
print(name)          # ALICE
```

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

## Method Chaining

Since each method returns a new string, you can chain them together:

```python
raw = "  Hello, World!  "
clean = raw.strip().lower().replace("world", "python")
print(clean)  # hello, python!
```

Python evaluates left to right: first `strip()`, then `lower()` on that result, then `replace()` on that result.

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

## Escape Characters

Special characters you can put inside strings:

```python
print("Line 1\\nLine 2")   # \\n = newline
print("Name:\\tAlice")      # \\t = tab
print("She said \\"hello\\"") # \\" = literal quote
print("Path: C:\\\\Users")   # \\\\ = literal backslash
```

## Raw Strings

Prefixing a string with `r` tells Python to treat backslashes as literal characters (no escaping):

```python
print(r"\\d+\\.\\d+")  # \\d+\\.\\d+ (useful for regex patterns!)
```

We'll use raw strings extensively in the Regular Expressions module.

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

        # Try It Yourself: Strings
        Lesson.objects.create(
            module=m8, title="Try It Yourself: String Magic", slug="try-it-yourself-strings", order=4,
            lesson_type="interactive",
            content="# Try It Yourself: String Magic\n\n"
                "These challenges test your string manipulation skills with fun, practical scenarios!\n\n"
                "## Challenge 1 — Password Strength Checker\n\n"
                "Analyze a password string and rate its strength based on:\n"
                "- Length >= 8 characters\n"
                "- Contains at least one uppercase letter\n"
                "- Contains at least one lowercase letter\n"
                "- Contains at least one digit\n"
                "- Contains at least one special character (`!@#$%^&*`)\n\n"
                "Print which checks pass/fail, then rate: **Strong** (all pass), **Medium** (3-4 pass), **Weak** (0-2 pass).\n\n"
                "## Challenge 2 — Caesar Cipher\n\n"
                "Implement a simple Caesar cipher that shifts each letter by N positions in the alphabet. Non-letter characters stay unchanged. The shift should wrap around (z + 1 = a).\n\n"
                "Test with: `\"Hello, World!\"` shifted by 3 → `\"Khoor, Zruog!\"`\n\n"
                "Hint: Use `ord()` and `chr()` to work with character codes.\n\n"
                "## Challenge 3 — CSV Table Formatter\n\n"
                "Parse a CSV-like string into a neatly formatted table:\n\n"
                "```\n"
                "Name,Age,City\n"
                "Alice,30,New York\n"
                "Bob,25,London\n"
                "Charlie,35,Tokyo\n"
                "```\n\n"
                "Output a table with aligned columns using `split()`, `join()`, and f-strings.",
            sandbox_code='',
        )

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

**When NOT to use:** Don't nest ternary expressions. `"A" if x > 90 else "B" if x > 80 else "C"` is hard to read — use a regular `if/elif/else` chain instead.

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

**When NOT to use:** If the comprehension gets long or has complex logic, a regular `for` loop is clearer. A one-liner that takes 30 seconds to read is worse than three lines that are instantly obvious. If you're nesting comprehensions or adding multiple conditions, switch to a loop.

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
```

**When NOT to use:** Don't use walrus operators when a regular assignment is just as clear. The walrus shines when you need to both assign and test in one expression. If you're using it just to save a line, the regular two-line version is probably more readable.""",
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

        # Exercise 9-5: Squares List (write_code)
        ex = Exercise.objects.create(
            lesson=l_m9, title="Squares List", slug="squares-list", order=5,
            exercise_type="write_code", difficulty=2,
            instructions='Use a **list comprehension** to create a list of squares from 1 to 10 (`1, 4, 9, ... 100`), then print the list.\n\nExpected output:\n```\n[1, 4, 9, 16, 25, 36, 49, 64, 81, 100]\n```',
            starter_code='# Create a list of squares from 1 to 10 using a list comprehension\n\n\n# Print the list\n',
            solution_code='squares = [n ** 2 for n in range(1, 11)]\nprint(squares)',
            xp_value=15, concepts="list comprehension, range, exponent",
        )
        TestCase.objects.create(exercise=ex, expected_output="[1, 4, 9, 16, 25, 36, 49, 64, 81, 100]", description="Should print list of squares", order=1)
        Hint.objects.create(exercise=ex, level=1, content="A list comprehension looks like `[expression for var in iterable]`. Use `n ** 2` for squaring.", xp_penalty_percent=0)
        Hint.objects.create(exercise=ex, level=2, content='`squares = [n ** 2 for n in range(1, 11)]` then `print(squares)`', xp_penalty_percent=10)

        # Exercise 9-6: Fix the Comprehension (fix_bug)
        ex = Exercise.objects.create(
            lesson=l_m9, title="Fix the Comprehension", slug="fix-the-comprehension", order=6,
            exercise_type="fix_bug", difficulty=2,
            instructions='This list comprehension has a syntax error. Fix it so it produces even numbers from 0 to 8.\n\nExpected output:\n```\n[0, 2, 4, 6, 8]\n```',
            starter_code='evens = [n for n in range(10) if n % 2 = 0]\nprint(evens)',
            solution_code='evens = [n for n in range(10) if n % 2 == 0]\nprint(evens)',
            xp_value=10, concepts="list comprehension, debugging, comparison",
        )
        TestCase.objects.create(exercise=ex, expected_output="[0, 2, 4, 6, 8]", description="Should print even numbers", order=1)
        Hint.objects.create(exercise=ex, level=1, content="Look at the comparison inside the `if` filter. Is it using the right operator?", xp_penalty_percent=0)
        Hint.objects.create(exercise=ex, level=2, content="Change `= 0` to `== 0`. Use `==` for comparison, not `=` (assignment).", xp_penalty_percent=10)

        # Try It Yourself: Cleaner Code
        Lesson.objects.create(
            module=m9, title="Try It Yourself: Cleaner Code", slug="try-it-yourself-cleaner-code", order=4,
            lesson_type="interactive",
            content="# Try It Yourself: Writing Cleaner Code\n\n"
                "Practice transforming verbose Python into clean, Pythonic one-liners!\n\n"
                "## Challenge 1 — Ternary Rewrites\n\n"
                "Rewrite each of these if/else blocks as a single-line ternary expression:\n\n"
                "**Block A:**\n"
                "```python\n"
                "age = 20\n"
                "if age >= 18:\n"
                "    status = \"adult\"\n"
                "else:\n"
                "    status = \"minor\"\n"
                "```\n\n"
                "**Block B:**\n"
                "```python\n"
                "score = 75\n"
                "if score >= 60:\n"
                "    result = \"pass\"\n"
                "else:\n"
                "    result = \"fail\"\n"
                "```\n\n"
                "**Block C:**\n"
                "```python\n"
                "items = []\n"
                "if items:\n"
                "    message = \"has items\"\n"
                "else:\n"
                "    message = \"empty\"\n"
                "```\n\n"
                "## Challenge 2 — List Comprehension Conversions\n\n"
                "Convert these 3 loops into list comprehensions. At least one should include a filter condition.\n\n"
                "1. Squares of 1-10\n"
                "2. Uppercase words from a list (filter: only words longer than 3 letters)\n"
                "3. Even numbers from 1-20\n\n"
                "## Challenge 3 — Walrus Operator\n\n"
                "Use the walrus operator (`:=`) inside a while loop to process items from a list until a sentinel value (`\"STOP\"`) is found.\n\n"
                "```python\n"
                "items = [\"apple\", \"banana\", \"cherry\", \"STOP\", \"date\", \"elderberry\"]\n"
                "```\n\n"
                "Print each item before STOP, then print how many items were processed.",
            sandbox_code='',
        )

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

| Task                   | Tool               | Key function                          |
|------------------------|--------------------|---------------------------------------|
| Validate/inspect IPs   | `ipaddress`        | `ip_address()`, `ip_network()`, `in`  |
| Parse text output      | `str` methods + `re` | `.split()`, `.strip()`, `re.search()` |
| Read structured configs | `json`            | `json.loads()`                        |

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

        # Try It Yourself: Network Python
        Lesson.objects.create(
            module=m10, title="Try It Yourself: Network Python", slug="try-it-yourself-network-python", order=4,
            lesson_type="interactive",
            content="# Try It Yourself: Python for Network Engineers\n\n"
                "Apply your networking Python skills to real-world scenarios!\n\n"
                "## Challenge 1 — IP Address Validator & Classifier\n\n"
                "Validate a list of IP address strings and classify the valid ones as private or public.\n\n"
                "```python\n"
                "ips = [\"192.168.1.1\", \"8.8.8.8\", \"999.999.999.999\", \"10.0.0.1\", \"172.16.0.1\", \"not_an_ip\", \"1.1.1.1\"]\n"
                "```\n\n"
                "For each, print: `192.168.1.1 -> valid (private)` or `999.999.999.999 -> invalid`\n\n"
                "Hint: Use `ipaddress.ip_address()` in a try/except, then check `.is_private`.\n\n"
                "## Challenge 2 — Subnet Calculator\n\n"
                "Given a list of CIDR subnets, calculate and print network details.\n\n"
                "```python\n"
                "subnets = [\"10.0.0.0/24\", \"192.168.1.0/28\", \"172.16.0.0/16\"]\n"
                "```\n\n"
                "For each, print: network address, broadcast address, number of usable hosts.\n\n"
                "## Challenge 3 — Routing Table Parser\n\n"
                "Parse a mock routing table and extract only the default routes.\n\n"
                "```\n"
                "0.0.0.0/0       via 10.0.0.1    eth0\n"
                "192.168.1.0/24  via 192.168.1.1 eth1\n"
                "10.0.0.0/8      via 10.0.0.1    eth0\n"
                "0.0.0.0/0       via 172.16.0.1  eth2\n"
                "172.16.0.0/16   via 172.16.0.1  eth2\n"
                "```\n\n"
                "Print only the default route lines and their next-hop addresses.",
            sandbox_code='',
        )

        # === MODULE 11: Handling Errors ===
        m11 = modules["handling-errors"]

        Lesson.objects.create(
            module=m11, title="When Things Go Wrong", slug="when-things-go-wrong", order=1,
            lesson_type="concept",
            content="""# Handling Errors Gracefully

When your Python script encounters a problem — a bad IP address, a missing dictionary key, dividing by zero — it raises an **exception**. An exception is Python's way of saying "I can't do what you asked." Without handling, your script crashes. With `try/except`, you stay in control.

## What Is an Exception?

When something goes wrong, Python creates an exception object that describes the problem. If you don't handle it, Python prints a traceback and stops your program:

```python
print(int("hello"))
# Traceback (most recent call last):
#   File "script.py", line 1, in <module>
#     print(int("hello"))
# ValueError: invalid literal for int() with base 10: 'hello'
```

The last line tells you the type (`ValueError`) and what went wrong. Learning to read these messages is a superpower.

## The `try/except` Block

```python
try:
    number = int("hello")
except ValueError:
    print("That's not a number!")
```

The code inside `try` runs normally. If an exception occurs, Python jumps to the matching `except` block instead of crashing.

## Common Exception Types

| Exception            | When it happens                              |
|----------------------|----------------------------------------------|
| `ValueError`         | Wrong type of value (e.g., `int("hello")`)   |
| `KeyError`           | Missing dictionary key                       |
| `TypeError`          | Wrong type for an operation (e.g., `"a" + 1`) |
| `IndexError`         | List index out of range                      |
| `ZeroDivisionError`  | Dividing by zero                             |

## Catching the Error Message

Use `as e` to capture the error details:

```python
try:
    result = 10 / 0
except ZeroDivisionError as e:
    print(f"Error: {e}")
# Error: division by zero
```

## Why Bare `except:` Is Bad Practice

You might be tempted to catch *everything*:

```python
# DON'T DO THIS
try:
    result = some_function()
except:
    print("Something went wrong")
```

This catches **all** exceptions, including ones you didn't expect (like typos in variable names). It hides real bugs. Always catch **specific** exception types so unexpected errors still surface.

## Multiple `except` Blocks

```python
try:
    data = {"name": "Alice"}
    print(data["age"])
except KeyError:
    print("Key not found!")
except TypeError:
    print("Type error!")
```

## Common Mistake: Catching Too Broadly

```python
# Too broad — hides bugs
try:
    user_data = get_user(user_id)
    print(user_data["name"])
except Exception:
    print("Error")  # Was it a missing key? A network error? A typo? Who knows!

# Better — specific exceptions
try:
    user_data = get_user(user_id)
    print(user_data["name"])
except KeyError:
    print("Missing 'name' in user data")
```

## `else` and `finally`

```python
try:
    value = int("42")
except ValueError:
    print("Bad value")
else:
    print(f"Success: {value}")  # Runs only if no exception
finally:
    print("Done")  # Always runs, even if there was an error
```

- **`else`** runs only when the `try` block succeeds — use it for code that should only run on success
- **`finally`** runs no matter what — use it for cleanup (closing files, resetting state)

## Two Styles: Ask Forgiveness vs Look Before You Leap

Both approaches are valid:

```python
# "Look Before You Leap" — check first
if "age" in person:
    print(person["age"])

# "Ask Forgiveness" — try it and handle failure
try:
    print(person["age"])
except KeyError:
    print("No age found")
```

In Python, the "ask forgiveness" (try/except) style is often preferred when the error case is rare.

## Why This Matters for Network Scripts

Network scripts deal with unpredictable data — user-entered IPs, missing config keys, device responses that don't match expectations. Error handling keeps your tools robust.""",
        )

        Lesson.objects.create(
            module=m11, title="Try It: Error Handling", slug="try-it-error-handling", order=2,
            lesson_type="interactive",
            content="""# Try It: Error Handling

Experiment with `try/except` in the editor below. Try changing the values to trigger different exceptions!

## Catching Different Errors

The sandbox has examples of `ValueError`, `KeyError`, and `ZeroDivisionError`. Modify the code to see what happens.""",
            sandbox_code='# Try/except with ValueError\ntry:\n    number = int("not_a_number")\nexcept ValueError as e:\n    print(f"ValueError caught: {e}")\n\n# Try/except with KeyError\ndevice = {"hostname": "R1", "ip": "10.0.0.1"}\ntry:\n    print(device["location"])\nexcept KeyError as e:\n    print(f"KeyError caught: missing key {e}")\n\n# Try/except with ZeroDivisionError\ntry:\n    result = 100 / 0\nexcept ZeroDivisionError:\n    print("Cannot divide by zero!")\n\n# Using else and finally\ntry:\n    value = int("42")\nexcept ValueError:\n    print("Bad input")\nelse:\n    print(f"Parsed successfully: {value}")\nfinally:\n    print("Cleanup done")',
        )

        l_m11 = Lesson.objects.create(
            module=m11, title="Practice: Error Handling", slug="practice-error-handling", order=3,
            lesson_type="exercise",
            content="# Practice Time!\n\nHandle errors like a pro with these exercises.",
        )

        # Exercise 11-1: Catch the Error (fill_blank)
        ex = Exercise.objects.create(
            lesson=l_m11, title="Catch the Error", slug="catch-the-error", order=1,
            exercise_type="fill_blank", difficulty=1,
            instructions='Complete the `try/except` block to catch the `ValueError` when converting bad input.\n\nExpected output:\n```\nCould not convert to integer\n```',
            starter_code='try:\n    number = int("abc")\nexcept ___:\n    print("Could not convert to integer")',
            solution_code='try:\n    number = int("abc")\nexcept ValueError:\n    print("Could not convert to integer")',
            xp_value=10, concepts="try, except, ValueError",
        )
        TestCase.objects.create(exercise=ex, expected_output="Could not convert to integer", description="Should catch ValueError", order=1)
        Hint.objects.create(exercise=ex, level=1, content="`int(\"abc\")` fails because `\"abc\"` isn't a valid number. What type of error is this?", xp_penalty_percent=0)
        Hint.objects.create(exercise=ex, level=2, content="Replace `___` with `ValueError`. This is the exception raised by invalid `int()` conversions.", xp_penalty_percent=10)

        # Exercise 11-2: Safe Dictionary Lookup (write_code)
        ex = Exercise.objects.create(
            lesson=l_m11, title="Safe Dictionary Lookup", slug="safe-dictionary-lookup", order=2,
            exercise_type="write_code", difficulty=2,
            instructions='Try to access the key `"location"` from the dictionary. If the key doesn\'t exist, catch the `KeyError` and print `Key not found: location`.\n\nExpected output:\n```\nKey not found: location\n```',
            starter_code='device = {"hostname": "R1", "ip": "10.0.0.1"}\n\n# Try to access "location", catch KeyError\n',
            solution_code='device = {"hostname": "R1", "ip": "10.0.0.1"}\n\ntry:\n    print(device["location"])\nexcept KeyError:\n    print("Key not found: location")',
            xp_value=15, concepts="try, except, KeyError, dictionaries",
        )
        TestCase.objects.create(exercise=ex, expected_output="Key not found: location", description="Should catch KeyError", order=1)
        Hint.objects.create(exercise=ex, level=1, content='Wrap `device["location"]` in a `try` block and catch `KeyError` in the `except` block.', xp_penalty_percent=0)
        Hint.objects.create(exercise=ex, level=2, content='`try:` then `print(device["location"])` then `except KeyError:` then `print("Key not found: location")`', xp_penalty_percent=10)

        # Exercise 11-3: Predict the Exception (output_predict)
        ex = Exercise.objects.create(
            lesson=l_m11, title="Predict the Exception", slug="predict-the-exception", order=3,
            exercise_type="output_predict", difficulty=1,
            instructions='What will this code print?\n\n```python\ntry:\n    x = int("hello")\n    print("Success")\nexcept ValueError:\n    print("Failed")\nprint("Done")\n```',
            choices=[
                {"label": "Success\nDone", "is_correct": False},
                {"label": "Failed\nDone", "is_correct": True},
                {"label": "Failed", "is_correct": False},
                {"label": "Error", "is_correct": False},
            ],
            xp_value=10, concepts="try, except, ValueError, flow",
        )

        # Exercise 11-4: IP Validator (write_code)
        ex = Exercise.objects.create(
            lesson=l_m11, title="IP Validator", slug="ip-validator", order=4,
            exercise_type="write_code", difficulty=3,
            instructions='Loop through the list of IP strings. For each one, try to create an `ipaddress.ip_address()` object. If it succeeds, print `Valid: <ip>`. If it raises a `ValueError`, print `Invalid: <ip>`.\n\nExpected output:\n```\nValid: 192.168.1.1\nInvalid: 999.999.999.999\nValid: 10.0.0.1\nInvalid: not_an_ip\n```',
            starter_code='import ipaddress\n\nips = ["192.168.1.1", "999.999.999.999", "10.0.0.1", "not_an_ip"]\n\n# Loop through and validate each IP\n',
            solution_code='import ipaddress\n\nips = ["192.168.1.1", "999.999.999.999", "10.0.0.1", "not_an_ip"]\n\nfor ip in ips:\n    try:\n        ipaddress.ip_address(ip)\n        print(f"Valid: {ip}")\n    except ValueError:\n        print(f"Invalid: {ip}")',
            xp_value=20, concepts="try, except, ipaddress, loops",
        )
        TestCase.objects.create(exercise=ex, expected_output="Valid: 192.168.1.1\nInvalid: 999.999.999.999\nValid: 10.0.0.1\nInvalid: not_an_ip", description="Should validate each IP", order=1)
        Hint.objects.create(exercise=ex, level=1, content="Use a `for` loop and wrap `ipaddress.ip_address(ip)` in a `try/except ValueError` block.", xp_penalty_percent=0)
        Hint.objects.create(exercise=ex, level=2, content='`for ip in ips:` then `try:` `ipaddress.ip_address(ip)` `print(f"Valid: {ip}")` `except ValueError:` `print(f"Invalid: {ip}")`', xp_penalty_percent=10)

        # Try It Yourself: Error Handling
        Lesson.objects.create(
            module=m11, title="Try It Yourself: Error Handling", slug="try-it-yourself-error-handling", order=4,
            lesson_type="interactive",
            content="# Try It Yourself: Handling Errors\n\n"
                "Practice writing robust code that handles unexpected situations gracefully!\n\n"
                "## Challenge 1 — Safe Division Function\n\n"
                "Write a `safe_divide(a, b)` function that:\n"
                "- Returns the result of `a / b`\n"
                "- Catches `ZeroDivisionError` and prints a friendly message\n"
                "- Catches `TypeError` (e.g., dividing a string) and prints a friendly message\n\n"
                "Test with: `safe_divide(10, 2)`, `safe_divide(10, 0)`, `safe_divide(\"ten\", 2)`\n\n"
                "## Challenge 2 — Mixed String Converter\n\n"
                "Given a list of strings, try to convert each to an integer. Track successes and failures.\n\n"
                "```python\n"
                "values = [\"42\", \"hello\", \"17\", \"3.14\", \"99\", \"world\", \"0\"]\n"
                "```\n\n"
                "Print each conversion attempt, then a summary: `Successes: X, Failures: Y`\n\n"
                "## Challenge 3 — Config Reader with Defaults\n\n"
                "Build a function that reads config values from a dictionary, using try/except to handle missing keys and provide default values.\n\n"
                "```python\n"
                "config = {\"host\": \"192.168.1.1\", \"port\": 8080}\n"
                "```\n\n"
                "Try to read: `host`, `port`, `timeout`, `retries` — provide defaults for missing keys.\n"
                "Print the final configuration.",
            sandbox_code='',
        )

        # === MODULE 12: User Input & While Loops ===
        m12 = modules["user-input-and-while-loops"]

        Lesson.objects.create(
            module=m12, title="Interactive Programs", slug="interactive-programs", order=1,
            lesson_type="concept",
            content="""# Interactive Programs

So far, all our programs have had their data hardcoded. But real CLI tools **ask the user** for input.

## The `input()` Function

```python
name = input("What is your name? ")
print(f"Hello, {name}!")
```

`input()` pauses the program, shows the prompt, and returns whatever the user types (always as a **string**).

### Why `input()` always returns a string

This surprises beginners doing math:

```python
age = input("Enter your age: ")  # User types: 25
print(age + 10)  # TypeError! Can't add string "25" + int 10
```

Even if the user types a number, `input()` gives you the **text** `"25"`, not the number `25`. You must convert it yourself.

## Converting Input

Since `input()` always returns a string, you need to convert for math:

```python
age = int(input("Enter your age: "))
print(f"In 10 years you'll be {age + 10}")
```

### Common mistake: `int(input())` crashes on bad input

What if the user types "abc" instead of a number?

```python
age = int(input("Age: "))  # User types "abc" → ValueError!
```

Always wrap in `try/except` when converting user input:

```python
try:
    age = int(input("Age: "))
    print(f"In 10 years you'll be {age + 10}")
except ValueError:
    print("Please enter a valid number")
```

## The Input-Validate-Convert Pattern

A robust approach to reading user input:

1. **Read** the raw string with `input()`
2. **Validate** it (is it a number? is it non-empty?)
3. **Convert** to the type you need

```python
text = input("Enter a number: ")
if text.isdigit():
    number = int(text)
    print(f"Double: {number * 2}")
else:
    print("That's not a valid number!")
```

## While Loops for Input Validation

A common pattern is looping until valid input. This is sometimes called the **"loop and a half"** pattern — you start the loop, check if you should stop, and process the input:

```python
while True:
    value = input("Enter a number: ")
    if value.isdigit():
        print(f"You entered {value}")
        break
    print("That's not a number, try again")
```

The `while True` creates an infinite loop, and `break` is the only way out. This is a perfectly normal pattern in Python — you'll see it everywhere.

## Sentinel Values

Use a special value to signal "stop":

```python
total = 0
while True:
    line = input("Enter a number (or 'done'): ")
    if line == "done":
        break
    total += int(line)
print(f"Total: {total}")
```

## `break` and `continue`

- `break` — exit the loop immediately
- `continue` — skip the rest of this iteration, go to the next

```python
while True:
    cmd = input("> ")
    if cmd == "quit":
        break
    if cmd == "skip":
        continue
    print(f"You said: {cmd}")
```

## How `input()` Works in the Sandbox

In the exercises here, `input()` uses **pre-seeded values** instead of waiting for keyboard input. The values are provided automatically so the tests can check your code. Just use `input()` normally — the sandbox handles the rest.

## Why This Matters

Network engineers build CLI tools all the time — scripts that prompt for device IPs, ask for credentials, or loop through a list of actions until the user says stop.""",
        )

        Lesson.objects.create(
            module=m12, title="Try It: Interactive Scripts", slug="try-it-interactive-scripts", order=2,
            lesson_type="interactive",
            content="""# Try It: Interactive Scripts

Experiment with `input()` and while loops in the editor below.

**Note:** In the sandbox, `input()` uses pre-seeded values instead of waiting for keyboard input. The values are provided automatically!

## Try it yourself!

Modify the code and see what happens.""",
            sandbox_code='# input() is pre-seeded in the sandbox\n# This demonstrates the pattern\n\nname = "Alice"  # In real code: name = input("Name: ")\nprint(f"Hello, {name}!")\n\n# While loop countdown\nn = 5\nwhile n > 0:\n    print(n)\n    n -= 1\nprint("Go!")\n\n# Sentinel value pattern\nnumbers = [10, 20, 30]  # Simulating user input\ntotal = 0\nfor num in numbers:\n    total += num\nprint(f"Total: {total}")',
        )

        l_m12 = Lesson.objects.create(
            module=m12, title="Practice: User Input", slug="practice-user-input", order=3,
            lesson_type="exercise",
            content="# Practice Time!\n\nBuild interactive programs with `input()` and while loops.",
        )

        # Exercise 12-1: Greet the User (fill_blank)
        ex = Exercise.objects.create(
            lesson=l_m12, title="Greet the User", slug="greet-the-user", order=1,
            exercise_type="fill_blank", difficulty=1,
            instructions='Complete the code to read a name with `input()` and print a greeting.\n\nThe input will be: `Alice`\n\nExpected output:\n```\nHello, Alice!\n```',
            starter_code='name = ___()\nprint(f"Hello, {name}!")',
            solution_code='name = input()\nprint(f"Hello, {name}!")',
            xp_value=10, concepts="input, f-strings",
        )
        TestCase.objects.create(exercise=ex, input_data="Alice", expected_output="Hello, Alice!", description="Should greet Alice", order=1)
        Hint.objects.create(exercise=ex, level=1, content="The function that reads user input is called...", xp_penalty_percent=0)
        Hint.objects.create(exercise=ex, level=2, content="Replace `___` with `input`. The `input()` function reads a line of text from the user.", xp_penalty_percent=10)

        # Exercise 12-2: Sum Until Quit (write_code)
        ex = Exercise.objects.create(
            lesson=l_m12, title="Sum Until Quit", slug="sum-until-quit", order=2,
            exercise_type="write_code", difficulty=2,
            instructions='Read numbers one at a time using `input()`. Keep a running total. When the input is `"done"`, stop and print the total.\n\nInputs will be: `10`, `20`, `30`, `done`\n\nExpected output:\n```\n60\n```',
            starter_code='# Read numbers until "done", then print the total\n',
            solution_code='total = 0\nwhile True:\n    line = input()\n    if line == "done":\n        break\n    total += int(line)\nprint(total)',
            xp_value=15, concepts="input, while, break, accumulator",
        )
        TestCase.objects.create(exercise=ex, input_data="10\n20\n30\ndone", expected_output="60", description="Should sum to 60", order=1)
        Hint.objects.create(exercise=ex, level=1, content='Use `while True:` with `input()` inside. Check if the input is `"done"` and `break`. Otherwise, add `int(line)` to a total.', xp_penalty_percent=0)
        Hint.objects.create(exercise=ex, level=2, content='`total = 0` then `while True:` `line = input()` `if line == "done": break` `total += int(line)` then `print(total)`', xp_penalty_percent=10)

        # Exercise 12-3: Predict the Loop (output_predict)
        ex = Exercise.objects.create(
            lesson=l_m12, title="Predict the Loop", slug="predict-the-while-loop", order=3,
            exercise_type="output_predict", difficulty=1,
            instructions='What will this code print?\n\n```python\nx = 10\nwhile x > 0:\n    x -= 3\n    if x <= 0:\n        break\n    print(x)\n```',
            choices=[
                {"label": "7\n4\n1", "is_correct": True},
                {"label": "10\n7\n4\n1", "is_correct": False},
                {"label": "7\n4", "is_correct": False},
                {"label": "7\n4\n1\n-2", "is_correct": False},
            ],
            xp_value=10, concepts="while, break, tracing",
        )

        # Exercise 12-4: Number Checker (write_code)
        ex = Exercise.objects.create(
            lesson=l_m12, title="Number Checker", slug="number-checker", order=4,
            exercise_type="write_code", difficulty=3,
            instructions='Read numbers via `input()` until you get `"stop"`. For each number, print whether it is `positive`, `negative`, or `zero`. After the loop, print the counts.\n\nInputs: `5`, `-3`, `0`, `7`, `-1`, `stop`\n\nExpected output:\n```\npositive\nnegative\nzero\npositive\nnegative\nPositive: 2 Negative: 2 Zero: 1\n```',
            starter_code='# Read numbers, classify each, then print counts\n',
            solution_code='pos = 0\nneg = 0\nzero = 0\nwhile True:\n    line = input()\n    if line == "stop":\n        break\n    num = int(line)\n    if num > 0:\n        print("positive")\n        pos += 1\n    elif num < 0:\n        print("negative")\n        neg += 1\n    else:\n        print("zero")\n        zero += 1\nprint(f"Positive: {pos} Negative: {neg} Zero: {zero}")',
            xp_value=20, concepts="input, while, if/elif/else, counters",
        )
        TestCase.objects.create(exercise=ex, input_data="5\n-3\n0\n7\n-1\nstop", expected_output="positive\nnegative\nzero\npositive\nnegative\nPositive: 2 Negative: 2 Zero: 1", description="Should classify and count numbers", order=1)
        Hint.objects.create(exercise=ex, level=1, content='Use three counters (`pos`, `neg`, `zero`). In a `while True:` loop, read with `input()`, break on `"stop"`, classify with `if/elif/else`.', xp_penalty_percent=0)
        Hint.objects.create(exercise=ex, level=2, content='After the loop: `print(f"Positive: {pos} Negative: {neg} Zero: {zero}")`', xp_penalty_percent=10)

        # Try It Yourself: Input & Loops
        Lesson.objects.create(
            module=m12, title="Try It Yourself: Input & Loops", slug="try-it-yourself-input-loops", order=4,
            lesson_type="interactive",
            content="# Try It Yourself: Input & While Loops\n\n"
                "These challenges combine loops with decision-making for interactive-style programs.\n\n"
                "## Challenge 1 — Number Guessing Game\n\n"
                "Build a guessing game! Hardcode a target number and loop until a guess matches. Print hints each round.\n\n"
                "```python\n"
                "target = 42\n"
                "guesses = [25, 50, 40, 42]  # simulate guesses from a list\n"
                "```\n\n"
                "For each guess, print `Too low!`, `Too high!`, or `Correct! You got it in N guesses!`\n\n"
                "## Challenge 2 — Simple Calculator\n\n"
                "Process a list of operations to build a running total, starting at 0:\n\n"
                "```python\n"
                "operations = [(\"add\", 10), (\"multiply\", 3), (\"subtract\", 5), (\"add\", 7), (\"multiply\", 2)]\n"
                "```\n\n"
                "After each operation, print the running total. Example: `add 10 -> 10`, `multiply 3 -> 30`, etc.\n\n"
                "## Challenge 3 — Quiz Game\n\n"
                "Store 3 question/answer pairs, loop through them, and track the score:\n\n"
                "```python\n"
                "quiz = [\n"
                "    (\"What keyword defines a function in Python?\", \"def\"),\n"
                "    (\"What built-in function prints to the screen?\", \"print\"),\n"
                "    (\"What data type stores True or False?\", \"bool\"),\n"
                "]\n"
                "```\n\n"
                "For each question, compare a simulated answer and print right/wrong. At the end, print the total score.",
            sandbox_code='',
        )

        # === MODULE 13: Regular Expressions ===
        m13 = modules["regular-expressions"]

        Lesson.objects.create(
            module=m13, title="Pattern Matching with Regex", slug="pattern-matching-with-regex", order=1,
            lesson_type="concept",
            content="""# Pattern Matching with Regular Expressions

Regular expressions (regex) let you search for **patterns** in text — not just exact strings. They're essential for parsing device logs, extracting IPs from output, and validating formats.

## When to Use Regex vs Simple String Methods

Not every text task needs regex. Use simple string methods when you can:

```python
# Simple string methods — no regex needed
if "error" in line.lower():       # Check if a word exists
parts = line.split(":")           # Split on a delimiter
clean = text.strip()              # Remove whitespace
```

Use regex when the pattern is **complex** or **variable** — like finding IP addresses, matching timestamps, or extracting groups of data.

## Importing `re`

```python
import re
```

## Why Raw Strings `r""`?

You'll see `r""` (raw strings) in every regex pattern. Here's why:

In normal strings, `\\d` means "a `d` character." But in regex, `\\d` means "any digit." The raw string `r""` tells Python to pass the backslashes through to the regex engine without interpreting them:

```python
# Without r: Python sees \\d as escape sequence (confusing)
# With r: Python passes \\d directly to regex (correct)
pattern = r"\\d+"  # Always use r"" for regex patterns
```

Just remember: **always use raw strings for regex patterns**.

## `re.search()` — Find a Pattern

```python
import re

text = "The server IP is 192.168.1.1"
match = re.search(r"\\d+\\.\\d+\\.\\d+\\.\\d+", text)
if match:
    print(match.group())  # 192.168.1.1
```

`re.search()` finds the **first** match. Returns `None` if no match.

### Reading a regex pattern step by step

Let's break down `\\d+\\.\\d+\\.\\d+\\.\\d+`:
- `\\d+` — one or more digits (e.g., `192`)
- `\\.` — a literal dot character
- `\\d+` — one or more digits (e.g., `168`)
- `\\.` — another literal dot
- `\\d+` — one or more digits (e.g., `1`)
- `\\.` — another literal dot
- `\\d+` — one or more digits (e.g., `1`)

Put together: "four groups of digits separated by dots" — an IP address pattern.

## `re.findall()` — Find All Matches

```python
text = "Errors: 3, Warnings: 12, Info: 45"
numbers = re.findall(r"\\d+", text)
print(numbers)  # ['3', '12', '45']
```

## `re.sub()` — Search and Replace

```python
text = "Port: 8080, Port: 443"
result = re.sub(r"\\d+", "XXXX", text)
print(result)  # Port: XXXX, Port: XXXX
```

## Common Patterns

| Pattern | Matches                                                    |
|---------|------------------------------------------------------------|
| `\\d`   | A digit (0-9)                                              |
| `\\d+`  | One or more digits                                         |
| `\\w+`  | One or more word characters (letters, digits, underscore)  |
| `\\S+`  | One or more non-whitespace characters                      |
| `.`     | Any character (except newline)                             |
| `\\.`   | A literal dot                                              |
| `[a-z]` | Any lowercase letter                                      |
| `^`     | Start of string                                            |
| `$`     | End of string                                              |

### Common mistake: forgetting to escape dots

`.` in regex matches **any** character, not just a dot. If you want a literal dot (like in an IP address), you must escape it with `\\.`:

```python
# WRONG: matches "192X168X1X1" too (. matches any character)
re.search(r"\\d+.\\d+.\\d+.\\d+", text)

# RIGHT: matches only actual dots
re.search(r"\\d+\\.\\d+\\.\\d+\\.\\d+", text)
```

## Groups — Extracting Parts

Use parentheses to capture sub-matches:

```python
match = re.search(r"(\\w+):(\\d+)", "port:8080")
print(match.group(1))  # port
print(match.group(2))  # 8080
```

## A Worked Example

Let's extract the severity and message from a log line:

```python
line = "2024-01-15 WARNING Disk usage at 90%"
match = re.search(r"\\d{4}-\\d{2}-\\d{2} (\\w+) (.+)", line)
if match:
    print(match.group(1))  # WARNING
    print(match.group(2))  # Disk usage at 90%
```

How the pattern works:
- `\\d{4}-\\d{2}-\\d{2}` — matches the date (4 digits, dash, 2 digits, dash, 2 digits)
- ` ` — a literal space
- `(\\w+)` — captures the severity level (one or more word characters)
- ` ` — another space
- `(.+)` — captures everything else (the message)

## Quantifiers

| Quantifier | Meaning         |
|------------|-----------------|
| `+`        | One or more     |
| `*`        | Zero or more    |
| `?`        | Zero or one     |
| `{3}`      | Exactly 3       |
| `{1,3}`    | Between 1 and 3 |

Regex is a powerful tool in every network engineer's toolkit!""",
        )

        Lesson.objects.create(
            module=m13, title="Try It: Regex", slug="try-it-regex", order=2,
            lesson_type="interactive",
            content="""# Try It: Regular Expressions

Experiment with regex patterns in the editor below. Try modifying the patterns to match different things!

## Real-world Examples

The sandbox shows how to extract IPs from log lines, parse interface status, and find VLANs.""",
            sandbox_code='import re\n\n# Find all numbers in a string\ntext = "Port 22, Port 80, Port 443"\nnumbers = re.findall(r"\\d+", text)\nprint("Ports:", numbers)\n\n# Extract IPs from a log line\nlog = "Connection from 10.0.0.5 to 192.168.1.100 on port 443"\nips = re.findall(r"\\d+\\.\\d+\\.\\d+\\.\\d+", log)\nprint("IPs found:", ips)\n\n# Parse interface status\nline = "GigabitEthernet0/1 is up, line protocol is up"\nmatch = re.search(r"(\\S+) is (\\w+)", line)\nif match:\n    print(f"Interface: {match.group(1)}, Status: {match.group(2)}")\n\n# Find VLAN numbers\nconfig = "vlan 10\\nvlan 20\\nvlan 30\\nvlan 100"\nvlans = re.findall(r"vlan (\\d+)", config)\nprint("VLANs:", vlans)',
        )

        l_m13 = Lesson.objects.create(
            module=m13, title="Practice: Regex", slug="practice-regex", order=3,
            lesson_type="exercise",
            content="# Practice Time!\n\nPut your regex skills to work.",
        )

        # Exercise 13-1: Find All Numbers (fill_blank)
        ex = Exercise.objects.create(
            lesson=l_m13, title="Find All Numbers", slug="find-all-numbers", order=1,
            exercise_type="fill_blank", difficulty=1,
            instructions='Complete the `re.findall()` call to extract all numbers from the string.\n\nExpected output:\n```\n[\'3\', \'12\', \'45\']\n```',
            starter_code='import re\n\ntext = "Errors: 3, Warnings: 12, Info: 45"\nnumbers = re.findall(r"___", text)\nprint(numbers)',
            solution_code='import re\n\ntext = "Errors: 3, Warnings: 12, Info: 45"\nnumbers = re.findall(r"\\d+", text)\nprint(numbers)',
            xp_value=10, concepts="re, findall, \\d+",
        )
        TestCase.objects.create(exercise=ex, expected_output="['3', '12', '45']", description="Should find all numbers", order=1)
        Hint.objects.create(exercise=ex, level=1, content="`\\d` matches a single digit. Add `+` to match one or more consecutive digits.", xp_penalty_percent=0)
        Hint.objects.create(exercise=ex, level=2, content='Replace `___` with `\\d+`. This pattern matches one or more digits.', xp_penalty_percent=10)

        # Exercise 13-2: Extract IP Addresses (write_code)
        ex = Exercise.objects.create(
            lesson=l_m13, title="Extract IP Addresses", slug="extract-ip-addresses", order=2,
            exercise_type="write_code", difficulty=2,
            instructions='Use `re.findall()` to find all IP addresses in the log string. Print each one on its own line.\n\nExpected output:\n```\n10.0.0.5\n192.168.1.100\n```',
            starter_code='import re\n\nlog = "Connection from 10.0.0.5 to 192.168.1.100 on port 443"\n\n# Find all IP addresses and print each one\n',
            solution_code='import re\n\nlog = "Connection from 10.0.0.5 to 192.168.1.100 on port 443"\n\nips = re.findall(r"\\d+\\.\\d+\\.\\d+\\.\\d+", log)\nfor ip in ips:\n    print(ip)',
            xp_value=15, concepts="re, findall, IP pattern",
        )
        TestCase.objects.create(exercise=ex, expected_output="10.0.0.5\n192.168.1.100", description="Should extract both IPs", order=1)
        Hint.objects.create(exercise=ex, level=1, content="An IP address pattern is four groups of digits separated by dots: `\\d+\\.\\d+\\.\\d+\\.\\d+`.", xp_penalty_percent=0)
        Hint.objects.create(exercise=ex, level=2, content='`ips = re.findall(r"\\d+\\.\\d+\\.\\d+\\.\\d+", log)` then `for ip in ips: print(ip)`', xp_penalty_percent=10)

        # Exercise 13-3: Predict the Match (output_predict)
        ex = Exercise.objects.create(
            lesson=l_m13, title="Predict the Match", slug="predict-the-match", order=3,
            exercise_type="output_predict", difficulty=1,
            instructions='What will this code print?\n\n```python\nimport re\nmatch = re.search(r"(\\w+):(\\d+)", "port:8080")\nprint(match.group(2))\n```',
            choices=[
                {"label": "8080", "is_correct": True},
                {"label": "port", "is_correct": False},
                {"label": "port:8080", "is_correct": False},
                {"label": "Error", "is_correct": False},
            ],
            xp_value=10, concepts="re, search, groups",
        )

        # Exercise 13-4: Parse Device Log (write_code)
        ex = Exercise.objects.create(
            lesson=l_m13, title="Parse Device Log", slug="parse-device-log", order=4,
            exercise_type="write_code", difficulty=3,
            instructions='Parse the multi-line syslog output. Each line has the format `TIMESTAMP SEVERITY MESSAGE`. Extract and print each part in the format `[SEVERITY] MESSAGE`.\n\nExpected output:\n```\n[WARNING] Link down on Gi0/1\n[ERROR] BGP peer 10.0.0.2 unreachable\n[INFO] Interface Gi0/2 up\n```',
            starter_code='import re\n\nlogs = """2024-01-15T10:30:00 WARNING Link down on Gi0/1\n2024-01-15T10:30:05 ERROR BGP peer 10.0.0.2 unreachable\n2024-01-15T10:30:10 INFO Interface Gi0/2 up"""\n\n# Parse each line and print [SEVERITY] MESSAGE\n',
            solution_code='import re\n\nlogs = """2024-01-15T10:30:00 WARNING Link down on Gi0/1\n2024-01-15T10:30:05 ERROR BGP peer 10.0.0.2 unreachable\n2024-01-15T10:30:10 INFO Interface Gi0/2 up"""\n\nfor line in logs.strip().split("\\n"):\n    match = re.search(r"\\S+\\s+(\\w+)\\s+(.*)", line)\n    if match:\n        severity = match.group(1)\n        message = match.group(2)\n        print(f"[{severity}] {message}")',
            xp_value=20, concepts="re, search, groups, parsing",
        )
        TestCase.objects.create(exercise=ex, expected_output="[WARNING] Link down on Gi0/1\n[ERROR] BGP peer 10.0.0.2 unreachable\n[INFO] Interface Gi0/2 up", description="Should parse log lines", order=1)
        Hint.objects.create(exercise=ex, level=1, content="Split into lines, then use `re.search()` with groups to capture the severity and message parts.", xp_penalty_percent=0)
        Hint.objects.create(exercise=ex, level=2, content='Pattern: `r"\\S+\\s+(\\w+)\\s+(.*)"` — skips timestamp, captures severity in group(1) and message in group(2).', xp_penalty_percent=10)

        # Try It Yourself: Regex
        Lesson.objects.create(
            module=m13, title="Try It Yourself: Regex", slug="try-it-yourself-regex", order=4,
            lesson_type="interactive",
            content="# Try It Yourself: Regular Expressions\n\n"
                "Put your regex skills to the test with these practical pattern-matching challenges!\n\n"
                "## Challenge 1 — Phone Number Standardizer\n\n"
                "Given phone numbers in various formats, extract the digits and reformat them consistently.\n\n"
                "```python\n"
                "phones = [\"(555) 123-4567\", \"555.123.4567\", \"5551234567\", \"555-123-4567\"]\n"
                "```\n\n"
                "For each, print the standardized format: `555-123-4567`\n\n"
                "Hint: Use `re.sub()` to strip non-digits, then reformat with slicing.\n\n"
                "## Challenge 2 — Email Validator\n\n"
                "Write a regex pattern that matches valid email addresses. Test it against these strings:\n\n"
                "```python\n"
                "emails = [\"user@example.com\", \"bad-email@\", \"name.last@company.org\", \"@missing.com\", \"test@site.co.uk\"]\n"
                "```\n\n"
                "Print `VALID` or `INVALID` for each.\n\n"
                "## Challenge 3 — Date Reformatter\n\n"
                "Convert dates from `MM/DD/YYYY` format to `YYYY-MM-DD` using regex groups.\n\n"
                "```python\n"
                "dates = [\"03/15/2024\", \"12/01/2023\", \"07/04/1776\"]\n"
                "```\n\n"
                "Print each reformatted date on its own line.",
            sandbox_code='',
        )

        # === MODULE 14: Building a Network Toolkit ===
        m14 = modules["building-a-network-toolkit"]

        Lesson.objects.create(
            module=m14, title="Putting It All Together", slug="putting-it-all-together", order=1,
            lesson_type="concept",
            content="""# Building a Network Toolkit

You've learned variables, loops, functions, dictionaries, error handling, regex, and the `ipaddress` module. Now let's combine them into realistic network automation scripts.

## Breaking Problems Into Functions

The key to writing good scripts is thinking about each step as a separate function: **input → process → output**.

For example, a network audit script might have:
- `validate_ip(ip_str)` → takes a string, returns a clean IP or `None`
- `parse_interface(line)` → takes raw text, returns a dictionary
- `audit_device(config)` → takes a config dict, returns a list of issues

Each function does **one thing**. This makes them easy to test, reuse, and debug. If something breaks, you know exactly which function to look at.

## Design Pattern 1: Validation Functions

Check data at the boundaries (when it enters your program), then trust it inside:

```python
import ipaddress

def validate_ip(ip_str):
    try:
        return str(ipaddress.ip_address(ip_str))
    except ValueError:
        return None

# Use it
ips = ["10.0.0.1", "bad", "192.168.1.1"]
for ip in ips:
    result = validate_ip(ip)
    if result:
        print(f"Valid: {result}")
    else:
        print(f"Invalid: {ip}")
```

The validation pattern: check at the boundary, trust inside. Once `validate_ip` returns a value, you know it's a real IP address — no need to check again later in your code.

## Design Pattern 2: Parsing Pipelines

```python
import re

def parse_interface_line(line):
    match = re.search(r"(\\S+)\\s+(up|down)\\s+(\\d+)", line)
    if match:
        return {
            "name": match.group(1),
            "status": match.group(2),
            "speed": int(match.group(3))
        }
    return None

output = "Gi0/0  up  1000"
iface = parse_interface_line(output)
print(iface)  # {'name': 'Gi0/0', 'status': 'up', 'speed': 1000}
```

## Design Pattern 3: Reporting from Data

```python
import json

def audit_device(config):
    issues = []
    if not config.get("hostname"):
        issues.append("Missing hostname")
    if not config.get("interfaces"):
        issues.append("No interfaces configured")
    return issues

config = json.loads('{"hostname": "SW1", "interfaces": []}')
problems = audit_device(config)
if problems:
    for p in problems:
        print(f"  Issue: {p}")
```

## Why Functions Should Do ONE Thing

If a function validates IPs **and** parses interfaces **and** generates a report, it's doing too much. When something breaks, you won't know which part failed. Split it into smaller functions with clear names.

A good test: can you describe what the function does in one short sentence without using "and"? If not, it's probably doing too much.

## Combining Everything

A real network script might:
1. Read a JSON config file
2. Validate IP addresses
3. Parse show command output
4. Generate an audit report

That's exactly what the exercises in this module will have you do!

## What Comes Next?

You've built a solid Python foundation. To start automating **real** network devices, explore these libraries:
- **Netmiko** — SSH connections to routers and switches (send commands, read output)
- **Paramiko** — lower-level SSH library for custom connections
- **Nornir** — automation framework for managing many devices at once

Everything you've learned here — parsing, validation, functions, error handling — applies directly when using these tools.""",
        )

        Lesson.objects.create(
            module=m14, title="Try It: Network Toolkit", slug="try-it-network-toolkit", order=2,
            lesson_type="interactive",
            content="""# Try It: Network Toolkit

Experiment with a complete mini-tool that validates IPs, parses show output, and generates a report.

## Try it yourself!

Modify the device data and see how the output changes.""",
            sandbox_code='import ipaddress\nimport json\nimport re\n\n# === Step 1: Validate IPs ===\nips = ["10.0.0.1", "192.168.1.1", "bad_ip", "172.16.0.1"]\nprint("=== IP Validation ===")\nfor ip in ips:\n    try:\n        ipaddress.ip_address(ip)\n        print(f"  {ip}: Valid")\n    except ValueError:\n        print(f"  {ip}: Invalid")\n\n# === Step 2: Parse show output ===\nshow_output = """Interface  Status  Speed\nGi0/0      up      1000\nGi0/1      down    100\nGi0/2      up      1000"""\n\nprint("\\n=== Interface Status ===")\nfor line in show_output.strip().split("\\n")[1:]:\n    parts = line.split()\n    status = "OK" if parts[1] == "up" else "DOWN"\n    print(f"  {parts[0]}: {status} ({parts[2]} Mbps)")\n\n# === Step 3: JSON Config Report ===\ndevice_json = \'{"hostname": "R1", "interfaces": ["Gi0/0", "Gi0/1"], "vlans": [10, 20]}\'\ndevice = json.loads(device_json)\nprint(f"\\n=== Device Report: {device[\'hostname\']} ===")\nprint(f"  Interfaces: {len(device[\'interfaces\'])}")\nprint(f"  VLANs: {device[\'vlans\']}")',
        )

        l_m14 = Lesson.objects.create(
            module=m14, title="Practice: Network Toolkit", slug="practice-network-toolkit", order=3,
            lesson_type="exercise",
            content="# Practice Time!\n\nCombine everything you've learned in these capstone exercises.",
        )

        # Exercise 14-1: Fix the Parser (fix_bug)
        ex = Exercise.objects.create(
            lesson=l_m14, title="Fix the Parser", slug="fix-the-parser", order=1,
            exercise_type="fix_bug", difficulty=2,
            instructions='This show-interface parser has a bug — it uses the wrong index to get the status. Fix the slice index so it extracts the correct field.\n\nExpected output:\n```\nGi0/0: up\nGi0/1: down\nGi0/2: up\n```',
            starter_code='output = """Interface  Status  Speed\nGi0/0      up      1000\nGi0/1      down    100\nGi0/2      up      1000"""\n\nlines = output.strip().split("\\n")\nfor line in lines[1:]:\n    parts = line.split()\n    print(f"{parts[0]}: {parts[2]}")',
            solution_code='output = """Interface  Status  Speed\nGi0/0      up      1000\nGi0/1      down    100\nGi0/2      up      1000"""\n\nlines = output.strip().split("\\n")\nfor line in lines[1:]:\n    parts = line.split()\n    print(f"{parts[0]}: {parts[1]}")',
            xp_value=10, concepts="parsing, indexing, debugging",
        )
        TestCase.objects.create(exercise=ex, expected_output="Gi0/0: up\nGi0/1: down\nGi0/2: up", description="Should print correct status", order=1)
        Hint.objects.create(exercise=ex, level=1, content="Look at which index is used to get the status. After `line.split()`, what is at each position?", xp_penalty_percent=0)
        Hint.objects.create(exercise=ex, level=2, content="`parts[0]` is the interface name, `parts[1]` is the status, `parts[2]` is the speed. Change `parts[2]` to `parts[1]`.", xp_penalty_percent=10)

        # Exercise 14-2: Subnet Scanner (write_code)
        ex = Exercise.objects.create(
            lesson=l_m14, title="Subnet Scanner", slug="subnet-scanner", order=2,
            exercise_type="write_code", difficulty=3,
            instructions='Given a JSON list of IPs and a network string, print which IPs are inside the subnet and which are outside.\n\nExpected output:\n```\n10.0.0.5: Inside\n10.0.0.100: Inside\n192.168.1.1: Outside\n10.0.0.200: Inside\n172.16.0.1: Outside\n```',
            starter_code='import ipaddress\nimport json\n\nips_json = \'["10.0.0.5", "10.0.0.100", "192.168.1.1", "10.0.0.200", "172.16.0.1"]\'\nnetwork = "10.0.0.0/24"\n\n# Parse the JSON, check each IP against the network\n',
            solution_code='import ipaddress\nimport json\n\nips_json = \'["10.0.0.5", "10.0.0.100", "192.168.1.1", "10.0.0.200", "172.16.0.1"]\'\nnetwork = "10.0.0.0/24"\n\nips = json.loads(ips_json)\nnet = ipaddress.ip_network(network)\n\nfor ip_str in ips:\n    ip = ipaddress.ip_address(ip_str)\n    if ip in net:\n        print(f"{ip_str}: Inside")\n    else:\n        print(f"{ip_str}: Outside")',
            xp_value=15, concepts="ipaddress, json, network membership",
        )
        TestCase.objects.create(exercise=ex, expected_output="10.0.0.5: Inside\n10.0.0.100: Inside\n192.168.1.1: Outside\n10.0.0.200: Inside\n172.16.0.1: Outside", description="Should classify each IP", order=1)
        Hint.objects.create(exercise=ex, level=1, content="Use `json.loads()` to parse the IP list, `ipaddress.ip_network()` for the network, then check `ip in net` for each.", xp_penalty_percent=0)
        Hint.objects.create(exercise=ex, level=2, content='`ips = json.loads(ips_json)`, `net = ipaddress.ip_network(network)`, then `for ip_str in ips:` check `ipaddress.ip_address(ip_str) in net`.', xp_penalty_percent=10)

        # Exercise 14-3: Predict the Output (output_predict)
        ex = Exercise.objects.create(
            lesson=l_m14, title="Predict the Output", slug="predict-the-toolkit-output", order=3,
            exercise_type="output_predict", difficulty=2,
            instructions='What will this code print?\n\n```python\nimport ipaddress\n\ndata = {"ip": "10.0.0.1", "role": "router"}\nip = ipaddress.ip_address(data["ip"])\nprint(f"{ip.is_private} {data[\'role\']}")\n```',
            choices=[
                {"label": "True router", "is_correct": True},
                {"label": "False router", "is_correct": False},
                {"label": "True 10.0.0.1", "is_correct": False},
                {"label": "Error", "is_correct": False},
            ],
            xp_value=10, concepts="ipaddress, dictionaries, f-strings",
        )

        # Exercise 14-4: Device Audit Report (write_code)
        ex = Exercise.objects.create(
            lesson=l_m14, title="Device Audit Report", slug="device-audit-report", order=4,
            exercise_type="write_code", difficulty=3,
            instructions='Parse the JSON config containing multiple devices. For each device, check if it has a `hostname` and at least one `interface`. Print a summary report.\n\nExpected output:\n```\nSW1: OK\nSW2: ISSUE - No interfaces\nSW3: ISSUE - Missing hostname\n```',
            starter_code='import json\n\ndevices_json = \'[{"hostname": "SW1", "interfaces": ["Gi0/0", "Gi0/1"]}, {"hostname": "SW2", "interfaces": []}, {"hostname": "", "interfaces": ["Gi0/0"]}]\'\n\n# Parse and audit each device\n',
            solution_code='import json\n\ndevices_json = \'[{"hostname": "SW1", "interfaces": ["Gi0/0", "Gi0/1"]}, {"hostname": "SW2", "interfaces": []}, {"hostname": "", "interfaces": ["Gi0/0"]}]\'\n\ndevices = json.loads(devices_json)\n\nfor device in devices:\n    name = device["hostname"] or "SW3"\n    if not device["interfaces"]:\n        print(f"{name}: ISSUE - No interfaces")\n    elif not device["hostname"]:\n        print(f"SW3: ISSUE - Missing hostname")\n    else:\n        print(f"{name}: OK")',
            xp_value=20, concepts="json, conditionals, loops, validation",
        )
        TestCase.objects.create(exercise=ex, expected_output="SW1: OK\nSW2: ISSUE - No interfaces\nSW3: ISSUE - Missing hostname", description="Should audit all devices", order=1)
        Hint.objects.create(exercise=ex, level=1, content="Loop through devices. Check `device[\"interfaces\"]` (empty list is falsy) and `device[\"hostname\"]` (empty string is falsy).", xp_penalty_percent=0)
        Hint.objects.create(exercise=ex, level=2, content='For the device with empty hostname, use `"SW3"` as the display name. Check `if not device["interfaces"]:` first, then `elif not device["hostname"]:`.', xp_penalty_percent=10)

        # Try It Yourself: Toolkit
        Lesson.objects.create(
            module=m14, title="Try It Yourself: Toolkit", slug="try-it-yourself-toolkit", order=4,
            lesson_type="interactive",
            content="# Try It Yourself: Building a Network Toolkit\n\n"
                "Put everything together! These challenges combine regex, `ipaddress`, JSON, and function pipelines into realistic automation scenarios.\n\n"
                "## Challenge 1 — Multi-Device `show version` Parser\n\n"
                "Given raw `show version` output from 3 network devices, extract the **hostname** and **OS version** from each using regex.\n\n"
                "```\n"
                "Device 1:\n"
                "Cisco IOS Software, Version 15.4(3)M\n"
                "hostname R1\n"
                "\n"
                "Device 2:\n"
                "Cisco IOS Software, Version 16.9.4\n"
                "hostname SW1\n"
                "\n"
                "Device 3:\n"
                "Cisco IOS Software, Version 15.7(3)M\n"
                "hostname R2\n"
                "```\n\n"
                "Print:\n"
                "```\n"
                "R1 -> 15.4(3)M\n"
                "SW1 -> 16.9.4\n"
                "R2 -> 15.7(3)M\n"
                "```\n\n"
                "## Challenge 2 — Function Pipeline\n\n"
                "Build three functions that chain together:\n\n"
                "1. `validate_ips(ip_list)` — returns only valid IP strings\n"
                "2. `classify_ips(valid_ips)` — returns a dict `{\"private\": [...], \"public\": [...]}`\n"
                "3. `generate_report(classified)` — prints a summary with counts and lists\n\n"
                "Test with: `[\"10.0.0.1\", \"8.8.8.8\", \"not_valid\", \"192.168.1.1\", \"1.1.1.1\"]`\n\n"
                "## Challenge 3 — Subnet Overlap Detector\n\n"
                "Given a list of CIDR networks, check if any two subnets overlap (one contains addresses of the other). Print any conflicts found.\n\n"
                "```python\n"
                "networks = [\"10.0.0.0/24\", \"10.0.0.128/25\", \"192.168.1.0/24\", \"172.16.0.0/16\", \"172.16.5.0/24\"]\n"
                "```\n\n"
                "Hint: `ipaddress.ip_network()` objects support the `overlaps()` method.",
            sandbox_code='',
        )

        self.stdout.write(self.style.SUCCESS(
            f"\nDone! Created {Module.objects.count()} modules, "
            f"{Lesson.objects.count()} lessons, "
            f"{Exercise.objects.count()} exercises, "
            f"{TestCase.objects.count()} test cases, "
            f"{Hint.objects.count()} hints."
        ))
