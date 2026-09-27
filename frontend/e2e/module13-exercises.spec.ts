import { test, expect } from '@playwright/test';
import { registerUser, getHeaderXP, typeInMonaco } from './helpers';

const MODULE13_BASE = '/module/regular-expressions/lesson/practice-regex/exercise';

test.describe('Module 13 Exercise Validation', () => {
  test('find-all-numbers: correct answer passes and awards 10 XP', async ({ page }) => {
    await registerUser(page);

    await page.goto(`${MODULE13_BASE}/find-all-numbers`);
    await expect(page.getByRole('heading', { name: 'Find All Numbers' })).toBeVisible();

    await typeInMonaco(
      page,
      'import re\n\ntext = "Errors: 3, Warnings: 12, Info: 45"\nnumbers = re.findall(r"\\d+", text)\nprint(numbers)'
    );

    await page.getByRole('button', { name: /Submit/ }).click();
    await expect(page.getByText(/Exercise Complete/)).toBeVisible({ timeout: 15000 });

    await page.waitForTimeout(1000);
    const xp = await getHeaderXP(page);
    expect(xp).toBe(10);
  });

  test('find-all-numbers: wrong answer shows failure', async ({ page }) => {
    await registerUser(page);

    await page.goto(`${MODULE13_BASE}/find-all-numbers`);

    await typeInMonaco(page, 'print("wrong")');

    await page.getByRole('button', { name: /Submit/ }).click();
    await expect(page.getByText(/tests passed/)).toBeVisible({ timeout: 10000 });
  });

  test('extract-ip-addresses: correct answer passes and awards 15 XP', async ({ page }) => {
    await registerUser(page);

    await page.goto(`${MODULE13_BASE}/extract-ip-addresses`);
    await expect(page.getByRole('heading', { name: 'Extract IP Addresses' })).toBeVisible();

    await typeInMonaco(
      page,
      'import re\n\nlog = "Connection from 10.0.0.5 to 192.168.1.100 on port 443"\n\nips = re.findall(r"\\d+\\.\\d+\\.\\d+\\.\\d+", log)\nfor ip in ips:\n    print(ip)'
    );

    await page.getByRole('button', { name: /Submit/ }).click();
    await expect(page.getByText(/Exercise Complete/)).toBeVisible({ timeout: 15000 });

    await page.waitForTimeout(1000);
    const xp = await getHeaderXP(page);
    expect(xp).toBe(15);
  });

  test('predict-the-match: correct choice awards 10 XP', async ({ page }) => {
    await registerUser(page);

    await page.goto(`${MODULE13_BASE}/predict-the-match`);
    await expect(page.getByRole('heading', { name: 'Predict the Match' })).toBeVisible();

    await page.getByRole('button', { name: '8080', exact: true }).click();
    await page.getByText('Check Answer').click();

    await expect(page.getByText('Correct! Great job!')).toBeVisible({ timeout: 5000 });

    await page.waitForTimeout(1000);
    const xp = await getHeaderXP(page);
    expect(xp).toBe(10);
  });

  test('predict-the-match: wrong choice shows error', async ({ page }) => {
    await registerUser(page);

    await page.goto(`${MODULE13_BASE}/predict-the-match`);

    await page.getByRole('button', { name: 'Error', exact: true }).click();
    await page.getByText('Check Answer').click();

    await expect(page.getByText('Not quite! Try again.')).toBeVisible({ timeout: 5000 });
  });

  test('parse-device-log: correct answer passes and awards 20 XP', async ({ page }) => {
    await registerUser(page);

    await page.goto(`${MODULE13_BASE}/parse-device-log`);
    await expect(page.getByRole('heading', { name: 'Parse Device Log' })).toBeVisible();

    await typeInMonaco(
      page,
      'import re\n\nlogs = """2024-01-15T10:30:00 WARNING Link down on Gi0/1\n2024-01-15T10:30:05 ERROR BGP peer 10.0.0.2 unreachable\n2024-01-15T10:30:10 INFO Interface Gi0/2 up"""\n\nfor line in logs.strip().split("\\n"):\n    match = re.search(r"\\S+\\s+(\\w+)\\s+(.*)", line)\n    if match:\n        severity = match.group(1)\n        message = match.group(2)\n        print(f"[{severity}] {message}")'
    );

    await page.getByRole('button', { name: /Submit/ }).click();
    await expect(page.getByText(/Exercise Complete/)).toBeVisible({ timeout: 15000 });

    await page.waitForTimeout(1000);
    const xp = await getHeaderXP(page);
    expect(xp).toBe(20);
  });
});
