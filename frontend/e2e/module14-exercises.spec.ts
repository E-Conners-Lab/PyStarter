import { test, expect } from '@playwright/test';
import { registerUser, getHeaderXP, typeInMonaco } from './helpers';

const MODULE14_BASE =
  '/module/building-a-network-toolkit/lesson/practice-network-toolkit/exercise';

test.describe('Module 14 Exercise Validation', () => {
  test('fix-the-parser: correct fix passes and awards 10 XP', async ({ page }) => {
    await registerUser(page);

    await page.goto(`${MODULE14_BASE}/fix-the-parser`);
    await expect(page.getByRole('heading', { name: 'Fix the Parser' })).toBeVisible();

    await typeInMonaco(
      page,
      'output = """Interface  Status  Speed\nGi0/0      up      1000\nGi0/1      down    100\nGi0/2      up      1000"""\n\nlines = output.strip().split("\\n")\nfor line in lines[1:]:\n    parts = line.split()\n    print(f"{parts[0]}: {parts[1]}")'
    );

    await page.getByRole('button', { name: /Submit/ }).click();
    await expect(page.getByText(/Exercise Complete/)).toBeVisible({ timeout: 15000 });

    await page.waitForTimeout(1000);
    const xp = await getHeaderXP(page);
    expect(xp).toBe(10);
  });

  test('fix-the-parser: submitting buggy code shows failure', async ({ page }) => {
    await registerUser(page);

    await page.goto(`${MODULE14_BASE}/fix-the-parser`);

    // Submit the original buggy code (uses parts[2] instead of parts[1])
    await typeInMonaco(
      page,
      'output = """Interface  Status  Speed\nGi0/0      up      1000\nGi0/1      down    100\nGi0/2      up      1000"""\n\nlines = output.strip().split("\\n")\nfor line in lines[1:]:\n    parts = line.split()\n    print(f"{parts[0]}: {parts[2]}")'
    );

    await page.getByRole('button', { name: /Submit/ }).click();
    await expect(page.getByText(/tests passed/)).toBeVisible({ timeout: 10000 });
  });

  test('subnet-scanner: correct answer passes and awards 15 XP', async ({ page }) => {
    await registerUser(page);

    await page.goto(`${MODULE14_BASE}/subnet-scanner`);
    await expect(page.getByRole('heading', { name: 'Subnet Scanner' })).toBeVisible();

    await typeInMonaco(
      page,
      `import ipaddress
import json

ips_json = '["10.0.0.5", "10.0.0.100", "192.168.1.1", "10.0.0.200", "172.16.0.1"]'
network = "10.0.0.0/24"

ips = json.loads(ips_json)
net = ipaddress.ip_network(network)

for ip_str in ips:
    ip = ipaddress.ip_address(ip_str)
    if ip in net:
        print(f"{ip_str}: Inside")
    else:
        print(f"{ip_str}: Outside")`
    );

    await page.getByRole('button', { name: /Submit/ }).click();
    await expect(page.getByText(/Exercise Complete/)).toBeVisible({ timeout: 15000 });

    await page.waitForTimeout(1000);
    const xp = await getHeaderXP(page);
    expect(xp).toBe(15);
  });

  test('predict-the-toolkit-output: correct choice awards 10 XP', async ({ page }) => {
    await registerUser(page);

    await page.goto(`${MODULE14_BASE}/predict-the-toolkit-output`);
    await expect(page.getByRole('heading', { name: 'Predict the Output' })).toBeVisible();

    await page.locator('button').filter({ hasText: 'True router' }).click();
    await page.getByText('Check Answer').click();

    await expect(page.getByText('Correct! Great job!')).toBeVisible({ timeout: 5000 });

    await page.waitForTimeout(1000);
    const xp = await getHeaderXP(page);
    expect(xp).toBe(10);
  });

  test('predict-the-toolkit-output: wrong choice shows error', async ({ page }) => {
    await registerUser(page);

    await page.goto(`${MODULE14_BASE}/predict-the-toolkit-output`);

    await page.locator('button').filter({ hasText: 'False router' }).click();
    await page.getByText('Check Answer').click();

    await expect(page.getByText('Not quite! Try again.')).toBeVisible({ timeout: 5000 });
  });

  test('device-audit-report: correct answer passes and awards 20 XP', async ({ page }) => {
    await registerUser(page);

    await page.goto(`${MODULE14_BASE}/device-audit-report`);
    await expect(page.getByRole('heading', { name: 'Device Audit Report' })).toBeVisible();

    await typeInMonaco(
      page,
      `import json

devices_json = '[{"hostname": "SW1", "interfaces": ["Gi0/0", "Gi0/1"]}, {"hostname": "SW2", "interfaces": []}, {"hostname": "", "interfaces": ["Gi0/0"]}]'

devices = json.loads(devices_json)

for device in devices:
    name = device["hostname"] or "SW3"
    if not device["interfaces"]:
        print(f"{name}: ISSUE - No interfaces")
    elif not device["hostname"]:
        print(f"SW3: ISSUE - Missing hostname")
    else:
        print(f"{name}: OK")`
    );

    await page.getByRole('button', { name: /Submit/ }).click();
    await expect(page.getByText(/Exercise Complete/)).toBeVisible({ timeout: 15000 });

    await page.waitForTimeout(1000);
    const xp = await getHeaderXP(page);
    expect(xp).toBe(20);
  });
});
