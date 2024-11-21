"""
Tests for the ability to run code in both the student and teacher view of the application
"""

from playwright.sync_api import Page, expect
import pytest

pytestmark = pytest.mark.parametrize(
    "url", [("http://localhost:8000"), ("http://localhost:8000/student.html")]
)


def test_python_runs(page: Page, url):
    """
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


def test_buttons_disable(page: Page, url):
    """
    Test that running a python program enables/disables the right buttons,
    and stopping it from running enables/disables the correct buttons.
    Serves the purpose of checking if looping error in FireFox does not occur.
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

    # 4. Refresh the page. This should kill the looping Python script.

    page.evaluate("window.location.reload()")

    # 5. Expect run button to be enabled, end button to be disabled
    expect(page.locator("#run-button")).to_be_enabled()
    expect(page.locator("#end-button")).to_be_disabled()


def test_python_code_execution_with_input(page: Page, url):
    """
    Test that Python code correctly handles user input via the worker.
    """

    page.goto(url)

    # 1. Put code in the code area
    codearea_locator = page.locator("#code-area")
    python_code = """
    name = await input("What is your name?")
    print("Hello", name)
    """
    codearea_locator.fill(python_code)

    # 2. Click Run Button
    page.locator("#run-button").click()

    # 3. Simulate user input with a mock 'hi' response
    page.on(
        "dialog", lambda dialog: dialog.accept("world")
    )  # Simulate the prompt with 'world'

    # 4. Assert that the output is correct
    expect(page.locator("#code-output")).to_have_text("Hello world", timeout=20000)
