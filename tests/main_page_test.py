from playwright.sync_api import Page, expect
import os

current_working_directory = os.getcwd()
full_path = "http://localhost:8000"

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

def test_student_link_navigates(page: Page):

    # This functionality can only truly be tested on a live webpage
    # GitHub pages presents the best environment to do this in.
    # Step 1: Navigate to index.html on github page
    page.goto(full_path)

    # Step 2: Input text in input field
    page.locator("#code-area").fill("test input")

    # Step 3: Input text in output field
    page.locator("#output-text").fill("test output")

    # Step 4: Pushing the (share) Button
    page.context.grant_permissions(["clipboard-write"])
    page.locator("#share").click()

    # Step 5: Checking for Alert 
    page.locator("#link-display").click()

    expect(page.locator("#alert")).to_be_visible()
    expect(page.locator("#alert")).to_have_text("Link copied to clipboard")