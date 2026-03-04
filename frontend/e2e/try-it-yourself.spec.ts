import { test, expect } from '@playwright/test';
import { registerUser, typeInMonaco } from './helpers';

const LESSONS = [
  {
    module: 'your-first-program',
    slug: 'try-it-yourself-print',
    title: 'Try It Yourself: Print',
    code: 'print("Hello from challenge!")\nprint("===== RECEIPT =====")',
    expectedOutput: 'Hello from challenge!',
  },
  {
    module: 'variables-and-data-types',
    slug: 'try-it-yourself-variables',
    title: 'Try It Yourself: Variables & Data Types',
    code: 'distance = 350\nmpg = 25\ngas_price = 3.50\ncost = (distance / mpg) * gas_price\nprint(f"Trip cost: ${cost:.2f}")',
    expectedOutput: 'Trip cost: $49.00',
  },
  {
    module: 'making-decisions',
    slug: 'try-it-yourself-conditionals',
    title: 'Try It Yourself: Making Decisions',
    code: 'weight = 3\nif weight < 1:\n    cost = 5.00\nelif weight <= 5:\n    cost = 10.00\nelse:\n    cost = 20.00\nprint(f"${cost:.2f}")',
    expectedOutput: '$10.00',
  },
  {
    module: 'loops',
    slug: 'try-it-yourself-loops',
    title: 'Try It Yourself: Loops',
    code: 'for i in range(1, 6):\n    print("*" * i)',
    expectedOutput: '*\n**\n***',
  },
  {
    module: 'functions',
    slug: 'try-it-yourself-functions',
    title: 'Try It Yourself: Functions',
    code: 'def max_of_three(a, b, c):\n    if a >= b and a >= c:\n        return a\n    elif b >= c:\n        return b\n    return c\nprint(max_of_three(10, 25, 17))',
    expectedOutput: '25',
  },
  {
    module: 'lists-and-tuples',
    slug: 'try-it-yourself-lists',
    title: 'Try It Yourself: Lists & Tuples',
    code: 'numbers = [14, 7, 22, 3]\nevens = [n for n in numbers if n % 2 == 0]\nprint("Evens:", evens)',
    expectedOutput: 'Evens: [14, 22]',
  },
  {
    module: 'dictionaries',
    slug: 'try-it-yourself-dictionaries',
    title: 'Try It Yourself: Dictionaries',
    code: 'contacts = {"Alice": "555-0101", "Bob": "555-0102"}\nprint("Bob:", contacts["Bob"])',
    expectedOutput: 'Bob: 555-0102',
  },
  {
    module: 'string-magic',
    slug: 'try-it-yourself-strings',
    title: 'Try It Yourself: String Magic',
    code: 'def caesar(text, shift):\n    result = ""\n    for c in text:\n        if c.isalpha():\n            base = ord("A") if c.isupper() else ord("a")\n            result += chr((ord(c) - base + shift) % 26 + base)\n        else:\n            result += c\n    return result\nprint(caesar("Hello", 3))',
    expectedOutput: 'Khoor',
  },
  {
    module: 'writing-cleaner-code',
    slug: 'try-it-yourself-cleaner-code',
    title: 'Try It Yourself: Writing Cleaner Code',
    code: 'status = "adult" if 20 >= 18 else "minor"\nprint(status)\nsquares = [x**2 for x in range(1, 6)]\nprint(squares)',
    expectedOutput: 'adult',
  },
  {
    module: 'python-for-network-engineers',
    slug: 'try-it-yourself-network-python',
    title: 'Try It Yourself: Python for Network Engineers',
    code: 'import ipaddress\naddr = ipaddress.ip_address("192.168.1.1")\nprint(f"{addr} -> {"private" if addr.is_private else "public"}")',
    expectedOutput: '192.168.1.1 -> private',
  },
  {
    module: 'handling-errors',
    slug: 'try-it-yourself-error-handling',
    title: 'Try It Yourself: Handling Errors',
    code: 'def safe_divide(a, b):\n    try:\n        return a / b\n    except ZeroDivisionError:\n        return "Cannot divide by zero"\nprint(safe_divide(10, 2))\nprint(safe_divide(10, 0))',
    expectedOutput: '5.0',
  },
  {
    module: 'user-input-and-while-loops',
    slug: 'try-it-yourself-input-loops',
    title: 'Try It Yourself: Input & While Loops',
    code: 'target = 42\nguesses = [25, 50, 42]\nfor g in guesses:\n    if g < target:\n        print("Too low!")\n    elif g > target:\n        print("Too high!")\n    else:\n        print("Correct!")\n        break',
    expectedOutput: 'Too low!',
  },
  {
    module: 'regular-expressions',
    slug: 'try-it-yourself-regex',
    title: 'Try It Yourself: Regular Expressions',
    code: 'import re\ndigits = re.sub(r"\\D", "", "(555) 123-4567")\nprint(f"{digits[:3]}-{digits[3:6]}-{digits[6:]}")',
    expectedOutput: '555-123-4567',
  },
  {
    module: 'building-a-network-toolkit',
    slug: 'try-it-yourself-toolkit',
    title: 'Try It Yourself: Building a Network Toolkit',
    code: 'import re\ntext = "Cisco IOS Software, Version 15.4(3)M\\nhostname R1"\nver = re.search(r"Version (\\S+)", text).group(1)\nhost = re.search(r"hostname (\\S+)", text).group(1)\nprint(f"{host} -> {ver}")',
    expectedOutput: 'R1 -> 15.4(3)M',
  },
];

test.describe('Try It Yourself Challenge Lessons', () => {
  test('lesson page loads with empty editor and challenge content', async ({ page }) => {
    await registerUser(page);

    // Test Module 1's Try It Yourself lesson
    await page.goto('/module/your-first-program/lesson/try-it-yourself-print');

    // Challenge content should be visible
    await expect(page.getByText('Try It Yourself: Print')).toBeVisible({ timeout: 10000 });
    await expect(page.getByText('Challenge 1')).toBeVisible();
    await expect(page.getByRole('heading', { name: /ASCII Art/ })).toBeVisible();

    // Editor should be present
    await page.waitForSelector('.monaco-editor', { timeout: 10000 });

    // Run button should exist
    await expect(page.getByRole('button', { name: /Run/ })).toBeVisible();
  });

  test('student can write and run code in empty sandbox', async ({ page }) => {
    await registerUser(page);

    await page.goto('/module/your-first-program/lesson/try-it-yourself-print');
    await page.waitForSelector('.monaco-editor', { timeout: 10000 });

    // Type a solution into the empty editor
    await typeInMonaco(page, 'print("My ASCII Art")\nprint("  *  ")\nprint(" *** ")\nprint("*****")');

    // Run the code
    await page.getByRole('button', { name: /Run/ }).click();

    // Should show output
    await expect(page.locator('pre').filter({ hasText: 'My ASCII Art' })).toBeVisible({
      timeout: 10000,
    });
  });

  test('student can mark Try It Yourself lesson as complete', async ({ page }) => {
    await registerUser(page);

    await page.goto('/module/your-first-program/lesson/try-it-yourself-print');
    await expect(page.getByText('Try It Yourself: Print')).toBeVisible({ timeout: 10000 });

    // Mark complete button should exist for interactive lessons
    const completeBtn = page.getByRole('button', { name: /Mark as Complete/ });
    await expect(completeBtn).toBeVisible();
    await completeBtn.click();

    // Should redirect back to module page
    await page.waitForURL(/\/module\/your-first-program/, { timeout: 10000 });
  });

  // Test that each module's Try It Yourself lesson loads and runs code
  for (const lesson of LESSONS) {
    test(`Module ${lesson.module}: sandbox runs code correctly`, async ({ page }) => {
      await registerUser(page);

      await page.goto(`/module/${lesson.module}/lesson/${lesson.slug}`);

      // Verify lesson content loaded
      await expect(page.getByText(lesson.title)).toBeVisible({ timeout: 10000 });

      // Wait for editor
      await page.waitForSelector('.monaco-editor', { timeout: 10000 });

      // Type solution code
      await typeInMonaco(page, lesson.code);

      // Run the code
      await page.getByRole('button', { name: /Run/ }).click();

      // Verify output contains expected text
      await expect(
        page.locator('pre').filter({ hasText: lesson.expectedOutput })
      ).toBeVisible({ timeout: 15000 });
    });
  }
});
