// playwright.config.ts
import { defineConfig } from '@playwright/test';

export default defineConfig({
  reporter: [['html', { open: 'never' }], ['list']],
  use: {
    baseURL: process.env.PLAYWRIGHT_BASE_URL || 'http://frontend:80',
    headless: true,
    viewport: { width: 2560, height: 1440 },
    video: { mode: 'on', size: { width: 2560, height: 1440 } },
    screenshot: 'only-on-failure',
    trace: 'on-first-retry',
    launchOptions: {
      args: ['--disable-dev-shm-usage', '--disable-gpu', '--use-gl=swiftshader'],
    },
  },
  testDir: './tests',
});
