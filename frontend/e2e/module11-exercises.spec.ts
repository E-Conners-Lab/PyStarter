import { test, expect } from '@playwright/test';
import { registerUser, getHeaderXP, typeInMonaco } from './helpers';

const MODULE11_BASE = '/module/handling-errors/lesson/practice-error-handling/exercise';

test.describe('Module 11 Exercise Validation', () => {
  test('catch-the-error: correct answer passes and awards 10 XP', async ({ page }) => {
    await registerUser(page);

    await page.goto(`${MODULE11_BASE}/catch-the-error`);
    await expect(page.getByRole('heading', { name: 'Catch the Error' })).toBeVisible();

    await typeInMonaco(
      page,
      'try:\n    number = int("abc")\nexcept ValueError:\n    print("Could not convert to integer")'
    );

    await page.getByRole('button', { name: /Submit/ }).click();
    await expect(page.getByText(/Exercise Complete/)).toBeVisible({ timeout: 15000 });

    await page.waitForTimeout(1000);
    const xp = await getHeaderXP(page);
    expect(xp).toBe(10);
  });

  test('catch-the-error: wrong answer shows failure', async ({ page }) => {
    await registerUser(page);

    await page.goto(`${MODULE11_BASE}/catch-the-error`);

    await typeInMonaco(page, 'print("wrong")');

    await page.getByRole('button', { name: /Submit/ }).click();
    await expect(page.getByText(/tests passed/)).toBeVisible({ timeout: 10000 });
  });

  test('safe-dictionary-lookup: correct answer passes and awards 15 XP', async ({ page }) => {
    await registerUser(page);

    await page.goto(`${MODULE11_BASE}/safe-dictionary-lookup`);
    await expect(page.getByRole('heading', { name: 'Safe Dictionary Lookup' })).toBeVisible();

    await typeInMonaco(
      page,
      'device = {"hostname": "R1", "ip": "10.0.0.1"}\n\ntry:\n    print(device["location"])\nexcept KeyError:\n    print("Key not found: location")'
    );

    await page.getByRole('button', { name: /Submit/ }).click();
    await expect(page.getByText(/Exercise Complete/)).toBeVisible({ timeout: 15000 });

    await page.waitForTimeout(1000);
    const xp = await getHeaderXP(page);
    expect(xp).toBe(15);
  });

  test('predict-the-exception: correct choice awards 10 XP', async ({ page }) => {
    await registerUser(page);

    await page.goto(`${MODULE11_BASE}/predict-the-exception`);
    await expect(page.getByRole('heading', { name: 'Predict the Exception' })).toBeVisible();

    await page.getByRole('button', { name: 'Failed Done', exact: true }).click();
    await page.getByText('Check Answer').click();

    await expect(page.getByText('Correct! Great job!')).toBeVisible({ timeout: 5000 });

    await page.waitForTimeout(1000);
    const xp = await getHeaderXP(page);
    expect(xp).toBe(10);
  });

  test('predict-the-exception: wrong choice shows error', async ({ page }) => {
    await registerUser(page);

    await page.goto(`${MODULE11_BASE}/predict-the-exception`);

    await page.getByRole('button', { name: 'Error', exact: true }).click();
    await page.getByText('Check Answer').click();

    await expect(page.getByText('Not quite! Try again.')).toBeVisible({ timeout: 5000 });
  });

  test('ip-validator: correct answer passes and awards 20 XP', async ({ page }) => {
    await registerUser(page);

    await page.goto(`${MODULE11_BASE}/ip-validator`);
    await expect(page.getByRole('heading', { name: 'IP Validator' })).toBeVisible();

    await typeInMonaco(
      page,
      'import ipaddress\n\nips = ["192.168.1.1", "999.999.999.999", "10.0.0.1", "not_an_ip"]\n\nfor ip in ips:\n    try:\n        ipaddress.ip_address(ip)\n        print(f"Valid: {ip}")\n    except ValueError:\n        print(f"Invalid: {ip}")'
    );

    await page.getByRole('button', { name: /Submit/ }).click();
    await expect(page.getByText(/Exercise Complete/)).toBeVisible({ timeout: 15000 });

    await page.waitForTimeout(1000);
    const xp = await getHeaderXP(page);
    expect(xp).toBe(20);
  });
});
