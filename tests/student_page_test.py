from playwright.sync_api import Page, expect
import os

current_working_directory = os.getcwd()
file_name = "www/student.html"
full_path = "file://" + os.path.join(current_working_directory, file_name)


def test_title(page: Page):
    #  Step 1: Navigate to the student.html page
    page.goto(full_path)

    #  Step 2: Check the page title
    expect(page).to_have_title("Integrative Coding Experience")


def test_student_input(page: Page):
    #  Step 1: Navigate to the student.html page
    page.goto(full_path)

    # Step 2: Test that text area is on page
    textarea_locator = page.locator("#output-text")
    assert textarea_locator.is_visible()
