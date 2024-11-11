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
    expect(page.locator("#code-output")).to_have_text("Hello, world!", timeout=20000)


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
        "Correct   ✔", timeout=20000
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
        "Does not match target output   ❌", timeout=20000
    )


def test_error_message_displayed(page: Page):
    """
    Test that an error message is displayed when there is an execution error.
    """
    textarea_locator = page.locator("#code-area")
    textarea_locator.fill("print('Hello world'")  # Missing closing parenthesis

    page.locator("#run-button").click()

    # Use expect to wait until the error message appears
    error_locator = page.locator("#code-output")
    expect(error_locator).to_contain_text("Error:", timeout=20000)
