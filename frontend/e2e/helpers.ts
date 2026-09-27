import { type Page, expect } from '@playwright/test';

/**
 * Register a fresh test user and return credentials.
 */
export async function registerUser(page: Page) {
  const ts = Date.now();
  const username = `testuser_${ts}`;
  const email = `test_${ts}@example.com`;
  const password = 'TestPass123!';

  await page.goto('/register');
  await page.getByLabel('Username').fill(username);
  await page.getByLabel('Password').fill(password);
  await page.getByRole('button', { name: 'Create Free Account' }).click();

  // Wait for redirect to dashboard
  await page.waitForURL('/dashboard', { timeout: 10000 });

  return { username, email, password };
}

/**
 * Log in with existing credentials.
 */
export async function loginUser(page: Page, username: string, password: string) {
  await page.goto('/login');
  await page.getByLabel('Username').fill(username);
  await page.getByLabel('Password').fill(password);
  await page.getByRole('button', { name: 'Log In' }).click();
  await page.waitForURL('/dashboard', { timeout: 10000 });
}

/**
 * Get the XP value displayed in the header.
 */
export async function getHeaderXP(page: Page): Promise<number> {
  const xpEl = page.locator('header').locator('text=/\\d+ XP/').first();
  const xpText = await xpEl.textContent();
  const match = xpText?.match(/(\d+)\s*XP/);
  return match ? parseInt(match[1], 10) : 0;
}

/**
 * Set code in a Monaco editor, replacing all existing content.
 * Uses Monaco's JS API directly to avoid autocomplete/auto-closing interference.
 */
export async function typeInMonaco(page: Page, code: string) {
  await page.waitForSelector('.monaco-editor', { timeout: 10000 });

  // Use Monaco's API to set the value directly — avoids auto-close bracket/quote issues
  await page.evaluate((newCode) => {
    const editor = (window as any).monaco?.editor?.getEditors?.()?.[0];
    if (editor) {
      editor.setValue(newCode);
    } else {
      // Fallback: find the editor model via the DOM data attribute
      const editorElement = document.querySelector('.monaco-editor') as any;
      const model = editorElement?.__view?.model ?? null;
      if (model) {
        model.setValue(newCode);
      }
    }
  }, code);

  // Small delay to let React state sync with the editor value
  await page.waitForTimeout(200);
}
