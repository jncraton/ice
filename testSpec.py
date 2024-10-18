from playwright.sync_api import Page, expect
import os

current_working_directory = os.getcwd()
file_name = "index.html"
full_path = "file://" + os.path.join(current_working_directory, file_name)

def test_title(page: Page):
    #  Step 1: Navigate to the index.html page
    page.goto(full_path)

    #  Step 2: Check the page title
    expect(page).to_have_title('Integrative Coding Experience')

def test_text(page: Page):
    #  Step 1: Navigate to the index.html page
    page.goto(full_path)
    
    #  Step 2: Verify that the new page contains specific text
    expectedText = 'Hello World!'
    expect(page.locator('body')).to_contain_text(expectedText)