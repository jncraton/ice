from playwright.sync_api import Page, expect

def test_title(page: Page):
    #  Step 1: Navigate to the page
    page.goto("https://jncraton.github.io/ice/")

    #  Step 2: Check the page title
    expect(page).to_have_title('I.C.E')

def test_text(page: Page):
    #  Step 1: Navigate to the page
    page.goto("https://jncraton.github.io/ice/")
    
    #  Step 2: Verify that the new page contains specific text
    expectedText = 'Hello World!'
    expect(page.locator('body')).toContainText(expectedText)