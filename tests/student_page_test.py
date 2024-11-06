"""
Tests for the student view of the application

These are the end-to-end UI tests for student.html
"""

from playwright.sync_api import Page, expect
import pytest


@pytest.fixture(scope="function", autouse=True)
def before_each(page: Page):
    """Load the page before each test"""
    page.goto("http://localhost:8000/student.html")


def test_title(page: Page):
    """Confirm the page has an appropriate title"""

    expect(page).to_have_title("Integrative Coding Experience")


def test_student_input(page: Page):
    """Confirm that output text is visible"""

    textarea_locator = page.locator("#target-text")
    assert textarea_locator.is_visible()


def test_python_runs(page: Page):
    """
    Test that basic python code can execute
    """

    # 1. Put code in code area
    textarea_locator = page.locator("#code-area")
    textarea_locator.fill('print("Hello, world!")')

    # 2. Click Run Button
    page.locator("#run-button").click()

    # 3. Assert desired output is
    expect(page.locator("#code-output")).to_have_text("Hello, world!", timeout=10000)


def test_buttons_disable(page: Page):
    """
    Test that running a python program enables/disables the right buttons,
    and stopping it from running enables/disables the correct buttons.
    """

    # 1. Put code in code area
    textarea_locator = page.locator("#code-area")
    textarea_locator.fill("while True:\n\tprint(1)")

    # 2. Click Run Button
    page.locator("#run-button").click()

    # 3. Expect run button to be disabled, end button to be enabled
    expect(page.locator("#run-button")).to_be_disabled()
    expect(page.locator("#end-button")).to_be_enabled()

    # 4. Click the End button
    page.locator("#end-button").click()

    # 5. Expect the run button to be enabled, end button to be disabled.
    expect(page.locator("#run-button")).to_be_enabled()
    expect(page.locator("#end-button")).to_be_disabled()


def test_check_output_correct(page: Page):
    """
    Test that the check output functionality works when the result of running the code 
    matches the target output.
    """
     
    # 1. Put code in code area
    codearea_locator = page.locator("#code-area")
    codearea_locator.fill("print('Hello World!')")
    
    # 2. Put code in Desired output
    targettext_locator = page.locator("#target-text")
    targettext_locator.evaluate("element => element.removeAttribute('disabled')")
    targettext_locator.fill("Hello World!")

    # 3. Click Run Button
    page.locator("#run-button").click()

    # 4. Check Output
    expect(page.locator("#check-code-result")).to_contain_text(
        "Correct   ✔", timeout=10000
    )


def test_check_output_incorrect(page: Page):
    """
    Test that the check output functionality works when the result of running the code 
    does not match the target output.
    """
    
    # 1. Put code in code area
    codearea_locator = page.locator("#code-area")
    codearea_locator.fill("print('Hello Word')")
    
    # 2. Put code in Desired output
    targettext_locator = page.locator("#target-text")
    targettext_locator.evaluate("element => element.removeAttribute('disabled')")
    targettext_locator.fill("Hello World!")

    # 3. Click Run Button
    page.locator("#run-button").click()

    # 4. Check Output
    expect(page.locator("#check-code-result")).to_contain_text(
        "Does not match target output   ❌"
    )


def test_buttons_disable_firefox_bug(page: Page):
    """
    Test that refreshing the page while the program is running leaves the
    buttons in appropriate states
    """

    # 1. Put code in code area
    textarea_locator = page.locator("#code-area")
    textarea_locator.fill("while True:\n\tprint(1)")

    # 2. Click Run Button
    page.locator("#run-button").click()

    # 3. Expect run button to be disabled, end button to be enabled
    expect(page.locator("#run-button")).to_be_disabled()
    expect(page.locator("#end-button")).to_be_enabled()

    # 4. Refresh the page. This should kill the looping Python script.

    page.evaluate("window.location.reload()")

    # 5. Expect run button to be enabled, end button to be disabled
    expect(page.locator("#run-button")).to_be_enabled()
    expect(page.locator("#end-button")).to_be_disabled()
