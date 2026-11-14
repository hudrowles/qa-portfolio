// PowderLine Board Sizer - TypeScript version of my Python Playwright tests.
// Same app, same spec (../docs/SPEC.md), just TypeScript instead of Python.
import { test, expect } from '@playwright/test';
import path from 'path';
import { pathToFileURL } from 'url';

// Where the app lives (same local HTML file the Python tests use)
const APP = pathToFileURL(path.resolve(__dirname, '../../apps/snowboard-sizer.html')).href;

// Spec #1, #4: a 178 cm, 75 kg rider -> 178 x 0.88 = 156.6 -> 157 cm
test('normal rider gets correct length', async ({ page }) => {
  await page.goto(APP);                                   // 1. open the app
  await page.fill('#h', '178');                           // 2. type 178 into the height box
  await page.fill('#w', '75');                            // 3. type 75 into the weight box
  await page.click('#go');                                // 4. click "Find my board"
  await expect(page.locator('#out')).toContainText('157 cm'); // 5. result should say 157 cm
});

// Spec #2: a light rider (under 55 kg) gets 3 cm shorter -> 157 - 3 = 154 cm
test('light rider gets shorter board', async ({ page }) => {
  await page.goto(APP);
  await page.fill('#h', '178');
  await page.fill('#w', '50');                                 // under 55 kg
  await page.click('#go');
  await expect(page.locator('#out')).toContainText('154 cm');  // 157 - 3
});
