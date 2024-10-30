"""
Tests for the teacher view of the application

These are the end-to-end UI test for index.html
"""

from playwright.sync_api import Page, expect
import pytest


@pytest.fixture(scope="function", autouse=True)
def before_each(page: Page):
    """Load the page before each test"""
    page.goto("http://localhost:8000")


def test_title(page: Page):
    """Confirm the page has an appropriate title"""

    expect(page).to_have_title("Integrative Coding Experience")


def test_desired_outcome(page: Page):
    """Confirm that output text is visible"""

    textbox_locator = page.locator("#output-text")
    assert textbox_locator.is_visible()


def test_student_link_navigates(page: Page):
    """Confirm that student link copies correctly"""

    # Step 1: Input text in input field
    page.locator("#code-area").fill("test input")

    # Step 2: Input text in output field
    page.locator("#output-text").fill("test output")

    # Step 3: Pushing the (share) Button
    page.context.grant_permissions(["clipboard-write"])
    page.locator("#share").click()

    # Step 4: Checking for Alert
    page.locator("#copy-link").click()

    expect(page.locator("#alert")).to_be_visible()
    expect(page.locator("#alert")).to_have_text("Link copied to clipboard")


def test_embed_code_generation(page: Page):
    """Confirm that the embed link returns the expected URL"""

    # Step 1: Fill the necessary fields
    page.fill("#code-area", "Sample code")  # Fill the code area with sample code
    page.fill(
        "#output-text", "Sample output"
    )  # Fill the output text area with sample output

    # Step 2: Click the Share button
    page.click("#share")  # Interacts with the button by its ID

    # Step 3: Wait for the embed code to appear in the textarea
    embed_code_display = page.locator(
        "#embed-code"
    )  # Ensure this matches your HTML structure
    expect(
        embed_code_display
    ).to_be_visible()  # Ensure the embed code textarea is visible

    # Step 4: Verify that the embed code is correct
    # Generate the expected URL based on the inputs
    expected_url = page.evaluate(
        """location.origin + location.pathname + "student.html#" + 
        btoa(JSON.stringify(["Sample code", "Sample output"]))"""
    )
    # Construct the expected embed code
    expected_embed_code = (
        f'<iframe src="{expected_url}" width="100%" '
        f'height="800" frameborder="0" allowfullscreen></iframe>'
    )

    # Assert that the displayed embed code matches the expected embed code
    expect(embed_code_display).to_have_value(expected_embed_code)

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
    expect(page.locator("#code-output")).to_have_text("Hello, world!")


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
    
