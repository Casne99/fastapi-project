// playwright.config.ts
import { defineConfig } from '@playwright/test';

export default defineConfig({
  use: {
    baseURL: process.env.PLAYWRIGHT_BASE_URL || 'http://frontend:80',
    headless: true,
  },
  testDir: './tests',
});

