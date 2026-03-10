import { test, expect } from '@playwright/test';

test('login fallito con credenziali errate', async ({ page }) => {
  await page.goto('/');
  await page.fill('#username', 'utenteinesistente');
  await page.fill('#password', 'passwordsbagliata');
  await page.click('button[type="submit"]');
  await expect(page.locator('#message')).toHaveText('Credenziali non valide');
});
