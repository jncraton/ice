"""
Tests for the ability to run code in both the student and teacher view of the application
"""

from playwright.sync_api import Page, expect

import pytest

pytestmark = pytest.mark.parametrize("url",[("http://localhost:8000"),("http://localhost:8000/student.html")])

def test_python_runs_teacher(page: Page, url):
    """
    Go to teacher page
    Test that basic python code can execute
    """

    page.goto(url)

    # 1. Put code in code area
    textarea_locator = page.locator("#code-area")
    textarea_locator.fill('print("Hello, world!")')

    # 2. Click Run Button
    page.locator("#run-button").click()

    # 3. Assert desired output is
    expect(page.locator("#code-output")).to_have_text("Hello, world!", timeout=15000)


def test_buttons_disable_teacher(page: Page, url):
    """
    Go to teacher page
    Test that running a python program enables/disables the right buttons,
    and stopping it from running enables/disables the correct buttons.
    """

    page.goto(url)

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
