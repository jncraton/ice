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
