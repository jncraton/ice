const { test, expect } = require('@playwright/test');

test('User can navigate and see expected text', async ({ page }) => {
    // Step 1: Navigate to the page
    await page.goto('https://jncraton.github.io/ice/');

    // Step 2: Check the page title
    await expect(page).toHaveTitle('I.C.E');

    // Step 3: Verify that the new page contains specific text
    const expectedText = 'Hello World!';
    await expect(page.locator('body')).toContainText(expectedText);
});