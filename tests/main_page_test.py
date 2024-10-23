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

def test_desired_outcome(page: Page):
    #  Step 1: Navigate to the index.html page
    page.goto(full_path)
    
    # Step 2: Check the page for a spot for desired output
    textbox_locator = page.locator("#output-text")
    assert textbox_locator.is_visible()
