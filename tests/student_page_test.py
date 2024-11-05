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


def test_error_message_displayed(page: Page):
    """
    Test that an error message is displayed when there is an execution error.
    """
    # 1. Enter code that will cause an error (e.g., division by zero)
    textarea_locator = page.locator("#code-area")
    textarea_locator.fill("print(1 / 0)")  # This will raise a ZeroDivisionError

    # 2. Click the Run Button
    page.locator("#run-button").click()

    # 3. Wait for the output to be updated
    page.wait_for_timeout(3000)

    # 4. Get the output text
    error_output = page.locator("#code-output").text_content()
    print("Error output:", error_output)

    # 5. Assert that an error message is displayed
    assert error_output, "No output was generated."
    assert (
        "Error:" in error_output
    ), f"Expected 'Error:' in output, but got: {error_output}"
