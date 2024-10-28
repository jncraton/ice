from playwright.sync_api import Page, expect
import os

current_working_directory = os.getcwd()
# file_name = "www/student.html"
# full_path = "file://" + os.path.join(current_working_directory, file_name)

full_path = "http://localhost:8000"


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


def test_python_runs(page: Page):
    # Test that basic python runs

    # 1. Go to page
    page.goto(full_path + "/student.html")

    # 2. Put code in code area
    textarea_locator = page.locator("#code-area")
    textarea_locator.fill('print("Hello, world!")')

    # 3. Click Run Button
    page.locator("#run-button").click()

    # 4. Assert desired output is
    expect(page.locator("#code-output")).to_have_text("Hello, world!")


def test_buttons_disable(page: Page):
    # Test that running a python program enables/disables the right buttons, and stopping it from running enables/disables the correct buttons.
    pass

def test_python_kills(page: Page):
    # Test that we can kill a python program
    pass
