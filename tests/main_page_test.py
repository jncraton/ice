"""
Tests for the teacher view of the application

These are the end-to-end UI test for index.html
"""

from playwright.sync_api import Page, expect
import pytest

from app.app import app


@pytest.fixture
def client():
    return app.test_client()


@pytest.fixture(scope="function", autouse=True)
def before_each(page: Page):
    """Load the page before each test"""
    page.goto("http://localhost:5000")


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
