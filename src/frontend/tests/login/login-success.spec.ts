import { test, expect } from '@playwright/test';
import { execSync } from 'child_process';
import path from 'path';

const scriptPath = path.resolve(__dirname, 'insert_test_user.py');

test('login effettuato con credenziali corrette', async ({ page }) => {
  execSync(`python3 "${scriptPath}" utentevalido passwordcorretta`, { stdio: 'inherit' });
  await page.goto('/');
  await page.fill('#username', 'utentevalido');
  await page.fill('#password', 'passwordcorretta');
  await page.click('button[type="submit"]');
  await expect(page.locator('#message')).toHaveText('Login effettuato!');
});
