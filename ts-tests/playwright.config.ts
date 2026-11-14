import { defineConfig } from '@playwright/test';

// Runs every *.spec.ts file in ./tests with Chromium.
export default defineConfig({
  testDir: './tests',
  use: { browserName: 'chromium' },
});
